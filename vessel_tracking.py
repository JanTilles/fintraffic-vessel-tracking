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
        # Decode the raw message
        raw_message = msg.payload.decode("utf-8")
        print(f"Raw MQTT Message: {raw_message}")

        # Parse the topic to extract MMSI
        topic_parts = msg.topic.split("/")
        if len(topic_parts) >= 3 and topic_parts[0] == "vessels-v2":
            mmsi = topic_parts[1]
        else:
            mmsi = "Unknown"

        # Parse the message as JSON
        data = json.loads(raw_message)
        lat = data.get("lat")
        lon = data.get("lon")
        heading = data.get("heading")
        sog = data.get("sog")  # Extract speed over ground

        if lat is not None and lon is not None:
            # Check if the vessel with the same MMSI already exists
            for vessel in vessel_locations:
                if vessel["mmsi"] == mmsi:
                    # Update the existing vessel's data
                    vessel["lat"] = lat
                    vessel["lon"] = lon
                    vessel["heading"] = heading
                    vessel["sog"] = sog
                    break
            else:
                # Add a new vessel entry if it doesn't exist
                vessel_locations.append({"mmsi": mmsi, "lat": lat, "lon": lon, "heading": heading, "sog": sog})
            print(f"Updated Vessel: MMSI={mmsi}, lat={lat}, lon={lon}, heading={heading}, sog={sog}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Global variable to store the MQTT client
mqtt_client = None

def fetch_vessel_data():
    global mqtt_client
    mqtt_client = mqtt.Client(transport="websockets")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.tls_set()  # Enable TLS
    mqtt_client.connect("meri.digitraffic.fi", 443, 60)
    mqtt_client.loop_forever()  # Run indefinitely

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
    global mqtt_client
    print("Shutting down...")

    # Stop the MQTT client loop
    if mqtt_client is not None:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

    # Exit the program
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start fetching vessel data
    fetch_vessel_data()
