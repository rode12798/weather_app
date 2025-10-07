<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Weather Finder</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: #e8f3ff;
            margin: 0;
        }
        h1 {
            background: #1a73e8;
            color: white;
            padding: 10px;
            border-radius: 8px;
            width: fit-content;
            margin: 20px auto;
        }
        input, button {
            padding: 10px;
            margin: 5px;
        }
        .card {
            background: white;
            width: 250px;
            margin: 20px auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
        }
        .forecast {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        .forecast-card {
            background: #fff;
            border-radius: 10px;
            width: 130px;
            padding: 10px;
            box-shadow: 0px 0px 5px rgba(0,0,0,0.1);
        }
        .forecast-card img {
            width: 50px;
        }
        canvas {
            margin-top: 30px;
            max-width: 500px;
        }
    </style>
</head>
<body>
    <h1>☁ Weather Finder.com</h1>
    <form method="POST">
        <input type="text" name="city" placeholder="Enter City" required>
        <button type="submit">Search</button>
    </form>

    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}

    {% if weather %}
    <div class="card">
        <h2>{{ weather.city }}</h2>
        <p>🌡 Temperature: {{ weather.temp }} °C</p>
        <p>💧 Humidity: {{ weather.humidity }} %</p>
        <p>☁ Condition: {{ weather.description }}</p>
    </div>

    {% if forecast_data and forecast_data.forecast %}
    <h3>5-Day Forecast</h3>
    <div class="forecast">
        {% for day in forecast_data.forecast %}
        <div class="forecast-card">
            <h4>{{ day.date }}</h4>
            <img src="http://openweathermap.org/img/w/{{ day.icon }}.png" alt="icon">
            <p>{{ day.temp }} °C</p>
            <p>{{ day.desc }}</p>
        </div>
        {% endfor %}
    </div>

    <canvas id="tempChart"></canvas>
    <script>
        const labels = {{ forecast_data.labels | tojson }};
        const temps = {{ forecast_data.temps | tojson }};

        new Chart(document.getElementById('tempChart'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Temperature (°C)',
                    data: temps,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.3,
                    fill: false
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: false }
                }
            }
        });
    </script>
    {% endif %}
    {% endif %}
</body>
</html>
