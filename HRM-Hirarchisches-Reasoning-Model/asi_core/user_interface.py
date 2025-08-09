import sys
from pathlib import Path

# Add the project root to the Python path to allow importing from asi_core
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asi_core.role_manager import RoleManager
from asi_core.feedback_store import FeedbackStore

class UserInterface:
    """Handles the interactive user session, including input and output."""

    def __init__(self, role_manager: RoleManager, feedback_store: FeedbackStore):
        """
        Initializes the UserInterface with necessary components.

        Args:
            role_manager (RoleManager): An instance of the RoleManager.
            feedback_store (FeedbackStore): An instance of the FeedbackStore.
        """
        self.role_manager = role_manager
        self.feedback_store = feedback_store
        self.active_role = None
        self.user_id = "interactive_user_001" # Static for now

    def _select_role(self, user_input: str) -> dict:
        """
        Selects the most appropriate role based on user input.
        This is a placeholder for a more sophisticated selection logic.
        """
        # Simple keyword-based routing for demonstration
        all_roles = self.role_manager.get_all_roles()
        for role in all_roles:
            if role['name'].lower() in user_input.lower():
                return role
        
        # Default to a general-purpose role if no keyword matches
        return self.role_manager.get_role_by_name('AURA') or all_roles[0]

    def start_interaction(self):
        """Starts the main interactive loop for the user."""
        print("\n--- ASI Core Interactive Session ---\n")
        print("Welcome to the ASI Core. I am ready to assist you.")
        print("You can suggest a role by mentioning its name (e.g., 'Prometheus, give me an idea').")
        print("Type 'exit' to end the session or 'feedback' to leave feedback.")

        while True:
            if self.active_role:
                prompt = f"[{self.active_role['name']}] > "
            else:
                prompt = "> "

            user_input = input(prompt)

            if user_input.lower() == 'exit':
                print("Ending session. Goodbye!")
                break
            
            if user_input.lower() == 'feedback':
                self.handle_feedback()
                continue

            # 1. Select a role for this interaction
            self.active_role = self._select_role(user_input)

            # 2. Generate a response (placeholder)
            response = f"As {self.active_role['name']}, I acknowledge your input: '{user_input}'. My capabilities include: {', '.join(self.active_role['capabilities'])}."
            print(f"\n[ASI Response]: {response}\n")

    def handle_feedback(self):
        """Handles the process of collecting feedback from the user."""
        print("\nEntering feedback mode.")
        feedback_text = input("Please provide your feedback: ")
        if feedback_text:
            self.feedback_store.add_feedback(
                user_id=self.user_id,
                feedback_text=feedback_text,
                context={'active_role': self.active_role['name'] if self.active_role else 'None'}
            )
            print("Thank you for your feedback!\n")
        else:
            print("Feedback cancelled.\n")