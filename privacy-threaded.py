import re
import threading
import subprocess
import os
import sys

HEADER = '''@echo off
:: https://privacy.sexy — v0.13.7 — Thu, 26 Dec 2024 18:38:22 GMT
:: Ensure admin privileges
fltmc >nul 2>&1 || (
    echo Administrator privileges are required.
    PowerShell Start -Verb RunAs '%0' 2> nul || (
        echo Right-click on the script and select "Run as administrator".
        pause & exit 1
    )
    exit 0
)
:: Initialize environment
setlocal EnableExtensions DisableDelayedExpansion
'''

def execute_block(block, index):
    temp_filename = f'temp_script_{index}.bat'
    with open(temp_filename, 'w') as temp_file:
        temp_file.write(HEADER)
        for line in block:
            temp_file.write(f'{line}\n')
    subprocess.run([temp_filename], shell=True)
    os.remove(temp_filename)

def main(script_name, max_threads):
    if not os.path.exists(script_name):
        print(f"Error: The script file '{script_name}' does not exist.")
        print("Usage: python privacy-threaded.py <script_name> <max_threads>")
        return

    with open(script_name, 'r') as file:
        content = file.read()
    blocks = re.split(r'''

:: ----------------------------------------------------------''', content)
    threads = []

    for i in range(0, len(blocks), max_threads):
        for j, block in enumerate(blocks[i:i + max_threads]):
            lines = block.strip().split('\n')
            thread = threading.Thread(target=execute_block, args=(lines, i + j))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    script_name = 'privacy-script.bat'
    max_threads = 10

    if len(sys.argv) > 1:
        script_name = sys.argv[1]
    if len(sys.argv) > 2:
        max_threads = int(sys.argv[2])

    main(script_name, max_threads)