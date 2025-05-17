import cv2
import mss
import pyautogui
import numpy as np
import threading
import time
import webbrowser

BASE_DISTANCE = 390 # 390

def screen_capture(start_event):
# def screen_capture():
    start_event.wait()

    start_time = time.perf_counter()
    coef = 1.0
    speed = 3.6

    with mss.mss() as sct:
        # monitor = {"top" : 165, "left" : 681, "width" : 615, "height" : 117}
        monitor = {"top" : 410, "left" : 170, "width" : 1250, "height" : 233}
        # monitor = {"top" : 400, "left" : 57, "width" : 865, "height" : 180}
        cv2.namedWindow("Screen Capture", cv2.WINDOW_NORMAL)

        while True:
            screenshot = sct.grab(monitor) 
            frame = np.array(screenshot)

            # curr_time = time.perf_counter()
            # print(f'FPS = {1 / (curr_time - prev_time):.1f}')
            # prev_time = curr_time

            # plt.figure()
            # plt.imshow(frame)
            # plt.show()
            # break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
            _, binary = cv2.threshold(gray, 83, 255, cv2.THRESH_BINARY_INV)
            binary = cv2.dilate(binary, np.ones((9, 9)))
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_SIMPLE)

            timer = time.perf_counter() - start_time
            if timer < 116.7:
                coef = timer * speed
            # print(timer)

            jump_threshold = BASE_DISTANCE + coef
            # print(jump_threshold)
            for i, contour in enumerate(contours):
                (x, y, w, h) = cv2.boundingRect(contour)
                if w*h > 600:
                    if y + h > 178  and 40+w < x+w < jump_threshold:
                        pyautogui.press('space')
                    # if i == 1:
                    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    # else:
                    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # cv2.imshow("Screen Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

def start_game_and_capture():
    start_event = threading.Event()

    t = threading.Thread(target=screen_capture, args=(start_event,), daemon=True)
    t.start()

    webbrowser.open("https://chromedino.com/", new=1)
    time.sleep(2)

    pyautogui.press("space")
    start_event.set()

    t.join()

if __name__ == '__main__':
    start_game_and_capture()
    # screen_capture()