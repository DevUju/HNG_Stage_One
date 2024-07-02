from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import requests

app = Flask(__name__)

IP = request.headers.getlist("X-Forwarded-For")
API_KEY = "6ed1d1b943ab46b9804145041240207"
URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={IP}"

def get_user_location():
    try:
        response = requests.get(url=URL)
        data = response.json()
        lat, lon = data['loc'].split(',')
        geolocator = Nominatim(user_agent="location_search")
        location = geolocator.reverse((lat, lon))
        return location
    except:
        print("Error: Unable to detect your location.")
        return None

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = input("Enter your name: ")
    # Get location from IP address
    location = get_user_location()
    # Get temperature from weather API
    response= requests.get(url=URL)
    weather_data = response.json()
    temperature = weather_data['main']['temp']

    greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}'
    return jsonify({'client_ip': IP, 'location': location, 'greeting': greeting})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



