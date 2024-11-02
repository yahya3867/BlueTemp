var map = L.map('map').setView([25.3043, -90.0659], 5);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 10
}).addTo(map);

const ctx = document.getElementById('chart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Actual',
                data: [],
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                spanGaps: false
            },
            {
                label: 'Predicted',
                data: [],
                fill: false,
                borderColor: 'rgb(192, 192, 75)',
                spanGaps: false
            }
        ]
    },
    options: {
        scales: {
            x: {
                type: 'category',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Water Temperature (°C)'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false,
    }
});
