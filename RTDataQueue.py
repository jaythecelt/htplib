'''
    Data Queue

    Singleton base class for inter-thread communications
'''
from HtpLogger import HtpLogger
import queue


QUEUE_MAX_SIZE = 1
QUEUE_PUT_TIMEOUT = 0.002
QUEUE_GET_TIMEOUT = 0.002

class RTDataQueue:
    instance = None
    
    def __init__(self):
        if not RTDataQueue.instance:
            RTDataQueue.instance = RTDataQueue.__RTDataQueue()

    # Proxy for inner class
    def __getattr__(self, name):
        return getattr(self.instance, name)


    # Inner class for the singleton implementation.
    # Method implementations go here.
    class __RTDataQueue:
        dqueue = None
        log = None
        
        def __init__(self):
            self.log = HtpLogger.get()
            self.dqueue = queue.Queue(QUEUE_MAX_SIZE)
   
        def __str__(self):
            return repr(self)
        
        def put(self, v):
            try:
                self.dqueue.put(v, True, QUEUE_PUT_TIMEOUT)
            except (queue.Full):
                self.log.warning("RTData Queue is full, value dropped: " + str(v))
                return
                
        def get(self):
            try:
                rtn = self.dqueue.get(True, QUEUE_GET_TIMEOUT)
            except (queue.Empty):
                rtn = None
            return rtn

        def isEmpty(self):
            return self.dqueue.empty()
            
        def clear(self):
            while not self.dqueue.empty():
                try:
                    self.dqueue.get(False) # Non blocking
                except Empty:
                    continue
                self.dqueue.task_done()
