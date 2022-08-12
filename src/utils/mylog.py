import os
import logging
import inspect
from datetime import datetime


class Log:
      
    def __init__(self):
        self.formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        self.root_app = os.getcwd()

    def init(self, profil):
        today = datetime.now()
        dnow = today.strftime(r"%y%m%d%H%M") 
        logFilename = f"{self.root_app}{os.path.sep}log{os.path.sep}{dnow}{profil}.log"
        print(logFilename)
        errlogFilename = f"{self.root_app}{os.path.sep}log{os.path.sep}{dnow}err-{profil}.log"
        self.intlg = self.setup_logger("genlog", logFilename)            
        self.interrlg = self.setup_logger("errlog", errlogFilename, logging.ERROR)
    
    def setup_logger(self, name, log_file, level=logging.INFO):
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(self.formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def lg(self, mess):       
        print(mess) 
        self.intlg.info(mess)

    def errlg(self, mess, func=""):               
        mess = f"EXCEPTION-{func}-{mess} \n\n {inspect.stack}"
        print(mess)  
        self.intlg.info(mess)
        self.interrlg.error(mess)