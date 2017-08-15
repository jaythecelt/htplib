'''
    Logger Class 
    Wraps the logging library, implemented as a Singleton.
    
    See https://docs.python.org/3.4/library/logging.config.html

    Features:
    - Sends Log messages to both the console and log file.
    - Each can have it's own logging level
    - Always logs to /home/pi/htplogs
    - Rotates log files, bound file size
    
    Example use:
    
    from HtpLogger import HtpLogger
    
    At the start of the application, call the costructor to define the 
    log file name and the log levels:
        log = HtpLogger("testLog", HtpLogger.DEBUG, HtpLogger.WARNING)
        
    In each module or class, obtain the HtpLogger instance:
        log = HtpLogger.get()

    If HtpLogger.get() is called before the constructor, a default file named
    'noname.log' is used, both console and file use the DEBUG logging level.
    When this happens, the user gets a warning message.
    
    

'''
import inspect
import logging
import logging.handlers

# TODO Catch exceptions


class HtpLogger(object):
    instance = None
    logger = None

    #Constants
    DEBUG    = logging.DEBUG
    INFO     = logging.INFO
    WARNING  = logging.WARNING
    ERROR    = logging.ERROR
    CRITICAL = logging.CRITICAL
    
    LOG_PATH = "/home/pi/htplogs/"
    MAX_FILE_SIZE = 1000000
    BACKUPS = 5
    
    def __init__(self, logPrefix, file_level, console_level):
        if not HtpLogger.instance:
            HtpLogger.instance = HtpLogger.__Logger(logPrefix, file_level, console_level)

    @classmethod
    def get(self):
        if not HtpLogger.instance:
            HtpLogger.instance = HtpLogger.__Logger(None, logging.DEBUG, logging.DEBUG)
            HtpLogger.instance.warning("Creating default HtpLogger instance! Not a good idea!")
        return self.instance
            
   # Proxy for inner class
    def __getattr__(self, name):
        return getattr(self.instance, name)
        
    # Inner class for the singlton implementation.
    # Method implementations go here.
    class __Logger:

    
        def __init__(self, prefix, file_level, console_level):        
            if prefix is None:
                prefix = "noName"

            function_name = inspect.stack()[1][3]
            self.logger = logging.getLogger(function_name)
            self.logger.setLevel(logging.DEBUG) #By default, logs all messages

            if console_level is not None:
                ch = logging.StreamHandler() #StreamHandler logs to console
                ch.setLevel(console_level)
                ch_format = logging.Formatter('%(message)s')
                ch.setFormatter(ch_format)
                self.logger.addHandler(ch)

            fNameStr = HtpLogger.LOG_PATH + "{0}.log".format(prefix)

            # Add the log message handler to the logger
            fh = logging.handlers.RotatingFileHandler(
                      fNameStr, 
                      maxBytes=HtpLogger.MAX_FILE_SIZE, 
                      backupCount=HtpLogger.BACKUPS)

            fh.setLevel(file_level)
#            fh_format = logging.Formatter('%(asctime)s - %(funcName)15s() - %(lineno)d - %(levelname)-8s - %(message)s')
            fh_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
            fh.setFormatter(fh_format)

            self.logger.addHandler(fh)
            self.logger.info("Starting log file " + fh.baseFilename)
            
            
        def debug(self, msg, *args, **kwargs):
            self.logger.debug(msg, *args, **kwargs)
          
        def info(self, msg, *args, **kwargs):
            self.logger.info(msg, *args, **kwargs)
        
        def warning(self, msg, *args, **kwargs):
            self.logger.warning(msg, *args, **kwargs)

        def error(self, msg, *args, **kwargs):
            self.logger.error(msg, *args, **kwargs)

        def critical(self, msg, *args, **kwargs):
            self.logger.critical(msg, *args, **kwargs)

        # Prints to console regardless of the logging level
        #   bypassing the console formatter.
        # Typically used to print a message to the console when
        #   the console logging level is null.
        # Also writes to the log as INFO
        def console(self, msg, *args, **kwargs):
            print(msg)
            self.logger.info(msg, *args, **kwargs)
    
    
def f1():
    log = HtpLogger("testLog", HtpLogger.DEBUG, HtpLogger.WARNING)
    log.debug('debug message')
    log.info('info message')
    log.warning('warning message')
    log.error('error message')
    log.critical('critical message')

def f2():
    log = HtpLogger.get()
    log.debug('debug message')
    log.info('info message')
    log.warning('warning message')
    log.error('error message')
    log.critical('critical message')

def main():
    f1()
    f2()
    log = HtpLogger.get()
    log.debug("All Done!")

#main()
    
    