import qrcode
import csv
import collections
import random, string

version_map = collections.OrderedDict()

with open("./size.csv", 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    index = 0
    for row in reader:
        if index % 4 == 0:
            version = int(row[0])
            version_map[version] = [int(row[4])]
        else:
            version_map[version].append(int(row[3]))
        index += 1

def randomword(length):
   return ''.join(random.choice(string.ascii_letters) for i in range(length))

def qr_search(size, error_correction):
    error_map = {
        "L" : 0,
        "M" : 1,
        "Q" : 2,
        "H" : 3,
    }
    ec = error_map[error_correction.upper()]
    for k, v in version_map.items():
        if v[ec] > size:
            return k

def make_basic_qr(size, error_correction):
    v = qr_search(size, error_correction)
    error_map = {
        "L" : qrcode.constants.ERROR_CORRECT_L,
        "M" : qrcode.constants.ERROR_CORRECT_M,
        "Q" : qrcode.constants.ERROR_CORRECT_Q,
        "H" : qrcode.constants.ERROR_CORRECT_H,
    }
    qr = qrcode.QRCode(
        version = v,
        error_correction = error_map[error_correction.upper()],
        box_size = 10,
        border = 4,
    )
    data = randomword(size)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    img.save("output.png")
    return img

# img = make_basic_qr(1000, 'h')


