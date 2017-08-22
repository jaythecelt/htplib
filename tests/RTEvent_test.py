'''
    Unit test for the RTEvent class

'''
import threading
import time
import json
from HtpLogger import HtpLogger
from RTEvent import RTEvent
from RTDataQueue import RTDataQueue
from FormulaTimer import FormulaTimer

DIGITAL_INPUT_SENSOR_TYPE = 'DI'

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d





def main():
    log = HtpLogger("RTEvent_test", HtpLogger.DEBUG, HtpLogger.DEBUG)
    testNo = 1
    try:
        rte = RTEvent()
        rtq = RTDataQueue()

        log.info("\n\n== DI Rising Edge tests ==")
#1
        log.info("\nTest: {0}".format(testNo))
        log.info("Obj: Previous value and current value both 1, no rising edge")
        log.info("Exp: No event in RTQueue, and submit returns false.")
        
        res = rte.submit(DIGITAL_INPUT_SENSOR_TYPE, 'DI0', 1, 1, RTEvent.DI_RISING_EDGE, 10)
        assert (res == False), "RTEvent.submit(..) returned True, expected False"
        assert (rtq.isEmpty() == True), "RTQueue is not empty"
        log.info("PASS")

#2    
        testNo += 1
        log.info("\nTest: {0}".format(testNo))
        log.info("Obj: current value = 0, previous value = 1 therefore no rising edge occurred (this is a falling edge).")
        log.info("Exp: No event in RTQueue, and submit returns false.")

        res = rte.submit(DIGITAL_INPUT_SENSOR_TYPE, 'DI0', 0, 1, RTEvent.DI_RISING_EDGE, 10)
        assert (res == False), "RTEvent.submit(..) returned True, expected False"
        assert (rtq.isEmpty() == True), "RTQueue is not empty"
        log.info("PASS")

#3
        testNo += 1
        log.info("\nTest: {0}".format(testNo))
        log.info("Obj: current value = 0, previous value = 0 therefore no rising edge occurred.")
        log.info("Exp: No event in RTQueue, and submit returns false.")
        res = rte.submit(DIGITAL_INPUT_SENSOR_TYPE, 'DI0', 0, 0, RTEvent.DI_RISING_EDGE, 10)
        assert (res == False), "RTEvent.submit(..) returned True, expected False"
        assert (rtq.isEmpty() == True), "RTQueue is not empty"
        log.info("PASS")

#4
        testNo += 1
        log.info("\nTest: {0}".format(testNo))
        log.info("Obj: current value = 1, previous value = 0 therefore rising edge occurred.")
        log.info("Exp: An event in RTQueue, and submit returns True.")
        res = rte.submit(DIGITAL_INPUT_SENSOR_TYPE, 'DI0', 1, 0, RTEvent.DI_RISING_EDGE, 10)
        assert (res == True), "RTEvent.submit(..) returned False"
        assert (rtq.isEmpty() == False), "RTQueue is empty"
        eventStr = rtq.get()

        parentJson = json.loads(eventStr)
        eventJson = json.loads(eventStr, object_hook=JSONObject)
        assert(eventJson.event.sensorType == 'DI'), "Unexpected value"
        assert(eventJson.event.eventType == 1),     "Unexpected value"
        assert(eventJson.event.label == 'DI0'),     "Unexpected value"
        assert(eventJson.event.formulaTime == 10),  "Unexpected value"
        assert(eventJson.event.value == 1),         "Unexpected value"
        log.info("PASS")

#5
        testNo += 1
        log.info("\nTest: {0}".format(testNo))
        log.info("Obj: current value = 0, previous value = 1 therefore falling edge occurred.")
        log.info("Exp: An event in RTQueue, and submit returns True.")
        res = rte.submit(DIGITAL_INPUT_SENSOR_TYPE, 'DI0', 0, 1, RTEvent.DI_FALLING_EDGE, 10)
        assert (res == True), "RTEvent.submit(..) returned False"
        assert (rtq.isEmpty() == False), "RTQueue is empty"
        eventStr = rtq.get()

        parentJson = json.loads(eventStr)
        eventJson = json.loads(eventStr, object_hook=JSONObject)
        assert(eventJson.event.sensorType == 'DI'), "Unexpected value"
        assert(eventJson.event.eventType == 2),     "Unexpected value"
        assert(eventJson.event.label == 'DI0'),     "Unexpected value"
        assert(eventJson.event.formulaTime == 10),  "Unexpected value"
        assert(eventJson.event.value == 0),         "Unexpected value"
        log.info("PASS")
    
    
    
        log.info("\n\n========== All {0} tests PASS ====================\n\n".format(testNo))
    except KeyboardInterrupt:
        HtpLogger.get().info ("Exiting")

    finally:
        pass
    
    
if __name__ == "__main__":
    logPrefix = "RTEvent_test"
    log = HtpLogger(logPrefix, HtpLogger.DEBUG, HtpLogger.DEBUG)
    main()
