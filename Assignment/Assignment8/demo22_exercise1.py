# blur_video.py
# Demonstrates 2D spatial filtering

import cv2

cap = cv2.VideoCapture(0)

import numpy as np

print("Switch to video window. Then press 'p' to save image, 'q' to quit")


kernel = np.ones((9, 9)) / 81

kernel = np.ones((31, 31))/(31 * 31)

kernel = np.ones((9,9), np.float32)/81    # alternately, explicitly specify the data type

while True:

    [ok, frame] = cap.read()  # Read one frame



    frame = cv2.filter2D(frame, -1, kernel)
    frame = cv2.Canny(frame, 100, 200)


    cv2.imshow('Live video (edges detected)', frame)

    key = cv2.waitKey(1)


    if key == ord('p'):
        cv2.imwrite('edges_detected.jpg', frame)
        print("save")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
