import os
import subprocess
from dotenv import load_dotenv

import os
import sys

script_name = "start"

script_path = os.path.realpath(__file__)

# Check the operating system
if sys.platform.startswith("win"):
    # Windows, generate the path to the script in the user directory
    script_path = os.path.join(os.environ["USERPROFILE"], script_name + ".py")
else:
    # Linux, generate the path to the script in the home directory
    script_path = os.path.join(os.environ["HOME"], script_name + ".py")

# Path to the Svelte application
svelte_path = os.path.abspath('frontend/app/')

# Paths to the Python files
backend_path = os.path.abspath('backend')
app_path = os.path.join(backend_path, 'app.py')
test_path = os.path.join(backend_path, 'test_money.py')

# Launch the Python files in new console windows
subprocess.Popen(['x-terminal-emulator', '-e', 'python', app_path], cwd=backend_path)
subprocess.Popen(['x-terminal-emulator', '-e', 'python', test_path], cwd=backend_path)

# Launch the Svelte application in a new console window
subprocess.Popen(['x-terminal-emulator', '-e', 'npm', 'run', 'dev'], cwd=svelte_path)

# Load environment variables
load_dotenv()
svelte_app_url = os.getenv("svelte_app_url")

subprocess.Popen(['xsg-open', svelte_app_url])
