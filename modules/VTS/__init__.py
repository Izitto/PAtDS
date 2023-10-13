import os
import importlib


# Get the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Get all files.
views = [f for f in os.listdir(script_dir) if f.endswith(".py") and f != "__init__.py"]

# Import all files from modules folder.
for view in views:
    module_path = os.path.splitext(view)[0]  # Remove the '.py' extension
    module_name = "modules.VTS." + module_path
    importlib.import_module(module_name)
    print('App imported ' + view + ' successfully.')
