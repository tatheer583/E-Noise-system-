from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
import pickle
import numpy as np
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-prod'

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'instance', 'database.db')
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)

# db models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    logs = db.relationship('SensorLog', backref='user', lazy=True)

class SensorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mq2 = db.Column(db.Float)
    mq3 = db.Column(db.Float)
    mq5 = db.Column(db.Float)
    mq7 = db.Column(db.Float)
    mq135 = db.Column(db.Float)
    prediction = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

# load the trained model (sklearn)
MODEL_PATH = os.path.join(current_dir, 'models', 'trained_ai_model.pkl')
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    else:
        print(f"warn: model file not found at {MODEL_PATH}. predictions won't work.")

# label map for the model output
LABELS = {
    0: "Clean Air",
    1: "Smoke Detected",
    2: "Gas Leak",
    3: "Alcohol Presence",
    4: "Polluted Air"
}

# Routes
# TODO: add rate limiting here later
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    print(f"DEBUG: Signup attempt for user: {data.get('username')}")
    
    if not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password required"}), 400
        
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_pw)
    try:
        db.session.add(new_user)
        db.session.commit()
        print(f"DEBUG: User {data['username']} created successfully")
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Signup error: {str(e)}")
        return jsonify({"message": "Username already exists or database error"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(f"DEBUG: Login attempt for user: {data.get('username')}")
    
    user = User.query.filter_by(username=data['username']).first()
    if user:
        if bcrypt.check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            print(f"DEBUG: Login successful for {data['username']}")
            return jsonify({"message": "Logged in", "user_id": user.id}), 200
        else:
            print(f"DEBUG: Invalid password for {data['username']}")
    else:
        print(f"DEBUG: User {data['username']} not found")
        
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.json # Expecting {mq2, mq3, mq5, mq7, mq135, user_id?}
    
    # Predict status

    features = pd.DataFrame([[data['mq2'], data['mq3'], data['mq5'], data['mq7'], data['mq135']]], 
                            columns=['mq2', 'mq3', 'mq5', 'mq7', 'mq135'])
    prediction_label = "Unknown"
    
    if model:
        pred_idx = model.predict(features)[0]
        prediction_label = LABELS.get(pred_idx, "Unknown")
    
    new_log = SensorLog(
        mq2=data['mq2'],
        mq3=data['mq3'],
        mq5=data['mq5'],
        mq7=data['mq7'],
        mq135=data['mq135'],
        prediction=prediction_label,
        user_id=data.get('user_id')
    )
    db.session.add(new_log)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "prediction": prediction_label
    })

@app.route('/history', methods=['GET'])
def get_history():
    # Return last 50 logs regardless of user
    logs = SensorLog.query.order_by(SensorLog.timestamp.desc()).limit(50).all()
    history = [{
        "mq2": log.mq2, "mq3": log.mq3, "mq5": log.mq5, "mq7": log.mq7, "mq135": log.mq135,
        "prediction": log.prediction, "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for log in logs]
    return jsonify(history)

@app.route('/current-status', methods=['GET'])
def current_status():
    # Get the latest log
    log = SensorLog.query.order_by(SensorLog.timestamp.desc()).first()
    if log:
        return jsonify({
            "mq2": log.mq2, "mq3": log.mq3, "mq5": log.mq5, "mq7": log.mq7, "mq135": log.mq135,
            "prediction": log.prediction, "timestamp": log.timestamp.strftime("%H:%M:%S")
        })
    return jsonify({"message": "No data available"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    load_model()
    # Cloud Run expects the app to listen on the port defined by the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

