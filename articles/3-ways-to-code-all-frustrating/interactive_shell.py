import subprocess

while True:
    try:
        command = input('> ')
    except EOFError:
        break
    if command.strip().lower() == 'exit':
        break
    if not command.strip():
        continue
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='')
    except Exception as e:
        print(f"Error executing command: {e}")

