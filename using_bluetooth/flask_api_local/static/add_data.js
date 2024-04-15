
        document.getElementById('runScriptButton').addEventListener('click', function() {

            const loadingDiv = document.getElementById('loading');
            loadingDiv.style.display = 'block';

            //const recordNumber = record_number;
            //var muscle = muscle_Name

            fetch(`/rundemo?record_number=${record_number}&muscle_type=${muscle_Name}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                console.log('Result:', data.result);

                loadingDiv.style.display = 'none';

                fetchRecord(data)
                // Handle response from the server as needed
            })
            .catch(error => {
                console.error('Error:', error);

                loadingDiv.style.display = 'none';
                // Handle errors
            });
        });

        function fetchRecord() {
            const recordNumber = record_number
            //var muscle_type = 

            document.getElementById('myChart').scrollIntoView({ behavior: 'smooth' });

            if (recordNumber) {
                fetch(`/get_recording?record_number=${record_number}&muscle_type=${muscle_Name}`)  // Pass record number as a query parameter
                    .then(response => response.json())
                    .then(data => {
                        const recordNumber = data.record_number;
                        let sensorData = data.data;  // Replace with actual data field name

                        // Chart.js configuration
                        let ctx = document.getElementById('myChart').getContext('2d');
                        let myChart = new Chart(ctx, {
                            type: 'line',  // Choose chart type (e.g., line, bar, pie)
                            data: {
                            labels: [...Array(sensorData.length).keys()],  // Generate labels for data points
                            datasets: [{
                                label: `Record #${record_number} and Muscle Type: ${muscle_Name}`,
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
            record_number = record_number + 1
        }

 
        