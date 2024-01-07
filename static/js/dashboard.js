const ctx = document.getElementById("myChart").getContext("2d");

new Chart(ctx, {
  type: "line",
  data: {
    labels: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    datasets: [
      {
        label: "Invoice Revenue",
        data: [1200, 340, 0, 1450, 1200, 3000, 5000],
        borderWidth: 1,
        fill: false,
        pointStyle: "rectRot",
        pointRadius: 10,
        pointHoverRadius: 15,
        borderColor: "#9384d1",
      },
    ],
  },
  options: {
    scales: {
      x: {
        ticks: {
          color: "white",
          borderColor: "white",
        },
        scaleLabel: {
          color: "white",
          borderColor: "white",
        },
      },
      y: {
        beginAtZero: true,
        ticks: {
          color: "white",
          precision: 0, // this will show only whole numbers
          min: 1000, // this will set the minimum value of the y axis
          max: 5000, // this will set the maximum value of the y axis
          stepSize: 1500, // this will set the interval between the tick marks
          callback: function (value) {
            // if the value is zero, return an empty string
            if (value === 0) {
              return "";
            }
            // if the value is greater than or equal to 1000, return the value divided by 1000 with a K suffix
            if (value >= 1000) {
              return value / 1000 + "K";
            }
            // otherwise, return the value as it is
            return value;
          },
        },
        scaleLabel: {
          color: "white",
        },
      },
    },
  },
});
