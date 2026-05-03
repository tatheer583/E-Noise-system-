import requests
import time
import random

API_URL = "http://127.0.0.1:5000/sensor-data"

def simulate_arduino():
    print("Starting Mock Sensor Data Stream...")
    while True:
        # Occasionally simulate pollution
        is_polluted = random.random() > 0.8
        
        if is_polluted:
            data = {
                "mq2": random.uniform(400, 700),
                "mq3": random.uniform(20, 50),
                "mq5": random.uniform(300, 600),
                "mq7": random.uniform(200, 400),
                "mq135": random.uniform(500, 800)
            }
        else:
            data = {
                "mq2": random.uniform(20, 50),
                "mq3": random.uniform(5, 15),
                "mq5": random.uniform(15, 30),
                "mq7": random.uniform(10, 30),
                "mq135": random.uniform(40, 90)
            }
        
        try:
            response = requests.post(API_URL, json=data)
            print(f"Sent: {data} | Server: {response.json().get('prediction')}")
        except Exception as e:
            print(f"Error sending data: {e}")
            
        time.sleep(3)

if __name__ == "__main__":
    simulate_arduino()
