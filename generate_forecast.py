import openai
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    After each section, provide 2-3 bullet-point predictions specific to that area. Have sections showing assumptions and reasoning for these assumptions.
    At the end of the report, summarize whether sentiment trends toward a positive or negative future using visual cues (e.g., 📈 or 📉).
    Include a final paragraph predicting the next month, and another for the next year.
    Ensure the report is at least 1000 words.
    Format it with HTML tags (like <h4>, <ul>, <li>, <p>) to structure the response.
    """

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
