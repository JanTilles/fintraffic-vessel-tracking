# Vessel Tracking Script

This script uses Traficom digitraffic messaging source for fetching the maritime vessel locations and plots them on a map.

## How it works

1. Connects to the Traficom digitraffic MQTT broker to receive vessel location data.
2. Parses the received data to extract latitude, longitude, and heading information.
3. Stores the vessel locations.
4. Plots the vessel locations on a map using Folium.
5. Saves the map as an HTML file and opens it in a web browser.

## Requirements

- paho-mqtt
- folium
- webbrowser

## Usage

Run the script to fetch vessel data and plot it on a map:

```bash
python fintraffic_vessel_tracking.py