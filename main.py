import streamlit as st
import google.generativeai as genai
import requests

st.title("Weather Description Generator")

city = st.text_input("Enter your city name:")

openweather_api_key = "55e6a9da875518aecf9380a4e503459c"
genai_api_key = "AIzaSyBNR2g_CSmLe4qIvBZz-ZIR_siVudUNF4U"

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

        try:
            genai.configure(api_key=genai_api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)

            description = response.text
            st.success(description)
            st.info(f"Temperature: {temp}°C")

        except Exception as e:
            st.error(f"Error fetching description from Gemini API: {str(e)}")
    else:
        st.error("City not found. Please check your spelling and try again!")
