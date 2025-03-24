import socket
import sounddevice as sd
import numpy as np
import RPi.GPIO as GPIO  # Import GPIO library for Raspberry Pi
import time  # Import time for buzzer duration

# GPIO setup
BUZZER_PIN = 18  # Example GPIO pin for the buzzer
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUZZER_PIN, GPIO.OUT)  # Set the buzzer pin as output

# UDP server setup
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 5005
THRESHOLD = 80  # Example threshold value

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Server listening on port 5005...")

# Wait for the client to send its IP address
data, addr = sock.recvfrom(1024)
client_ip = addr[0]  # Extract the client's IP address from the received data
print(f"Client IP received: {client_ip}")

# Function to calculate decibel level from audio data
def calculate_db(indata):
    rms = np.sqrt(np.mean(indata**2))  # Calculate root mean square of audio data
    db = 20 * np.log10(rms)  # Convert RMS to decibels
    return db

# Callback function to process audio data
def audio_callback(indata, frames, time, status):
    db = calculate_db(indata)
    print(f"Current sound level: {db:.2f} dB")

    # Send data to client
    message = f"Sound level: {db:.2f} dB"
    sock.sendto(message.encode(), (client_ip, UDP_PORT))  # Use the client's IP address

    # Send alert if sound level exceeds threshold
    if db > THRESHOLD:
        alert_message = f"ALERT! Noise level: {db:.2f} dB"
        sock.sendto(alert_message.encode(), (client_ip, UDP_PORT))

        # Activate the buzzer
        print("Activating buzzer...")
        GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn on the buzzer
        time.sleep(0.5)  # Buzzer duration (adjustable)
        GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off the buzzer

# Start audio stream
try:
    print("Starting sound level monitoring...")
    with sd.InputStream(callback=audio_callback):
        sd.sleep(100000)  # Monitor for 100 seconds (adjustable)
finally:
    GPIO.cleanup()  # Clean up GPIO settings when the program exits