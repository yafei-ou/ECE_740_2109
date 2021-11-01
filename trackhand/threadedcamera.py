#!usr/bin/env python3
# __author__ = 3van0
# 2021-6-2

from threading import Thread

class ThreadedCamera:
    def __init__(self, cap):

        self.capture = cap

        self.thread = Thread(target = self.update, args = ())
        self.thread.daemon = True
        self.thread.start()

        self.status = False
        self.frame  = None

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
    
    def isOpened(self):
        return self.status

    def read(self):
        return self.status, self.frame
