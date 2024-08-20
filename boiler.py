import os

# Define the folder structure as a dictionary
structure = {
    'app': {
        '__init__.py': None,
        'main.py': None,
        'routers': {
            '__init__.py': None,
        },
        'crud': {
            '__init__.py': None,
        },
        'schemas': {
            '__init__.py': None,
        },
        'models': {
            '__init__.py': None,
        },
        'external_services': {
            '__init__.py': None,
        },
        'utils': {
            '__init__.py': None,
        },
        # Add the new files directly within the 'app' directory
        'settings.py': None,
        'exceptions.py': None,
        'constants.py': None,
        'database.py': None,
        'security.py': None,
    },
    'tests': {
        '__init__.py': None,
    },
    'requirements.txt': None,
    '.gitignore': None,
    'README.md': None,
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if content is None:
            # Create a file
            with open(path, 'w') as f:
                pass
        else:
            # Create a directory
            os.makedirs(path, exist_ok=True)
            # Recursively create the structure inside the directory
            create_structure(path, content)

# Create the project structure
create_structure('.', structure)

print("Project folder structure created successfully.")
