const gain_loss = document.getElementById("gain-loss")

const set_color = () => {
    if (gain_loss.innerHTML.substring(0,1) == "-"){
        gain_loss.style.color = "red"
    }
    else {
        gain_loss.style.color = "green"
    }
};

document.onload=set_color()

const renderChart = (data, labels) =>{
    const ctx = document.getElementById('valueBySymbol').getContext('2d');
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
                fontSize: 12,
                boxWidth: 10
            }
        }
      },
    });
  };

const getLineChartData = () => {
    console.log("fetching");
    fetch("stock-value-summary")
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


const performance = (data, labels) =>{
    const ctx = document.getElementById('performance').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Total Value',
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
            display: false,
            position: "right",
        }
      },
    });
  };

  const getPerformanceChartData = () => {
    console.log("fetching");
    fetch("portfolio-performance")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const [labels, data] = [
            Object.keys(results),
            Object.values(results)
        ];

        performance(data, labels);
    });
};

document.onload = getPerformanceChartData()