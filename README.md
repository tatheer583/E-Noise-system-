<div align="center">

  <h1>🌐 Smart E-Nose AI Monitoring System</h1>
  
  <p>
    <strong>A Comprehensive Hardware & Software IoT Solution for Real-Time Air Quality Classification</strong>
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

This repository contains an end-to-end **Hardware and Software merged system**. 

The physical hardware (an Arduino coupled with an array of MQ gas sensors) continuously senses and collects raw environmental data. This telemetry is streamed to a Python-based backend where a Machine Learning model analyzes it in real-time, classifying the air quality and instantly visualizing the results on a high-performance web dashboard.

> **Note**: This project is designed to be **100% Local**. There are no `.env` files to configure and no external API keys required to run the core system.

---

## ✨ Key Features

- **🧠 Real-Time AI Classification**: A Random Forest model instantly categorizes air into: `Clean Air`, `Smoke`, `Gas Leak`, `Alcohol`, or `Polluted Air`.
- **💻 Dynamic Dashboard**: A futuristic dark-mode UI built with glassmorphism principles.
- **🎨 Reactive Visuals**: Features a custom HTML5 Canvas particle simulation that reacts dynamically to air quality (particles become chaotic during pollution).
- **📊 Interactive Analytics**: Live time-series charts (via Chart.js) and a real-time historical logging table.
- **🔐 Secure Authentication**: Includes operator registration and login using hashed passwords (`Bcrypt`).

---

## 🗂️ Project Architecture

```text
E-Nose System/
├── backend/
│   ├── app.py                 # Core Flask REST API & WebSocket Logic
│   ├── train_model.py         # AI Training Script (Random Forest)
│   ├── mock_sender.py         # Software Simulator (for use without hardware)
│   └── serial_bridge.py       # Hardware-to-Software Serial Bridge
├── frontend/
│   ├── dashboard.html         # Main UI / Dashboard
│   ├── login.html             # Operator Authentication
│   ├── app.js                 # Frontend Logic & Particle Simulation
│   └── style.css              # Design System
├── arduino/
│   └── sensors.ino            # Physical Hardware Firmware
└── models/
    └── trained_ai_model.pkl   # Serialized Machine Learning Model
```

---

## 🚀 Getting Started

### 1. The Easy Way (Windows)
If you are on Windows, simply double-click the included `start.bat` file. It will automatically boot up the backend, the frontend server, and the mock data simulator, then give you a link to open in your browser.

### 2. Manual Setup

**Step 1: Install Dependencies**
Navigate to the `backend` folder and install the required Python packages:
```bash
cd backend
pip install flask flask-sqlalchemy flask-bcrypt flask-cors scikit-learn pandas numpy requests pyserial
```

**Step 2: Start the Backend Server**
```bash
python app.py
```

**Step 3: Feed Data to the System**
*   **Option A (Simulation):** If you don't have the hardware plugged in, run the simulator in a new terminal:
    ```bash
    python mock_sender.py
    ```
*   **Option B (Real Hardware):** Upload `arduino/sensors.ino` to your Arduino, then run the serial bridge:
    ```bash
    python serial_bridge.py
    ```

**Step 4: Launch the Dashboard**
Open the `frontend/login.html` file in any modern web browser to access the system.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.
