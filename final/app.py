from flask import Flask, request, render_template

import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/city')
def search_by_city():
    key = 'deeb10dd2998cb3ea5ddf7240b75c918'
    city = request.args.get('q')

    # call API
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}'
    response = requests.get(url).json()

    # exception handling
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {city.title()}. Error message = {message}'

    # get temperature
    current_temperature = response.get('main', {}).get('temp')
    if current_temperature:
        current_temperature_fahrenheit = round((current_temperature - 273.15) * 9/5 + 32, 2)
        current_temperature_celsius = round(current_temperature - 273.15, 2)
        return f'Current temperature of {city.title()} is {current_temperature_fahrenheit} &#8457;, {current_temperature_celsius} &#8451;'
    else:
        return f'Error getting temperature for {city.title()}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)