import datetime
import os
import openai
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

TONE_LABELS = {
    "pessimistic": "🙁 Pessimistic",
    "cautious": "😐 Cautious",
    "neutral": "😶 Neutral",
    "optimistic": "😊 Optimistic"
}

TIMEFRAME_LABELS = {
    "daily": "🕛 Daily Forecast",
    "weekly": "🗓️ Weekly Forecast",
    "monthly": "📅 Monthly Forecast",
    "yearly": "📆 Yearly Forecast"
}

def generate_forecast(tone: str, timeframe: str):
    today = datetime.date.today()
    date_str = today.strftime("%A, %B %d, %Y")

    intro = f"<h2>{TIMEFRAME_LABELS[timeframe]} - {date_str}</h2>"
    intro += f"<h3>Tone: {TONE_LABELS[tone]}</h3>"

    prompt = f"""
    Generate a detailed {timeframe} forecast based on current global trends.
    Use the tone: {tone}.
    The forecast must include clear sections with bold titles for:
    - Economy
    - Job Market
    - Consumer Behavior
    - Technology
    - Environment
    - Geopolitics
    - Health/Public Safety

    For each section:
    - Provide two full paragraphs explaining the current state.
    - Add a paragraph explaining the reasoning for your predictions.
    - Add a paragraph predicting near- and mid-term trends.

    At the end of the report, summarize whether sentiment trends toward a positive or negative future using visual cues (e.g., 📈 or 📉).
    Include a final paragraph predicting the next month, and another for the next year.
    Ensure the report is at least 1000 words.
    Format it with HTML tags (like <h4>, <ul>, <li>, <p>) to structure the response.
    """

    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional economic and global trend analyst."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.7,
        max_tokens=4096
    )

    body = response.choices[0].message.content.strip()
    forecast_html = intro + body
    forecast_text = intro + body + "\n"

    folder_path = os.path.join("forecasts", timeframe)
    os.makedirs(folder_path, exist_ok=True)
    filename = f"{today.isoformat()}_{tone}.txt"
    full_path = os.path.join(folder_path, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(forecast_text)

    with open("latest_forecast.txt", "w", encoding="utf-8") as f:
        f.write(forecast_text)

    return forecast_html, full_path

@app.route("/", methods=["GET", "POST"])
def index():
    forecast_html = None
    file_path = None

    if request.method == "POST":
        tone = request.form.get("tone")
        timeframe = request.form.get("timeframe")

        # Fallbacks to prevent crashes if form doesn't send tone or timeframe
        if tone not in TONE_LABELS:
            tone = "neutral"
        if timeframe not in TIMEFRAME_LABELS:
            timeframe = "daily"

        forecast_html, file_path = generate_forecast(tone, timeframe)

    return render_template("index.html", tones=TONE_LABELS, timeframes=TIMEFRAME_LABELS, forecast_html=forecast_html, file_path=file_path)

@app.route("/download")
def download():
    path = request.args.get("path")
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
