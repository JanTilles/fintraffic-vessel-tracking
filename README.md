# Vessel Tracking System

This project is a vessel tracking system that fetches real-time vessel location data from an MQTT broker, processes the data, and visualizes it on an interactive map using a Flask web application.

## Features
- Fetches vessel location data (`lat`, `lon`, `heading`, `sog`) from the MQTT topic `vessels-v2/+/location`.
- Extracts the MMSI (Maritime Mobile Service Identity) from the MQTT topic.
- Displays vessel locations on an interactive map using Leaflet.js.
- Automatically updates the map every 5 seconds with the latest vessel data.
- Opens the map in the default web browser when the Flask server starts.
- Includes a utility script to log raw MQTT messages for debugging.
- Gracefully shuts down the Flask server and MQTT client when `Ctrl+C` is pressed.

## Requirements
- Python 3.7+
- MQTT broker access (e.g., `meri.digitraffic.fi`)
- Web browser for viewing the map

## Installation
1. Clone the repository or copy the project files to your local machine.
2. Install the required Python packages:
   ```bash
   pip install paho-mqtt flask
   ```
3. Ensure you have an active internet connection to load the Leaflet.js map tiles.

## Usage

### 1. Start the Vessel Tracking System
Run the main script to start fetching vessel data and serving the map:
```bash
python vessel_tracking.py
```
- The Flask server will start at `http://127.0.0.1:5000/`.
- The map will automatically open in your default web browser.

### 2. Debug MQTT Messages
Use the `mqtt_message_logger.py` script to log raw MQTT messages for debugging:
```bash
python mqtt_message_logger.py
```
- This script will print raw and parsed MQTT messages to the console.

## File Descriptions
### `vessel_tracking.py`
- Main script that fetches vessel data from the MQTT broker and serves the map using Flask.
- Processes `lat`, `lon`, `heading`, `sog`, and MMSI from the MQTT messages.
- Gracefully shuts down the MQTT client and Flask server when terminated.

### `templates/map.html`
- HTML template for the interactive map.
- Uses Leaflet.js to display vessel locations and updates markers every 5 seconds.
- Displays the following information in the popup for each vessel:
  - MMSI
  - Latitude and Longitude
  - Heading
  - Speed Over Ground (SOG)

### `mqtt_message_logger.py`
- Utility script to log raw MQTT messages for debugging.
- Helps verify the structure and content of incoming MQTT messages.

## How It Works
1. **Data Fetching**:
   - The `vessel_tracking.py` script connects to the MQTT broker and subscribes to the topic `vessels-v2/+/location`.
   - Incoming messages are parsed to extract `lat`, `lon`, `heading`, `sog`, and MMSI.

2. **Data Visualization**:
   - The Flask server serves an interactive map at `http://127.0.0.1:5000/`.
   - Vessel locations are displayed as markers on the map, and the map updates every 5 seconds.

3. **Debugging**:
   - Use `mqtt_message_logger.py` to inspect raw MQTT messages and ensure the data is being received correctly.

## Example MQTT Message
```json
{
  "time": 1742985298,
  "sog": 10.5,
  "cog": 141.0,
  "navStat": 0,
  "rot": 0,
  "posAcc": false,
  "raim": false,
  "heading": 141,
  "lon": 21.078755,
  "lat": 60.497457
}
```

## Notes
- The system uses MMSI as a unique identifier for vessels.
- Ensure the MQTT broker is accessible and provides valid data for the system to function correctly.

## License
This project is licensed under the MIT License.