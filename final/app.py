from flask import Flask, request, render_template

import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/city')
def search_by_city():
    key = 'deeb10dd2998cb3ea5ddf7240b75c918'
    city = request.args.get('city')
    data = get_results(city, key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('weather.html', location=location, weather=weather, feels_like=feels_like, temp=temp)

def get_results(city, api):
    # call API
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api}'
    response = requests.get(url).json()

    # exception handling
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {city.title()}. Error message = {message}'

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)