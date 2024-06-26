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
from utils.mydecorators import _error_decorator
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pathlib import Path
from datetime import datetime
import time

import hashlib


class Hashes():
        def __init__(self, hash, filepath): 
                self.hash = hash
                self.filepath = filepath

class Wavesplit:

        def trace(self, stck):                
                self.log.lg(f"{stck[0].function} ({ stck[0].filename}-{stck[0].lineno})")
   
        def init_main(self, command, jsonfile, param1, param2):            
                try:
                        self.root_app = os.getcwd()
                        self.log = mylog.Log()
                        self.log.init(jsonfile)
                        self.trace(inspect.stack())
                        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}conf{os.path.sep}{jsonfile}.json"
                        self.jsprms = jsonprms.Prms(jsonFn)
                        # self.test = self.jsprms.prms['test']
                        self.sounds_dir = f"{self.root_app}{os.path.sep}data{os.path.sep}sounds"
                        self.org_sound_dir = f"{self.sounds_dir}{os.path.sep}{self.jsprms.prms['org_sound_dir']}"                        
                        self.result_sound_dir = f"{self.sounds_dir}{os.path.sep}{self.jsprms.prms['result_sound_dir']}"
                        self.drumkit_main_path = self.jsprms.prms['drumkit_main_path']
                        self.drumkit_master = param1 if param1 !=''else self.jsprms.prms['drumkit_master']
                        self.drumkit_name = param2 if param2 != '' else self.jsprms.prms['drumkit_name']
                        self.drumkit_dest_path = f"{self.drumkit_main_path}{os.path.sep}{self.drumkit_master}{os.path.sep}{self.drumkit_name}"
                        self.global_error = False
                        self.log.lg("=HERE WE GO=")
                        keep_log_time = self.jsprms.prms['keep_log_time']
                        keep_log_unit = self.jsprms.prms['keep_log_unit']
                        self.log.lg(f"=>clean logs older than {keep_log_time} {keep_log_unit}")                       
                        file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", keep_log_time, keep_log_unit)
                except Exception as e:
                        self.log.errlg(f"Wasted, very wasted : {e}")
                        raise
        
        @_error_decorator()
        def set_version_dir(self, wavefile_path):
                self.trace(inspect.stack())  
                head, tail = os.path.split(wavefile_path)
                dest_dir_name = os.path.splitext(tail)[0]
                version_dir = f"{self.result_sound_dir}{os.path.sep}{dest_dir_name}"
                if not os.path.exists(version_dir):
                        os.mkdir(version_dir)  
                return dest_dir_name              

        @_error_decorator()
        def detect_leading_silence(self, sound, silence_threshold=-50.0, chunk_size=10):
                self.trace(inspect.stack())  
                trim_ms = 0 # ms
                assert chunk_size > 0 # to avoid infinite loop
                while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
                        trim_ms += chunk_size
                return trim_ms
        
        @_error_decorator()
        def treat_fade(self, sound, fade_in_percent, fade_out_percent):
                self.trace(inspect.stack())  
                if fade_in_percent > 0:
                        fade_in_len = round(sound.duration_seconds*1000*fade_in_percent/100)                        
                        res_sound = sound.fade_in(fade_in_len)
                if fade_out_percent > 0:
                        fade_out_len = round(sound.duration_seconds*1000*fade_out_percent/100)
                        if fade_in_percent > 0:
                                res_sound = res_sound.fade_out(fade_out_len)
                        else:
                                res_sound = sound.fade_out(fade_out_len)
                return res_sound
       
        @_error_decorator()
        def split_to_many(self, paudio):
                self.trace(inspect.stack())  
                segment_duration = self.jsprms.prms['one_note_length']
                segments = []                
                current_time = 0                                
                while current_time < len(paudio):
                        end_time = current_time + segment_duration
                        if end_time > len(paudio):
                                end_time = len(paudio)                        
                        segment = paudio[current_time:end_time]
                        segments.append(segment)

                        current_time = end_time                
                return segments

        @_error_decorator()
        def treat_wave(self, pwavefile_path, paudio):
                self.trace(inspect.stack())            
                dest_dir_name = self.set_version_dir(pwavefile_path)  
                self.log.lg(paudio.duration_seconds)                
                velocities = self.jsprms.prms['velocities']
                sounds = self.jsprms.prms['sounds']                                
                self.log.lg(f"audio segment RMS = {paudio.dBFS}")
                
                segments = self.split_to_many(paudio)
                numero_segment = 1
                cpt_sound = 0
                cpt_velocity = 0
                
                if len(segments) != len(sounds) * len(velocities) :
                        input(f"BAD number of sounds segments ln = {len(segments)} sounds = {len(sounds)} velocities = {len(velocities)}")
                for segment in segments:
                        dest_dir = f"{self.result_sound_dir}{os.path.sep}{dest_dir_name}{os.path.sep}{cpt_sound}{sounds[cpt_sound]}"                                                                                  
                        export_file_path = f"{dest_dir}{os.path.sep}{dest_dir_name}-{cpt_sound}{self.drumkit_name}-{velocities[cpt_velocity]}-{sounds[cpt_sound]}.wav"                                        
                        # final_sound.export(export_file_path, format="wav")  # Ajustez le format si besoin
                        # print(f"{segment.dBFS} {segment.duration_seconds}")
                        #min_silence_length = 100  # Durée minimale du silence en millisecondes
                        #silence_threshold = -50  # Seuil de silence en dBFS (plus la valeur est basse, plus le seuil est sensible)
                        min_silence_length = self.jsprms.prms['silence']['length']  # Durée minimale du silence en millisecondes
                        silence_threshold = -self.jsprms.prms['silence']['dbfs_threshold']   # Seuil de silence en dBFS (plus la valeur est basse, plus le seuil est sensible)
                        # Découper le fichier en segments en supprimant les parties silencieuses
                        segments = split_on_silence(segment, min_silence_len=min_silence_length, silence_thresh=silence_threshold)                        
                        if len(segments) > 0:
                                # and segment[0].duration_seconds > self.jsprms.prms['duration_threshold']:
                                segment = segments[0] 
                                if not os.path.exists(dest_dir):
                                        os.mkdir(dest_dir)
                                fade_in_percent = self.jsprms.prms['fade_percent']['in']
                                fade_out_percent = self.jsprms.prms['fade_percent']['out']
                                if fade_in_percent > 0 or fade_out_percent > 0:
                                        segment = self.treat_fade(segment, fade_in_percent, fade_out_percent)                                                                                           
                                segment.export(export_file_path, format="wav") 

                                numero_segment += 1
                        else:
                                self.log.lg(f"TOO WEAK = export_file_path = {export_file_path}")
                        if cpt_velocity == len(velocities) - 1:
                                cpt_velocity = 0
                                cpt_sound += 1
                        else:
                                cpt_velocity += 1
                        
                        

        @_error_decorator()
        def getfilehash(self,fname):
                self.trace(inspect.stack())  
                hash = hashlib.blake2b()
                with open(fname, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                                hash.update(chunk)
                return hash.hexdigest()
        
        @_error_decorator()
        def is_in_hashes(self, hashobj, hashlist):                
                self.trace(inspect.stack())  
                for hashline in hashlist:
                        if hashline.hash == hashobj.hash:
                                return hashline                                              
                return False

        @_error_decorator()
        def write_to_deleted_files(self, text_file, pth, hash_of_file, res):                                       
                self.trace(inspect.stack())  
                head, tail = os.path.split(pth)
                dest_dir_name = os.path.splitext(tail)[0]                
                text_file.write("#####################\n")                                                
                text_file.write(f"{self.jsprms.prms['drumkit_name']} - {dest_dir_name}\n")                                
                text_file.write(f"delete {pth}\n")
                text_file.write(f"hash of file ={hash_of_file} = hash found {res.hash}\n")
                text_file.write(f"IS EQUAL TO {res.filepath}\n")

        @_error_decorator()
        def delete_doubles(self, dest_dir):
                self.trace(inspect.stack())  
                hashlist = []
                deleted_file_path =  f"{self.root_app}{os.path.sep}data{os.path.sep}deletedfiles.txt"
                text_file = open(deleted_file_path, "w")                
                for pth in sorted(Path(dest_dir).rglob('*.wav')):                        
                        if pth.is_file():            
                                hash_of_file = self.getfilehash(pth)                            
                                hashobj = Hashes(hash=hash_of_file, filepath=pth)
                                res = self.is_in_hashes(hashobj, hashlist)
                                if res is False:
                                # if not hashobj in hashlist:                                                
                                        hashlist.append(hashobj)    
                                        print(f'append {pth} hash={hashobj.hash}')
                                else:                                       
                                        os.unlink(pth)         
                                        pth_path = os.path.dirname(pth)
                                        if len(os.listdir(pth_path)) == 0:
                                                os.rmdir(pth_path)
                                        self.write_to_deleted_files(text_file, pth, hash_of_file, res)                                                                                      
                text_file.close()                                
                                        
        @_error_decorator()
        def split_waves(self):
                self.trace(inspect.stack())  
                file_utils.clean_dir(self.result_sound_dir)            
                for wavefile_path in sorted(Path(self.org_sound_dir).rglob('*.Wav')):
                                if wavefile_path.is_file():                                        
                                        myaudio = AudioSegment.from_wav(wavefile_path) 
                                        self.treat_wave(pwavefile_path=wavefile_path, paudio=myaudio)

        def move_drum_kit(self):
                self.trace(inspect.stack())  
                for dir_path in os.scandir(self.result_sound_dir):
                        if dir_path.is_dir():       
                                shutil.move(dir_path.path, self.drumkit_dest_path)

        def presetconv(self):
                self.trace(inspect.stack())  
                file_to_convert = f"{self.root_app}{os.path.sep}data{os.path.sep}presets{os.path.sep}msMain1.MultiSample"
                f=open(file_to_convert,"rb")
                s=f.read()
                f.close()
                first = b'1KVLTdirect'
                prout =b'2KVLToverrr'
                s=s.replace(first ,prout)
                result_file = f"{self.root_app}{os.path.sep}data{os.path.sep}presets{os.path.sep}msOver1.MultiSample"
                f=open(result_file,"wb")
                f.write(s)
                f.close()


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
                        print(f"command={command}")     
                        # command="presetconv"
                        self.init_main(command, jsonfile, param1, param2)                                                
                        if (command == "split"):  
                                master_path = f"{self.drumkit_main_path}{os.path.sep}{self.drumkit_master}"    
                                if not os.path.exists(master_path):
                                        os.mkdir(master_path)
                                if not os.path.exists(self.drumkit_dest_path):
                                        os.mkdir(self.drumkit_dest_path)
                                else: 
                                        if input ('drumkit path already exists, remove it ? (type y) : ')=='y':
                                                file_utils.clean_dir(self.drumkit_dest_path)
                                        else:
                                                raise ValueError('drumkit path already exists')                        
                                # input("Press Enter to continue...")
                                self.split_waves()
                                # input("Press Enter to copy drumkit and clean org path...")
                                if self.jsprms.prms['delete_doubles']:
                                        self.delete_doubles(self.result_sound_dir)
                                if self.global_error is False:
                                        if self.jsprms.prms['move_drumkits']:
                                                self.move_drum_kit() 
                                        if self.jsprms.prms['move_drumkits'] and self.jsprms.prms['clean_dirs_at_end']:
                                                file_utils.clean_dir(self.org_sound_dir)
                                                # file_utils.clean_dir(self.result_sound_dir)          
                        if (command == "presetconv"):
                                self.presetconv()
                        if (command == "clean"):                                
                                self.delete_doubles(self.drumkit_main_path)
                        self.log.lg("=>> THE END COMPLETE <<=")
                except KeyboardInterrupt:
                        print("==>> Interrupted <<==")
                        pass
                except Exception as e:
                        print("==>> GLOBAL MAIN EXCEPTION <<==")
                        self.log.errlg(e)
                        return False
                        # raise                        
                finally:
                        print("==>> DONE <<==")