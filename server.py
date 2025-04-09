#!/usr/bin/env python3
import RPi.GPIO as GPIO
import socket
import time
import subprocess

# ===== Hardware Config =====
SOUND_SENSOR_PIN = 17
UDP_PORT = 5005
THRESHOLD = 3  # Adjust as needed

# ===== GPIO Setup =====
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ===== Network Setup =====
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

server_ip = subprocess.getoutput("hostname -I").split()[0]

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
    for _ in range(5):
        if GPIO.input(SOUND_SENSOR_PIN) == GPIO.HIGH:  # Sound detected
            triggers += 1
        time.sleep(0.02)
    return triggers >= THRESHOLD

try:
    while True:
        if detect_sound():
            alert_msg = "ALERT: Noise detected!"
            sock.sendto(alert_msg.encode(), ('255.255.255.255', UDP_PORT))
            print(f"[{time.ctime()}] {alert_msg}")
        else:
            sock.sendto(b"STATUS: Normal", ('255.255.255.255', UDP_PORT))
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nServer stopped")
finally:
    GPIO.cleanup()
    sock.close()
