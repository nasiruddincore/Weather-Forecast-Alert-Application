import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import os
import json

# Load .env
load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Create folders
os.makedirs("reports", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("data", exist_ok=True)


def fetch_weather(city):

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(BASE_URL, params=params)

        data = response.json()

        if response.status_code != 200:
            print(f"\nAPI Error: {data.get('message')}")
            return None

        return data

    except Exception as e:
        print(f"\nError: {e}")
        return None


def load_sample_data():

    sample_data = {
        "main": {
            "temp": 44,
            "humidity": 90
        },
        "weather": [
            {
                "main": "Rain"
            }
        ],
        "wind": {
            "speed": 18
        }
    }

    return sample_data


def analyze_weather(data):

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["main"]
    wind_speed = data["wind"]["speed"]

    alerts = []

    if temp > 40:
        alerts.append("High Temperature Alert")

    if humidity > 85:
        alerts.append("High Humidity Alert")

    if weather.lower() in ["rain", "thunderstorm"]:
        alerts.append("Rain / Storm Alert")

    if wind_speed > 15:
        alerts.append("Strong Wind Alert")

    return {
        "temperature": temp,
        "humidity": humidity,
        "weather": weather,
        "wind_speed": wind_speed,
        "alerts": alerts
    }


def display_weather(city, analysis):

    print("\n========== WEATHER REPORT ==========")

    print(f"City         : {city}")
    print(f"Temperature  : {analysis['temperature']} °C")
    print(f"Humidity     : {analysis['humidity']} %")
    print(f"Weather      : {analysis['weather']}")
    print(f"Wind Speed   : {analysis['wind_speed']} m/s")

    print("\n========== ALERTS ==========")

    if analysis["alerts"]:

        for alert in analysis["alerts"]:
            print(f"⚠ {alert}")

    else:
        print("No alerts detected.")


def save_report(city, analysis):

    report = {
        "City": city,
        "Temperature": analysis["temperature"],
        "Humidity": analysis["humidity"],
        "Weather": analysis["weather"],
        "Wind Speed": analysis["wind_speed"],
        "Alerts": ", ".join(analysis["alerts"]),
        "Timestamp": datetime.now()
    }

    df = pd.DataFrame([report])

    file_path = f"reports/{city}_weather_report.csv"

    df.to_csv(file_path, index=False)

    print(f"\nReport Saved: {file_path}")


def create_chart(city, analysis):

    labels = ["Temperature", "Humidity", "Wind Speed"]

    values = [
        analysis["temperature"],
        analysis["humidity"],
        analysis["wind_speed"]
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.title(f"Weather Metrics - {city}")

    plt.ylabel("Values")

    chart_path = f"images/{city}_weather_chart.png"

    plt.savefig(chart_path)

    plt.close()

    print(f"Chart Saved: {chart_path}")


def main():

    print("\n===== Weather Forecast & Alert Application =====")

    print(f"\nLoaded API Key: {API_KEY}")

    city = input("\nEnter City Name: ")

    data = fetch_weather(city)

    # Automatic simulation fallback
    if not data:

        print("\nUsing Simulation Mode...")

        data = load_sample_data()

    analysis = analyze_weather(data)

    display_weather(city, analysis)

    save_report(city, analysis)

    create_chart(city, analysis)

    print("\nApplication Finished Successfully.")


if __name__ == "__main__":
    main()