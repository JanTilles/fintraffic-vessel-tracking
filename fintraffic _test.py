import paho.mqtt.client as mqtt
import time
import json
import folium
import webbrowser

# Store vessel locations
vessel_locations = []

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("vessels-v2/+/location")

def on_message(client, userdata, msg):
    global vessel_locations
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        #print(f"Received message: {data}")
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
    client.loop_start()

    time.sleep(30)  # Increase runtime to 30 seconds

    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker")

def plot_map():
    if not vessel_locations:
        print("No vessel data received, skipping map creation.")
        return

    # Create a map centered around the first vessel location
    m = folium.Map(location=vessel_locations[0], zoom_start=6)

    # Add vessel markers
    for lat, lon in vessel_locations:
        folium.Marker([lat, lon], popup=f"Vessel @ {lat}, {lon}").add_to(m)

    # Save and open the map
    map_file = "vessel_map.html"
    m.save(map_file)
    webbrowser.open(map_file)

if __name__ == "__main__":
    fetch_vessel_data()
    plot_map()
