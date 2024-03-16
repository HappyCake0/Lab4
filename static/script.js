
var data = {
  labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6'],
  datasets: [
    {
      label: 'CPU_t',
      data: [18, 12, 6, 9, 12, 3, 9],
      fill: false,
      stepped: true,
    }
  ]
};
const config = {
  options: {
      scales: {
      y:
       {
           display: true,
           labelString: 'Ось Y'
       }
      ,
      x: [
       {
         scaleLabel: {
           display: true,
           labelString: 'Ось X'
         },
       }
      ],
    },
    responsive: true,
    interaction: {
      intersect: false,
      axis: 'x'
    },
    plugins: {
      title: {
        display: true,
      }
    }
  }
};



var data1 = {
  labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6'],
  datasets: [
    {
      label: 'CPU_N',
      data: [18, 12, 6, 9, 12, 3, 9],
      fill: false,
      stepped: true,
    }
  ]
};
const config1 = {
  options: {
      scales: {
      y:
       {
           display: true,
           labelString: 'Ось Y'
       }
      ,
      x: [
       {
         scaleLabel: {
           display: true,
           labelString: 'Ось X'
         },
       }
      ],
    },
    responsive: true,
    interaction: {
      intersect: false,
      axis: 'x'
    },
    plugins: {
      title: {
        display: true,
      }
    }
  }
};


var data2 = {
  labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6'],
  datasets: [
    {
      label: 'GPU_t',
      data: [18, 12, 6, 9, 12, 3, 9],
      fill: false,
      stepped: true,
    }
  ]
};
const config2 = {
  options: {
      scales: {
      y:
       {
           display: true,
           labelString: 'Ось Y'
       }
      ,
      x: [
       {
         scaleLabel: {
           display: true,
           labelString: 'Ось X'
         },
       }
      ],
    },
    responsive: true,
    interaction: {
      intersect: false,
      axis: 'x'
    },
    plugins: {
      title: {
        display: true,
      }
    }
  }
};


var data3 = {
  labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6'],
  datasets: [
    {
      label: 'GPU_N',
      data: [18, 12, 6, 9, 12, 3, 9],
      fill: false,
      stepped: true,
    }
  ]
};
const config3 = {
  options: {
      scales: {
      y:
       {
           display: true,
           labelString: 'Ось Y'
       }
      ,
      x: [
       {
         scaleLabel: {
           display: true,
           labelString: 'Ось X'
         },
       }
      ],
    },
    responsive: true,
    interaction: {
      intersect: false,
      axis: 'x'
    },
    plugins: {
      title: {
        display: true,
      }
    }
  }
};


const data4 = {
  labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6'],
  datasets: [
    {
      label: 'MEM',
      data: [18, 12, 6, 9, 12, 3, 9],
      fill: false,
      stepped: true,
    }
  ]
};
const config4 = {
  options: {
      scales: {
      y:
       {
           display: true,
           labelString: 'Ось Y'
       }
      ,
      x: [
       {
         scaleLabel: {
           display: true,
           labelString: 'Ось X'
         },
       }
      ],
    },
    responsive: true,
    interaction: {
      intersect: false,
      axis: 'x'
    },
    plugins: {
      title: {
        display: true,
      }
    }
  }
};
    const myChart = new Chart(
      document.getElementById('CPUt'),{
          type:"line",
            data: data,
            options: config
      }
    );
    const myChart1 = new Chart(
      document.getElementById('CPUn'),{
          type:"line",
            data: data1,
            options: config1
      }
    );
    const myChart2 = new Chart(
      document.getElementById('GPUt'),{
          type:"line",
            data: data2,
            options: config2
      }
    );
    const myChart3 = new Chart(
      document.getElementById('GPUn'),{
          type:"line",
            data: data3,
            options: config3
      }
    );
    var myChart4 = new Chart(
      document.getElementById('MEM'),{
          type:"line",
            data: data4,
            options: config4
      }
    );

document.getElementById('btn').onclick = myFunction;
function myFunction() {
    var xhr = new XMLHttpRequest();
    var date1 = document.getElementById('datetime1').value.replace(/:/g, '-').replace(/T/g, ':');
    var date2 = document.getElementById('datetime2').value.replace(/:/g, '-').replace(/T/g, ':');
    var selected = document.getElementById('aproximate').value;
    var request_body = {
        "datetime-from": date1,
        "datetime-to": date2,
	    "approximate": selected
    };
    var url = "/stats";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var json = JSON.parse(xhr.responseText);
        renderGrafics(json);
    }
};
xhr.send(JSON.stringify(request_body));
}
function renderGrafics(data){
    reRenderChart(myChart, data, "CPU_t");
    reRenderChart(myChart1, data, "CPU_N");
    reRenderChart(myChart2, data, "GPU_t");
    reRenderChart(myChart3, data, "GPU_N");
    reRenderChart(myChart4, data, "memory");
}

function reRenderChart(chart, data, metric){
    chart.data.labels = [];
    chart.data.datasets.forEach((dataset)=>{dataset.data=[]});
    data.forEach((element)=>{
        chart.data.labels.push(element["time"]);
        chart.data.datasets.forEach((dataset)=>{dataset.data.push(parseFloat(element["data"][metric]))});
    });

    chart.update();
}

