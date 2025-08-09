import unittest
import json
import os
from pathlib import Path
import sys

# Add the project root to the Python path to allow importing from asi_core
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from asi_core.role_manager import RoleManager

class TestRoleManager(unittest.TestCase):
    """Unit tests for the RoleManager class."""

    def setUp(self):
        """Set up temporary role configuration files for tests."""
        self.valid_roles_path = Path('test_valid_roles.json')
        self.invalid_roles_path = Path('test_invalid_roles.json')
        self.malformed_roles_path = Path('test_malformed_roles.json')

        # Create a valid roles file
        valid_data = {
            "roles": [
                {"name": "TestRole1", "description": "Desc1", "capabilities": ["cap1"]},
                {"name": "TestRole2", "description": "Desc2", "capabilities": ["cap2"]}
            ]
        }
        with open(self.valid_roles_path, 'w') as f:
            json.dump(valid_data, f)

        # Create an invalid roles file (missing 'description')
        invalid_data = {
            "roles": [
                {"name": "TestRole1", "capabilities": ["cap1"]}
            ]
        }
        with open(self.invalid_roles_path, 'w') as f:
            json.dump(invalid_data, f)
            
        # Create a malformed roles file (missing 'roles' key)
        malformed_data = {"other_key": []}
        with open(self.malformed_roles_path, 'w') as f:
            json.dump(malformed_data, f)

    def tearDown(self):
        """Remove temporary files after tests."""
        for path in [self.valid_roles_path, self.invalid_roles_path, self.malformed_roles_path]:
            if os.path.exists(path):
                os.remove(path)

    def test_successful_loading(self):
        """Test loading roles from a valid configuration file."""
        rm = RoleManager(self.valid_roles_path)
        self.assertEqual(len(rm.get_all_roles()), 2)

    def test_get_all_roles(self):
        """Test retrieving all roles."""
        rm = RoleManager(self.valid_roles_path)
        roles = rm.get_all_roles()
        self.assertIsInstance(roles, list)
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0]['name'], 'TestRole1')

    def test_get_role_by_name(self):
        """Test retrieving a specific role by name."""
        rm = RoleManager(self.valid_roles_path)
        role = rm.get_role_by_name('TestRole2')
        self.assertIsNotNone(role)
        self.assertEqual(role['description'], 'Desc2')

    def test_get_non_existent_role(self):
        """Test retrieving a role that does not exist."""
        rm = RoleManager(self.valid_roles_path)
        role = rm.get_role_by_name('NonExistentRole')
        self.assertIsNone(role)

    def test_file_not_found_error(self):
        """Test that FileNotFoundError is raised for a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            RoleManager(Path('non_existent_file.json'))

    def test_invalid_role_definition_error(self):
        """Test that ValueError is raised for an invalid role definition."""
        with self.assertRaises(ValueError):
            RoleManager(self.invalid_roles_path)
            
    def test_malformed_json_error(self):
        """Test that ValueError is raised for a malformed JSON structure."""
        with self.assertRaises(ValueError):
            RoleManager(self.malformed_roles_path)

if __name__ == '__main__':
    unittest.main()