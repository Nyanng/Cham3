import numpy as np
import cv2

video_capture = cv2.VideoCapture(0)
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
deviation = width * 0.15
right = int(width/2 - deviation)
left = int(width/2 + deviation)


def update_result():
    result = -1

    _, frame = video_capture.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blur = cv2.blur(rgb, (10, 10))
    mask = cv2.inRange(blur, (23, 60, 70), (30, 255, 250))
    opening = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), iterations=3)

    kernel = np.ones((7, 7), np.uint8)
    dilate = cv2.dilate(opening, kernel, iterations=3)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        cv2.drawContours(frame, c, -1, 255, 3)

    if len(cnts) != 0:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'X-AXIS  ' + str(x+w / 2), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 1, cv2.LINE_AA)
        result = x+w / 2

    cv2.putText(frame, 'RIGHT RANGE  0 - ' + str(right), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, 'CENTER RANGE  ' + str(right) + ' - ' + str(left), (10, 80), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, 'LEFT RANGE  ' + str(left) + ' - ' + str(width), (10, 110), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.line(frame, (left, 0), (left, height), (0, 0, 255), 2)
    cv2.line(frame, (right, 0), (right, height), (0, 0, 255), 2)
    cv2.imshow('debg window', frame)

    if(result == -1):
        return '찾을 수 없음', frame
    elif(result <= right):
        cv2.putText(frame, 'RESULT  RIGHT', (10, 140), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 255), 1, cv2.LINE_AA)
        return '오른쪽', frame
    elif(right < result and result < left):
        cv2.putText(frame, 'RESULT  CENTER', (10, 140), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 255), 1, cv2.LINE_AA)
        return '중앙', frame

    else:
        cv2.putText(frame, 'RESULT  LEFT', (10, 140), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 255), 1, cv2.LINE_AA)
        return '왼쪽', frame
