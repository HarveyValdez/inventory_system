// static/js/chart.js - Fixed height version

document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('stockChart');
    if (!canvas) return;

    const categories = JSON.parse(canvas.dataset.categories || '[]');
    const stocks = JSON.parse(canvas.dataset.stocks || '[]');

    if (categories.length > 0 && stocks.length > 0) {
        // Set fixed canvas size
        canvas.style.height = '250px';
        
        new Chart(canvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Total Stock',
                    data: stocks,
                    backgroundColor: 'rgba(0, 184, 148, 0.8)',
                    borderColor: 'rgba(0, 184, 148, 1)',
                    borderWidth: 1,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // This is key for fixed height
                plugins: { 
                    legend: { display: false } 
                },
                scales: {
                    y: { 
                        beginAtZero: true, 
                        title: { display: true, text: 'Stock Quantity' } 
                    },
                    x: { 
                        title: { display: true, text: 'Category' } 
                    }
                }
            }
        });
    } else {
        canvas.style.display = 'none';
        const card = canvas.closest('.card');
        if (card) card.innerHTML += '<p class="text-muted text-center mt-3">No category data</p>';
    }
});