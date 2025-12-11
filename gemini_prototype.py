import cv2
import speech_recognition as sr
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import subprocess
import tempfile

# Load environment variables
load_dotenv()

print("🚀 Initializing Gemini AI Prototype...")

# Setup Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    GEMINI_API_KEY = input("Enter your Gemini API key: ")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

def speak(text):
    """FIXED: Use Windows VBScript instead of PowerShell"""
    print(f"🔊 SPEAKING: {text}")
    
    # Clean text - KEEP IT SHORT!
    clean_text = text.replace('**', '').replace('*', '').replace('`', '').replace('"', "'")
    
    # MAX 80 CHARACTERS - SHORT TEXT WON'T TIMEOUT!
    if len(clean_text) > 80:
        clean_text = clean_text[:77] + "..."
    
    # Use VBScript (MORE RELIABLE than PowerShell)
    try:
        # Create VBS script
        vbscript = f'''
        Set speaker = CreateObject("SAPI.SpVoice")
        speaker.Speak "{clean_text}"
        '''
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.vbs', mode='w') as f:
            f.write(vbscript)
            vbs_file = f.name
        
        # Run VBScript
        result = subprocess.run(
            ['cscript', '//Nologo', vbs_file],
            capture_output=True,
            text=True,
            timeout=45 # 5 second timeout
        )
        
        # Clean up temp file
        try:
            os.unlink(vbs_file)
        except:
            pass
            
    except subprocess.TimeoutExpired:
        print(f"⚠️ TTS timed out for: {clean_text[:50]}...")
    except Exception as e:
        print(f"⚠️ TTS Error: {str(e)[:50]}")

def capture_image():
    """Capture single image from webcam"""
    print("📸 Looking for camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Camera not found!")
        return None
    
    print("✅ Camera found! Smile for 3 seconds...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        cv2.imwrite('captured_image.jpg', frame)
        print("✅ Image saved")
        return 'captured_image.jpg'
    return None

def record_voice():
    """Record voice and convert to text"""
    recognizer = sr.Recognizer()
    
    print("🎤 Speak now (10 seconds)...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("🔄 Processing speech...")
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("⏰ No speech detected.")
            return "What do you see in this image?"
        except sr.UnknownValueError:
            print("❓ Could not understand audio.")
            return "What do you see in this image?"
        except Exception as e:
            print(f"❌ Error: {e}")
            return "What do you see?"

def get_spoken_response(full_response):
    """Extract ONLY the 'Subject' or 'The Subject' part to speak"""
    
    # Split the response into lines
    lines = full_response.split('\n')
    
    # Look for lines containing 'Subject' or 'The Subject'
    subject_lines = []
    
    for line in lines:
        line = line.strip()
        # Look for subject-related lines
        if ('subject:' in line.lower() or 'the subject:' in line.lower() or 
            'subject -' in line.lower() or '* subject' in line.lower()):
            
            # Clean the line
            clean_line = line.replace('**', '').replace('*', '').replace('`', '')
            clean_line = clean_line.replace('Subject:', '').replace('subject:', '')
            clean_line = clean_line.replace('The Subject:', '').replace('the subject:', '')
            clean_line = clean_line.strip(' -*•')
            
            if clean_line:  # If we have content after cleaning
                subject_lines.append(clean_line)
        
        # Also catch bullet points about the subject
        elif line.startswith('*') and any(word in line.lower() for word in ['person', 'woman', 'man', 'looking', 'face']):
            clean_line = line.replace('*', '').strip()
            subject_lines.append(clean_line)
    
    # If we found subject lines, combine them
    if subject_lines:
        # Take up to 2 subject lines
        subject_text = '. '.join(subject_lines[:2])
        
        # Make it conversational
        if not subject_text.lower().startswith(('i see', 'i can see', 'there is')):
            subject_text = 'I see ' + subject_text[0].lower() + subject_text[1:]
        
        # Ensure it ends with period
        if not subject_text.endswith('.'):
            subject_text = subject_text + '.'
        
        # Keep it reasonable length
        if len(subject_text) > 100:
            subject_text = subject_text[:97] + '...'
        
        return subject_text
    
    # If no subject found, look for person description in the text
    response_lower = full_response.lower()
    if any(word in response_lower for word in ['person', 'woman', 'man', 'girl', 'boy']):
        # Find the sentence describing the person
        sentences = full_response.split('. ')
        for sent in sentences:
            sent_lower = sent.lower()
            if any(word in sent_lower for word in ['person', 'woman', 'man', 'girl', 'boy']):
                clean_sent = sent.replace('**', '').replace('*', '').replace('`', '')
                if not clean_sent.lower().startswith('i '):
                    clean_sent = 'I see ' + clean_sent[0].lower() + clean_sent[1:]
                if len(clean_sent) > 100:
                    clean_sent = clean_sent[:97] + '...'
                if not clean_sent.endswith('.'):
                    clean_sent = clean_sent + '.'
                return clean_sent
    
    # Fallback
    return "I can see the image."
def main():
    # Test speech FIRST with SHORT text
    print("🔊 Testing audio...")
    speak("Testing Gemini AI Prototype's audio...")
    print("✅ Audio test complete.\n")
    
    speak("Hello. Let's begin.")
    
    while True:
        print("\n" + "="*50)
        print("1️⃣ VOICE INPUT")
        user_text = record_voice()
        
        print("\n2️⃣ CAMERA CAPTURE")
        image_path = capture_image()
        
        print("\n3️⃣ SENDING TO GEMINI...")
        
        try:
            if image_path:
                import PIL.Image
                img = PIL.Image.open(image_path)
                
                # Ask Gemini
                response = model.generate_content([user_text, img])
                gemini_response = response.text
            else:
                response = model.generate_content(user_text)
                gemini_response = response.text
            
            print("\n4️⃣ FULL GEMINI RESPONSE (printed in terminal):")
            print("="*50)
            print(gemini_response)
            print("="*50)
            
            # Get BRIEF response to speak (NOT the whole thing!)
            spoken_text = get_spoken_response(gemini_response)
            print(f"\n🎯 BRIEF VERSION (will speak this): {spoken_text}")
            
            print("\n5️⃣ SPEAKING NOW...")
            speak(spoken_text)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            speak("Sorry error")
        
        print("\n" + "="*50)
        choice = input("\nContinue? (y/n): ").lower()
        if choice != 'y':
            speak("Goodbye")
            break

if __name__ == "__main__":
    main()
