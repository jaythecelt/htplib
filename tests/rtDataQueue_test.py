from RTDataQueue import RTDataQueue
import time
import threading



class theThread(threading.Thread):
    def __init__(self, count):
        threading.Thread.__init__(self)
        self.count = count
        
    def run(self):
        q = RTDataQueue()
        while self.count > 0 :
            q.put(self.count)
            self.count = self.count + 1
            time.sleep(.002)
        return
            




rtq = RTDataQueue()

rtq.put("Data A")
rtq.put("Data B")
rtq.put("Data C")
rtq.put("Data D")
rtq.put("Data E")

ix = 0
tt = theThread(10)
tt.daemon = True
tt.setDaemon(True)
tt.start()
while True: #not rtq.isEmpty():
    s = rtq.get()
    print ("{0}".format(s))
    time.sleep(0.5)
    
    
    
    
    