import numpy as np
from PIL import Image

def find_coeffs(pb, pa):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

def find_new_xy(w, h, x_pos, y_pos):
    wide_range = [-100, 100]
    narrow_range = [-0.15, 0.15]
    x_coeff = np.interp(x_pos, wide_range, narrow_range)
    y_coeff = np.interp(y_pos, wide_range, narrow_range)
    # print(x_coeff)
    # print(y_coeff)
    if x_coeff > 0:
        y1, y2 = h * x_coeff, h * (1 - x_coeff)
        y0, y3 = 0, h
    else:
        y0, y3 = h * abs(x_coeff), h * (1 + x_coeff)
        y1, y2 = 0, h
    if y_coeff > 0:
        x0, x1 = w * y_coeff, w * (1 - y_coeff)
        x2, x3 = w, 0
    else:
        x3, x2 = w * abs(y_coeff), w * (1 + y_coeff)
        x0, x1 = 0, w
    return [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]

def find_coeffs_by_map(w, h, x_pos, y_pos):
    pos = [(0, 0), (w, 0), (w, h), (0, h)]
    new_pos = find_new_xy(w, h, x_pos, y_pos)
    return find_coeffs(pos, new_pos)

def distort_image(img, x_pos, y_pos):
    # img = Image.open("output.png")
    # img = img
    width, height = img.size
    # x_slider, y_slider = x_pos, y_pos
    coeffs = find_coeffs_by_map(width, height, x_pos, y_pos)

    img = img.transform((width, height), Image.PERSPECTIVE, coeffs,
            Image.BICUBIC)#.save("distorted.png")
    img.save("distorted.png")
    return img

if __name__ == '__main__':
    print(find_new_xy(100, 100, -50, -26))

# img = Image.open("output.png")
# width, height = img.size
# x_slider, y_slider = -77, 50


# coeffs = find_coeffs_by_map(width, height, x_slider, y_slider)

# img.transform((width, height), Image.PERSPECTIVE, coeffs,
#         Image.BICUBIC).save("distorted.png")








# img = face()
# pic = Image.open("output.png").convert("L")

# coeffs = find_coeffs(
#         [(0, 0), (width, 0), (width, height), (0, height)],
#         [(0, height*0.2), (width, 0), (width, height), (0, height*0.8)])
# img = np.array(pic)

# projective_array = [
#     [1, 0, 10],
#     [0, 1, 20],
#     [0, 0, 1]
# ]

# A = img.shape[0] / 3.0
# w = 2.0 / img.shape[1]

# shift = lambda x: A * np.sin(2.0*np.pi*x * w)



# for i in range(img.shape[0]):
#     # img[:,i] = np.roll(img[:,i], int(shift(i)))
#     img[:,i] = map(shift, img[:,i])

# output = Image.fromarray(img)
# output.save("distorted.jpg")

# # pic.putdata(img)
# # pic.save("distorted.jpg")

# plt.imshow(img, cmap=plt.cm.gray)
# plt.show()
