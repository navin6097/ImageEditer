from flask import Flask, request
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return data.get("lat"), data.get("lon"), data
    except:
        return None, None, {}

def reverse_geocode(lat, lon):
    try:
        geolocator = Nominatim(user_agent="geoapi")
        location = geolocator.reverse((lat, lon), exactly_one=True)
        return location.address if location else "Address not found"
    except:
        return "Reverse geocoding failed"

@app.route("/")
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    lat, lon, data = get_ip_info(ip)
    address = reverse_geocode(lat, lon) if lat and lon else "Not available"

    return f"""
        <h1>IP & Location Info</h1>
        <p><b>IP Address:</b> {ip}</p>
        <p><b>City:</b> {data.get('city')}</p>
        <p><b>Region:</b> {data.get('regionName')}</p>
        <p><b>Country:</b> {data.get('country')}</p>
        <p><b>Latitude:</b> {lat}</p>
        <p><b>Longitude:</b> {lon}</p>
        <p><b>Address:</b> {address}</p>
    """


