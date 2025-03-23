import socket
import json
import pyttsx3
from gtts import gTTS
import os
import playsound

# Socket settings
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5001

# Initialize pyttsx3 (for English)
engine = pyttsx3.init()

# English-to-Tamil translation dictionary
translation_dict = {
    "Bad Weld": "மோசமான கம்பி இணைப்பு",
    "Good Weld": "நல்ல கம்பி இணைப்பு",
    "Defect": "குற்றம்"
}

# Start the socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Listening for results on port {PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive data
    data = conn.recv(4096).decode()
    conn.close()

    # Process received data
    try:
        detections = json.loads(data)
        english_message = "Detected: "
        tamil_message = "கண்டறியப்பட்டது: "

        for detection in detections:
            label = detection["label"]
            confidence = detection["confidence"]
            
            # Translate label to Tamil if available
            tamil_label = translation_dict.get(label, label)  

            english_message += f"{label} with {confidence:.2f} percent confidence. "
            tamil_message += f"{tamil_label} {confidence:.2f} சதவீத நம்பிக்கையுடன். "

        # Speak in English using pyttsx3
        print(f"Speaking in English: {english_message}")
        engine.say(english_message)
        engine.runAndWait()

        # Speak in Tamil using gTTS
        print(f"Speaking in Tamil: {tamil_message}")
        tts = gTTS(text=tamil_message, lang="ta")
        tts.save("tamil_audio.mp3")

        # Play Tamil audio in Windows
        playsound.playsound("tamil_audio.mp3")

    except json.JSONDecodeError:
        print("Failed to decode received data.")

