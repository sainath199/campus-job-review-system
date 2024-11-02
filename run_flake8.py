import yaml
import subprocess

# Load configuration from _config.yml
with open('_config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Extract Flake8 settings
flake8_config = config.get('flake8', {})

# Build the command for Flake8
flake8_command = ['flake8']

# Add options to command based on extracted settings
if 'max-line-length' in flake8_config:
    flake8_command.append(f'--max-line-length={flake8_config["max-line-length"]}')

if 'exclude' in flake8_config:
    flake8_command.append(f'--exclude={",".join(flake8_config["exclude"])}')

# Run Flake8
subprocess.run(flake8_command + ['your_project_directory/'])  # Replace with your actual directory
