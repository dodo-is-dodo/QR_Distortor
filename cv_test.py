import cv2
import numpy as np

cap = cv2.VideoCapture(0)
prev = None

ret, frame = cap.read()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)

# circles = cv2.HoughCircles(prev,cv2.HOUGH_GRADIENT,1,20,
#                             param1=50,param2=30,minRadius=0,maxRadius=0)
prev = img
while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.absdiff(img, prev, prev)

    prev = cv2.medianBlur(prev, 5)
    circles = cv2.HoughCircles(prev,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=15,minRadius=0,maxRadius=10000)

    print(circles)
    if np.any(circles):
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(prev,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(prev,(i[0],i[1]),2,(0,0,255),3)

    # cv2.imshow('frame', gray)
    cv2.imshow('gray', gray)
    cv2.imshow('frame', prev)
    prev = img
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
