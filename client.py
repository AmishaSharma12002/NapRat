import socket

def receive_server_info(client_ip, client_port):
    """Receives server IP and port from a known source."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((client_ip, client_port))
        s.listen(1)
        print(f"Listening for server info on {client_ip}:{client_port}...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024).decode('utf-8')
            server_ip, server_port = data.split(':')
            return server_ip, int(server_port)

def send_command(ip, port, command):
    """Sends a command to the server and prints the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print(f"Connecting to server {ip}:{port}...")
            s.connect((ip, port))
            s.sendall(command.encode('utf-8'))
            
            response = s.recv(4096).decode('utf-8')
            print(f"Response from server:\n{response}")
        except Exception as e:
            print(f"Failed to connect or send command: {e}")

if __name__ == "__main__":
    client_ip = "10.4.40.75"  # IP address to listen for server info
    client_port = 12345    # Port to listen for server info

    # Receive server IP and port
    server_ip, server_port = receive_server_info(client_ip, client_port)
    print(f"Received server info: IP={server_ip}, Port={server_port}")

    while True:
        command = input(f"{server_ip}> ")
        if command.lower() in ["exit", "quit"]:
            send_command(server_ip, server_port, command)
            break
        send_command(server_ip, server_port, command)
