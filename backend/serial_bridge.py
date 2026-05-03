import serial
import json
import requests
import time

# Configuration
SERIAL_PORT = 'COM3'  # Update this to your Arduino port
BAUD_RATE = 9600
API_URL = "http://127.0.0.1:5000/api/sensor-data"

def run_bridge():
    print(f"Connecting to Arduino on {SERIAL_PORT}...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) # Wait for connection
        print("Connected! Streaming data to API...")
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                try:
                    # Expecting JSON string from Arduino
                    data = json.loads(line)
                    response = requests.post(API_URL, json=data)
                    print(f"Sent: {data} | Server Response: {response.json().get('prediction')}")
                except json.JSONDecodeError:
                    print(f"Received non-JSON data: {line}")
                except Exception as e:
                    print(f"API Error: {e}")
                    
    except serial.SerialException as e:
        print(f"Serial Error: {e}")
    except KeyboardInterrupt:
        print("Stopping bridge...")

if __name__ == "__main__":
    print("pyserial is required: pip install pyserial")
    run_bridge()
