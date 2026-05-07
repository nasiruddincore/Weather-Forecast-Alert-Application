import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from datetime import datetime
import os

# Load .env
load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Create folders
os.makedirs("reports", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("data", exist_ok=True)

st.set_page_config(
    page_title="Weather Forecast & Alert App",
    layout="centered"
)

st.title("🌦 Weather Forecast & Alert Application")

st.write("Get live weather updates and alerts.")

st.write(f"Loaded API Key: {API_KEY}")

city = st.text_input("Enter City Name")


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
            st.error(f"API Error: {data.get('message')}")
            return None

        return data

    except Exception as e:
        st.error(f"Error: {e}")
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

    st.warning("Using Simulation Mode")

    return sample_data


def analyze_weather(data):

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["main"]
    wind_speed = data["wind"]["speed"]

    alerts = []

    if temp > 40:
        alerts.append("⚠ High Temperature Alert")

    if humidity > 85:
        alerts.append("⚠ High Humidity Alert")

    if weather.lower() in ["rain", "thunderstorm"]:
        alerts.append("⚠ Rain / Storm Alert")

    if wind_speed > 15:
        alerts.append("⚠ Strong Wind Alert")

    return {
        "temperature": temp,
        "humidity": humidity,
        "weather": weather,
        "wind_speed": wind_speed,
        "alerts": alerts
    }


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

    return file_path


def create_chart(city, analysis):

    labels = ["Temperature", "Humidity", "Wind Speed"]

    values = [
        analysis["temperature"],
        analysis["humidity"],
        analysis["wind_speed"]
    ]

    plt.figure(figsize=(7, 4))

    plt.bar(labels, values)

    plt.title(f"Weather Metrics - {city}")

    chart_path = f"images/{city}_weather_chart.png"

    plt.savefig(chart_path)

    plt.close()

    return chart_path


if city:

    data = fetch_weather(city)

    # Automatic fallback
    if not data:
        data = load_sample_data()

    analysis = analyze_weather(data)

    st.subheader("📍 Current Weather")

    st.write(f"### City: {city}")
    st.write(f"🌡 Temperature: {analysis['temperature']} °C")
    st.write(f"💧 Humidity: {analysis['humidity']} %")
    st.write(f"☁ Weather: {analysis['weather']}")
    st.write(f"🌬 Wind Speed: {analysis['wind_speed']} m/s")

    st.subheader("🚨 Alerts")

    if analysis["alerts"]:

        for alert in analysis["alerts"]:
            st.warning(alert)

    else:
        st.success("No alerts detected.")

    # Save report
    report_path = save_report(city, analysis)

    st.success(f"Report Saved: {report_path}")

    # Create chart
    chart_path = create_chart(city, analysis)

    st.image(chart_path)

    # Table
    st.subheader("📊 Weather Data Table")

    table_data = pd.DataFrame({
        "Metric": [
            "Temperature",
            "Humidity",
            "Wind Speed"
        ],
        "Value": [
            analysis["temperature"],
            analysis["humidity"],
            analysis["wind_speed"]
        ]
    })

    st.dataframe(table_data)