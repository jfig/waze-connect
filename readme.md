# Waze Connect 

## !! WIP Warning / Alpha stage - Thread with caution !!

This project fetches real-time traffic alert data from Waze for Cities Partner Program and processes it to filter actionable alerts based on specific criteria. It supports sending notifications for these filtered alerts to a specified webhook URL, making it suitable for integration with messaging platforms.

Webhook have been successfully teste with Microsoft Teams and Slack.


## Features

- Fetches real-time alert data from multiple Waze API endpoints.
- Filters alerts based on user-defined criteria (e.g., alert types to include or exclude).
- Sends notifications for filtered, actionable alerts to a specified webhook URL.

## Getting Started

### Prerequisites

- Python 3.6+
- requests library
- dotenv library (for managing environment variables)

### Installation

1. Clone the repository:

    ```sh
    git clone git@github.com:jfig/waze-connect.git
    cd waze-connect/app
    ```

2. Install required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

### Configuration

Create a `.env` file in the root directory with the following content, adjusting the values according to your setup, an example may be found at `.env-example`:

```sh
WEBHOOK_URL='your_webhook_url'
WAZE_URLS='waze_api_url_1,waze_api_url_2'
POLL_INTERVAL_SECONDS=120
ALERT_ON='ACCIDENT,JAM'
ALERT_OFF='HAZARD_WEATHER_FOG'
```

### Usage

Run the application:

```sh
python app.py
```

## How It Works

- **Data Fetching:** The application periodically fetches traffic alert data from the configured Waze API URLs.
- **Alert Filtering:** It then filters the fetched alerts based on the configured criteria (`ALERT_ON`, `ALERT_OFF`).
- **Notification:** For each actionable alert, a notification is sent to the configured `WEBHOOK_URL`.

## Roadmap / Future Plans

* MQTT send new alerts, status changes, and termination via MQTT, will require keeping track of active alerts.
* Alert filtering by type and ranking, only send alert above certain ranking, definable by alert type
* Suppress Alerts if another similar of same type is within a certain distance, enabled and distance configurable by type
* New Geo-Fence, Waze for Cities has a limit of points defining each polygon, this leads to the inclusion of lots of other roads near the operation a filter by Street Name may be used to filter out other Street and Geo-JSON defined Geo-fences in intersections to 

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Loose notes to integrate above or on `/docs/`


**Confidence scores**: Waze gives each incident a confidence score based on how Waze drivers passing by the incident react to the report. Drivers can mark the incident either with a “thumbs up” to indicate that the incident is accurate or “not there” to indicate that the incident is no longer visible. The score ranges between 0 and 10, and a higher score indicates more positive feedback from Waze users.

**Reliability scores**: Waze also gives each incident a reliability score based on the experience level of the reporter. Wazers gain experience levels by driving with Waze and contributing to the map. The higher their level, the higher their reliability score. The score ranges between 0 and 10, with 10 being the most reliable.
