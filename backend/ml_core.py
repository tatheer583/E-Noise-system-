import os
import pickle
import pandas as pd
import logging

class MLCore:
    """Manages Machine Learning model loading and predictions."""
    
    LABELS = {
        0: "Clean Air",
        1: "Smoke Detected",
        2: "Gas Leak",
        3: "Alcohol Presence",
        4: "Polluted Air"
    }

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.logger = logging.getLogger(__name__)

    def load_model(self):
        """Loads the scikit-learn model from disk."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                self.logger.info("ML Model loaded successfully.")
            except Exception as e:
                self.logger.error(f"Failed to load model: {e}")
        else:
            self.logger.warning(f"Model file not found at {self.model_path}. Predictions will be 'Unknown'.")

    def predict(self, data: dict) -> str:
        """Runs prediction on incoming sensor data."""
        if not self.model:
            return "Unknown"
        
        try:
            features = pd.DataFrame([[
                data['mq2'], data['mq3'], data['mq5'], data['mq7'], data['mq135']
            ]], columns=['mq2', 'mq3', 'mq5', 'mq7', 'mq135'])
            
            pred_idx = self.model.predict(features)[0]
            return self.LABELS.get(pred_idx, "Unknown")
        except Exception as e:
            self.logger.error(f"Prediction error: {e}")
            return "Error"
