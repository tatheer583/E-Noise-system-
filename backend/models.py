from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    logs = db.relationship('SensorLog', backref='user', lazy=True)

class SensorLog(db.Model):
    """Sensor data log model."""
    id = db.Column(db.Integer, primary_key=True)
    mq2 = db.Column(db.Float)
    mq3 = db.Column(db.Float)
    mq5 = db.Column(db.Float)
    mq7 = db.Column(db.Float)
    mq135 = db.Column(db.Float)
    prediction = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def to_dict(self):
        return {
            "mq2": self.mq2,
            "mq3": self.mq3,
            "mq5": self.mq5,
            "mq7": self.mq7,
            "mq135": self.mq135,
            "prediction": self.prediction,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
