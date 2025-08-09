import json
import hashlib
from datetime import datetime
from pathlib import Path

class FeedbackStore:
    """Handles the storage and retrieval of user feedback in a GDPR-compliant manner."""

    def __init__(self, storage_path: str):
        """
        Initializes the FeedbackStore.

        Args:
            storage_path (str): The path to the JSON file used for storage.
        """
        self.storage_path = Path(storage_path)
        self._ensure_storage_file_exists()

    def _ensure_storage_file_exists(self):
        """Ensures the storage file and its parent directories exist."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _pseudonymize_user_id(self, user_id: str) -> str:
        """Creates a non-reversible pseudonym for the user ID."""
        return hashlib.sha256(user_id.encode('utf-8')).hexdigest()

    def _load_feedback(self) -> list:
        """Loads the feedback data from the JSON file."""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_feedback(self, data: list):
        """Saves the feedback data to the JSON file."""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_feedback(self, user_id: str, feedback_text: str, context: dict = None, metadata: dict = None) -> dict:
        """
        Adds a new feedback entry.

        Args:
            user_id (str): The original identifier for the user (will be pseudonymized).
            feedback_text (str): The text of the feedback.
            context (dict, optional): The context in which the feedback was given. Defaults to None.
            metadata (dict, optional): Additional metadata. Defaults to None.

        Returns:
            dict: The feedback entry that was added.
        """
        all_feedback = self._load_feedback()

        new_entry = {
            'feedback_id': len(all_feedback) + 1,
            'user_pseudonym': self._pseudonymize_user_id(user_id),
            'timestamp_utc': datetime.utcnow().isoformat(),
            'feedback_text': feedback_text,
            'context': context or {},
            'metadata': metadata or {}
        }

        all_feedback.append(new_entry)
        self._save_feedback(all_feedback)
        
        return new_entry

    def get_feedback_by_user(self, user_id: str) -> list:
        """
        Retrieves all feedback entries for a given user.

        Args:
            user_id (str): The original identifier for the user.

        Returns:
            list: A list of feedback entries for the user.
        """
        user_pseudonym = self._pseudonymize_user_id(user_id)
        all_feedback = self._load_feedback()
        return [entry for entry in all_feedback if entry['user_pseudonym'] == user_pseudonym]

    def get_all_feedback(self) -> list:
        """Retrieves all feedback entries."""
        return self._load_feedback()

# Example Usage (for testing purposes)
if __name__ == '__main__':
    # This part will only run when the script is executed directly
    storage_file = 'data/feedback_archive.json'
    feedback_store = FeedbackStore(storage_path=storage_file)

    print(f"Using storage file: {Path(storage_file).resolve()}")

    # Add some feedback
    user1_feedback = feedback_store.add_feedback(
        user_id='user_alex_123',
        feedback_text='This is a great feature, but it could be faster.',
        context={'module': 'hrm_chat', 'version': '1.2'},
        metadata={'sentiment': 'positive', 'category': 'performance'}
    )
    print(f"Added feedback: {user1_feedback}")

    user2_feedback = feedback_store.add_feedback(
        user_id='user_beta_456',
        feedback_text='I found a bug in the file loading.',
        context={'module': 'file_loader'},
        metadata={'sentiment': 'negative', 'category': 'bug'}
    )
    print(f"Added feedback: {user2_feedback}")

    # Retrieve feedback
    print("\n--- All Feedback ---")
    all_entries = feedback_store.get_all_feedback()
    print(json.dumps(all_entries, indent=2))

    print("\n--- Feedback for user_alex_123 ---")
    alex_entries = feedback_store.get_feedback_by_user('user_alex_123')
    print(json.dumps(alex_entries, indent=2))