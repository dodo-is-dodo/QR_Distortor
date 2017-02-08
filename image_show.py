from qr_maker import make_basic_qr
from distort_qr import distort_image

import tkinter as tk
import cv2
import cv2.aruco as aruco
import PIL
from PIL import Image, ImageTk

width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()

original_qr = make_basic_qr(100, "H")
distorted_qr = distort_image(original_qr, -20, -26)

def show_frame():
    _, frame = cap.read()
    # ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(corners)
    img = original_qr.resize((700, 700), PIL.Image.ANTIALIAS)
    imgtk = PIL.ImageTk.PhotoImage(img)
    # img = Image.fromarray(cv2image)
    # imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

show_frame()
root.mainloop()
