import cv2
import mss
import pyautogui
import numpy as np
import threading
import time
import webbrowser

BASE_SPEED = 6          # юн./кадр
ACC_PER_SEC = 0.001 * 60  # 0.06 юн./с
MAX_SPEED  = 13
PX_PER_UNIT = 70

BASE_DISTANCE = 150 # 466

# def jump_and_duck(duck_time=0.2):
#     pyautogui.press('space')
#     pyautogui.keyDown('down')
#     threading.Timer(duck_time, pyautogui.keyUp, args=('down',)).start()

def screen_capture(start_event):
# def screen_capture():
    start_event.wait()

    start_time = time.perf_counter()
    coef = 1.0

    with mss.mss() as sct:
        # monitor = {"top" : 165, "left" : 681, "width" : 615, "height" : 117}
        monitor = {"top" : 410, "left" : 170, "width" : 1250, "height" : 233}
        cv2.namedWindow("Screen Capture", cv2.WINDOW_NORMAL)

        while True:
            screenshot = sct.grab(monitor) 
            frame = np.array(screenshot)

            elapsed = time.perf_counter() - start_time      # секунды
            speed_units = min(BASE_SPEED + ACC_PER_SEC * elapsed, MAX_SPEED)
            coef = speed_units * PX_PER_UNIT
            jump_threshold = BASE_DISTANCE + coef

            gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
            _, binary = cv2.threshold(gray, 83, 255, cv2.THRESH_BINARY_INV)
            binary = cv2.dilate(binary, np.ones((9, 9)))
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_SIMPLE)

            for i, contour in enumerate(contours):
                (x, y, w, h) = cv2.boundingRect(contour)
                if w*h > 600:
                    if y + h > 178  and 40+w < x+w < jump_threshold:
                        pyautogui.press('space')
                        pyautogui.press('down')

            cv2.imshow("Screen Capture", frame)
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