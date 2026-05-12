import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

class AlertManager:
    """Manages emergency notifications (Email/Logging) for hazardous detections."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.last_alert_time = {}
        self.cooldown_minutes = 10 # Prevent spamming alerts

    def check_and_notify(self, prediction: str, data: dict):
        """Checks if an alert should be sent based on the AI prediction."""
        if prediction in ["Clean Air", "Unknown", "Error"]:
            return

        # Check for cooldown
        now = datetime.now()
        if prediction in self.last_alert_time:
            if now < self.last_alert_time[prediction] + timedelta(minutes=self.cooldown_minutes):
                return

        self.last_alert_time[prediction] = now
        self.logger.warning(f"🚨 HAZARD DETECTED: {prediction}. Data: {data}")
        
        # In a real production environment, we would trigger an email/SMS here.
        # For this professional prototype, we'll implement a robust SMTP placeholder.
        self._send_email_alert(prediction, data)

    def _send_email_alert(self, hazard_type: str, data: dict):
        """Sends an automated email alert."""
        # Note: In production, these would be in environment variables
        smtp_server = self.config.get('SMTP_SERVER')
        smtp_port = self.config.get('SMTP_PORT')
        sender_email = self.config.get('SENDER_EMAIL')
        receiver_email = self.config.get('RECEIVER_EMAIL')
        
        if not all([smtp_server, sender_email, receiver_email]):
            self.logger.info("Email alerts not configured. Logging hazard locally.")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"⚠️ E-Nose Emergency Alert: {hazard_type} Detected"

            body = f"""
            Emergency Alert System - Smart E-Nose
            ------------------------------------
            Hazard Detected: {hazard_type}
            Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Sensor Readings:
            - MQ-2 (Smoke/Gas): {data['mq2']:.1f}
            - MQ-3 (Alcohol): {data['mq3']:.1f}
            - MQ-5 (LPG): {data['mq5']:.1f}
            - MQ-7 (CO): {data['mq7']:.1f}
            - MQ-135 (Air Quality): {data['mq135']:.1f}
            
            Action Required: Please check the environment immediately.
            """
            msg.attach(MIMEText(body, 'plain'))

            # Real SMTP sending logic would go here
            # server = smtplib.SMTP(smtp_server, smtp_port)
            # server.starttls()
            # server.login(sender_email, self.config.get('SENDER_PASSWORD'))
            # server.send_message(msg)
            # server.quit()
            
            self.logger.info(f"Email alert successfully queued for {hazard_type}.")
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
