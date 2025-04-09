from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import difflib

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/record", methods=["POST"])
def record_audio():
    # Simulating recording completion (In real implementation, record & save file)
    return jsonify({"message": "Recording Completed"})

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    recognizer = sr.Recognizer()
    
    # Simulating a recorded audio file
    audio_file = "recorded_audio.wav"

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return jsonify({"transcription": text})
    except sr.UnknownValueError:
        return jsonify({"transcription": "Could not understand the audio"})
    except sr.RequestError:
        return jsonify({"transcription": "Error connecting to speech service"})

@app.route("/compare", methods=["POST"])
def compare_texts():
    reference_text = request.form["reference_text"]
    transcription_result = request.form["transcription_result"]

    similarity = difflib.SequenceMatcher(None, reference_text.lower(), transcription_result.lower()).ratio()
    accuracy = round(similarity * 100, 2)

    diff = list(difflib.ndiff(reference_text.split(), transcription_result.split()))
    differences = " ".join([word for word in diff if word.startswith("- ") or word.startswith("+ ")])

    suggestions = "Try to match the pronunciation better" if accuracy < 70 else "Good job!"

    return jsonify({"accuracy": accuracy, "differences": differences, "suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True)
