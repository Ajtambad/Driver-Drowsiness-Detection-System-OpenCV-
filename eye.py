import cv2
import numpy as np
import dlib
from math import hypot
import winsound
import time

video = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("E:\\Amogh\\MiniProject\\shape_predictor_68_face_landmarks.dat")


font = cv2.FONT_HERSHEY_SIMPLEX
flag = 0
mouth_flag = 0
flag_check = 500
mouth_flag_check = 800
count = 0

def horizontal(m,n):
    xl1 = landmark.part(m).x
    yl1 = landmark.part(m).y
    xl2 = landmark.part(n).x
    yl2 = landmark.part(n).y

    cv2.line(frame, (xl1,yl1), (xl2,yl2), (0,0,255), 1)
    return(hypot((xl2 - xl1), (yl2 - yl1)))

def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


while True:
    image, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        landmark = predictor(gray, face)
        for i in range(37,47):
            x = landmark.part(i).x
            y = landmark.part(i).y
            cv2.circle(frame, (x,y), 1, (255,0,0), -1)

        for j in range(48, 68):
            xm = landmark.part(j).x
            ym = landmark.part(j).y
            cv2.circle(frame, (xm , ym), 1, (0,255,0), -1)

            right_horizontal = horizontal(36,39)
            left_horizontal = horizontal(42,45)

            center_top_right = midpoint(landmark.part(37), landmark.part(38))
            center_bottom_right= midpoint(landmark.part(40), landmark.part(41))

            right_vertical = hypot((center_top_right[0] - center_bottom_right[0]), (center_top_right[1] - center_bottom_right[1]))


            cv2.line(frame, center_top_right, center_bottom_right, (0,0,255), 1)

            center_top_left = midpoint(landmark.part(43), landmark.part(44))
            center_bottom_left = midpoint(landmark.part(46), landmark.part(47))

            left_vertical = hypot((center_top_left[0] - center_bottom_left[0]), (center_top_left[1] - center_bottom_left[1]))

            cv2.line(frame, center_top_left, center_bottom_left, (0,0,255), 1)

            ratio_right = right_horizontal/right_vertical
            ratio_left = left_horizontal/left_vertical
            blinking_ratio = (ratio_left + ratio_right)/2

            if blinking_ratio > 5.7:
                #cv2.putText(frame, "BLINKING", (50, 150), font, 4, (0,0,255))
                flag += 1
                #print(flag)
                if flag >= flag_check:
                    cv2.putText(frame, "SLEEPING", (50, 150), font, 4, (0,0,255))
                    winsound.Beep(4500, 1000)
                    flag = 0
            else:
                flag = 0

            mouth_horizontal_distance = hypot(landmark.part(48).x - landmark.part(54).x, landmark.part(48).y - landmark.part(54).y)
            mouth_vertical_distance = hypot(landmark.part(51).x - landmark.part(66).x, landmark.part(51).y - landmark.part(66).y)
            mouth_ratio = mouth_horizontal_distance/mouth_vertical_distance

            if(mouth_ratio<2):
                mouth_flag += 1
                print(mouth_flag)
                if mouth_flag >= mouth_flag_check:
                    cv2.putText(frame, "Yawning", (50, 150), font, 4, (0,0,255))
                    winsound.Beep(1500, 1000)
                    mouth_flag = 0
            else:
                mouth_flag = 0
    cv2.imshow("Eye", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
