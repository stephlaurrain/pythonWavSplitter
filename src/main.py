import datetime
import sys
import os, shutil
from os import path
from os import listdir
from os.path import isfile, join

import inspect
import utils.file_utils as file_utils
import utils.mylog as mylog
import utils.jsonprms as jsonprms

from utils.mydecorators import _error_decorator, _trace_decorator

from pydub import AudioSegment, silence
from pathlib import Path

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
                        sounds_dir = f"{self.root_app}{os.path.sep}data{os.path.sep}sounds"
                        self.org_sound_dir = f"{sounds_dir}{os.path.sep}{self.jsprms.prms['org_sound_dir']}"                        
                        self.result_sound_dir = f"{sounds_dir}{os.path.sep}{self.jsprms.prms['result_sound_dir']}"
                        self.log.lg("=HERE WE GO=")
                        self.log.lg(f"=>clean logs older than {self.jsprms.prms['keep_log_days']} days")
                        file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", self.jsprms.prms['keep_log_days'])
                        
                except Exception as e:
                        print("wasted")
                        raise
        
        @_trace_decorator        
        @_error_decorator()
        def clean_dir(self, dir_to_clean):                        
                # for pth in sorted(Path(dir_to_clean).rglob('*.wav')):                                                                      
                #        os.remove(str(pth))                            
                for filename in os.listdir(dir_to_clean):
                        file_path = os.path.join(dir_to_clean, filename)
                        try:
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                        os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path)
                        except Exception as e:
                                print('Failed to delete %s. Reason: %s' % (file_path, e))

        @_trace_decorator        
        @_error_decorator()
        def first_split(self, wavefile_path):
                print(wavefile_path)
                myaudio = AudioSegment.from_wav(wavefile_path)                
                # dBFS=myaudio.dBFS
                # lsilence = silence.detect_silence(myaudio, min_silence_len=1000, silence_thresh=dBFS-16)
                # lsilence = [((start/1000),(stop/1000)) for start,stop in lsilence] #in sec
                # print(lsilence)
                
                # first split
                # res = silence.split_on_silence(myaudio, min_silence_len=self.jsprms.prms['first_split_time'], silence_thresh=-40)
                ## GOOD
                res = silence.split_on_silence(myaudio, min_silence_len=self.jsprms.prms['split_time'], 
                                silence_thresh=self.jsprms.prms['split_treshold'], keep_silence=self.jsprms.prms['keep_silence'])
                # res = silence.split_on_silence(myaudio, min_silence_len=2000, silence_thresh=-40, keep_silence=False)
                # res = silence.detect_nonsilent(myaudio,11)
                # print (f"res = {res}")
                velocities = self.jsprms.prms['velocities']
                sounds = self.jsprms.prms['sounds']
                # print(self.jsprms.prms['velocities'])
                
                # for snd in res:
                # print (len(res))
                cpt_velocity =0
                cpt_sound=0
                for idx, snd in enumerate(res):
                        dest_dir =f"{self.result_sound_dir}{os.path.sep}{cpt_sound}{sounds[cpt_sound]}"
                        if not os.path.exists(dest_dir):
                                os.mkdir(dest_dir)
                        #print(velocities[idx])
                        #
                        snd.export(f"{dest_dir}{os.path.sep}{velocities[cpt_velocity]}-{sounds[cpt_sound]}.wav", format="wav")
                        cpt_velocity +=1
                        if cpt_velocity>=len(velocities):
                                cpt_velocity=0
                                cpt_sound+=1
                                if cpt_sound>=len(sounds):
                                        cpt_sound=0

                        
        @_trace_decorator        
        @_error_decorator()
        def treat_wave(self, wavefile_path):
                self.clean_dir(self.result_sound_dir)
                self.first_split(wavefile_path)
                
                

        @_trace_decorator        
        @_error_decorator()
        def split_waves(self):
                
                
                # sound_files = [f for f in listdir(org_sound_dir) if isfile(join(org_sound_dir, f))]
                for pth in sorted(Path(self.org_sound_dir).rglob('*.Wav')):
                                if pth.is_file():
                                        print(pth)
                                        self.treat_wave(pth)
                                        
                                        


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
                                # input("Press Enter to continue...")
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