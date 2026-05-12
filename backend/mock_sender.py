import requests
import time
import random
import logging

class MockSensorArray:
    """Simulates an Arduino-based sensor array sending telemetry to an API."""

    def __init__(self, api_url: str, interval: float = 3.0):
        self.api_url = api_url
        self.interval = interval
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def generate_telemetry(self) -> dict:
        """Generates realistic sensor data based on a pollution probability."""
        is_polluted = random.random() > 0.8
        
        if is_polluted:
            # Simulated high values for smoke/gas detection
            return {
                "mq2": random.uniform(400, 700),
                "mq3": random.uniform(20, 50),
                "mq5": random.uniform(300, 600),
                "mq7": random.uniform(200, 400),
                "mq135": random.uniform(500, 800)
            }
        
        # Normal baseline values
        return {
            "mq2": random.uniform(20, 50),
            "mq3": random.uniform(5, 15),
            "mq5": random.uniform(15, 30),
            "mq7": random.uniform(10, 30),
            "mq135": random.uniform(40, 90)
        }

    def start_streaming(self):
        """Infinite loop to stream telemetry to the backend API."""
        self.logger.info(f"Starting Mock Sensor Data Stream to {self.api_url}...")
        while True:
            data = self.generate_telemetry()
            try:
                response = requests.post(self.api_url, json=data, timeout=5)
                response.raise_for_status()
                prediction = response.json().get('prediction', 'Unknown')
                self.logger.info(f"Telemetry Sent | Prediction: {prediction}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Network error: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
            
            time.sleep(self.interval)

if __name__ == "__main__":
    # Default local configuration
    API_ENDPOINT = "http://127.0.0.1:5000/sensor-data"
    simulator = MockSensorArray(api_url=API_ENDPOINT)
    simulator.start_streaming()
