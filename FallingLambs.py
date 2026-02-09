import random

import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

# Set Camera max width and height
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Read Assets
lamb_img = cv2.imread('./Images/sheep.png', cv2.IMREAD_UNCHANGED)
lamb_img = cv2.resize(lamb_img, (40, 40))
wolf_img = cv2.imread('./Images/wolf.png', cv2.IMREAD_UNCHANGED)
wolf_img = cv2.resize(wolf_img, (40, 40))

# Previous Time for FPS Counting
pTime = 0
# Bool variable for only spawning one object at respective second
fell = False
# Array for keeping the falling_objects
falling_objects = []
# Game points
points = 0
# Initialize Hand Detector unit
detector = htm.handDetector()

class falling_object():
    def __init__(self, x_coord, y_coord, isLamb: bool):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.isLamb = isLamb


# Global function to overaly the given coordinate on the camera with an image
def overlay_image(background, overlay, x, y):
    h, w = overlay.shape[:2]

    # Calculate boundaries
    y1, y2 = max(0, y), min(background.shape[0], y + h)
    x1, x2 = max(0, x), min(background.shape[1], x + w)

    # Calculate overlay boundaries
    oy1, oy2 = max(0, -y), h - max(0, (y + h) - background.shape[0])
    ox1, ox2 = max(0, -x), w - max(0, (x + w) - background.shape[1])

    if overlay.shape[2] == 4:  # PNG with alpha channel
        alpha = overlay[oy1:oy2, ox1:ox2, 3] / 255.0
        for c in range(3):
            background[y1:y2, x1:x2, c] = (1 - alpha) * background[y1:y2, x1:x2, c] + alpha * overlay[oy1:oy2, ox1:ox2,
                                                                                              c]
    else:  # JPG or PNG without alpha
        background[y1:y2, x1:x2] = overlay[oy1:oy2, ox1:ox2]


while True:
    success, img = cap.read()
    # Flip the image so it's less mind tricking
    img = cv2.flip(img, 1)

    # FPS counter
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

    # Spawn a falling object
    if int(cTime) % 2 == 0 and not fell:
        print("Fall!")
        fell = True
        isLamb = random.randint(0,1)
        falling_objects.append(falling_object(x_coord= random.randint(30, wCam - 30) , y_coord= 0, isLamb= isLamb == 1))
    elif int(cTime) % 2 != 0 and fell:
        fell = False

    if len(falling_objects) != 0:
        for id, object in enumerate(falling_objects):
            if object.y_coord > hCam:
                if object.isLamb:
                    points = -1
                falling_objects.remove(object)
            else:
                falling_objects[id] = falling_object(object.x_coord, object.y_coord + 10, object.isLamb == 1)
                if(object.isLamb):
                    overlay_image(img, lamb_img, int(object.x_coord) - 15, int(object.y_coord) - 15)
                else:
                    overlay_image(img, wolf_img, int(object.x_coord) - 15, int(object.y_coord) - 15)


    img = detector.findHands(img, draw = False)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) != 0:
        thumb = lmList[4]
        index = lmList[8]

        x1,y1 = thumb[1], thumb[2]
        x2,y2 = index[1], index[2]

        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1),(x2,y2), (255,0,255),3)

        if len(falling_objects) != 0:
            for id, object in enumerate(falling_objects):
                if (x2 < object.x_coord < x1 or x1 < object.x_coord < x2 ) and (y1 < object.y_coord < y1 + 15 or y2 < object.y_coord < y2 + 15):
                    falling_objects.remove(object)
                    if object.isLamb:
                        points += 1
                    else:
                        points -= 1

    cv2.putText(img, f'POINTS: {points}', (wCam-170, hCam -30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    if points < 0:
        cv2.putText(img, f'GAME OVER', (wCam - int(wCam/2) - 170, hCam - int(hCam/2)), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 5)


    cv2.imshow("Img", img)
    cv2.waitKey(1)