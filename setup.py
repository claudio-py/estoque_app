import subprocess
import sys
import os
import venv

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

# Detect system paths
is_windows = os.name == "nt"
venv_path = "venv"

# Create venv if missing
if not os.path.isdir(venv_path):
    print("Virtual environment not found. Creating...")
    venv.create(venv_path, with_pip=True)

# Determine the python inside venv
python_exec = (
    os.path.join(venv_path, "Scripts", "python.exe")
    if is_windows
    else os.path.join(venv_path, "bin", "python")
)

# Install dependencies
run(f'"{python_exec}" -m pip install -r requirements.txt')

# Apply migrations
run(f'"{python_exec}" manage.py migrate')

# Create superuser (waits for user input)
run(f'"{python_exec}" manage.py createsuperuser')

# Run server
run(f'"{python_exec}" manage.py runserver )
