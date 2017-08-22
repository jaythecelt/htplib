import sched, time
import RPi.GPIO as GPIO
import counterQueue

from HtpLogger import HtpLogger



class HumiditySensorTask():
    UPDATE_PERIOD = 0.994  # In seconds
    PRIORITY = 1
    latchPin = 13
    clkPin = 19
    dataPin = 26
    counterDataDebug = False
    saveStartTime = 0

    def __init__(self):
        self.stop = False
        self._initGPIO()
        
        
        return

    def _initGPIO(self):
        self.startTime = 0
        self.endTime = 1
        # Pin definitions
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.latchPin, GPIO.OUT)
        GPIO.setup(self.clkPin, GPIO.OUT)
        GPIO.setup(self.dataPin, GPIO.IN)
    

    
    def terminate(self):
        HtpLogger.get().info("Terminating HumiditySensorTask")
        self.scheduleRunning = False
        GPIO.cleanup()
        
    
    
    def run(self):
        self.humSched = sched.scheduler(time.time, time.sleep)
        curEvent = self.humSched.enter(self.UPDATE_PERIOD,  self.PRIORITY, self._humDataHandler)

        self.scheduleRunning = True
        # Blocks while the schedule is running
        HtpLogger.get().debug("_humThread: running humSched()")
        self.humSched.run()
        self.scheduleRunning = False
        HtpLogger.get().debug("humThread stopped")

        return        

    '''
    Callback for the scheduler
    '''
    def _humDataHandler(self, a = 'default'):
        #TODO: Add error handling
        
        if not self.scheduleRunning:
            return
        
        # Schedule next callback
        curEvent = self.humSched.enter(self.UPDATE_PERIOD,  self.PRIORITY, self._humDataHandler)
    
        # Latch counter data
        GPIO.output(self.latchPin, GPIO.LOW)
        self.endTime = time.time()
        self.startTime = self.saveStartTime  # get the start time from the last time the handler was called
    
        # Restart the counter and get the start time
        #  i.e. start the new count
        GPIO.output(self.latchPin, GPIO.HIGH)     
        self.saveStartTime = time.time()    
       
        # Shift previous, latched data out from register
        shift = 23
        count = 0
        for i in range(0,24):
            #Drop the clk signal
            GPIO.output(self.clkPin, GPIO.LOW)  # Clock pin to LOW
            k = GPIO.input(self.dataPin) # Read the bit
            count = count | (k << shift)
            shift = shift - 1
            GPIO.output(self.clkPin, GPIO.HIGH)  # Clock pin to HIGH
    
        rawCount = count
        sampleTime = self.endTime - self.startTime  # Actual sample time in seconds
        count = int(float(count)/sampleTime)        # Filter to compensate for variations in the sample period.
    
        diff = rawCount - count
        if (self.counterDataDebug):
            HtpLogger.get().debug("Count = %d  \t sample time = %f \t diff = %d", count, sampleTime, diff)
        
        ctrQ = counterQueue.CounterDataQueue() # get the counter data queue
        ctrQ.put((0,count))
       
        
