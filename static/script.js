let chart;
let alertBox = document.getElementById('alertBox');

async function fetchEnergy() {
    const response = await fetch('/api/energy');
    const data = await response.json();
    updateAlert(data.tip, data.overuse);
}

async function fetchHistory() {
    const response = await fetch('/api/history');
    const json = await response.json();
    if (json.values) {
        updateChart(json.labels, json.values);
    }
}

function updateAlert(tip, overuse) {
    alertBox.innerText = tip;
    alertBox.className = 'banner ' + (overuse ? 'warn' : 'ok');
}

function updateChart(labels, values) {
    if (!chart) {
        const ctx = document.getElementById('usageChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Energy Usage (kWh)',
                    data: values,
                    backgroundColor: 'rgba(0, 128, 0, 0.2)',
                    borderColor: 'green',
                    borderWidth: 2
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } else {
        chart.data.labels = labels;
        chart.data.datasets[0].data = values;
        chart.update();
    }
}

// 🔄 Refresh every 5 seconds
setInterval(() => {
    fetchEnergy();
    fetchHistory();
}, 5000);

// Initial load
fetchEnergy();
fetchHistory();
