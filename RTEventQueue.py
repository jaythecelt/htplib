'''
    Queue for Real Time Events

    Singleton base class for inter-thread communications
'''
from HtpLogger import HtpLogger
import queue
import threading


QUEUE_MAX_SIZE = 10
QUEUE_PUT_TIMEOUT = 0.002
QUEUE_GET_TIMEOUT = 0.002

class RTEventQueue:
    instance = None

    def __init__(self):
        if not RTEventQueue.instance:
            RTEventQueue.instance = RTEventQueue.__RTEventQueue()
        
    # Proxy for inner class
    def __getattr__(self, name):
        return getattr(self.instance, name)


    # Inner class for the singleton implementation.
    # Method implementations go here.
    class __RTEventQueue:
        dqueue = None
        log = None
        
        def __init__(self):
            self.log = HtpLogger.get()
            self.dqueue = queue.Queue(QUEUE_MAX_SIZE)
            self.supressQueueFullWarning = True
            self._value_lock = threading.Lock()
   
        def __str__(self):
            return repr(self)
        
        def put(self, v):
            with self._value_lock:
                try:
                    self.dqueue.put(v, True, QUEUE_PUT_TIMEOUT)
                except (queue.Full):
                    if (not self.supressQueueFullWarning):
                        self.log.warning("RTEvent Queue is full, value dropped: " + str(v))
                    return
                
        def get(self):
            with self._value_lock:
                try:
                    rtn = self.dqueue.get(True, QUEUE_GET_TIMEOUT)
                except (queue.Empty):
                    rtn = None
            return rtn

        def isEmpty(self):
            return self.dqueue.empty()
            
        def clear(self):
            with self._value_lock:
                while not self.dqueue.empty():
                    try:
                        self.dqueue.get(False) # Non blocking
                    except Empty:
                        continue
                    self.dqueue.task_done()

        def setSupressQueueFullWarning(self, supressQueueFullWarning):
            with self._value_lock:
                self.supressQueueFullWarning = supressQueueFullWarning
