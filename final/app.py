from flask import Flask, request

import requests
import configparser

app = Flask(__name__)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['weatherapi']['API_KEY']

@app.route('/')
def index():
    return '<h1>Welcome to weather app</h1>'

@app.route('/city')
def search_by_city():
    key = get_api_key()
    city = request.args.get('q')

    # call API
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
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