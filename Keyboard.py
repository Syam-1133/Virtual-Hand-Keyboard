import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Initialize camera and hand detector
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height
detector = HandDetector(detectionCon=0.7, maxHands=1)

# Keyboard layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["Space", "Enter", "Delete"]  # Space bar, Enter button, and Delete button
]

# Variables
text = ""
delay_counter = 0
pressed_key = None  # Stores the last pressed key
button_states = {}  # Tracks the state of each button (pressed or not)

# Button dimensions and spacing
button_width, button_height = 80, 80
spacing = 10
start_x, start_y = 100, 200  # Adjusted start_y to move the keyboard down


def draw_keyboard(img, key_list):
    """Draw the keyboard with a realistic UI."""
    global button_states

    # Draw a background for the keyboard
    cv2.rectangle(img, (start_x - spacing, start_y - spacing),
                  (start_x + 10 * (button_width + spacing), start_y + 4 * (button_height + spacing)),
                  (50, 50, 50), cv2.FILLED)

    for y, row in enumerate(key_list):
        for x, key in enumerate(row):
            if key == "Space":  # Special case for space bar
                x1 = start_x + 2 * (button_width + spacing)  # Center the space bar
                y1 = start_y + y * (button_height + spacing)
                x2 = x1 + 6 * (button_width + spacing)  # Make space bar wider
                y2 = y1 + button_height
            elif key == "Enter":  # Special case for Enter button
                x1 = start_x + 8 * (button_width + spacing)  # Place Enter button at the end
                y1 = start_y + y * (button_height + spacing)
                x2 = x1 + 2 * (button_width + spacing)  # Make Enter button wider
                y2 = y1 + button_height
            elif key == "Delete":  # Special case for Delete button
                x1 = start_x + 0 * (button_width + spacing)  # Place Delete button at the start
                y1 = start_y + y * (button_height + spacing)
                x2 = x1 + 2 * (button_width + spacing)  # Make Delete button wider
                y2 = y1 + button_height
            else:
                x1 = start_x + x * (button_width + spacing)
                y1 = start_y + y * (button_height + spacing)
                x2 = x1 + button_width
                y2 = y1 + button_height

            # Button color: Default gray, pressed yellow
            color = (80, 80, 80) if key != pressed_key else (0, 255, 255)

            # Draw rounded buttons with shadows
            cv2.rectangle(img, (x1, y1), (x2, y2), (40, 40, 40), -1, cv2.LINE_AA)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 5, cv2.LINE_AA)

            # Draw button text (white color, larger font)
            if key == "Space":
                cv2.putText(img, key, (x1 + 50, y1 + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
            elif key == "Enter":
                cv2.putText(img, key, (x1 + 10, y1 + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
            elif key == "Delete":
                cv2.putText(img, key, (x1 + 10, y1 + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
            else:
                cv2.putText(img, key, (x1 + 25, y1 + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

            # Store button coordinates for interaction
            button_states[key] = (x1, y1, x2, y2)
    return img


def check_key_press(pos, key_list):
    """Check if the finger is pressing a key."""
    for y, row in enumerate(key_list):
        for x, key in enumerate(row):
            x1, y1, x2, y2 = button_states[key]
            if x1 < pos[0] < x2 and y1 < pos[1] < y2:
                return key
    return None


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip for mirror effect
    hands, img = detector.findHands(img, flipType=False)

    # Draw keyboard
    img = draw_keyboard(img, keys)

    # Display typed text (with increased height and width)
    display_width = 10 * (button_width + spacing)  # Match keyboard width
    cv2.rectangle(img, (start_x, 50), (start_x + display_width, 150), (50, 50, 50), cv2.FILLED)  # Wider display area
    cv2.putText(img, text, (start_x + 10, 120), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)  # Larger text

    if hands:
        # Get the position of the index finger
        lmList = hands[0]['lmList']
        index_finger = lmList[8][:2]  # (x, y) of index finger
        middle_finger = lmList[12][:2]  # (x, y) of middle finger

        # Calculate distance between index and middle fingers
        length, _, img = detector.findDistance(index_finger, middle_finger, img)

        # Ensure only one finger is pressing
        if length > 50:
            key = check_key_press(index_finger, keys)

            if key and delay_counter == 0:
                pressed_key = key  # Store pressed key for visual feedback
                if key == "Space":
                    text += " "  # Add a space to the text
                elif key == "Enter":
                    text += "\n"  # Add a newline to the text
                elif key == "Delete":
                    text = text[:-1]  # Remove the last character
                else:
                    text += key  # Append the key to the text
                delay_counter = 1  # Add delay to prevent multiple presses

    # Delay counter to reset pressed key
    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10:  # Reset after 10 frames
            delay_counter = 0
            pressed_key = None  # Reset the pressed key

    # Show the image
    cv2.imshow("Virtual Keyboard", img)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()