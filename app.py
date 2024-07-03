from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)


API_KEY = "6ed1d1b943ab46b9804145041240207"

def get_user_location():
    try:
        if request.headers.getlist("X-Forwarded-For"):
            user_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            user_ip = request.remote_addr
        return user_ip
    except:
        print("Error: Unable to detect your location.")
        return None

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', "Guest")
    client_ip = get_user_location()
    print(client_ip)
    if client_ip:
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={client_ip}")
    else:
        response = "Location Does Not Exist!"
    

    weather_data = response.json()
    temperature = weather_data['current']['temp_f']
    location = weather_data['location']['region']
    greeting = f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}'

    return json.dumps({'client_ip': client_ip, 'location': location, 'greeting': greeting}, sort_keys=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
