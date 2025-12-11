🚀 Gemini Vision-Voice Assistant

A multimodal AI prototype that combines speech recognition, webcam image capture, Gemini Flash model, and Windows text-to-speech to create an interactive AI assistant capable of seeing, listening, and speaking.

🧠 Features

✔ Speech-to-Text (STT) – User speaks, and the system converts voice to text using Google STT
✔ Webcam Image Capture – Captures a photo via OpenCV
✔ Gemini Multimodal Processing – Sends both text + image to Google Gemini
✔ AI Explanation + Summary – Long detailed response in terminal & short summary spoken aloud
✔ Windows Text-to-Speech (TTS) – Assistant speaks back using SAPI
✔ Smooth Interaction Loop – Continues until user exits manually

🏗️ Tech Stack

Python 3.8+

SpeechRecognition

OpenCV

Google Gemini API (gemini-flash-latest)

Windows SAPI (VBScript-based TTS)

dotenv for API key management

📂 Project Structure
project/
│── gemini_prototype.py
│── requirements.txt
│── .env
│── captured_image.jpg        # auto-generated
│── README.md

🔧 Installation & Setup
1️⃣ Create and activate a virtual environment
python -m venv venv


Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

2️⃣ Install project dependencies
pip install -r requirements.txt

3️⃣ Add your Gemini API key

Create a .env file (if not existing) and add:

GEMINI_API_KEY=your_api_key_here

4️⃣ Run the prototype
python gemini_prototype.py


On running, the assistant will:
🎙️ Ask you to speak
📸 Capture a photo (3-second countdown)
🤖 Send both inputs to Gemini
📝 Display a detailed response
🔊 Speak a short summary aloud

🔍 How It Works (Internal Flow)

Loads API key from .env

Captures your voice, converts to text (fallback if unclear)

Activates webcam, captures image

Sends text + image to Gemini for multimodal analysis

Receives detailed output — prints to screen

Extracts a short summary

Uses Windows TTS to speak the summary

Repeats until you choose to exit

🖥️ Requirements

Windows OS (for built-in TTS)

Microphone

Webcam

Stable internet

Gemini API Key

🛡️ Notes

Do not share your API key publicly.

TTS uses temporary .vbs files and works only on Windows.

If the microphone or webcam does not work, check Windows permissions.

⭐ Future Improvements (Optional)

Add cross-platform TTS (Mac/Linux support)

Introduce GUI with Tkinter or PyQt

Add conversation memory

Auto-upload images to Gemini as base64 instead of storing files
