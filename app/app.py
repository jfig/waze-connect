import requests
import json
import time
import logging
import strings
import os
import sys
import signal
from typing import Any, Dict
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables from file if it exists
load_dotenv()

map_urls_str = os.getenv('MAP_URLS', '{}')
try:
    MAP_URLS = json.loads(map_urls_str)
except json.JSONDecodeError as e:
    logging.error(f"Error parsing MAP_URLS: {e}")
    MAP_URLS = None

# Constants and Configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WAZE_URLS = [url.strip() for url in os.getenv('WAZE_URLS', '').split(',')]


POLL_INTERVAL_SECONDS = int(os.getenv('POLL_INTERVAL_SECONDS', 120))

ALERT_ON = os.getenv('ALERT_ON', '').split(',')
if ALERT_ON == ['']:
    ALERT_ON = None

ALERT_OFF = os.getenv('ALERT_OFF', '').split(',')
if ALERT_OFF == ['']:
    ALERT_OFF = None    

# Initialize a dictionary to track the last_millis for each URL
last_millis_per_url = {url: 0 for url in WAZE_URLS}

# List of active alarms 
active_alarms = []


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Functions


def signal_handler(sig, frame):
    """
    Handle the signal received by the application.

    Args:
        sig (int): The signal number.
        frame (frame): The current stack frame.

    Returns:
        None
    """
    logging.info("Waze Alerts has been stopped (SIGTERM received).")
    send_message(WEBHOOK_URL, "Waze Alerts", "Waze Alerts has been stopped.")
    # Perform any cleanup here
    sys.exit(0)



