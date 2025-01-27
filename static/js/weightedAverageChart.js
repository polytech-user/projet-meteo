document.addEventListener('DOMContentLoaded', function () {
    // Récupérer les éléments HTML
    const daysEle = document.getElementById('flask-days');
    const averagesEle = document.getElementById('flask-averages');

    // Vérifier que les éléments existent
    if (!daysEle || !averagesEle) {
        console.error("Les éléments HTML pour les données sont introuvables.");
        return;
    }

    // Vérifier que les données ne sont pas vides
    if (!daysEle.dataset.info || !averagesEle.dataset.info) {
        console.error("Les données sont vides ou non définies.");
        return;
    }

    // Afficher les données brutes pour débogage
    console.log("Données brutes (days):", daysEle.dataset.info);
    console.log("Données brutes (averages):", averagesEle.dataset.info);

    // Parser les données JSON
    let days, averages;
    try {
        days = JSON.parse(daysEle.dataset.info);
        averages = JSON.parse(averagesEle.dataset.info);
    } catch (error) {
        console.error("Erreur lors du parsing JSON :", error);
        return;
    }

    // Vérifier que les données parsées sont valides
    if (!Array.isArray(days) || !Array.isArray(averages)) {
        console.error("Les données parsées ne sont pas des tableaux valides.");
        console.log("Days parsés:", days);
        console.log("Averages parsés:", averages);
        return;
    }

    console.log("Days:", days);
    console.log("Averages:", averages);

    // Créer le graphique
    const ctx = document.getElementById('weightedAverageChart').getContext('2d');
    const weightedAverageChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                label: 'Moyenne pondérée des résultats journaliers',
                data: averages,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Moyenne pondérée des résultats journaliers par jour de l\'année',
                    font: {
                        size: 18,
                        weight: 'bold',
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    },
                    color: '#333'
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Jours de l\'année (MM-DD)'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Moyenne pondérée'
                    }
                }
            }
        }
    });
});