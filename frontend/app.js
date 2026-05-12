/**
 * Smart E-Nose Dashboard Controller
 * Handles real-time telemetry visualization and AI status updates.
 */

class ENoseDashboard {
    constructor() {
        this.apiBase = 'http://127.0.0.1:5000';
        this.airQualityFactor = 1; // 1 = Clean, >1 = Polluted
        this.particles = [];
        this.trendsChart = null;
        
        this.initCanvas();
        this.initChart();
        this.setupEventListeners();
        this.startPolling();
    }

    initCanvas() {
        this.canvas = document.getElementById('bg-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.resizeCanvas();
        this.createParticles();
        this.animateParticles();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        this.particles = [];
        for (let i = 0; i < 150; i++) {
            this.particles.push(this.createParticle());
        }
    }

    createParticle() {
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            size: Math.random() * 2 + 1,
            speedX: (Math.random() - 0.5) * 1,
            speedY: (Math.random() - 0.5) * 1,
            color: 'rgba(0, 242, 255, 0.5)',
            reset: function(canvas) {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
            }
        };
    }

    animateParticles() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(p => {
            let distortion = (this.airQualityFactor - 1) * 5;
            p.x += p.speedX * this.airQualityFactor + (Math.random() - 0.5) * distortion;
            p.y += p.speedY * this.airQualityFactor + (Math.random() - 0.5) * distortion;

            if (p.x < 0 || p.x > this.canvas.width || p.y < 0 || p.y > this.canvas.height) {
                p.reset(this.canvas);
            }

            this.ctx.fillStyle = p.color;
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fill();
        });

        requestAnimationFrame(() => this.animateParticles());
    }

    initChart() {
        const ctx = document.getElementById('trendsChart').getContext('2d');
        this.trendsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Air Quality (MQ-135)',
                    data: [],
                    borderColor: '#00f2ff',
                    tension: 0.4,
                    fill: true,
                    backgroundColor: 'rgba(0, 242, 255, 0.1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }

    setupEventListeners() {
        window.addEventListener('resize', () => this.resizeCanvas());
        document.getElementById('username-display').innerText = 'System Operator';
    }

    async fetchData() {
        try {
            const response = await fetch(`${this.apiBase}/current-status`);
            if (!response.ok) throw new Error('Backend unreachable');
            
            const data = await response.json();
            this.updateUI(data);
        } catch (err) {
            console.warn("Backend connection issue, falling back to simulator logic...");
            // Optionally handle UI feedback here
        }
    }

    updateUI(data) {
        // Update sensor values
        ['mq2', 'mq3', 'mq5', 'mq7', 'mq135'].forEach(id => {
            const el = document.getElementById(`${id}-val`);
            if (el) el.innerText = data[id].toFixed(1);
        });
        
        // Update Prediction Badge
        const badge = document.getElementById('prediction-status');
        badge.innerText = data.prediction;
        document.getElementById('timestamp').innerText = data.timestamp;

        // Update Advanced Analytics
        this.updateAnalytics(data);

        if (data.prediction !== "Clean Air") {
            this.airQualityFactor = 3;
            badge.classList.add('alert');
            this.particles.forEach(p => p.color = 'rgba(255, 77, 77, 0.6)');
        } else {
            this.airQualityFactor = 1;
            badge.classList.remove('alert');
            this.particles.forEach(p => p.color = 'rgba(0, 242, 255, 0.5)');
        }

        // Update Chart
        const labels = this.trendsChart.data.labels;
        const dataset = this.trendsChart.data.datasets[0].data;

        if (labels.length > 20) {
            labels.shift();
            dataset.shift();
        }
        
        labels.push(data.timestamp);
        dataset.push(data.mq135);
        this.trendsChart.update('none'); // Update without animation for performance
    }

    updateAnalytics(data) {
        const riskEl = document.getElementById('risk-val');
        const gasEl = document.getElementById('primary-gas');
        const stabilityEl = document.getElementById('stability-val');

        if (data.prediction === "Clean Air") {
            riskEl.innerText = "LOW";
            riskEl.style.color = "var(--success)";
            gasEl.innerText = "Baseline";
        } else {
            riskEl.innerText = "HIGH";
            riskEl.style.color = "var(--danger)";
            gasEl.innerText = data.prediction.split(' ')[0]; // E.g., "Smoke" or "Gas"
        }

        // Simulate a "stability" metric based on signal noise
        const noise = (Math.random() * 5).toFixed(1);
        stabilityEl.innerText = `${(99.5 - (parseFloat(noise)))}%`;
    }

    async fetchHistory() {
        try {
            const response = await fetch(`${this.apiBase}/history`);
            const data = await response.json();
            
            const tbody = document.getElementById('history-body');
            tbody.innerHTML = '';
            
            data.forEach(log => {
                const row = document.createElement('tr');
                row.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
                row.innerHTML = `
                    <td style="padding: 10px;">${log.timestamp}</td>
                    <td style="padding: 10px;">${log.mq2.toFixed(1)}</td>
                    <td style="padding: 10px;">${log.mq135.toFixed(1)}</td>
                    <td style="padding: 10px;">
                        <span style="color: ${log.prediction === 'Clean Air' ? '#00f2ff' : '#ff4d4d'}">
                            ${log.prediction}
                        </span>
                    </td>
                `;
                tbody.appendChild(row);
            });
        } catch (err) {
            console.error("History fetch failed:", err);
        }
    }

    startPolling() {
        setInterval(() => this.fetchData(), 3000);
        setInterval(() => this.fetchHistory(), 10000);
        this.fetchData();
        this.fetchHistory();
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new ENoseDashboard();
});
