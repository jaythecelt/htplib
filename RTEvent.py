'''

    Class implemented as a Singleton.
    
    
    Methods provided:
    
    Example use:

'''

import json
from HtpLogger import HtpLogger
from RTDataQueue import RTDataQueue



class RTEvent(object):
    instance = None
    
    DI_RISING_EDGE  = 1
    DI_FALLING_EDGE = 2
    
    EVENT_KEY        = "event"
    SENSOR_TYPE_KEY  = "sensorType"
    EVENT_TYPE_KEY   = "eventType"
    LABEL_KEY        = "label"
    FORMULA_TIME_KEY = "formulaTime"
    VALUE_KEY        = "value"

    def __init__(self):
        if not RTEvent.instance:
            RTEvent.instance = RTEvent.__RTEvent()
            
   # Proxy for inner class
    def __getattr__(self, name):
        return getattr(self.instance, name)

    # Inner class for the singleton implementation.
    # Method implementations go here.
    class __RTEvent:
       
        def __init__(self):
            pass
        
        def submit(self, sensorType, label, val, prevVal, eventType, timeMark):
            
            if not self._eventOccured(sensorType, label, val, prevVal, eventType, timeMark):
                return False
            
            eventDict = {}
            eventDict[RTEvent.SENSOR_TYPE_KEY] = sensorType
            eventDict[RTEvent.LABEL_KEY] = label
            eventDict[RTEvent.VALUE_KEY] = val
            eventDict[RTEvent.EVENT_TYPE_KEY] = eventType
            eventDict[RTEvent.FORMULA_TIME_KEY] = timeMark
            
            parentDict = {}
            parentDict[RTEvent.EVENT_KEY] = eventDict
            eventJson = json.dumps(parentDict)
            
            rtQueue = RTDataQueue()
            rtQueue.put(eventJson)
            
            HtpLogger.get().debug("Event detected: {0}".format(eventJson))
            
            return True
        

        def _eventOccured(self, sensorType, label, val, prevVal, eventType, timeMark ):
            if (eventType==RTEvent.DI_RISING_EDGE):
                if ((val==1) and (prevVal==0)):
                    return True
                
            elif (eventType==RTEvent.DI_FALLING_EDGE):
                if ((val==0) and (prevVal==1)):
                    return True
            return False
            
