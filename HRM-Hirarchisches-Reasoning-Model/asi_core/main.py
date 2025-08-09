import sys
from pathlib import Path

# Add the project root to the Python path to allow importing from asi_core
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from asi_core.role_manager import RoleManager
from asi_core.feedback_store import FeedbackStore
from asi_core.user_interface import UserInterface

class AsiApplication:
    """The main application class for the ASI core system."""

    def __init__(self):
        """Initializes all core components of the ASI system."""
        base_path = Path(__file__).parent
        roles_path = base_path / 'data' / 'roles.json'
        feedback_path = base_path / 'data' / 'feedback_archive.json'

        try:
            print("Initializing ASI Core System...")
            self.role_manager = RoleManager(roles_path)
            self.feedback_store = FeedbackStore(feedback_path)
            print("RoleManager and FeedbackStore initialized successfully.")
        except (FileNotFoundError, ValueError) as e:
            print(f"[ERROR] Failed to initialize a core component: {e}")
            sys.exit(1)

    def run_demonstration(self):
        """Runs a simple demonstration of the integrated components."""
        print("\n--- Running ASI Core Demonstration ---")

        # 1. Demonstrate RoleManager
        print("\n1. Listing all available agent roles:")
        all_roles = self.role_manager.get_all_roles()
        if all_roles:
            for role in all_roles:
                print(f"  - Role: {role['name']}")
        else:
            print("  No roles found.")

        # 2. Demonstrate FeedbackStore
        print("\n2. Adding a new feedback entry:")
        user_id = "demo_user_001"
        feedback_text = "The role demonstration was very clear."
        entry = self.feedback_store.add_feedback(
            user_id=user_id,
            feedback_text=feedback_text,
            context={'module': 'main_demonstration'}
        )
        print(f"  Feedback added with ID: {entry['feedback_id']}")

        # 3. Retrieve the feedback to confirm
        print(f"\n3. Retrieving feedback for user '{user_id}':")
        user_feedback = self.feedback_store.get_feedback_by_user(user_id)
        if user_feedback:
            for fb in user_feedback:
                print(f"  - [{fb['timestamp_utc']}] {fb['feedback_text']}")
        else:
            print("  No feedback found for this user.")
        
        print("\n--- Demonstration Complete ---")


def main():
    """Main entry point for the application."""
    app = AsiApplication()
    # app.run_demonstration() # We keep the demo logic but run the interactive UI by default

    # Initialize and start the interactive user interface
    ui = UserInterface(role_manager=app.role_manager, feedback_store=app.feedback_store)
    ui.start_interaction()

if __name__ == '__main__':
    main()