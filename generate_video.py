from moviepy.config import change_settings

# Update path to match where your magick.exe is
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16\magick.exe"})

from gtts import gTTS
from moviepy.editor import TextClip, AudioFileClip, CompositeVideoClip, ColorClip
import datetime
import os

def generate_video_from_forecast(forecast_text, output_dir="videos"):
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Generate audio
    tts = gTTS(text=forecast_text, lang="en")
    audio_path = os.path.join(output_dir, "output_audio.mp3")
    tts.save(audio_path)
    print("[✔] Voice saved to 'output_audio.mp3'")

    # Step 2: Create text clip (ImageMagick required here)
    clip = TextClip(forecast_text, fontsize=24, color='white', size=(1280, 720), method='caption')
    clip = clip.set_duration(10)

    # Step 3: Background color
    background = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=10)

    # Step 4: Composite with audio
    final_clip = CompositeVideoClip([background, clip.set_position('center')])
    final_clip = final_clip.set_audio(AudioFileClip(audio_path))

    # Step 5: Save video
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_path = os.path.join(output_dir, f"forecast_{now}.mp4")
    final_clip.write_videofile(video_path, fps=24)
    print(f"[✔] Video saved to {video_path}")
