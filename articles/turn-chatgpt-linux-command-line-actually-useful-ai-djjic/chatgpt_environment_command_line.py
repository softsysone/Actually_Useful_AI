import os
import subprocess
import getpass
import socket
import shlex

# Example user input command
input_data = "ls -l /"

# Get Environmental Variables for prompt
username = getpass.getuser()  # Get the current username
hostname = socket.gethostname()  # Get the current hostname
prompt = f"{username}@{hostname}$ "

try:
    command_results = subprocess.run(
        input_data,
        shell=True,
        capture_output=True,
        text=True
    )

    # Display the results
    print(command_results.stdout, end="")  # Print standard output

    if command_results.stderr:
        print(command_results.stderr, end="")  # Print error output if any

except Exception as e:
    print(f"Error executing command: {e}")

# Print the prompt
print(prompt)

