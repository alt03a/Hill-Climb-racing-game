import cv2
from pynput.keyboard import Key, Controller
import mediapipe as mp

cam = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
keyboard = Controller()
fingers=[4,8,12,16,20]
while True:
    _, frame = cam.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            landmarks = hand.landmark
            fingers_up = 0
            for finger in fingers[1:]:
                finger_y = landmarks[finger].y
                base_y = landmarks[finger - 2].y
                if finger_y > base_y:
                    fingers_up+=1
            if fingers_up > 3:
                keyboard.release(Key.right)
                keyboard.press(Key.left)
                cv2.putText(frame, "Brake", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                keyboard.release(Key.left)
                keyboard.press(Key.right)
                cv2.putText(frame, "Gas", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    else:
        keyboard.release(Key.left)
        keyboard.release(Key.right)
        cv2.putText(frame, "Release", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Hill Climb Controller", frame)
    cv2.waitKey(1)
