import cv2 
from BackgroundRefresher import BackgroundRefresher, WaitingForDataException
import numpy as np 
import json 

class MotionDetector:
    def __init__(self):
        self.background_difference_threshold = None 
        self.num_of_frames = None 
        self.refresh_hz = None 
        self.accept_new_frame_time = None 

        self.loadJSON()        
        
        self.background_refresher = BackgroundRefresher(
                                        num_of_frames=self.num_of_frames, 
                                        refresh_hz=self.refresh_hz, 
                                        accept_new_frame_time=self.accept_new_frame_time
                                        )

    def detectMotion(self, frame: np.array) -> np.array:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.background_refresher.addFrame(frame)
        try:
            median = self.background_refresher.getMedian()
            difference_with_background = cv2.absdiff(median, frame).astype(np.uint8)
            _, thresholded_frame = cv2.threshold(difference_with_background, self.background_difference_threshold, 255, cv2.THRESH_BINARY)
        
        except WaitingForDataException:
            #this exception occurs at the beginning when quantity of frames already collected to calculate median is insufficient to proceed
            thresholded_frame = np.zeros(shape=(480, 640))

        return thresholded_frame

    
    def loadJSON(self) -> None:
        with open('config.json', 'r') as cfg:
            self.__dict__ = json.load(cfg)