<div align="center">

  <h1>🌐 Smart E-Nose AI Monitoring System</h1>
  
  <p>
    <strong>A Comprehensive Integrated Hardware & Software IoT Solution for Real-Time Air Quality Classification</strong>
  </p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
    <img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white" alt="Arduino" />
    <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  </p>
</div>

<br />

## 📖 About The Project

The **Smart E-Nose** is a fully **integrated software and hardware** base project. It bridges the gap between physical environmental sensing and modern artificial intelligence. The physical hardware (an Arduino with a 5-sensor array) collects raw telemetry, which is then processed by a locally hosted Python backend using Machine Learning to classify air quality in real-time.

---

## ✨ 10 Key Features

1.  **Multi-Sensor Fusion**: Simultaneously monitors MQ-2, MQ-3, MQ-5, MQ-7, and MQ-135 sensors.
2.  **AI-Powered Classification**: Uses a Random Forest model to distinguish between Clean Air, Smoke, Gas Leaks, Alcohol, and Pollution.
3.  **Futuristic UI**: A high-performance dashboard built with a sleek Glassmorphism design system.
4.  **Reactive Background**: An HTML5 Canvas particle simulation that reacts dynamically to pollution levels (turning red and chaotic when gas is detected).
5.  **Live Time-Series Charts**: Interactive data visualization using Chart.js for tracking sensor trends.
6.  **Secure Authentication**: Operator login system with Bcrypt-hashed password security and SQLite database management.
7.  **Automated Serial Bridge**: Proprietary Python script that seamlessly converts hardware signals into API-ready JSON data.
8.  **Software Simulator**: A built-in mock data sender allowing full system testing without physical hardware.
9.  **Historical Analytics**: Dedicated logging system that stores past sensor readings and AI predictions for audit trails.
10. **Zero-Config Deployment**: Optimized for 100% local operation with no external dependencies or API keys required.

---

## 🔌 Circuit Diagram & Hardware Setup

The system utilizes an Arduino Uno as the central brain, connected to an array of five specialized gas sensors.

![Circuit Diagram](docs/circuit_diagram.png)

*   **MQ-2**: Smoke & Combustible Gases
*   **MQ-3**: Alcohol Vapor
*   **MQ-5**: LPG & Natural Gas
*   **MQ-7**: Carbon Monoxide
*   **MQ-135**: Air Quality (Benzene, Alcohol, Smoke)

---

## 🛡️ Security & Safety Applications

This project is designed for critical environment monitoring in various public and private sectors:

*   **🏫 Schools**: Provides early warning systems for chemistry labs and cafeterias to prevent fire hazards and ensure student safety.
*   **🏢 Offices**: Monitors indoor air quality (IAQ) and detects unauthorized smoking or alcohol presence in restricted zones.
*   **🛍️ Malls & Public Spaces**: Monitors food courts for gas leaks and ensures the overall safety of large crowds by detecting atmospheric pollutants instantly.

---

## 🧠 Challenges & Solutions

Developing a merged hardware-software system presented several unique challenges:

*   **Challenge: Sensor Noise**: Raw sensor data from MQ sensors can be highly volatile and noisy.
    *   **Solution**: Implemented a software-based filtering layer and used a robust Random Forest ML model which is naturally resistant to outliers and noise.
*   **Challenge: Real-time Data Synchronization**: Ensuring the web dashboard reflects hardware changes without lag.
    *   **Solution**: Built a multi-threaded Serial Bridge in Python that pushes data to the Flask API as soon as it's received from the Arduino.
*   **Challenge: UI Performance**: Running a complex particle simulation alongside live charts was resource-heavy.
    *   **Solution**: Optimized the Canvas rendering loop and used efficient data-shifting techniques in Chart.js to maintain 60FPS.

---

## 🔮 Future Advancements

*   **Mobile Integration**: Developing a dedicated Flutter app for remote mobile monitoring via smartphones.
*   **IoT Cloud Sync**: Enabling data synchronization with AWS or Firebase for global access.
*   **Predictive Maintenance**: Training the AI to detect when a sensor is failing or needs recalibration based on historical drift.
*   **Alert System**: Integration of SMS (Twilio) and Email (SendGrid) notifications for instant emergency alerts.

---

## 🚀 Getting Started

### 1. The Easy Way (Windows)
Double-click `start.bat`. It will boot the backend, frontend, and simulator automatically.

### 2. Manual Setup
Refer to the documentation inside the `backend` and `frontend` folders for detailed installation steps.

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.
