import numpy as np 
import cv2 
from MotionDetector import MotionDetector
from time import sleep 
import argparse 

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Program that takes frames from webcam/video as input and displays objects in motion")
        self.parser.add_argument("-path", dest ="path", default=0, metavar="(str)", help="source of video - absolute path. If not specified webcam will be used")
        self.parser.add_argument("-width", dest="width", default=640, type=int, metavar="(int)", help="width of displayed image")
        self.parser.add_argument("-height", dest="height", default=480, type=int,  metavar="(int)", help="height of displayed image")
        self.parser.add_argument("-original", dest="display_original",type=bool, metavar="(bool)", default=True, help="if set to true then original image will also be displayed")
    
    def get_args(self):
        args = self.parser.parse_args()
        return args 

class Main:
    def __init__(self, path: (str or int), width: int, height: int, display_original: bool):
        self.cap = cv2.VideoCapture(path)
        self.width = width 
        self.height = height 
        self.display_original = display_original

        self.detector = MotionDetector()

    def run(self):
        ret, frame = self.cap.read()
        q = None 
        while ret:
            frame = cv2.resize(frame, (self.width, self.height))
            motion_image = self.detector.detectMotion(frame)
            
            cv2.imshow("motion", motion_image)
            if self.display_original:
                cv2.imshow("original", frame)

            #pause the video feature
            key = cv2.waitKey(1)
            if key == ord("p"):
                key = cv2.waitKey(1)
                while not key == ord("p"):
                    key = cv2.waitKey(1)
                    sleep(0.1)
            
            sleep(0.01) 
            ret, frame = self.cap.read()


        self.cap.release()
        cv2.destroyAllWindows() 


if __name__ == "__main__":
    parser = Parser()
    args = parser.get_args()
    main = Main(args.path, args.width, args.height, args.display_original)
    main.run()