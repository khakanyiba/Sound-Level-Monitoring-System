#!/usr/bin/env python3
import RPi.GPIO as GPIO
import socket
import time

# ===== Hardware Config =====
SOUND_SENSOR_PIN = 17  # GPIO17 for sound sensor (digital out)
UDP_PORT = 5005        # Network port
THRESHOLD = 3          # Min triggers to confirm noise (adjust as needed)

# ===== Initialize =====
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Normally HIGH

# ===== Network Setup =====
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = socket.gethostbyname(socket.gethostname())  # Get Pi's IP

print(f"""\n
SOUND MONITORING SERVER 
-------------------------------------------
Sensor: GPIO{SOUND_SENSOR_PIN}
Server IP: {server_ip}
Port: {UDP_PORT}
Threshold: {THRESHOLD} activations
""")

def detect_sound():
    """Check for sustained sound (avoid false triggers)"""
    triggers = 0
    for _ in range(5):  # Check 5 times
        if GPIO.input(SOUND_SENSOR_PIN) == 0:  # 0 = sound detected
            triggers += 1
        time.sleep(0.02)  # 20ms between checks
    return triggers >= THRESHOLD

try:
    while True:
        if detect_sound():
            alert_msg = "ALERT: Noise detected!"
            sock.sendto(alert_msg.encode(), ('<broadcast>', UDP_PORT))
            print(f"[{time.ctime()}] {alert_msg}")
        else:
            sock.sendto(b"STATUS: Normal", ('<broadcast>', UDP_PORT))
        
        time.sleep(0.1)  # Main loop delay

except KeyboardInterrupt:
    print("\nServer stopped")
finally:
    GPIO.cleanup()
    sock.close()