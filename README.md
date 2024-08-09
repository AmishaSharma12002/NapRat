# NapRat

NapRat is a Python-based Remote Access Trojan (RAT) simulator designed for educational and testing purposes. This tool allows you to remotely control a machine, execute commands, and manipulate files as if you were using the command line directly on the target system. 

> **WARNING**: This tool is for educational purposes only. Unauthorized use of this tool is illegal and unethical. Always obtain proper permission before testing or using NapRat on any system.

## Features

- **Remote Command Execution**: Execute commands on the remote machine.
- **File Manipulation**: Create, delete, rename, move, copy, and list files and directories.
- **Firewall Management**: Automatically manages the Windows Firewall to allow or block connections.
- **Administrative Privileges**: Ensures the script is run with administrative privileges to manage system settings.

## Requirements

- Python 3.x
- Windows Operating System (for firewall management)
- Administrative privileges

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ammycodex/NapRat.git
    cd NapRat
    ```

2. **Install dependencies** (if any are added later):
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Server

1. **Run the server script**:
   - Open Command Prompt or PowerShell as Administrator.
   - Navigate to the directory where `server.py` is located.
   - Run the script:
     ```bash
     python server.py
     ```

   The server will automatically manage the Windows Firewall, find an open port, and start listening for incoming connections.

### Running the Client

1. **Run the client script**:
   - Open Command Prompt or PowerShell (no admin rights needed).
   - Run the client script:
     ```bash
     python client.py
     ```

2. **Connect to the server**:
   - The client will listen for server information (IP and port) and then allow you to send commands to the server.

### Available Commands

- `cd <directory>`: Change the current directory.
- `cp <source> <destination>`: Copy files and directories.
- `mv <source> <destination>`: Move or rename files and directories.
- `rm <target>`: Remove files and directories.
- `mkdir <directory>`: Create a new directory.
- `dir`: List files in the current directory.
- `pwd`: Print the current working directory.
- `ren <oldname> <newname>`: Rename a file or directory.
- `type <filename>`: Display the content of a file.
- `echo <message>`: Print a message.
- `rmdir <directory>`: Remove a directory.
- `exit` or `quit`: Close the connection.

### Stopping the Server

- When the server is stopped, it will automatically close the open port and restore the Windows Firewall settings.

## Security Note

This tool requires administrative privileges to manage the Windows Firewall and execute certain commands. Always be cautious when running scripts with elevated privileges.

## Disclaimer

**NapRat** is provided "as is" without any warranty. The creators are not responsible for any damage caused by the use or misuse of this tool. Use it responsibly and legally.

---


