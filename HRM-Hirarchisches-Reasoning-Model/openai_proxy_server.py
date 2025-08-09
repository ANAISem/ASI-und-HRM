#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI-Compatible Proxy Server for HRM

This server acts as a bridge, exposing the local HRM model
through an OpenAI-compatible API endpoint. This allows Trae
to connect to it as if it were a standard OpenAI-compatible provider.
"""

import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import asyncio

# Import the existing HRM server logic
from mcp_hrm_server import HRMMCPServer

# --- Pydantic Models for OpenAI Compatibility ---

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{''.join(str(ord(c)) for c in 'local-hrm')}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(asyncio.get_event_loop().time()))
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage

# --- FastAPI Application ---

app = FastAPI(
    title="HRM OpenAI-Compatible Proxy",
    description="Exposes the local HRM model via an OpenAI-compatible API.",
    version="1.0.0",
)

# Add CORS middleware to allow requests from the local HTML file
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, including 'null' for local files
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Instantiate the local HRM server
hrm_model = HRMMCPServer()

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    """Handles chat completion requests, mimicking the OpenAI API."""
    # Validate the model name
    if request.model != "hrm-local-model":
        raise HTTPException(
            status_code=404,
            detail=f"Model '{request.model}' not found. Please use 'hrm-local-model'."
        )

    if request.stream:
        raise HTTPException(
            status_code=400,
            detail="Streaming is not supported by this local proxy."
        )

    # Extract the last user message as the prompt
    last_user_message = next((msg.content for msg in reversed(request.messages) if msg.role == 'user'), None)
    if not last_user_message:
        raise HTTPException(
            status_code=400,
            detail="No user message found in the request."
        )

    # Get the completion from the local HRM model
    try:
        hrm_result = await hrm_model.handle_completion(last_user_message)
        completion_text = hrm_result.get("completion", "")
        usage_info = hrm_result.get("usage", {"prompt_tokens": 0, "completion_tokens": 0})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing with HRM model: {str(e)}")

    # Format the response to be OpenAI-compatible
    response_message = ChatMessage(role="assistant", content=completion_text)
    choice = ChatCompletionChoice(index=0, message=response_message, finish_reason="stop")
    usage = Usage(
        prompt_tokens=usage_info.get("prompt_tokens", 0),
        completion_tokens=usage_info.get("completion_tokens", 0),
        total_tokens=usage_info.get("prompt_tokens", 0) + usage_info.get("completion_tokens", 0)
    )

    return ChatCompletionResponse(
        model=request.model,
        choices=[choice],
        usage=usage
    )

@app.get("/v1/models")
async def list_models():
    """Provides a list of available models, mimicking the OpenAI API."""
    return {
        "object": "list",
        "data": [
            {
                "id": "hrm-local-model",
                "object": "model",
                "created": int(asyncio.get_event_loop().time()),
                "owned_by": "user"
            }
        ]
    }

@app.get("/files/list")
async def list_project_files():
    """Lists all non-hidden files in the project directory, ignoring venv."""
    files = []
    project_root = os.getcwd()
    for root, dirs, filenames in os.walk(project_root, topdown=True):
        # Exclude hidden directories and venv
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
        
        # Exclude hidden files
        for filename in [f for f in filenames if not f.startswith('.')]:
            # Get the relative path from the project root
            relative_path = os.path.relpath(os.path.join(root, filename), project_root)
            files.append(relative_path)
            
    return {"files": sorted(files)}

@app.get("/files/read")
async def read_project_file(path: str):
    """Reads the content of a specific file in the project."""
    # Security check to prevent accessing files outside the project directory
    if not os.path.abspath(path).startswith(os.getcwd()):
        raise HTTPException(status_code=403, detail="Access denied.")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"path": path, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting HRM OpenAI-Compatible Proxy Server...")
    print("✅ Server is running. Configure Trae to connect to http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)