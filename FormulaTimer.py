'''
    Timer for tracking elapsed time of a formula
    Class implemented as a Singleton.
    
    Note:  From https://docs.python.org/3/library/time.html - 
    "time() returns the most accurate time available"
    
    
    Methods provided:
    start: Start the formula elapsed timer

    getElapsedTime:  Returns the number of ms since the start of the timer
                     as a float

    getElapsedTimeByte: Returns the nummber of ms since the start of the timer
                     as an integer represented as a four byte array, big endian order.
    
    Example use:
        ft = FormulaTimer()
        ft.start()
        time.sleep(2)
        print(ft.getElapsedTime())
        time.sleep(2)
        print(ft.getElapsedTimeBytes())

'''
import time
from HtpLogger import HtpLogger

# TODO Catch exceptions around number formatting and timer overruns
# TODO Possible generate exception when reading time without starting timer


class FormulaTimer(object):
    instance = None

    def __init__(self):
        if not FormulaTimer.instance:
            FormulaTimer.instance = FormulaTimer.__FormulaTimer()
            
   # Proxy for inner class
    def __getattr__(self, name):
        return getattr(self.instance, name)

    # Inner class for the singlton implementation.
    # Method implementations go here.
    class __FormulaTimer:
        startTime = None
       
        def __init__(self):
            self.startTime = None
        
        def start(self):
            HtpLogger.get().info("Started the elapsed time.")
            self.startTime = time.time() * 1000.0
            
        def reset(self):
            HtpLogger.get().info("Reset the elapsed time.")
            self.startTime = time.time() * 1000.0
            
        def stop(self):
            HtpLogger.get().info("Stopped the elapsed time.")
            self.startTime = None
            
        '''
            Returns True if the timer is running, False if stopped or
            never started.
        '''
        def isRunning(self):
            if self.startTime is None:
                return False
            return True
            
        '''
            Returns the elapsed time in ms.  This is the 
            number of ms since the call to start() or 
            reset().
            
            Returns an integer, not floating point.
            
        '''
        def getElapsedTime(self):
            now = time.time()
            if self.startTime==None:
                #self.log.warning("FormulaTimer timer not started.")
                return 0
            now = now * 1000.0  # Convert to ms
            diff = round(now - self.startTime) # round to nearest integer
            return int(diff)
        
        '''
            Returns the elapsed time in seconds.
            Returns the time as a float, in fractional seconds, 
            rounded to 6 significant digits.
        '''
        def getElapsedTimeSec(self):
            now = time.time()
            if self.startTime==None:
                return 0.0
            t = (now * 1000.0) - self.startTime
            t = round(t/1000.0, 6)
            return t 
        
        
        '''
            Returns four byte array in Big Endian order representing the 
            elapsed time in ms.
        '''
        def getElapsedTimeBytes(self):
            t = self.getElapsedTime()
            if t==None:
                t = 0
            fourBytes = int(t).to_bytes(4, byteorder='big')
            return fourBytes


