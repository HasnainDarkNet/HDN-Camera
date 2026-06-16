# 📸 Webcam Access Simulation – Educational Cybersecurity Project
![how-do-i-allow-camera-access-on-my-browser-1705929422](https://github.com/user-attachments/assets/89bc054a-975f-4ec7-a543-b4806d72148f)

⚠️ **Disclaimer**
This project is created strictly for **educational and cybersecurity awareness purposes only**.
Unauthorized access to any device or camera without proper permission is illegal.
Use this project only in a controlled lab environment and on devices you own.

---

## 🎯 Project Overview

This project demonstrates how a Python script can:

- Access the system webcam using OpenCV
- Capture images at defined intervals
- Send captured images over a network socket
- Run silently in the background using `.pyw`
- Automatically delete temporary files after sending

The purpose is to help students understand how certain malware techniques may operate,
so they can better defend against such threats.

---

## 🛠 Technologies Used

- Python 3
- OpenCV (cv2)
- Socket Programming
- OS Module
- Time Module

---

## ⚙ How It Works (Educational Explanation)

1. The script initializes the system camera.
2. Captures a single frame.
3. Saves it temporarily as `capture.jpg`.
4. Sends the file to a configured server IP and port.
5. Deletes the local file.
6. Waits for the defined interval.
7. Repeats the process.

This demonstrates how data exfiltration techniques may function in real-world attack scenarios.

---

## 🔧 Configuration Section

Inside the script you can configure:

- `KALI_IP` → Listening server IP
- `PORT` → Listening port number
- `INTERVAL_SECONDS` → Time between captures
- `ALSO_SAVE_ON_WINDOWS` → Local debugging option

⚠️ Always test inside a lab environment.

---

## 🧪 Safe Testing Guidelines

✔ Use Virtual Machines  
✔ Use isolated lab networks  
✔ Use only your own authorized systems  
✔ Inform anyone involved in testing  

❌ Never deploy on real user systems  
❌ Never use without permission  

---

## 🛡 Security Awareness – How To Protect Yourself

To prevent unauthorized webcam access:

- Review app permissions regularly
- Use antivirus / endpoint protection
- Enable firewall monitoring
- Keep OS and software updated
- Disable unused webcams
- Physically cover webcam when not in use

---

## 📚 Educational Purpose

This project helps learners understand:

- Webcam API handling in Python
- Background execution techniques
- Network file transmission basics
- Importance of cybersecurity defenses

---

## ⚠ Legal Notice

The author does not promote misuse of this project.
Any illegal activity performed using similar techniques is solely the responsibility of the user.

---

## 👨‍💻 Author

Hasnain Dark Net  
Cybersecurity Research & Awareness
