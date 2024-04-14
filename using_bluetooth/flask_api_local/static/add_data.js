let myChart; // Variable to hold the chart instance

        function fetchRecord() {
            const recordNumber = document.getElementById('record-number-input').value;

            if (recordNumber) {
                fetch(`/get_recording?record_number=${recordNumber}`)  // Pass record number as a query parameter
                    .then(response => response.json())
                    .then(data => {
                        const recordNumber = data.record_number;
                        const sensorData = data.data;  // Replace with actual data field name
                        
                        // Clear existing chart if it exists
                        if (myChart) {
                            myChart.destroy();
                        }

                        // Chart.js configuration
                        const ctx = document.getElementById('myChart').getContext('2d');
                        myChart = new Chart(ctx, {
                            type: 'line',  // Choose chart type (e.g., line, bar, pie)
                            data: {
                            labels: [...Array(sensorData.length).keys()],  // Generate labels for data points
                            datasets: [{
                                label: `Record #${recordNumber}`,
                                data: sensorData,
                                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                borderColor: 'rgba(255, 99, 132, 1)',
                                borderWidth: 1
                            }]
                            },
                            options: {
                            scales: {
                                yAxes: [{
                                ticks: {
                                    beginAtZero: true
                                }
                                }]
                            }
                            }
                        });
                    });
            } else {
                alert("Please enter a valid record number.");
            }
        }