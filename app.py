import os
from flask import Flask, request, send_file, render_template_string
from google import genai
from google.genai import types

app = Flask(__name__)

# API Key hum Environment Variable se lenge (Security ke liye)
# Render par hum API_KEY set karenge taaki code mein na likhni pade
API_KEY = os.environ.get("AIzaSyDbC2TPZ02gIz8LHPafcMvir5aL70s1V2g")
client = genai.Client(api_key=API_KEY)

# Ye HTML design hai jo user ko browser mein dikhega
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Gemini AI Assistant</title></head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h2>Gemini 2.0 Flash Voice Assistant</h2>
    <form action="/ask" method="get">
        <input type="text" name="prompt" placeholder="Kuch poochhiye..." style="width: 300px; padding: 10px;" required>
        <button type="submit" style="padding: 10px 20px;">Poochho</button>
    </form>
    <br><br>
    {% if audio_ready %}
        <h3>Jawab:</h3>
        <audio controls autoplay>
            <source src="/get-audio" type="audio/wav">
        </audio>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE, audio_ready=False)

@app.route('/ask')
def ask_gemini():
    prompt = request.args.get('prompt')
    if not prompt:
        return "Please provide a prompt", 400

    # Gemini ko call karna
    config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Aoede")
            )
        )
    )

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config=config
    )

    # Audio file save karna server (Render) par
    audio_bytes = response.candidates[0].content.parts[0].inline_data.data
    with open("response.wav", "wb") as f:
        f.write(audio_bytes)

    # Page reload karna aawaz ke sath
    return render_template_string(HTML_PAGE, audio_ready=True)

@app.route('/get-audio')
def get_audio():
    # Saved audio file browser ko bhejna
    return send_file("response.wav", mimetype="audio/wav")

if __name__ == '__main__':
    # Ye local testing ke liye hai, Render gunicorn use karega
    app.run(host='0.0.0.0', port=5000)
