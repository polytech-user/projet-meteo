const datesElement = document.getElementById('flask-date-analyse');
const resultatsElement = document.getElementById('flask-resultats');

const dates = JSON.parse(datesElement.dataset.info);
const resultats = JSON.parse(resultatsElement.dataset.info);



document.addEventListener('DOMContentLoaded', function () {

    // Chart.register(ChartZoom); 
        
    const ctx = document.getElementById('resultChart').getContext('2d');
    


    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [{
                label: 'Résultat journalier',
                data: resultats,
                backgroundColor: resultats.map(value => 
                    value >= 0 
                    ? 'rgba(54, 162, 235, 0.2)' // Bleu translucide pour positifs
                    : 'rgba(255, 99, 132, 0.2)' // Rouge translucide pour négatifs
                ),
                borderColor: resultats.map(value => 
                    value >= 0 
                    ? 'rgba(54, 162, 235, 1)' // Bleu opaque pour positifs
                    : 'rgba(255, 99, 132, 1)' // Rouge opaque pour négatifs
                ),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 0.2,
            plugins: {
                title: {
                    display: true,
                    text: `Résultat journalier pour l'année considérée`,
                    font: {
                        size: 18,
                        weight: 'bold'
                    }
                },
            },
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    title: {
                        display: true,
                        text: 'Résultat (€)'
                    },
                    beginAtZero: true
                }
            }
            
        }
    });
});
