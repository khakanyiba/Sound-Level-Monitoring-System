import socket
import sounddevice as sd
import numpy as np

#UDP server setup
UDP_IP = "0.0.0.0"  #listen on all interfaces
UDP_PORT = 5005
THRESHOLD = 80  #example sound threshold

#create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
    sock.sendto(message.encode(), ("CLIENT_IP", UDP_PORT))  #the client ip will be the IP of the device running the client script

    #send alert if sound level exceeds threshold
    if db > THRESHOLD:
        alert_message = f"ALERT! Noise level: {db:.2f} dB"
        sock.sendto(alert_message.encode(), ("CLIENT_IP", UDP_PORT))

#start audio stream
print("Starting sound level monitoring...")
with sd.InputStream(callback=audio_callback):
    sd.sleep(100000)  #monitor for 100 seconds (can be adjusted)