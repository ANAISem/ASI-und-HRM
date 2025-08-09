import unittest
import json
import os
from pathlib import Path
import sys

# Add the project root to the Python path to allow importing from asi_core
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from asi_core.feedback_store import FeedbackStore

class TestFeedbackStore(unittest.TestCase):
    """Unit tests for the FeedbackStore class."""

    def setUp(self):
        """Set up a temporary storage file for each test."""
        self.test_storage_path = 'test_feedback_archive.json'
        # Ensure the file is clean before each test
        if os.path.exists(self.test_storage_path):
            os.remove(self.test_storage_path)
        self.feedback_store = FeedbackStore(storage_path=self.test_storage_path)

    def tearDown(self):
        """Remove the temporary storage file after each test."""
        if os.path.exists(self.test_storage_path):
            os.remove(self.test_storage_path)

    def test_initialization_creates_file(self):
        """Test if initializing the store creates the storage file."""
        self.assertTrue(os.path.exists(self.test_storage_path))
        with open(self.test_storage_path, 'r') as f:
            content = json.load(f)
        self.assertEqual(content, [])

    def test_add_feedback(self):
        """Test adding a single feedback entry."""
        entry = self.feedback_store.add_feedback(
            user_id='test_user_1',
            feedback_text='It works!',
            context={'page': 'home'},
            metadata={'rating': 5}
        )

        self.assertEqual(entry['feedback_text'], 'It works!')
        self.assertIn('user_pseudonym', entry)
        self.assertNotEqual(entry['user_pseudonym'], 'test_user_1')

        all_feedback = self.feedback_store.get_all_feedback()
        self.assertEqual(len(all_feedback), 1)
        self.assertEqual(all_feedback[0]['feedback_text'], 'It works!')

    def test_pseudonymization_is_consistent(self):
        """Test that the same user_id always results in the same pseudonym."""
        pseudonym1 = self.feedback_store._pseudonymize_user_id('consistent_user')
        pseudonym2 = self.feedback_store._pseudonymize_user_id('consistent_user')
        self.assertEqual(pseudonym1, pseudonym2)

    def test_pseudonymization_is_different_for_different_users(self):
        """Test that different user_ids result in different pseudonyms."""
        pseudonym1 = self.feedback_store._pseudonymize_user_id('user_A')
        pseudonym2 = self.feedback_store._pseudonymize_user_id('user_B')
        self.assertNotEqual(pseudonym1, pseudonym2)

    def test_get_feedback_by_user(self):
        """Test retrieving feedback for a specific user."""
        self.feedback_store.add_feedback('user_A', 'Feedback from A')
        self.feedback_store.add_feedback('user_B', 'Feedback from B')
        self.feedback_store.add_feedback('user_A', 'More feedback from A')

        feedback_a = self.feedback_store.get_feedback_by_user('user_A')
        feedback_b = self.feedback_store.get_feedback_by_user('user_B')
        feedback_c = self.feedback_store.get_feedback_by_user('user_C')

        self.assertEqual(len(feedback_a), 2)
        self.assertEqual(len(feedback_b), 1)
        self.assertEqual(len(feedback_c), 0)
        self.assertEqual(feedback_a[0]['feedback_text'], 'Feedback from A')
        self.assertEqual(feedback_b[0]['feedback_text'], 'Feedback from B')

    def test_data_structure_of_entry(self):
        """Test the structure and keys of a feedback entry."""
        entry = self.feedback_store.add_feedback('test_user', 'Structure test')
        expected_keys = ['feedback_id', 'user_pseudonym', 'timestamp_utc', 'feedback_text', 'context', 'metadata']
        self.assertCountEqual(entry.keys(), expected_keys)
        self.assertIsInstance(entry['feedback_id'], int)
        self.assertIsInstance(entry['user_pseudonym'], str)
        self.assertIsInstance(entry['timestamp_utc'], str)
        self.assertIsInstance(entry['context'], dict)
        self.assertIsInstance(entry['metadata'], dict)

if __name__ == '__main__':
    unittest.main()