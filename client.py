import socket

# UDP client setup
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 5005

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Client listening for broadcast messages on port 5005...")
while True:
    data, addr = sock.recvfrom(1024)  # Receive data from the server
    message = data.decode()

    # Check if the message is an alert
    if "ALERT!" in message:
        print(f"\n*** ALERT RECEIVED ***\n{message}\n")
    else:
        print(f"Received message from {addr}: {message}")