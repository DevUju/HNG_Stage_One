from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
import requests

app = Flask(__name__)

headers = {'Authorization': 'Bearer 0d9e78a4407977'}
API_Key = "9792ff02e8419b2c2ef8157cd36c3a05"

def get_user_location():
    try:
        response = requests.get('https://ipinfo.io/' + request.remote_addr + '/json', headers=headers)
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
    visitor_name = "Mark"
    client_ip = "127.0.0.1"

    # Get location from IP address
    location = get_user_location()

    # Get temperature from weather API
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={API_Key}")
    weather_data = response.json()
    temperature = weather_data['main']['temp']

    greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}'
    return jsonify({'client_ip': client_ip, 'location': location, 'greeting': greeting})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



