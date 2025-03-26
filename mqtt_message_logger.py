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

        # Attempt to parse the message as JSON
        data = json.loads(raw_message)
        print(f"Parsed Data: {data}")
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
