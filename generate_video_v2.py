from gtts import gTTS
from moviepy.editor import (
    TextClip,
    AudioFileClip,
    CompositeVideoClip,
    ColorClip,
    concatenate_videoclips
)
import os
from datetime import datetime
from PIL import Image

# Patch for Pillow compatibility
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# Config
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
FONT_SIZE = 48
FONT_COLOR = 'white'
BACKGROUND_COLOR = (30, 60, 40)  # Earth-tone green
FONT = "Arial-Bold"
DURATION_PER_LINE = 4  # seconds

def load_forecast():
    with open("latest_forecast.txt", "r") as file:
        return file.read().strip()

def generate_voiceover(text, output_path):
    tts = gTTS(text)
    tts.save(output_path)
    print("[v] Voice saved to", output_path)

def generate_text_clips(text, duration_per_line, total_duration):
    lines = [line.strip() for line in text.split('. ') if line.strip()]
    print(f"[i] Parsed {len(lines)} subtitle lines.")

    clips = []
    for i, line in enumerate(lines):
        try:
            print(f"[i] Processing line: {line}")
            clip = TextClip(
                line,
                fontsize=FONT_SIZE,
                color=FONT_COLOR,
                font=FONT,
                size=(VIDEO_WIDTH - 100, None),
                method='caption'
            ).set_duration(duration_per_line).set_position(("center", "bottom"))
            clips.append(clip)
        except Exception as e:
            print(f"[!] Failed to render subtitle: {line}")
            print("Error:", e)

    # Fill remaining time with a blank screen if needed
    subtitle_duration = sum(clip.duration for clip in clips)
    if subtitle_duration < total_duration:
        gap = total_duration - subtitle_duration
        filler = TextClip(" ", fontsize=1, size=(VIDEO_WIDTH, 1), method="caption") \
            .set_duration(gap)
        clips.append(filler)

    return clips

def create_video():
    forecast_text = load_forecast()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    audio_path = "output_audio.mp3"
    video_path = f"static/videos/forecast_{timestamp}.mp4"
    os.makedirs("static/videos", exist_ok=True)

    # Generate voice
    generate_voiceover(forecast_text, audio_path)
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration

    # Background
    background = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=BACKGROUND_COLOR).set_duration(audio_duration)

    # Subtitles
    text_clips = generate_text_clips(forecast_text, DURATION_PER_LINE, audio_duration)
    if not text_clips:
        print("[!] No subtitle clips were created. Aborting video render.")
        return

    subtitle_track = concatenate_videoclips(text_clips).set_duration(audio_duration)

    # Intro title
    title_clip = TextClip("Feyt NEWS", fontsize=72, color='white', font=FONT).set_duration(3).set_position("center")
    intro = CompositeVideoClip([background.set_duration(3), title_clip])

    # Body with subtitles & audio
    body = CompositeVideoClip([background, subtitle_track.set_audio(audio_clip)])

    # Final video
    final = concatenate_videoclips([intro, body], method="compose")
    final.write_videofile(video_path, fps=24, codec="libx264")
    print("[v] Video saved to", video_path)

if __name__ == "__main__":
    create_video()
