import marker_read
import gui
from time import sleep
from threading import Thread

def fuck():
    while 1:
        print("FUCK")
        sleep(0.3)

def main():
    ui = Thread(target=gui.main()) 
    ui.start()
    # fucku = Thread(target=fuck)
    # fucku.start()
    marker = Thread(target=marker_read.read_loop())
    marker.start()
    # ui = gui.UI()
    # # marker = marker_read.Marker()
    # ui.start()
    # marker.start()

if __name__ == '__main__':
    main()
