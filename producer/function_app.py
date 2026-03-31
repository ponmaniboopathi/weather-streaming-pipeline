import logging
import azure.functions as func
from azure.eventhub import EventHubProducerClient, EventData
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


import json
import requests


app = func.FunctionApp()

@app.timer_trigger(schedule="*/30 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def weatherapifunction(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    


 
    EVENT_HUB_NAME = "pmb-weather-streaming-eventhub"

    # Initialize producer
    # Config
    EVENT_HUB_NAMESPACE = "weatherstreamingnamespace.servicebus.windows.net"

    # Managed Identity Credential
    credential = DefaultAzureCredential()

    # Initialize Producer
    producer = EventHubProducerClient(
        fully_qualified_namespace=EVENT_HUB_NAMESPACE,
        eventhub_name=EVENT_HUB_NAME,
        credential=credential
    )



    def send_event(event):
        # Create batch
        event_data_batch = producer.create_batch()

        # Add event
        event_data_batch.add(EventData(json.dumps(event)))

        # Send batch
        producer.send_batch(event_data_batch)


    # -------------------------------
    # Handle API Response
    # -------------------------------
    def handle_response(response):
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"{response.status_code}: {response.text}"
            }

    # -------------------------------
    # Get Current Weather
    # -------------------------------
    def get_current_weather(base_url, api_key, location):
        url = f"{base_url}/current.json"
        params = {
            "key": api_key,
            "q": location,
            "aqi": "yes"
        }

        response = requests.get(url, params=params)
        return handle_response(response)

    # -------------------------------
    # Get Forecast
    # -------------------------------
    def get_forecast_weather(base_url, api_key, location, days):
        url = f"{base_url}/forecast.json"
        params = {
            "key": api_key,
            "q": location,
            "days": days
        }

        response = requests.get(url, params=params)
        return handle_response(response)

    # -------------------------------
    # Get Alerts
    # -------------------------------
    def get_alerts(base_url, api_key, location):
        url = f"{base_url}/alerts.json"
        params = {
            "key": api_key,
            "q": location,
            "alerts": "yes"
        }

        response = requests.get(url, params=params)
        return handle_response(response)

    # -------------------------------
    # Flatten Data
    # -------------------------------
    def flatten_data(current_weather, forecast_weather, alerts):

        location_data = current_weather.get("location", {})
        current = current_weather.get("current", {})
        condition = current.get("condition", {})
        air_quality = current.get("air_quality", {})

        forecast_days = forecast_weather.get("forecast", {}).get("forecastday", [])
        alert_list = alerts.get("alerts", {}).get("alert", [])

        flattened_data = {
            "name": location_data.get("name"),
            "region": location_data.get("region"),
            "country": location_data.get("country"),
            "lat": location_data.get("lat"),
            "lon": location_data.get("lon"),
            "localtime": location_data.get("localtime"),

            "temp_c": current.get("temp_c"),
            "is_day": current.get("is_day"),

            "condition_text": condition.get("text"),
            "condition_icon": condition.get("icon"),

            "wind_kph": current.get("wind_kph"),
            "wind_degree": current.get("wind_degree"),

            "air_quality": {
                "co": air_quality.get("co"),
                "no2": air_quality.get("no2"),
                "o3": air_quality.get("o3"),
                "so2": air_quality.get("so2"),
                "pm2_5": air_quality.get("pm2_5"),
                "pm10": air_quality.get("pm10"),
                "us_epa_index": air_quality.get("us-epa-index"),
                "gb_defra_index": air_quality.get("gb-defra-index")
            },

            "alerts": [
                {
                    "headline": alert.get("headline"),
                    "severity": alert.get("severity"),
                    "description": alert.get("desc"),
                    "instruction": alert.get("instruction")
                }
                for alert in alert_list
            ],

            "forecast": [
                {
                    "date": day.get("date"),
                    "maxtemp_c": day.get("day", {}).get("maxtemp_c"),
                    "mintemp_c": day.get("day", {}).get("mintemp_c"),
                    "condition": day.get("day", {}).get("condition", {}).get("text")
                }
                for day in forecast_days
            ]
        }

        return flattened_data
    
    def get_secret_from_keyvault(vault_url, secret_name):
        # Step 1: Authenticate using Managed Identity / Default Credential
        credential = DefaultAzureCredential()

        # Step 2: Create Secret Client
        secret_client = SecretClient(vault_url=vault_url, credential=credential)

        # Step 3: Fetch Secret
        retrieved_secret = secret_client.get_secret(secret_name)

        return retrieved_secret.value


    # -------------------------------
    # Main Function
    # -------------------------------
    def fetch_weather_data():
        base_url = "http://api.weatherapi.com/v1"
        location = "Chennai"
                
        # Config
        VAULT_URL = "https://kv-weather-streaming.vault.azure.net/"
        API_KEY_SECRET_NAME = "apikey"

        # Fetch API key
        weather_api_key = get_secret_from_keyvault(VAULT_URL, API_KEY_SECRET_NAME)


        current_weather = get_current_weather(base_url, api_key, location)
        forecast_weather = get_forecast_weather(base_url, api_key, location, 3)
        alerts = get_alerts(base_url, api_key, location)

        merged_data = flatten_data(current_weather, forecast_weather, alerts)

        print(json.dumps(merged_data, indent=3))

        # Sending Event Data
        send_event(merged_data)
        
    # Run
    fetch_weather_data()