async function loadEnergyData() {
    const res = await fetch('/api/energy');
    const data = await res.json();

    const tipsContainer = document.getElementById('tips');
    tipsContainer.innerHTML = '';
    data.tips.forEach(t => {
        const div = document.createElement('div');
        div.className = 'tip-box';
        div.innerHTML = `<b>${t.device}:</b> ${t.tip}`;
        tipsContainer.appendChild(div);
    });
}

async function loadChartData() {
    const res = await fetch('/api/history');
    const history = await res.json();
    const chartsContainer = document.getElementById('charts');
    chartsContainer.innerHTML = '';

    Object.keys(history).forEach(device => {
        const canvas = document.createElement('canvas');
        chartsContainer.appendChild(canvas);
        new Chart(canvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: history[device].map((_, i) => i + 1),
                datasets: [{
                    label: device,
                    data: history[device],
                    fill: false,
                    borderColor: '#2e7d32',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true }
                }
            }
        });
    });
}

async function loadSummaryChart() {
    const res = await fetch('/api/summary');
    const summary = await res.json();

    const summaryCanvas = document.createElement('canvas');
    document.getElementById('charts').appendChild(summaryCanvas);

    new Chart(summaryCanvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: summary.labels,
            datasets: [{
                label: 'Average Daily Usage',
                data: summary.values,
                fill: false,
                borderColor: '#00796b',
                backgroundColor: '#b2dfdb',
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            }
        }
    });
}

loadEnergyData();
loadChartData();
loadSummaryChart();
