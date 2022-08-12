import datetime
import sys
import os
from os import path
from os import listdir
from os.path import isfile, join

import inspect
import utils.file_utils as file_utils
import utils.mylog as mylog
import utils.jsonprms as jsonprms

from utils.mydecorators import _error_decorator, _trace_decorator

class Wavesplit:

        def trace(self, stck):
                #print (f"{stck.function} ({ stck.filename}-{stck.lineno})")                                
                self.log.lg(f"{stck.function} ({ stck.filename}-{stck.lineno})")
    
   
        def init_main(self, command, jsonfile):
                try:
                        self.root_app = os.getcwd()
                        self.log = mylog.Log()
                        self.log.init(jsonfile)
                        self.trace(inspect.stack()[0])
                        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}{jsonfile}.json"
                        self.jsprms = jsonprms.Prms(jsonFn)
                        # self.test = self.jsprms.prms['test']

                        self.log.lg("=HERE WE GO=")
                        self.log.lg(f"=>clean logs older than {self.jsprms.prms['keep_log_days']} days")
                        file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", self.jsprms.prms['keep_log_days'])
                        
                except Exception as e:
                        print("wasted")
                        raise

        @_trace_decorator        
        @_error_decorator()
        def split_waves(self):
                org_sound_dir = f"{self.root_app}{os.path.sep}data{os.path.sep}sounds{os.path.sep}org"
                
                sound_files = [f for f in listdir(org_sound_dir) if isfile(join(org_sound_dir, f))]
                print(sound_files)

        def main(self, command="", jsonfile="", param1="", param2=""):
                try:
                        # Init
                        # args
                        if command == "":
                                nb_args = len(sys.argv)
                                command = "test" if (nb_args == 1) else sys.argv[1]
                                # fichier json en param
                                jsonfile = "default" if (nb_args < 3) else sys.argv[2].lower()                                
                                param1 = "default" if (nb_args < 4) else sys.argv[3].lower()
                                param2 = "default" if (nb_args < 5) else sys.argv[4].lower()
                                param3 = "default" if (nb_args < 6) else sys.argv[5].lower()      
                                print("params=", command, jsonfile, param1, param2, param3)
                        # logs
                        print(command)     
                        command="split"
                        
                        self.init_main(command, jsonfile)                        
                        
                        if (command == "split"):                                
                                input("Press Enter to continue...")
                                self.split_waves()

                        self.log.lg("=THE END COMPLETE=")
                except KeyboardInterrupt:
                        print("==Interrupted==")
                        pass
                except Exception as e:
                        print("GLOBAL MAIN EXCEPTION")
                        self.log.errlg(e)
                        # raise
                        #
                finally:
                        print("finally")