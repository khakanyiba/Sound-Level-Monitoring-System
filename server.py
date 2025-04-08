#!/usr/bin/env python3
import RPi.GPIO as GPIO
import socket
import time
import math

# ===== Hardware Configuration =====
SOUND_SENSOR_PIN = 17    # GPIO17 for sound sensor (digital)
ALERT_LED_PIN = 18       # GPIO18 for LED indicator
UDP_PORT = 5005          # Network port
THRESHOLD_ACTIVATIONS = 3  # Min triggers to confirm noise
SAMPLE_RATE = 0.1        # Seconds per reading
DB_CALIBRATION = 30      # Adjust based on sensor sensitivity

# ===== Initialize Hardware =====
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Normally HIGH
GPIO.setup(ALERT_LED_PIN, GPIO.OUT)

# ===== Network Setup =====
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def calculate_db(activations):
    """Convert sensor triggers to simulated dB (0-100 scale)"""
    return min(100, DB_CALIBRATION + (activations * 10))  # Customize scaling

try:
    print("""\n
    SOUND LEVEL MONITORING SERVER
    -----------------------------
    Sensor: GPIO{} | Alert LED: GPIO{}
    Threshold: {} activations (~{} dB)
    Broadcast Port: {}
    """.format(SOUND_SENSOR_PIN, ALERT_LED_PIN, 
               THRESHOLD_ACTIVATIONS,
               calculate_db(THRESHOLD_ACTIVATIONS),
               UDP_PORT))

    while True:
        activations = 0
        start_time = time.time()
        
        # Sample for SAMPLE_RATE seconds
        while (time.time() - start_time) < SAMPLE_RATE:
            if GPIO.input(SOUND_SENSOR_PIN) == 0:  # 0 = sound detected
                activations += 1
            time.sleep(0.001)  # 1ms delay
        
        # Convert to dB and broadcast
        db_level = calculate_db(activations)
        status = f"DB:{db_level:.1f}"
        sock.sendto(status.encode(), ('<broadcast>', UDP_PORT))
        print(f"↳ {status}", end='\r')
        
        # Trigger alert if threshold exceeded
        if db_level > calculate_db(THRESHOLD_ACTIVATIONS):
            alert = f"ALERT! {db_level:.1f}dB (Threshold exceeded)"
            sock.sendto(alert.encode(), ('<broadcast>', UDP_PORT))
            GPIO.output(ALERT_LED_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(ALERT_LED_PIN, GPIO.LOW)

except KeyboardInterrupt:
    print("\nServer stopped")
finally:
    GPIO.cleanup()
    sock.close()