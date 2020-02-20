import threading
import numpy as np 
from time import time, sleep
from collections import deque 

class WaitingForDataException(Exception):
    pass 

inv = lambda x: 1 / x if x != 0 else np.inf

class BackgroundRefresher:
    def __init__(self, num_of_frames: int, refresh_hz: float, accept_new_frame_time: float):
        self.min_num_of_frames = num_of_frames
        self.refresh_time = inv(refresh_hz)
        self.accept_new_frame_time = accept_new_frame_time
        self.checkParams()

        self.median_img = None
        self.frames = deque()
        self.new_median_grabbed = True #set to true because we want to calculate first median regardless this fact
        self.last_append_time = time()                 
        
        self.thread = threading.Thread(target=self.medianCalculator, daemon=True)
        self.thread.start()

    def checkParams(self) -> None:
        assert(isinstance(self.min_num_of_frames, int) and self.min_num_of_frames > 0), "invalid number of frames"
        assert(self.refresh_time >= 0), "invalid refresh frequency"
        assert(self.accept_new_frame_time > 0), "invalid accept_new_frame_time"

    def medianCalculator(self) -> None:
        while True:
            #calculates new median after previous one is used
            if self.new_median_grabbed and self.numOfFramesSufficient():
                self.median_img = np.median(self.frames, axis=0).astype(np.uint8)
                self.new_median_grabbed = False

                #if below is true we want to calculate median only once - static background
                if self.refresh_time == np.inf: 
                    break 
                else:
                    sleep(self.refresh_time)
            else:
                sleep(0.05)

    def addFrame(self, frame: np.array) -> None:
        current_time = time()

        #condition below is true right after running script. it means that number of gathered frames is yet insufficient to calculate median, 
        #so we add every new frame regardless passed time to start algorithm ASAP
        if not self.numOfFramesSufficient():
            self.frames.append(frame)
            self.last_append_time = current_time    
        
        elif (current_time - self.last_append_time >= self.accept_new_frame_time):
            self.frames.append(frame)
            self.last_append_time = current_time    
            self.frames.popleft()
            
    def getMedian(self) -> np.array:
        if self.median_img is None:
            raise WaitingForDataException
        else:
            self.new_median_grabbed = True
            return self.median_img 
    

    def numOfFramesSufficient(self) -> bool:
        return (len(self.frames) >= self.min_num_of_frames)