from qr_maker import make_basic_qr
from distort_qr import distort_image
from tkinter import *
import PIL
from PIL import ImageTk
# import tkinter


original_qr = make_basic_qr(1000, "H")
# distorted_qr = distort_image(original_qr, -77, 50)
distorted_qr = distort_image(original_qr, -20, -26)

class ImageFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack(side=LEFT)
        img = distorted_qr.resize((700, 700), PIL.Image.ANTIALIAS)
        img = PIL.ImageTk.PhotoImage(img)
        self.lbl = Label(self, image=img)
        self.lbl.image = img
        # lbl.place(x=0, y=0)
        self.lbl.pack(fill=BOTH)

    def redraw(self, img):
        img = PIL.ImageTk.PhotoImage(img.resize((700, 700), PIL.Image.ANTIALIAS))
        self.lbl.configure(image = img)
        self.lbl.image = img

class RightFrame(Frame, ):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()


    def initUI(self):

        # self.pack(fill=BOTH, expand=True)
        self.pack(side=RIGHT, fill=X, expand=True)


        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="size", width=6)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        self.text_size = Entry(frame1)
        self.text_size.insert(END, "100")
        self.text_size.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="x distortion", width=12)
        lbl2.pack(side=LEFT, padx=5, pady=5)
        scale_x = Scale(frame2, from_=-100, to=100,
                        command=self.onScale_x, orient=HORIZONTAL)
        scale_x.pack(side=RIGHT, padx=15, fill=X, expand=True)
        self.x_pos = DoubleVar()

        frame3 = Frame(self)
        frame3.pack(fill=BOTH, expand=True)
        lbl3 = Label(frame3, text="y distortion", width=12)
        lbl3.pack(side=LEFT, padx=5, pady=5)
        scale_y = Scale(frame3, from_=-100, to=100,
                        command=self.onScale_y, orient=HORIZONTAL)
        scale_y.pack(side=RIGHT, padx=15, expand=True, fill=X)
        self.y_pos = DoubleVar()

        frame4 = Frame(self)
        frame4.pack(fill=X)#, expand=True)

        make_btn = Button(frame4, text="Make", command=self.onMake)
        make_btn.pack(side=RIGHT, padx=5, pady=5)

        frame5 = Frame(self)
        frame5.pack(fill=X)#, expand=True)

        distorted_btn = Button(frame5, text="Show distorted", command=self.onDistorted)
        distorted_btn.pack(side=RIGHT, padx=5, pady=5)
        original_btn = Button(frame5, text="Show Original", command=self.onOriginal)
        original_btn.pack(side=RIGHT, padx=5, pady=5)

    def onScale_x(self, val):
        v = float(val)
        self.x_pos.set(v)

    def onScale_y(self, val):
        v = float(val)
        self.y_pos.set(v)

    def onMake(self):
        global original_qr, distorted_qr
        size = int(self.text_size.get())
        original_qr = make_basic_qr(size, "H")
        distorted_qr = distort_image(original_qr, int(self.x_pos.get()), int(self.y_pos.get()))
        self.onOriginal()

    def onOriginal(self):
        self.parent.imageframe.redraw(original_qr)

    def onDistorted(self):
        global original_qr, distorted_qr
        distorted_qr = distort_image(original_qr, int(self.x_pos.get()), int(self.y_pos.get()))
        self.parent.imageframe.redraw(distorted_qr)




def main():
    root = Tk()
    root.title('QR_distortor')
    w = 1200
    h = 750

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.imageframe = ImageFrame(root)
    rightFrame = RightFrame(root)

    root.mainloop()

if __name__ == '__main__':
    main()
