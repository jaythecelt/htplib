from HtpLogger import HtpLogger
# Setup logger
logPrefix = "humiditySensor_test"
log = HtpLogger(logPrefix, HtpLogger.DEBUG, None)

import humiditySensor
import counterQueue
import time







def main():

    try:
        while True:
            log.console("\n------------------\nPress Enter to take a reading for ~ 2 sec...")
            input()
            ctrQ = counterQueue.CounterDataQueue()
            ctrQ.clear()
            humiditySensor.startHumThread()
            time.sleep(2)
            humiditySensor.stopHumThread()
            
            while not ctrQ.isEmpty():
                countTuple = ctrQ.get()
                log.console("sensor num: {0} \tcount: {1}".format(countTuple[0], countTuple[1] ))

    
    except KeyboardInterrupt:
        log.info("\nExiting")

    finally:
        humiditySensor.cleanup()
    
    
if __name__ == "__main__":
    main()
    