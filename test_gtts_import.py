from gtts import gTTS

text = "Hello, this is a test of gTTS working properly."
tts = gTTS(text=text, lang='en')
tts.save("test_output.mp3")

print("✔ gTTS worked and saved 'test_output.mp3'")
