import webbrowser
import requests
import os
import subprocess
import time
import shutil
import json
import socket

ip_address = '192.168.116.122'
port_number = '8080'

url = f"http://192.168.116.122:8080/photoaf.jpg"
file_name = "photo.jpg"
save_path = os.path.join(os.getcwd(), file_name)

# Download the image
response = requests.get(url)
if response.status_code == 200:
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Image saved as {save_path}")
else:
    print("Failed to download image")

# Wait for 5 seconds
time.sleep(5)

# Close Chromium browser
subprocess.Popen(["pkill", "chromium"])

# Define the path to the YOLO model and environment
yolo_dir = os.path.expanduser("~/yolov8/ultralytics-roboflow/ultralytics")
best_model = os.path.join(yolo_dir, "abhi_best.pt") 

# Ensure the output directory is always the same
output_dir = os.path.join(yolo_dir, "runs/detect/predict2")

# Delete the existing predict2/ directory if it exists
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

# Define the correct YOLOv8 command
command = f"""
source ~/myenv/bin/activate &&
cd {yolo_dir} &&
python3 -c "
import json
from ultralytics import YOLO
model = YOLO('{best_model}')
results = model.predict(source='{save_path}', imgsz=640, project='runs/detect',>
detections = []
for r in results:
    for box in r.boxes:
        label = model.names[int(box.cls)]
        confidence = float(box.conf[0]) * 100
        detections.append({{'label': label, 'confidence': confidence}})
with open('{yolo_dir}/results.json', 'w') as f:
    json.dump(detections, f)
"
"""

process = subprocess.Popen(command, shell=True, executable="/bin/bash")
process.wait()  

# Read the JSON file
json_file = os.path.join(yolo_dir, "results.json")
with open(json_file, "r") as f:
    data = f.read()

# Print the path of the saved image
output_image_path = os.path.join(output_dir, file_name)
print(f"Inference completed. Check the results at: {output_image_path}")

# Socket settings
WINDOWS_IP = "192.168.116.95"  

PORT = 5001

# Send the results to Windows via socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((WINDOWS_IP, PORT))
    s.sendall(data.encode())  # Send JSON data
    s.close()
    print("Results sent successfully to Windows.")
except Exception as e:
    print(f"Failed to send results: {e}")

# Open the predicted image automatically
subprocess.run(["xdg-open", output_image_path])
