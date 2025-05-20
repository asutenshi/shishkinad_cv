import cv2
import numpy as np
import matplotlib.pyplot as plt

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, 300)

glasses = cv2.imread('deal-with-it.png') # если я правильно понял, то у исходной пнг не прозрачный фон :(

face_cascade = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade-eye.xml")

while capture.isOpened():
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=15)

    real_eyes = []

    for x, y, w, h in eyes[:2]:
        real_eyes.append((x, y, w, h))
    
    if len(real_eyes) == 2:
        x1, y1, w1, h1 = real_eyes[0]
        x2, y2, w2, h2 = real_eyes[1]

        combined_x = min(x1, x2)
        combined_y = min(y1, y2)

        combined_right_x = max(x1 + w1, x2 + w2)
        combined_bottom_y = max(y1 + h1, y2 + h2)

        combined_w = combined_right_x - combined_x
        combined_h = combined_bottom_y - combined_y

        coef = combined_w / glasses.shape[1]
        glasses_resized = cv2.resize(glasses, (int(glasses.shape[1]*coef), int(glasses.shape[0]*coef)))
        offset = int(glasses_resized.shape[0] * 0.25)
        combined_y += offset
        mask = cv2.inRange(glasses_resized, np.array([1, 1, 1]), np.array([255, 255, 255]))
        roi = frame[combined_y:combined_y + glasses_resized.shape[0], combined_x:combined_x + glasses_resized.shape[1]]
        bg = cv2.bitwise_and(roi, roi, mask=mask)
        fg = cv2.bitwise_and(glasses_resized, glasses_resized, mask=cv2.bitwise_not(mask))
        combined = cv2.add(bg, fg)

        frame[combined_y:combined_y + combined.shape[0], combined_x:combined_x + combined.shape[1]] = combined

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break

    cv2.imshow("Camera", frame)
    real_eyes.clear()

capture.release()
cv2.destroyAllWindows()