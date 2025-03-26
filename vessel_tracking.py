import paho.mqtt.client as mqtt
import json
from flask import Flask, jsonify, render_template
import threading
import webbrowser
import signal
import sys

# Store vessel locations
vessel_locations = []

app = Flask(__name__)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("vessels-v2/+/location")

def on_message(client, userdata, msg):
    global vessel_locations
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        lat = data.get("lat")
        lon = data.get("lon")
        heading = data.get("heading")

        if lat and lon:
            vessel_locations.append((lat, lon))
            print(f"Received: lat={lat}, lon={lon}, heading={heading}")
    except Exception as e:
        print("Error parsing message:", e)

def fetch_vessel_data():
    client = mqtt.Client(transport="websockets")
    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_set()  # Enable TLS
    client.connect("meri.digitraffic.fi", 443, 60)
    client.loop_forever()  # Run indefinitely

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/vessels")
def get_vessels():
    return jsonify(vessel_locations)

def run_flask():
    # Open the map in the default web browser
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True, use_reloader=False)

def signal_handler(sig, frame):
    print("Shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start fetching vessel data
    fetch_vessel_data()
