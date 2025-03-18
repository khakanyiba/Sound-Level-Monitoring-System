import socket

#UDP client setup
UDP_IP = "0.0.0.0"  #listen on all interfaces
UDP_PORT = 5005

#create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Client listening for broadcast messages on port 5005...")
while True:
    data, addr = sock.recvfrom(1024)  #receive data from the server
    message = data.decode()
    print(f"Received message from {addr}: {message}")