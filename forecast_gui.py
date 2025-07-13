import tkinter as tk
from tkinter import messagebox
from news_scraper import fetch_headlines
from predictor import run_forecast

def run_forecast_for(timeframe):
    try:
        headlines = fetch_headlines()
        run_forecast(headlines, timeframe)
        messagebox.showinfo("Success", f"{timeframe.capitalize()} forecast generated!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run {timeframe} forecast:\n\n{e}")

# Create GUI window
window = tk.Tk()
window.title("Forecast Generator")
window.geometry("320x300")

label = tk.Label(window, text="Choose Forecast Type:", font=("Arial", 13))
label.pack(pady=10)

btn_daily = tk.Button(window, text="Run Daily Forecast", width=25, font=("Arial", 10), bg="lightblue",
                      command=lambda: run_forecast_for("daily"))
btn_daily.pack(pady=8)

btn_weekly = tk.Button(window, text="Run Weekly Forecast", width=25, font=("Arial", 10), bg="lightgreen",
                       command=lambda: run_forecast_for("weekly"))
btn_weekly.pack(pady=8)

btn_monthly = tk.Button(window, text="Run Monthly Forecast", width=25, font=("Arial", 10), bg="khaki",
                        command=lambda: run_forecast_for("monthly"))
btn_monthly.pack(pady=8)

btn_yearly = tk.Button(window, text="Run Yearly Forecast", width=25, font=("Arial", 10), bg="salmon",
                       command=lambda: run_forecast_for("yearly"))
btn_yearly.pack(pady=8)

# Optional: Exit button
btn_exit = tk.Button(window, text="Exit", width=15, font=("Arial", 10), command=window.destroy)
btn_exit.pack(pady=10)

window.mainloop()
