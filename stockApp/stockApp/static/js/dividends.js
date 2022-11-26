const renderChart = (data, labels) =>{
    const ctx = document.getElementById('divBySymbol').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: labels,
        datasets: [{
            label: 'Stock',
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        title: {
          display: false,
          text: "Current value by stock",
        },
        legend: {
            position: "bottom",
            align: 'center',
            labels:{
                fontSize: 10,
                boxWidth: 10
            }
        }
      },
    });
  };

const getLineChartData = () => {
    console.log("fetching");
    fetch("by_stock")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const [labels, data] = [
            Object.keys(results),
            Object.values(results)
        ];

        renderChart(data, labels);
    });
};

document.onload = getLineChartData()



const YearChart = (data, labels) =>{
    const ctx = document.getElementById('divByYear').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Total Amount',
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                }
            }]
        },
        title: {
          display: false,
          text: "Current value by stock",
        },
        legend: {
            display: false,
            position: "right",
            labels:{
                fontSize: 10,
                boxWidth: 10
            }
        }
      },
    });
  };

const getYearChartData = () => {
    console.log("fetching");
    fetch("dividend_by_year")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const [labels, data] = [
            Object.keys(results),
            Object.values(results)
        ];

        YearChart(data, labels);
    });
};

document.onload = getYearChartData()