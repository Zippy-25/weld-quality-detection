WELD QUALITY DETECTION:
This project detects welding defects using a “YOLOv8 model” running on a “Raspberry Pi 3B+”, which captures an image, runs inference, and sends results to a “Windows system” via sockets. The Windows system then provides real-time “audio feedback” in both “English and Tamil”.

Project Overview
- “Hardware”: Raspberry Pi 3B+
- “Model”: YOLOv8 (`best_100.pt`)
- “Communication”: Socket programming (Raspberry Pi → Windows)
- “Audio Output”: English (`pyttsx3`) & Tamil (`gTTS`)
![Screenshot 2025-03-23 171141](https://github.com/user-attachments/assets/658a8dc1-735a-417e-84cf-ac638af5396b)

1. Raspberry Pi captures an image and runs “YOLOv8” inference.
2. The detected results (e.g., *Good Weld, Bad Weld, Defect*) are “sent to Windows” via sockets.
3. Windows receives the results and “announces them using text-to-speech” in “English & Tamil”.

- “Labels Detected”: 
  - `Good Weld` → “"நல்ல கம்பி இணைப்பு"“
  - `Bad Weld` → “"மோசமான கம்பி இணைப்பு"“
  - `Defect` → “"குற்றம்"“
