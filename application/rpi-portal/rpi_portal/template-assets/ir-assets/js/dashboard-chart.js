(function () {
    'use strict'
    const pieChart = document.getElementById('pie-chart');
    new Chart(pieChart, {
        type: 'pie',
        data: {
            labels: [
                'Expected Income',
                'Actual Income'
            ],
            datasets: [{
                data: [expected, actual],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                ]
            }]
        }
    });

})()