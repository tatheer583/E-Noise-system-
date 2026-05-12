import serial
import json
import requests
import time
import logging

class SerialBridge:
    """Bridges physical Arduino Serial data to the Backend API."""

    def __init__(self, port: str, baud_rate: int, api_url: str):
        self.port = port
        self.baud_rate = baud_rate
        self.api_url = api_url
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def start(self):
        """Starts the serial listener and forwards data to the API."""
        self.logger.info(f"Connecting to Arduino on {self.port} at {self.baud_rate} baud...")
        try:
            with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
                time.sleep(2)  # Wait for Arduino to reset/stabilize
                self.logger.info("Connection established. Streaming telemetry...")
                
                while True:
                    if ser.in_waiting > 0:
                        raw_line = ser.readline().decode('utf-8').strip()
                        if not raw_line:
                            continue
                            
                        try:
                            # Expecting structured JSON from Arduino: {"mq2": val, ...}
                            sensor_data = json.loads(raw_line)
                            self._forward_to_api(sensor_data)
                        except json.JSONDecodeError:
                            self.logger.warning(f"Malformed data received: {raw_line}")
                        except Exception as e:
                            self.logger.error(f"Processing error: {e}")
                            
        except serial.SerialException as e:
            self.logger.error(f"Hardware Serial Error: {e}")
        except KeyboardInterrupt:
            self.logger.info("Bridge stopped by operator.")

    def _forward_to_api(self, data: dict):
        """Internal helper to POST data to the REST endpoint."""
        try:
            response = requests.post(self.api_url, json=data, timeout=5)
            response.raise_for_status()
            prediction = response.json().get('prediction', 'Unknown')
            self.logger.info(f"Data Forwarded | AI Result: {prediction}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API unreachable: {e}")

if __name__ == "__main__":
    # Standard configuration
    # Note: Operators should update SERIAL_PORT based on their local environment
    CONFIG = {
        "SERIAL_PORT": "COM3", 
        "BAUD_RATE": 9600,
        "API_URL": "http://127.0.0.1:5000/sensor-data"
    }
    
    bridge = SerialBridge(
        port=CONFIG["SERIAL_PORT"],
        baud_rate=CONFIG["BAUD_RATE"],
        api_url=CONFIG["API_URL"]
    )
    bridge.start()
