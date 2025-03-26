import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("vessels-v2/+/location")  # Subscribe to the vessel location topic

def on_message(client, userdata, msg):
    try:
        # Decode and print the raw message
        raw_message = msg.payload.decode("utf-8")
        print(f"Raw MQTT Message: {raw_message}")

        # Parse the topic to extract MMSI
        topic_parts = msg.topic.split("/")
        if len(topic_parts) >= 3 and topic_parts[0] == "vessels-v2":
            mmsi = topic_parts[1]
        else:
            mmsi = "Unknown"

        # Attempt to parse the message as JSON
        data = json.loads(raw_message)
        print(f"MMSI: {mmsi}")
        print(f"Parsed Data: {data}")

        # Optional: Access lat/lon and plot or process
        lat = data.get("lat")
        lon = data.get("lon")
        if lat is not None and lon is not None:
            print(f"Vessel {mmsi} at lat: {lat}, lon: {lon}")

    except Exception as e:
        print(f"Error processing message: {e}")

if __name__ == "__main__":
    client = mqtt.Client(transport="websockets")
    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_set()  # Enable TLS
    client.connect("meri.digitraffic.fi", 443, 60)

    print("Listening for MQTT messages. Press Ctrl+C to exit.")
    try:
        client.loop_forever()  # Run indefinitely
    except KeyboardInterrupt:
        print("Exiting...")
        client.disconnect()
