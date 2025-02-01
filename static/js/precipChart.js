const dates_ele = document.getElementById('flask-date');
const precipitations_ele = document.getElementById('flask-pluie');
const dates = JSON.parse(dates_ele.dataset.info);
const precipitations = JSON.parse(precipitations_ele.dataset.info);
const averagesElement = document.getElementById('flask-averages');
const averages = JSON.parse(averagesElement.dataset.info);

document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('precipitationChart').getContext('2d');
    let precipitationChart;

    // Fonction pour créer le graphique initial
    function createChart(filteredDates, filteredPrecipitations) {
        if (precipitationChart) {
            precipitationChart.destroy(); // Détruire le graphique existant s'il y en a un
        }

        precipitationChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: filteredDates,
                datasets: [{
                    label: 'Précipitations en mm',
                    data: filteredPrecipitations,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true, // Activer l'affichage du titre
                        text: 'Précipitations journalières par période annuelle', // Texte du titre
                        font: {
                            size: 18, // Taille de la police
                            weight: 'bold', // Poids de la police
                        },
                        padding: {
                            top: 10,
                            bottom: 20 // Espacement autour du titre
                        },
                        color: '#333' // Couleur du texte
                    }
                },
                layout: {
                    padding: {
                        left: 20,
                        right: 20,
                        top: 20,
                        bottom: 20
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true
                    },
                    y: {
                        beginAtZero: true,
                        title : {
                            display: true,
                            text: 'Précipitations en mm',
                            font: {
                                size: 12,
                                weight: 'bold'
                            }
                        }
                    }
                }
            }
        });
    }

    // Générer les options pour le sélecteur de période
    // Générer les options pour le sélecteur de période
    const periodSelect = document.getElementById('period-select');
    const uniqueYears = [...new Set(dates.map(date => date.split('-')[0]))]; // Extraire les années uniques

    uniqueYears.forEach(year => {
        const startDate = `${year}-01-01`;
        let endDate;

        // Si l'année est 2025, définir la date de fin comme la date du jour
        if (year === '2025') {
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0'); // Les mois commencent à 0
            const day = String(today.getDate()).padStart(2, '0');
            endDate = `${year}-${month}-${day}`;
        } else {
            endDate = `${parseInt(year) + 1}-01-01`;
        }

        const option = document.createElement('option');
        option.value = `${startDate}_${endDate}`;
        option.textContent = `${startDate} à ${endDate}`;
        periodSelect.appendChild(option);
    });

    // Sélectionner la première période par défaut
    const firstYear = uniqueYears[0];
    const firstStartDate = `${firstYear}-01-01`;
    const firstEndDate = `${parseInt(firstYear) + 1}-01-01`;

    // Filtrer les données pour la première période
    const initialFilteredData = dates.reduce((acc, date, index) => {
        if (date >= firstStartDate && date < firstEndDate) {
            acc.dates.push(date);
            acc.precipitations.push(precipitations[index]);
        }
        return acc;
    }, { dates: [], precipitations: [] });

    // Créer le graphique initial avec les données de la première période
    createChart(initialFilteredData.dates, initialFilteredData.precipitations);


    document.getElementById('average-value').textContent = `La moyenne annuelle des précipitations est de ${averages[0].toFixed(2)} mm`;
    // Définir la valeur du sélecteur sur la première période
    periodSelect.value = `${firstStartDate}_${firstEndDate}`;

    // Écouter les changements de sélection
    periodSelect.addEventListener('change', function () {
        const selectedPeriod = periodSelect.value;

        if (selectedPeriod === 'all') {
            // Afficher toutes les données
            createChart(dates, precipitations);
        } else {
            // Filtrer les données en fonction de la période sélectionnée
            const [startDate, endDate] = selectedPeriod.split('_');
            const filteredData = dates.reduce((acc, date, index) => {
                if (date >= startDate && date < endDate) {
                    acc.dates.push(date);
                    acc.precipitations.push(precipitations[index]);
                }
                return acc;
            }, { dates: [], precipitations: [] });

            createChart(filteredData.dates, filteredData.precipitations);

            const selectedIndex = periodSelect.selectedIndex;
            document.getElementById('average-value').textContent = `La moyenne annuelle des précipitations est de ${averages[selectedIndex].toFixed(2)} mm`;
        }
    });
});