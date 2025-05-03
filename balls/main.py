import time
import cv2
import numpy as np
import json
import os
import random
from collections import defaultdict

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, 300)

# cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)

def get_color(image):
    x, y, w, h = cv2.selectROI("Color selection", image)
    x, y, w, h = int(x), int(y), int(w), int(h)
    roi = image[y:y+h, x:x+w]
    color = (np.median(roi[:, :, 0]),
             np.median(roi[:, :, 1]),
             np.median(roi[:, :, 2]))
    cv2.destroyWindow("Color selection")
    return color


def get_ball(image, color):
    lower = (np.max(color[0]-5, 0), color[1]*0.8, color[2]*0.8)
    upper = (color[0]+5, 255, 255)
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        return True, (int(x), int(y), int(radius), mask)
    return False, (-1, -1, -1, np.array([]))

path = "settings.json"
if os.path.exists(path):
    base_colors = json.load(open(path, 'r'))
else:
    base_colors = {}

game_started = False
guess_colors = []

while capture.isOpened():
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break
    if key in ('1', '2', '3', '4'):
        color = get_color(hsv)
        base_colors[key] = color

    c1 = 0
    for key in base_colors:
        retr, (x, y, radius, mask) = get_ball(hsv, base_colors[key])
        if retr:
            c1 += 1
            # cv2.imshow("Mask", mask)
            cv2.circle(frame, (x, y), radius, (255, 255, 255), 2)
    # print(f'{c1=}')
    
    if len(base_colors) == 4:
        if not game_started:
            guess_colors = list(base_colors)
            random.shuffle(guess_colors)
            game_started = True
            print(guess_colors)
    if game_started:
        balls_coords = defaultdict(lambda: 0)

        c2 = 0
        for key in base_colors:
            retr, (x, y, radius, mask) = get_ball(hsv, base_colors[key])
            if retr:
                c2 += 1
                balls_coords[key] = (x, y)
        # result = sorted(list(balls_coords), key=lambda x: balls_coords[x])
        result = sorted(list(balls_coords), key=lambda k: (balls_coords[k][1], -balls_coords[k][0]))
        print(f'{result=}')
        cv2.putText(frame, f'Result = {result == guess_colors}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))

    cv2.putText(frame, f'Game started = {game_started}', (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
    cv2.imshow("Camera", frame)

capture.release()
cv2.destroyAllWindows()

json.dump(base_colors, open(path, 'w'))