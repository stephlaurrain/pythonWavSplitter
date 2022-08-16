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
        def __init__(self, split_threshold, split_time, seek_step, process_time, len): 
                self.split_threshold = split_threshold
                self.split_time = split_time
                self.seek_step = seek_step
                self.process_time = process_time
                self.len = len
        
        def __str__(self):
                return f"GOOD CONF : split_threshold = {self.split_threshold}, split_time = {self.split_time}, seek_step = {self.seek_step}, process_time = {self.process_time}, segments tab length = {self.len}"
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
                        self.sounds_dir = f"{self.root_app}{os.path.sep}data{os.path.sep}sounds"
                        self.org_sound_dir = f"{self.sounds_dir}{os.path.sep}{self.jsprms.prms['org_sound_dir']}"                        
                        self.result_sound_dir = f"{self.sounds_dir}{os.path.sep}{self.jsprms.prms['result_sound_dir']}"
                        self.global_error = False
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
        def treat_wave(self, pwavefile_path, paudio):
                watch_time_start = time.process_time()                
                dest_dir_name = self.set_version_dir(pwavefile_path)  
                print(paudio.duration_seconds)
                
                #res = silence.split_on_silence(paudio, min_silence_len=psplit_time, 
                #                silence_thresh=-psplit_threshold, keep_silence=False, seek_step=pseek_step)              

                velocities = self.jsprms.prms['velocities']
                sounds = self.jsprms.prms['sounds']
                extract_size = paudio.duration_seconds / (len(velocities)*len(sounds))*1000
                print(extract_size)
                
                # print(f"audio segment RMS = {snd.dBFS}")
                print(f"audio segment RMS = {paudio.dBFS}")
                cpt_sound = 0
                cpt_velocity = 0
                dest_dir = f"{self.result_sound_dir}{os.path.sep}{dest_dir_name}{os.path.sep}{cpt_sound}{sounds[cpt_sound]}"
                if not os.path.exists(dest_dir):
                                                os.mkdir(dest_dir) 
                export_file_path = f"{dest_dir}{os.path.sep}{velocities[cpt_velocity]}-{sounds[cpt_sound]}.wav"
                extract = paudio[:extract_size]
                res = silence.detect_nonsilent(extract, 80, -50)
                non_silence_len = res[0][1]
                print(non_silence_len)
                
                final_sound = extract[:non_silence_len]
                print(f"final_sound segment RMS = {final_sound.dBFS}")
                final_sound.export(export_file_path, format="wav")
                return
                
                
                
                cpt_velocity = 0
                cpt_sound = 0
               
                error_found = False
             
             
                if res_length <= good_length+tolerance_length and res_length >= good_length-tolerance_length:                
                        self.log.lg(f"FOUND GOOD SEGMENTS TAB LENGTH")                       
                        for idx, snd in enumerate(res):
                                # print(f"audio segment RMS = {snd.dBFS}")
                                if calculate is False:
                                        dest_dir = f"{self.result_sound_dir}{os.path.sep}{dest_dir_name}{os.path.sep}{cpt_sound}{sounds[cpt_sound]}"
                                        if not os.path.exists(dest_dir):
                                                os.mkdir(dest_dir)                                                                                
                                        export_file_path = f"{dest_dir}{os.path.sep}{velocities[cpt_velocity]}-{sounds[cpt_sound]}.wav"
                                        print(f"{export_file_path}, duration_seconds = {snd.duration_seconds}")                                
                                if snd.duration_seconds > self.jsprms.prms['size_threshold']['min'] and snd.duration_seconds < self.jsprms.prms['size_threshold']['max']:  
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
                                        self.log.lg(f"FILE HAS BAD SIZE = {velocities[cpt_velocity]}-{sounds[cpt_sound]}.wav duration = {snd.duration_seconds}") 
                                        self.log.lg(f"CONF IS NOT GOOD") 
                                        error_found = True
                                        break
                else : 
                        print(f"ERROR tab length is not GOOD") 
                        error_found = True                                              
                if calculate and not error_found:
                        self.log.lg(f"=== GOOD CONF FOUND ! ===")
                        process_time = time.process_time() - watch_time_start                        
                        good_res = GoodRes(split_threshold=psplit_threshold, split_time=psplit_time, seek_step=pseek_step, process_time=process_time, len=res_length)
                        self.save_good_res_to_statfile(pwavefile_path, good_res, good_length)
                        self.goodRes_array.append(good_res)                        
                        self.log.lg(str(good_res))
                        return process_time
                return 9999                                           
        
        @_trace_decorator        
        @_error_decorator()
        def save_good_res_to_statfile(self, wavefile_path, good_res, good_length):
                statfile_path =  f"{self.root_app}{os.path.sep}data{os.path.sep}statfile.txt"
                head, tail = os.path.split(wavefile_path)
                dest_dir_name = os.path.splitext(tail)[0]
                text_file = open(statfile_path, "a")
                text_file.write('#####################\n')
                text_file.write(f'{datetime.now().strftime(r"%y%m%d%H%M")} good_length = {good_length}\n')
                text_file.write(f"{self.jsprms.prms['drumkit_name']} - {dest_dir_name}\n")
                #for good_res in self.goodRes_array:                        
                text_file.write(f"{str(good_res)}\n")
                text_file.close()

        
        @_trace_decorator        
        @_error_decorator()
        def split_waves(self):
                file_utils.clean_dir(self.result_sound_dir)            
                for wavefile_path in sorted(Path(self.org_sound_dir).rglob('*.Wav')):
                                if wavefile_path.is_file():                                        
                                        myaudio = AudioSegment.from_wav(wavefile_path) 
                                        
                                        self.treat_wave(pwavefile_path=wavefile_path, paudio=myaudio)
                                        
                                        
        def move_drum_kit(self):
                drumkit_path = f"{self.jsprms.prms['drumkit_path']}{os.path.sep}{self.jsprms.prms['drumkit_name']}"
                if not os.path.exists(drumkit_path):
                        os.mkdir(drumkit_path)                  

                for dir_path in os.scandir(self.result_sound_dir):
                        if dir_path.is_dir():       
                                shutil.move(dir_path.path, drumkit_path)


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
                                # input("Press Enter to copy drumkit and clean org path...")
                                if self.global_error is False:
                                        if self.jsprms.prms['move_drumkits']:
                                                self.move_drum_kit() 
                                        if self.jsprms.prms['move_drumkits'] and self.jsprms.prms['clean_dirs_at_end']:
                                                file_utils.clean_dir(self.org_sound_dir)
                                                # file_utils.clean_dir(self.result_sound_dir)          
                                

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