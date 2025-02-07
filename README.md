# Virtual-Hand-Keyboard

# 🖐️ Virtual Hand-Tracking Keyboard using OpenCV & cvzone  

This project implements a **virtual keyboard** using **OpenCV**, **cvzone**, and **MediaPipe** hand tracking.  
It allows users to type using their fingers without touching a physical keyboard, making it an **interactive and AI-driven typing experience**.  

## ✨ Features
- 🖐️ **Hand Tracking** using `cvzone.HandTrackingModule`
- 🎹 **Virtual Keyboard UI** with dynamic button highlights
- 📸 **Real-time Camera Processing** for finger position detection
- 🏎️ **Smooth Typing Experience** with intelligent debounce handling
- 🔥 **Fully Interactive UI** with `OpenCV` and `cvzone`

---

## 📌 Dependencies
Make sure you have the following installed before running the project:

pip install opencv-python numpy cvzone mediapipe

## 🛠️ How It Works
1.The program initializes a camera feed and a hand tracker.

2.A virtual keyboard layout is drawn on the screen.

3.The system detects the index finger position to determine which key is being pressed.

4.If the middle finger is not touching, it registers the key press.

5.The pressed key is displayed as text, simulating real typing.

6.Special keys like Space, Enter, and Delete are handled.

7.The keyboard UI provides visual feedback when a key is pressed.


## 🚀 How to Run
Clone the repository

git clone https://github.com/Syam-1133/Virtual-Hand-Keyboard

Run the script

python keyboard.py





