// canvas bg setup
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let particles = [];
let airQualityFactor = 1; // 1 = Clean, >1 = Polluted

window.addEventListener('resize', resizeCanvas);
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();

class Particle {
    constructor() {
        this.reset();
    }
    reset() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 1;
        this.speedX = (Math.random() - 0.5) * 1;
        this.speedY = (Math.random() - 0.5) * 1;
        this.color = 'rgba(0, 242, 255, 0.5)';
    }
    update() {
        // mess up the particles if air is bad
        let distortion = (airQualityFactor - 1) * 5;
        this.x += this.speedX * airQualityFactor + (Math.random() - 0.5) * distortion;
        this.y += this.speedY * airQualityFactor + (Math.random() - 0.5) * distortion;

        if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
            this.reset();
        }
    }
    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function initParticles() {
    particles = [];
    for (let i = 0; i < 150; i++) {
        particles.push(new Particle());
    }
}
initParticles();

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
        p.update();
        p.draw();
    });
    requestAnimationFrame(animate);
}
animate();

// setup the main chart
const chartCtx = document.getElementById('trendsChart').getContext('2d');
let trendsChart = new Chart(chartCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Air Quality Index',
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

// backend api URL (make sure flask is running)
// backend api URL (auto-switches between local and Vercel)
const API_BASE = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' 
    ? 'http://127.0.0.1:5000' 
    : '/api';

let userId = localStorage.getItem('user_id');

if (!userId && !window.location.pathname.includes('login.html')) {
    // window.location.href = 'login.html'; 
    // Commented out for demo purposes so it doesn't loop if backend is off
}

async function fetchData() {
    try {
        const response = await fetch(`${API_BASE}/current-status`);
        const data = await response.json();
        
        if (data.mq2) {
            updateDashboard(data);
        }
    } catch (err) {
        console.error("cant reach backend, falling back to mock data", err);
        simulateData();
    }
}

function updateDashboard(data) {
    document.getElementById('mq2-val').innerText = data.mq2.toFixed(1);
    document.getElementById('mq3-val').innerText = data.mq3.toFixed(1);
    document.getElementById('mq5-val').innerText = data.mq5.toFixed(1);
    document.getElementById('mq7-val').innerText = data.mq7.toFixed(1);
    document.getElementById('mq135-val').innerText = data.mq135.toFixed(1);
    
    const badge = document.getElementById('prediction-status');
    badge.innerText = data.prediction;
    document.getElementById('timestamp').innerText = data.timestamp;

    // Update Air Quality Factor for Animation
    if (data.prediction !== "Clean Air") {
        airQualityFactor = 3;
        badge.classList.add('alert');
        particles.forEach(p => p.color = 'rgba(255, 77, 77, 0.6)');
    } else {
        airQualityFactor = 1;
        badge.classList.remove('alert');
        particles.forEach(p => p.color = 'rgba(0, 242, 255, 0.5)');
    }

    // Update Chart
    if (trendsChart.data.labels.length > 20) {
        trendsChart.data.labels.shift();
        trendsChart.data.datasets[0].data.shift();
    }
    trendsChart.data.labels.push(data.timestamp);
    trendsChart.data.datasets[0].data.push(data.mq135);
    trendsChart.update();
}

// Mock Data Simulation for Demo
function simulateData() {
    const isPolluted = Math.random() > 0.8;
    const mock = {
        mq2: isPolluted ? 400 + Math.random()*200 : 20 + Math.random()*20,
        mq3: 10 + Math.random()*10,
        mq5: 20 + Math.random()*20,
        mq7: isPolluted ? 100 + Math.random()*100 : 10 + Math.random()*10,
        mq135: isPolluted ? 500 + Math.random()*200 : 50 + Math.random()*30,
        prediction: isPolluted ? "Polluted Air" : "Clean Air",
        timestamp: new Date().toLocaleTimeString()
    };
    updateDashboard(mock);
}

setInterval(fetchData, 3000);

async function fetchHistory() {
    try {
        const response = await fetch(`${API_BASE}/history?user_id=${userId || ''}`);
        const data = await response.json();
        
        const tbody = document.getElementById('history-body');
        tbody.innerHTML = ''; // Clear current
        
        data.forEach(log => {
            const row = document.createElement('tr');
            row.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
            row.innerHTML = `
                <td style="padding: 10px;">${log.timestamp}</td>
                <td style="padding: 10px;">${log.mq2.toFixed(1)}</td>
                <td style="padding: 10px;">${log.mq135.toFixed(1)}</td>
                <td style="padding: 10px;">
                    <span style="color: ${log.prediction === 'Clean Air' ? 'var(--accent-blue)' : 'var(--danger)'}">
                        ${log.prediction}
                    </span>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error("Could not fetch history:", err);
    }
}

// Fetch history initially and then every 10 seconds
fetchHistory();
setInterval(fetchHistory, 10000);

function logout() {
    localStorage.removeItem('user_id');
    window.location.href = 'login.html';
}

// Initial Username Display
document.getElementById('username-display').innerText = localStorage.getItem('username') || 'Guest User';