def fetch_alert_data() -> Dict[str, Any]:
    """
    Fetch and merge alert data from multiple Waze API URLs, considering that 'jams' and 'alerts'
    keys might not always be present in the API response. Filters alerts to include only new ones
    based on 'pubMillis' and preserves 'endTimeMillis' for each URL.
    
    Returns:
    - dict[str, Any]: Merged and filtered alert data from the Waze APIs.
    """
    if WAZE_URLS is None or not WAZE_URLS:
        logging.error("Error: WAZE_URLS is not set.")
        raise ValueError("WAZE_URLS is not set.")

    merged_data = {"jams": [], "alerts": []}

    for url in WAZE_URLS:
        logging.debug(f"Fetching data from {url}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Filter new alerts and jams based on 'pubMillis' compared to last_millis for this URL
            new_alerts = [alert for alert in data.get('alerts', [])
                          if alert['pubMillis'] > last_millis_per_url[url]]
            new_jams = [jam for jam in data.get('jams', [])
                        if jam['pubMillis'] > last_millis_per_url[url]]

            merged_data["alerts"].extend(new_alerts)
            merged_data["jams"].extend(new_jams)

            # Update last_millis for this URL if 'endTimeMillis' is present in the response
            if 'endTimeMillis' in data:
                last_millis_per_url[url] = data['endTimeMillis']

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error for URL {url}: {e}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Error for URL {url}: {e}")

    # Remove 'jams' and 'alerts' keys if they are empty
    if not merged_data["jams"]:
        del merged_data["jams"]
    if not merged_data["alerts"]:
        del merged_data["alerts"]

    return merged_data

def filter_actionable_alerts(alerts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Filter the alerts to only include actionable alerts.

    Args:
    - alerts (list[dict[str, any]]): The alerts to filter.

    Returns:
    - list[dict[str, any]]: The actionable alerts.
    """
    actionable_alerts = []
    for alert in alerts:
        if ( 
            ALERT_ON is None or
            ( alert['type'] in ALERT_ON and alert['subtype'] == '' ) or 
            alert['subtype'] in ALERT_ON
        ):
            actionable_alerts.append(alert)
    return actionable_alerts


def send_message(webhook_url, title, text):
    """
    Send a message using a webhook.

    Args:
    - webhook_url (str): The URL of the webhook.
    - title (str): Title of the message card.
    - text (str): The text message to be sent.

    Returns:
    - response: The response from the Teams webhook.
    """
    message_card = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "title": title,
        "text": text
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(
        url=webhook_url,
        headers=headers,
        data=json.dumps(message_card)
    )

    return response

def create_map_links_str(x: float, y: float) -> str:
    """
    Creates a markdown-formatted string of map links with given coordinates.

    Given a pair of coordinates (x, y), this function dynamically generates a markdown string
    containing links to various map services defined in the MAP_URLS dictionary. Each map link
    is formatted with the service name and the URL, with the coordinates inserted into the URL.

    Args:
        x (float): The longitude of the location.
        y (float): The latitude of the location.

    Returns:
        str: A markdown-formatted string containing links to map services. If MAP_URLS is not defined
             or is empty, an empty string is returned.

    Example:
        >>> MAP_URLS = {"Google Maps": "https://www.google.com/maps?q={y},{x}",
                        "OpenStreetMap": "https://www.openstreetmap.org/?mlat={y}&mlon={x}"}
        >>> create_map_links_str(-74.0060, 40.7128)
        'Maps: [Google Maps](https://www.google.com/maps?q=40.7128,-74.0060) [OpenStreetMap](https://www.openstreetmap.org/?mlat=40.7128&mlon=-74.0060) '
    """
    # Check if MAP_URLS is not defined or empty, and return an empty string if so.
    if not MAP_URLS:
        return ""
    
    # Initialize the output string with "Map:" or "Maps:" depending on the number of map services defined.
    output = "Map: " if len(MAP_URLS) == 1 else "Maps: "
    
    # Iterate through each map service defined in MAP_URLS.
    for name, url in MAP_URLS.items():
        # Replace the placeholders in the URL template with the actual coordinates.
        formatted_url = url.format(x=x, y=y)
        # Append the markdown link for the map service to the output string.
        output += f"[{name}]({formatted_url}) "
    
    # Return the constructed string, removing any trailing space.
    return output.strip()
        

def main():

    # Register the signal handler for SIGTERM
    signal.signal(signal.SIGTERM, signal_handler)

    # check if the webhook URL is set
    if WEBHOOK_URL is None:
        logging.error("Error: WEBHOOK_URL is not set.")
        raise ValueError("WEBHOOK_URL is not set.")
 
    send_message(WEBHOOK_URL, "Waze Alerts", "Waze Alerts is now running.")

    try:
        while True:
            logging.debug("New turn")

            # Get data from Waze API
            try:
                data = fetch_alert_data()
            except ValueError:
                logging.warning(f"Waiting {POLL_INTERVAL_SECONDS} seconds before trying again...")
                time.sleep(POLL_INTERVAL_SECONDS)
                continue

            logging.debug("Data: " + str(data))

            actionable_alerts = filter_actionable_alerts(data.get('alerts', []))

            # Send a message for each new alert
            for alert in actionable_alerts:            
                logging.info("New alert: " + alert['type'] + " - " + alert['subtype'])

                if alert['subtype'] == '':
                    title = strings.alert_types.get(alert['type'], "")
                else:
                    title = strings.alert_subtypes.get(alert['subtype'], alert['subtype'])

                # Dynamically create the map link
                x = alert['location']['x']
                y = alert['location']['y']
                maps_str = create_map_links_str(x, y)

                rating = alert['reportRating']
                confidence = alert['confidence']
                reliability = alert['reliability']

                text = f"Rating: {rating} | Confidence: {confidence} | Reliability: {reliability} | Coordinates: {x}, {y}"
                if maps_str != "":
                    text += f" | {maps_str}"

                send_message(WEBHOOK_URL, title, text)
            
            # Wait 2 minutes before checking for new alerts
            time.sleep(POLL_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logging.info("Waze Alerts has been stopped by keyboard interrupt.")
        send_message(WEBHOOK_URL, "Waze Alerts", "Waze Alerts has been stopped by keyboard interrupt.")        

if __name__ == "__main__":
    main()
