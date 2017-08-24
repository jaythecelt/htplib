from HtpLogger import HtpLogger
# Setup logger
logPrefix = "humiditySensor_test"
log = HtpLogger(logPrefix, HtpLogger.DEBUG, None)

from HumiditySensorTask import HumiditySensorTask
import counterQueue
import time
import threading


humTask = None

def singleShotMode():
    while True:
        
        log.console("\n------------------\nPress Enter to take a reading for ~ 2 sec...")
        input()
        ctrQ = counterQueue.CounterDataQueue()
        ctrQ.clear()
        
        humTask = HumiditySensorTask()
        t = threading.Thread(target=humTask.run, args=())
        t.start()
        time.sleep(2)
        humTask.terminate()
        
        while not ctrQ.isEmpty():
            countTuple = ctrQ.get()
            log.console("sensor num: {0} \tcount: {1}".format(countTuple[0], countTuple[1] ))


def continuousMode():

    try:
        ctrQ = counterQueue.CounterDataQueue()
        humTask = HumiditySensorTask()
        t = threading.Thread(target=humTask.run, args=())
        t.start()

        while True:        
            while not ctrQ.isEmpty():
                countTuple = ctrQ.get()
                log.console("sensor num: {0} \tcount: {1}".format(countTuple[0], countTuple[1] ))
    except KeyboardInterrupt:
        print ("\nTerminating humidity sensor task")
        humTask.terminate()


def main():

    try:
        continuousMode()
    
    except KeyboardInterrupt:
        log.info("\nExiting")

    
if __name__ == "__main__":
    main()
    