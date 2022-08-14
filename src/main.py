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
from datetime import datetime
import time

class GoodRes():
        def __init__(self, split_threshold, split_time, seek_step, process_time): 
                self.split_threshold = split_threshold
                self.split_time = split_time
                self.seek_step = seek_step
                self.process_time = process_time
        
        def __str__(self):
                return f"GOOD CONF : split_threshold = {self.split_threshold}, split_time = {self.split_time}, seek_step = {self.seek_step}, process_time = {self.process_time}"
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
                        keep_log_time = self.jsprms.prms['keep_log_time']
                        keep_log_unit = self.jsprms.prms['keep_log_unit']
                        self.log.lg(f"=>clean logs older than {keep_log_time} {keep_log_unit}")
                        self.goodRes_array = []
                        file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", keep_log_time, keep_log_unit)
                except Exception as e:
                        print(f"Wasted, very wasted : {e}")
                        raise

        @_trace_decorator        
        @_error_decorator()
        def set_version_dir(self, wavefile_path):
                head, tail = os.path.split(wavefile_path)
                dest_dir_name = os.path.splitext(tail)[0]
                version_dir = f"{self.result_sound_dir}{os.path.sep}{dest_dir_name}"
                if not os.path.exists(version_dir):
                        os.mkdir(version_dir)  
                return dest_dir_name              
        
        @_trace_decorator        
        @_error_decorator()
        def treat_wave(self, psplit_threshold, psplit_time, pseek_step, pwavefile_path, paudio,  calculate=False):
                watch_time_start = time.process_time()
                print(f"split_threshold = {psplit_threshold} - split_time = {psplit_time} - seek_step = {pseek_step}")
                if calculate is False:
                        dest_dir_name = self.set_version_dir(pwavefile_path)  
                res = silence.split_on_silence(paudio, min_silence_len=psplit_time, 
                                silence_thresh=-psplit_threshold, keep_silence=False, seek_step=pseek_step)              
                velocities = self.jsprms.prms['velocities']
                sounds = self.jsprms.prms['sounds']
                loop_wait = self.jsprms.prms['loop_wait']
                cpt_velocity = 0
                cpt_sound = 0
                res_length = len(res)                
                good_length = len(sounds)*len(velocities)
                nb_errors = 0
                if good_length == res_length:  
                        self.log.lg(f"FOUND GOOD SEGMENTS TAB LENGTH")                       
                        for idx, snd in enumerate(res):
                                if calculate is False:
                                        dest_dir = f"{self.result_sound_dir}{os.path.sep}{dest_dir_name}{os.path.sep}{cpt_sound}{sounds[cpt_sound]}"
                                        if not os.path.exists(dest_dir):
                                                os.mkdir(dest_dir)                                                                                
                                        export_file_path = f"{dest_dir}{os.path.sep}{velocities[cpt_velocity]}-{sounds[cpt_sound]}.wav"
                                        # print(f"{export_file_path}, duration_seconds = {snd.duration_seconds}")                                
                                if snd.duration_seconds > self.jsprms.prms['size_threshold']:  
                                        if calculate is False:
                                                snd.export(export_file_path, format="wav")
                                                if loop_wait > 0:
                                                        time.sleep(loop_wait)                                                   
                                        cpt_velocity += 1
                                        if cpt_velocity >= len(velocities):
                                                cpt_velocity = 0
                                                cpt_sound += 1
                                                if cpt_sound >= len(sounds):
                                                        cpt_sound = 0
                                else:
                                        self.log.lg(f"FILE NOT EXPORTED = {velocities[cpt_velocity]}-{sounds[cpt_sound]}.wav duration = {snd.duration_seconds}") 
                                        nb_errors += 1
                else : 
                        # self.log.lg(f"ERROR = excepted length = {good_length}, length = {res_length}") 
                        nb_errors = 9999                                              
                if nb_errors == 0:
                        self.log.lg(f"=== GOOD CONF FOUND ! ===")
                        process_time = time.process_time() - watch_time_start                        
                        good_res = GoodRes(split_threshold=psplit_threshold, split_time=psplit_time, seek_step=pseek_step, process_time=process_time)
                        self.goodRes_array.append(good_res)                        
                        print(str(good_res))                                                

        @_trace_decorator        
        @_error_decorator()
        def calculate_params(self, pwavefile_path, paudio):                                                                    
                self.log.lg("====================================================================")
                self.log.lg(f"==>> FINDING BEST SCORE for {pwavefile_path}")
                self.log.lg("====================================================================")
                for split_time in range(self.jsprms.prms['split_time']['min'], self.jsprms.prms['split_time']['max'], self.jsprms.prms['split_time']['step']):                        
                        for split_threshold in range(self.jsprms.prms['split_threshold']['min'], self.jsprms.prms['split_threshold']['max'], self.jsprms.prms['split_threshold']['step']):                                                
                                for seek_step in range(self.jsprms.prms['seek_step']['min'], self.jsprms.prms['seek_step']['max'], self.jsprms.prms['seek_step']['step']):
                                        # print(f"seek_step = {seek_step}")
                                        # print(f"#####################################################")
                                        # print(f"wavefile_path = {pwavefile_path}")
                                        self.treat_wave(psplit_threshold=split_threshold, psplit_time=split_time, pseek_step=seek_step, pwavefile_path=pwavefile_path, paudio=paudio, calculate=True)

        @_trace_decorator        
        @_error_decorator()
        def split_waves(self):
                file_utils.clean_dir(self.result_sound_dir)            
                for wavefile_path in sorted(Path(self.org_sound_dir).rglob('*.Wav')):
                                if wavefile_path.is_file():                                        
                                        myaudio = AudioSegment.from_wav(wavefile_path) 
                                        self.calculate_params(wavefile_path, myaudio)                                                                                                                           
                                        if len(self.goodRes_array)>0:
                                                self.goodRes_array.sort(key=lambda x: x.process_time, reverse=False)
                                                # To return a new list, use the sorted() built-in function...
                                                # newlist = sorted(ut, key=lambda x: x.count, reverse=True)  
                                                best_res = self.goodRes_array[0]
                                                self.log.lg(f"BEST SCORE = {str(self.goodRes_array[0])}")
                                                self.log.lg("====================================================================")
                                                self.log.lg(f"==>> SPLITTING {wavefile_path}")
                                                self.log.lg("====================================================================")
                                                self.treat_wave(psplit_threshold=best_res.split_threshold, psplit_time=best_res.split_time, pseek_step=best_res.seek_step, pwavefile_path=wavefile_path, paudio=myaudio, calculate=False)
                                        else:
                                                self.log.errlg(f"NO BEST SCORE FOR : {wavefile_path}, FILE WAS NOT SPLITTED, PLEASE CHANGE PARAMS")
                                        self.goodRes_array.clear()

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
                        # command="split"
                        self.init_main(command, jsonfile)                                                
                        if (command == "split"):                                
                                # input("Press Enter to continue...")
                                self.split_waves()
                        self.log.lg("=>> THE END COMPLETE <<=")
                except KeyboardInterrupt:
                        print("==>> Interrupted <<==")
                        pass
                except Exception as e:
                        print("==>> GLOBAL MAIN EXCEPTION <<==")
                        self.log.errlg(e)
                        # raise                        
                finally:
                        print("==>> DONE <<==")