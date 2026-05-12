import os
import logging
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import config
from models import db, User, SensorLog
from ml_core import MLCore

# Initialize Extensions
bcrypt = Bcrypt()
cors = CORS()
ml_core = None

def create_app(config_name='default'):
    """Application factory for the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Setup Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Initialize Extensions with App
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    # Initialize ML Core
    global ml_core
    ml_core = MLCore(app.config['MODEL_PATH'])
    with app.app_context():
        ml_core.load_model()
        db.create_all()

    # --- API Routes ---

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "E-Nose API"}), 200

    @app.route('/sensor-data', methods=['POST'])
    def receive_data():
        """Handles incoming sensor telemetry and runs AI prediction."""
        data = request.json
        required_fields = ['mq2', 'mq3', 'mq5', 'mq7', 'mq135']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required sensor fields"}), 400

        prediction = ml_core.predict(data)
        
        try:
            new_log = SensorLog(
                mq2=data['mq2'],
                mq3=data['mq3'],
                mq5=data['mq5'],
                mq7=data['mq7'],
                mq135=data['mq135'],
                prediction=prediction,
                user_id=data.get('user_id')
            )
            db.session.add(new_log)
            db.session.commit()
            return jsonify({"status": "success", "prediction": prediction}), 201
        except Exception as e:
            logger.error(f"Database error: {e}")
            return jsonify({"error": "Internal server error during data persistence"}), 500

    @app.route('/current-status', methods=['GET'])
    def get_current_status():
        """Returns the most recent sensor reading and prediction."""
        latest_log = SensorLog.query.order_by(SensorLog.timestamp.desc()).first()
        if not latest_log:
            return jsonify({"message": "No data available"}), 404
        return jsonify(latest_log.to_dict()), 200

    @app.route('/history', methods=['GET'])
    def get_history():
        """Returns the last 50 historical logs."""
        logs = SensorLog.query.order_by(SensorLog.timestamp.desc()).limit(50).all()
        return jsonify([log.to_dict() for log in logs]), 200

    # Note: Authentication routes (signup/login) removed as per user request
    # for local-first seamless operation.

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
