import streamlit as st
from google import genai
import requests


st.title("Weather Description Generator")


city = st.text_input("Enter your city name:")

# API Keys (Make sure to replace with your actual API keys)
openweather_api_key = "API_KEY"  # Your openweather_api_key
genai_api_key = "API_KEY"  # Your Gemini API key

if city:

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=metric"
    weather_response = requests.get(weather_url)

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        weather_main = weather_data['weather'][0]['main']
        temp = weather_data['main']['temp']

        prompt = (
            f"City: {city}\n"
            f"Weather Condition: {weather_main}\n"
            f"Temperature: {temp}°C\n"
            f"Write a friendly and natural description of the weather."
        )

        client = genai.Client(api_key=genai_api_key)

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            description = response.text
            st.success(description)
            st.info(f"Temperature: {temp}°C")

        except Exception as e:
            st.error(f"Error fetching description from Gemini API: {str(e)}")
    else:
        st.error("City not found. Please check your spelling and try again!")
