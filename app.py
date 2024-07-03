from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)


API_KEY = "6ed1d1b943ab46b9804145041240207"
IP_API_KEY = "b5ef005b5ede469f9e8bbff8a3031f3b"

def get_user_location():
    try:
        response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={IP_API_KEY}")
        return response.json()["ip_address"]
    except:
        print("Error: Unable to detect your location.")
        return None

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('name')
    client_ip = get_user_location()
    # Get temperature from weather API
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={client_ip}")
    weather_data = response.json()
    temperature = weather_data['current']['temp_f']
    location = weather_data['location']['region']
    greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}'

    return json.dumps({'client_ip': client_ip, 'location': location, 'greeting': greeting}, sort_keys=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
