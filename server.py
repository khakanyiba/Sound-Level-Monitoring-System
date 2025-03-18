import socket
import sounddevice as sd
import numpy as np

#UDP server setup
UDP_IP = "0.0.0.0"  #listen on all interfaces
UDP_PORT = 5005
THRESHOLD = 80  #example threshold value

#create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Server listening on port 5005...")

#wait for the client to send its IP address
data, addr = sock.recvfrom(1024)
client_ip = addr[0]  #extract the client's IP address from the received data
print(f"Client IP received: {client_ip}")

#function to calculate decibel level from audio data
def calculate_db(indata):
    rms = np.sqrt(np.mean(indata**2))  #calculate root mean square of audio data
    db = 20 * np.log10(rms)  #convert RMS to decibels
    return db

#callback function to process audio data
def audio_callback(indata, frames, time, status):
    db = calculate_db(indata)
    print(f"Current sound level: {db:.2f} dB")

    #send data to client
    message = f"Sound level: {db:.2f} dB"
    sock.sendto(message.encode(), (client_ip, UDP_PORT))  #use the client's IP address

    #send alert if sound level exceeds threshold
    if db > THRESHOLD:
        alert_message = f"ALERT! Noise level: {db:.2f} dB"
        sock.sendto(alert_message.encode(), (client_ip, UDP_PORT))

#start audio stream
print("Starting sound level monitoring...")
with sd.InputStream(callback=audio_callback):
    sd.sleep(100000)  #monitor for 100 seconds (adjustable)