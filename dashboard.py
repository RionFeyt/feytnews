import streamlit as st
import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
from news_scraper import fetch_headlines
from predictor import save_forecast, send_email_forecast

# Load environment and API client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load tone directives and forecast prompts
def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

tone_directives = load_yaml("forecast_prompt_templates/tone_directives.yaml")
prompts = load_yaml("forecast_prompt_templates/prompts.yaml")

# Streamlit UI
st.set_page_config(page_title="Forecast Generator", layout="centered")
st.title("🌐 Geopolitical Forecast Generator")

forecast_type = st.selectbox("Select Forecast Type:", ["daily", "weekly", "monthly", "yearly", "long_term"])
tone = st.select_slider("Select Tone Bias:", options=["pessimistic", "cautious", "neutral", "optimistic"], value="neutral")

st.markdown("""
Adjust the tone to shift the forecast perspective:
- 😔 **Pessimistic** = Worst-case focus
- ⚠️ **Cautious** = Risk-aware
- 😐 **Neutral** = Balanced, analytical
- 😊 **Optimistic** = Focus on hope and positive momentum
""")

generate = st.button("Generate Forecast")

if generate:
    with st.spinner("Fetching headlines and generating forecast..."):
        try:
            headlines = fetch_headlines()
            tone_text = tone_directives[tone]
            prompt_template = prompts[forecast_type]
            joined_headlines = "\n".join(headlines)

            full_prompt = f"{prompt_template}\n\n{tone_text}\n\nHeadlines:\n{joined_headlines}"

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a geopolitical forecasting assistant."},
                    {"role": "user", "content": full_prompt}
                ]
            )

            forecast = response.choices[0].message.content
            save_forecast(forecast, forecast_type)
            send_email_forecast(forecast_type, forecast)

            st.success(f"{forecast_type.capitalize()} forecast complete!")
            st.text_area("Forecast Output:", forecast, height=400)

        except Exception as e:
            st.error(f"Error: {e}")