import datetime
import os
from generate_forecast import generate_forecast
from generate_video_v2 import create_video  # ✅ corrected import

def select_tone():
    tones = {
        "1": "pessimistic",
        "2": "cautious",
        "3": "neutral",
        "4": "optimistic"
    }
    print("Select a tone:")
    for key, value in tones.items():
        print(f"{key}. {value}")
    choice = input("Enter number: ")
    return tones.get(choice, "neutral")

def main():
    tone = select_tone()
    print("[*] Generating forecast...")
    forecast = generate_forecast(tone)
    print("[+] Forecast generated.\n")

    # Save forecast
    today = datetime.date.today().isoformat()
    filename = f"forecasts/{today}_{tone}.txt"
    os.makedirs("forecasts", exist_ok=True)

    with open(filename, "w") as f:
        f.write(forecast)
    with open("latest_forecast.txt", "w") as f:
        f.write(forecast)

    print(f"[✓] Forecast saved to '{filename}' and 'latest_forecast.txt'")

    # Auto-generate video
    print("[*] Generating video...")
    try:
        create_video()  # ✅ call the correct function
    except Exception as e:
        print("[!] Video generation failed:")
        print(e)

# ✅ New: Flask-compatible function
def run_forecast(tone):
    print(f"[*] Running web forecast generation with tone: {tone}")
    forecast = generate_forecast(tone)

    today = datetime.date.today().isoformat()
    filename = f"forecasts/{today}_{tone}.txt"
    os.makedirs("forecasts", exist_ok=True)

    with open(filename, "w") as f:
        f.write(forecast)
    with open("latest_forecast.txt", "w") as f:
        f.write(forecast)

    print(f"[✓] Forecast saved to '{filename}' and 'latest_forecast.txt'")

    try:
        create_video()
    except Exception as e:
        print("[!] Video generation failed:")
        print(e)
