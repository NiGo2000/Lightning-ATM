import json
import os
import subprocess
import time
from dotenv import load_dotenv

load_dotenv('.env')

# Check if API_KEY and invoice_key are defined
api_key = os.getenv("API_KEY")
invoice_key = os.getenv("invoice_key")

if api_key is None:
    api_key = input("Please enter your Admin Key: ")
    # Save the API key in the .env file
    with open(".env", "a") as f:
        f.write("\n")
        f.write(f"API_KEY={api_key}\n")

if invoice_key is None:
    invoice_key = input("Please enter your invoice key: ")
    # Save the invoice key in the .env file
    with open(".env", "a") as f:
        f.write("\n")
        f.write(f"invoice_key={invoice_key}\n")

# Path to the Svelte application
svelte_path = os.path.abspath('frontend/app/')

# Check if all required packages are installed
package_json = os.path.join(svelte_path, 'package.json')
with open(package_json, "r") as f:
    package_data = json.load(f)
required_packages = package_data.get('dependencies', {})
missing_packages = []
for package_name in required_packages:
    try:
        __import__(package_name)
    except ImportError:
        missing_packages.append(package_name)

if missing_packages:
    print(f"Missing packages: {missing_packages}")
    # Install missing packages
    subprocess.run(['npm', 'install'], cwd=svelte_path)

# Paths to the Python files
backend_path = os.path.abspath('backend')
app_path = os.path.join(backend_path, 'app.py')

# Launch the Python files in new console windows
subprocess.Popen(['x-terminal-emulator', '-e', 'python', app_path], cwd=backend_path)

# test without coin accepter
# coin_acceptor_test = os.path.join(backend_path, 'test_money.py')
# subprocess.Popen(['x-terminal-emulator', '-e', 'python', coin_acceptor_test], cwd=backend_path)

# Launch the Svelte application in a new console window
subprocess.Popen(['x-terminal-emulator', '-e', 'npm', 'run', 'dev'], cwd=svelte_path)

time.sleep(5)
svelte_app_url = os.getenv("svelte_app_url")
subprocess.Popen(['xdg-open', svelte_app_url])

