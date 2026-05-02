import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

# Generate synthetic data for the E-Nose
def generate_data(n_samples=200):
    data = []
    # Clean Air
    for _ in range(n_samples):
        data.append([
            np.random.uniform(10, 50),  # MQ-2
            np.random.uniform(5, 30),   # MQ-3
            np.random.uniform(10, 40),  # MQ-5
            np.random.uniform(5, 20),   # MQ-7
            np.random.uniform(20, 100), # MQ-135
            0 # Clean
        ])
    
    # Smoke
    for _ in range(n_samples):
        data.append([
            np.random.uniform(300, 800), # MQ-2 high
            np.random.uniform(10, 50),
            np.random.uniform(50, 200),
            np.random.uniform(50, 200),
            np.random.uniform(400, 900), # MQ-135 high
            1 # Smoke
        ])

    # Gas Leak
    for _ in range(n_samples):
        data.append([
            np.random.uniform(200, 600),
            np.random.uniform(10, 40),
            np.random.uniform(400, 900), # MQ-5 high
            np.random.uniform(20, 100),
            np.random.uniform(100, 400),
            2 # Gas Leak
        ])

    # Alcohol
    for _ in range(n_samples):
        data.append([
            np.random.uniform(20, 100),
            np.random.uniform(400, 900), # MQ-3 high
            np.random.uniform(20, 100),
            np.random.uniform(10, 50),
            np.random.uniform(100, 300),
            3 # Alcohol
        ])

    # Polluted Air
    for _ in range(n_samples):
        data.append([
            np.random.uniform(100, 300),
            np.random.uniform(50, 150),
            np.random.uniform(100, 300),
            np.random.uniform(200, 600), # MQ-7 high
            np.random.uniform(500, 900), # MQ-135 high
            4 # Polluted
        ])

    df = pd.DataFrame(data, columns=['mq2', 'mq3', 'mq5', 'mq7', 'mq135', 'label'])
    return df

def train_and_save():
    print("Generating synthetic data...")
    df = generate_data()
    X = df.drop('label', axis=1)
    y = df['label']

    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, '..', 'models', 'trained_ai_model.pkl')
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # We need to install joblib or use pickle. joblib is better for sklearn models.
    import pickle
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save()
