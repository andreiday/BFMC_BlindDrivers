import io
import time
import datetime
import sys
sys.path.append('.')

import cv2
import multiprocessing
from multiprocessing import Process
from threading import Thread, Event

from src.utils.templates.workerprocess import WorkerProcess
# from src.data.imageprocessing.writethreadlanes import WriteThreadLanes
from src.data.imageprocessing.writethread import WriteThreadFrameProc
# from src.data.imageprocessing.signdetect import SignDetection

class FrameProcessingProcess(WorkerProcess):
    #================================ LANE DETECTION PROCESS =====================================
    def __init__(self, inPs, outPs):
        """Process that:
            -   receives information about the frames from the cameraprocess.
            -   outputs information about the computed steering angle

        Parameters
        ----------
        inPs : list()
            input pipes
        outPs : list()
            output pipes
        daemon : bool, optional
            daemon process flag, by default True
        """
        super(FrameProcessingProcess,self).__init__(inPs, outPs)

    def _init_threads(self):
        '''
        '''
        frameProcTh = WriteThreadFrameProc(self.inPs[0], self.outPs[0])
        self.threads.append(frameProcTh)

    def run(self):
        super(FrameProcessingProcess,self).run()
        
