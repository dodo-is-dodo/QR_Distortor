import cv2
import cv2.aruco as aruco
import numpy as np
from threading import Thread

from qr_maker import make_basic_qr
from distort_qr import distort_image, find_coeffs
import gui
from PIL import Image

original_qr = make_basic_qr(100, "H")
# distorted_qr = distort_image(original_qr, -20, -26)

wh = 250
base_pos = [(0, 0), (wh, 0), (wh, wh), (0, wh)]

coeffs = find_coeffs(base_pos, base_pos)
img = original_qr.transform((700, 700), Image.PERSPECTIVE, coeffs,
        Image.BICUBIC)#.save("distorted.png")
img.save("distorted.png")

rate_map = {}
for i in range(40):
    rate_map[i] = 20*i



def read_loop():
    cap = cv2.VideoCapture(0)

    current_rate = 0

    x = 0
    y = 0
    x1, x2, x3, x4 = 0, 0, 0, 0
    y1, y2, y3, y4 = 0, 0, 0, 0

    width = 28.6
    height = 17.9
    depth = 25
    # ui = main_gui.UI()
    # ui.start()
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        #print(frame.shape) #480x640
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()

        #print(parameters)

        '''    detectMarkers(...)
            detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
            mgPoints]]]]) -> corners, ids, rejectedImgPoints
            '''
            #lists of ids and the corners beloning to each id
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        # print(corners)
        if corners:
            # print(corners[0][0])
            corner = corners[0][0]
            print(corner)
            x_left = max(corner[1][0], corner[2][0])
            y_top = max(corner[2][1], corner[3][1])
            cor = []
            # corner[0] = [x_left - corner[1][0], corner[1][1] - y_top]
            # corner[1] = [x_left - corner[0][0], corner[0][1] - y_top]
            # corner[2] = [x_left - corner[3][0], corner[3][1] - y_top]
            # corner[3] = [x_left - corner[2][0], corner[2][1] - y_top]
            cor.append([x_left - corner[2][0], y_top - corner[3][1]])
            cor.append([x_left - corner[3][0], y_top - corner[2][1]])
            cor.append([x_left - corner[0][0], y_top - corner[1][1]])
            cor.append([x_left - corner[1][0], y_top - corner[0][1]])
            x_max = max(cor[1][0] - cor[0][0], cor[2][0] - cor[3][0])
            y_max = max(cor[3][1] - cor[0][1], cor[2][1] - cor[1][1])
            xy_max = max(x_max, y_max)*2
            avg_len = 0
            avg_len += cor[1][0] - cor[0][0]
            avg_len += cor[2][1] - cor[1][1]
            avg_len += cor[2][0] - cor[3][0]
            avg_len += cor[3][1] - cor[0][1]
            avg_len /= 4*20
            print(avg_len)
            if rate_map[int(avg_len)] != current_rate:
                current_rate = rate_map[int(avg_len)]
                print("current rate changed to ", current_rate)
                original_qr = make_basic_qr(current_rate, "H")
            base_pos = [[0,0], [xy_max, 0], [xy_max, xy_max], [0, xy_max]]
            for i in range(4):
                cor[i][0] += 100
                cor[i][1] += 100
            # corner[1] = [corner[1][0] - x_left, y_top - corner[1][1]]
            # corner[2] = [corner[2][0] - x_left, y_top - corner[2][1]]
            # corner[3] = [corner[3][0] - x_left, y_top - corner[3][1]]
            # x, y = corner[0][0], corner[0][1]
            # for i in corner:
            #     i[0], i[1] = x_left - i[0], i[1] - y_top
            # print(x_left, y_top, sep=", ")
            print(cor)
            print()
            coeffs = find_coeffs(base_pos, cor)
            img = original_qr.transform((1000, 1000), Image.PERSPECTIVE, coeffs,
                    Image.BICUBIC)#.save("distorted.png")
            img.save("distorted.png")
            # x1, x2, x3, x4 = corners[0][0][0], corners[1][0][0], corners[2][0][0], corners[3][0][0]
            # y1, y2, y3, y4 = corners[0][0][1], corners[1][0][1], corners[2][0][1], corners[3][0][1]
            # x = sum(i[0][0] for i in corners[0])
            # y = sum(i[0][1] for i in corners[0])
        # real_x = np.interp(x, [0, 1280], [-width/2, width/2])
        # real_y = np.interp(y, [0, 720], [-height/2, height/2])
        # print(real_x, real_y, sep=", ")
        # print(x1, y1, sep=", ")
        # print(x2, y2, sep=", ")
        # print(x3, y3, sep=", ")
        # print(x4, y4, sep=", ")
        # print()
        # print(corners)

        #It's working.
        # my problem was that the cellphone put black all around it. The alrogithm
        # depends very much upon finding rectangular black blobs

        gray = aruco.drawDetectedMarkers(gray, corners)

        #print(rejectedImgPoints)
        # Display the resulting frame
        distorted_qr = cv2.imread("distorted.png", 0)
        cv2.imshow('qr', distorted_qr)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

class Marker(Thread):
    def run(self):
        read_loop()



if __name__ == '__main__':
    read_loop()
