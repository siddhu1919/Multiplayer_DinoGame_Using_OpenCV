import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
from directkeys import space_pressed
import time
import numpy as np 

# Create a named window that can be resized
cv2.namedWindow("P L A Y E R 1", cv2.WINDOW_NORMAL)


def gesture_control():
    detector=HandDetector(detectionCon=0.8, maxHands=1)

    space_key_pressed=space_pressed

    time.sleep(2.0)

    current_key_pressed = set()

    video=cv2.VideoCapture(1)

    while True:
        ret, frame = video.read()
        keyPressed = False
        spacePressed = False
        key_count = 0
        key_pressed = 0
        hands, img = detector.findHands(frame)
        # Additional code to make the window circular
        # Create a black image with the same dimensions as the frame
        mask = np.zeros_like(frame)
        # Define the center and radius of the circle
        rows, cols, _ = mask.shape
        center = (int(cols / 2), int(rows / 2))
        radius = min(center[0], center[1], cols - center[0], rows - center[1])
        # Draw a filled white circle in the mask image
        cv2.circle(mask, center, radius, (255, 255, 255), -1)
        # Apply the mask to the frame
        circular_frame = cv2.bitwise_and(frame, mask)
        # cv2.rectangle(img, (0, 480), (300, 425),(50, 50, 255), -2)
        # cv2.rectangle(img, (640, 480), (400, 425),(50, 50, 255), -2)
        if hands:
            lmList=hands[0]
            fingerUp=detector.fingersUp(lmList)
            # print(fingerUp)
            if fingerUp==[0,0,0,0,0]:
                cv2.putText(frame, 'Finger Count: 0', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'Jumping', (440,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                PressKey(space_key_pressed)
                spacePressed=True
                current_key_pressed.add(space_key_pressed)
                key_pressed=space_key_pressed
                keyPressed = True
                key_count=key_count+1
            if fingerUp==[0,1,0,0,0]:
                cv2.putText(frame, 'Finger Count: 1', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            if fingerUp==[0,1,1,0,0]:
                cv2.putText(frame, 'Finger Count: 2', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            if fingerUp==[0,1,1,1,0]:
                cv2.putText(frame, 'Finger Count: 3', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            if fingerUp==[0,1,1,1,1]:
                cv2.putText(frame, 'Finger Count: 4', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            if fingerUp==[1,1,1,1,1]:
                cv2.putText(frame, 'Finger Count: 5', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'Not Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            if not keyPressed and len(current_key_pressed) != 0:
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()
            elif key_count==1 and len(current_key_pressed)==2:    
                for key in current_key_pressed:             
                    if key_pressed!=key:
                        ReleaseKey(key)
                current_key_pressed = set()
                for key in current_key_pressed:
                    ReleaseKey(key)
                current_key_pressed = set()
        cv2.imshow("P L A Y E R 1",frame)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

gesture_control()