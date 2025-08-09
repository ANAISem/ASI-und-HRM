import json
from pathlib import Path

class RoleManager:
    """Manages the loading and accessing of agent roles from a configuration file."""

    def __init__(self, roles_path: Path):
        """
        Initializes the RoleManager and loads the roles from the specified path.

        Args:
            roles_path (Path): The path to the JSON file containing role definitions.
        """
        if not roles_path.exists():
            raise FileNotFoundError(f"Roles configuration file not found at: {roles_path}")
        self.roles_path = roles_path
        self._roles = self._load_roles()

    def _load_roles(self) -> dict:
        """Loads and validates roles from the JSON file, storing them in a dictionary keyed by role name."""
        with open(self.roles_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'roles' not in data or not isinstance(data['roles'], list):
            raise ValueError(f"Invalid format in {self.roles_path}: 'roles' key missing or not a list.")

        roles_map = {}
        for role in data['roles']:
            if not all(k in role for k in ['name', 'description', 'capabilities']):
                raise ValueError(f"Invalid role definition in {self.roles_path}. Missing required keys.")
            roles_map[role['name']] = role
        
        return roles_map

    def get_all_roles(self) -> list:
        """Returns a list of all loaded role definitions."""
        return list(self._roles.values())

    def get_role_by_name(self, name: str) -> dict | None:
        """
        Retrieves a specific role by its name.

        Args:
            name (str): The name of the role to retrieve.

        Returns:
            dict | None: The role definition as a dictionary, or None if not found.
        """
        return self._roles.get(name)

# Example Usage (for testing purposes)
if __name__ == '__main__':
    try:
        # Assuming the script is run from the project root
        roles_file_path = Path(__file__).parent / 'data' / 'roles.json'
        role_manager = RoleManager(roles_path=roles_file_path)

        print("Successfully loaded Role Manager.")
        print("-" * 20)

        # Get all roles
        all_roles = role_manager.get_all_roles()
        print(f"Found {len(all_roles)} roles:")
        for r in all_roles:
            print(f"  - {r['name']}: {r['description']}")
        print("-" * 20)

        # Get a specific role
        role_name = 'AURA'
        aura_role = role_manager.get_role_by_name(role_name)
        if aura_role:
            print(f"Details for role '{role_name}':")
            print(json.dumps(aura_role, indent=2, ensure_ascii=False))
        else:
            print(f"Role '{role_name}' not found.")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")