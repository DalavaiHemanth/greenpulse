function fetchData() {
    fetch('/api/energy')
        .then(res => res.json())
        .then(json => {
            document.getElementById('deviceName').innerText = json.data.device;
            document.getElementById('currentUsage').innerText = json.data.usage;
            document.getElementById('status').innerText = json.overuse ? "⚠️ Overuse Detected!" : "✅ Normal";
            document.getElementById('tipText').innerText = json.tip;
        });
}

window.onload = fetchData;
