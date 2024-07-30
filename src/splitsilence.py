import os
import re
import subprocess
from pathlib import Path
import inspect
import utils.file_utils as file_utils
import utils.mylog as mylog
import utils.jsonprms as jsonprms
from utils.mydecorators import _error_decorator

class SplitSilence:


    def trace(self, stck):                
            self.log.lg(f"{stck[0].function} ({ stck[0].filename}-{stck[0].lineno})")
   
    def init_main(self, jsonfile):            
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
    def treatfile(self, input_file):   
        silence_threshold = f"{str(-self.jsprms.prms['silence']['dbfs_threshold'])}dB" # "-30dB"
        silence_duration = str(self.jsprms.prms['silence']['duration']) # "0.5"
        simple_filename = file_utils.get_filename_without_extension(input_file)
        
        res_dir = f"{self.result_sound_dir}{os.path.sep}{simple_filename}"
        if not os.path.exists(res_dir):
            os.makedirs(res_dir)
        res_filename = f"{res_dir}{os.path.sep}{simple_filename}-"
        input(silence_duration)
        # Détecter les silences et enregistrer les informations dans silence_info.txt
        subprocess.run([
            "ffmpeg", "-i", input_file, "-af", f"silencedetect=noise={silence_threshold}:d={silence_duration}",
            "-f", "null", "-"
        ], stderr=open("silence_info.txt", "w"))

        # Initialiser les variables
        start_time = 0
        segment_index = 0

        # Lire le fichier silence_info.txt et extraire les informations de silence
        with open("silence_info.txt", "r") as f:
            for line in f:
                if "silence_start" in line:
                    silence_start = float(re.search(r'silence_start: ([\d\.]+)', line).group(1))
                    subprocess.run([
                        "ffmpeg", "-i", input_file, "-ss", str(start_time), "-to", str(silence_start), 
                        "-c", "copy", f"{res_filename}{segment_index}.wav"
                    ])
                    start_time = silence_start
                    segment_index += 1
                elif "silence_end" in line:
                    silence_end = float(re.search(r'silence_end: ([\d\.]+)', line).group(1))
                    start_time = silence_end

        # Extraire le dernier segment
        subprocess.run([
            "ffmpeg", "-i", input_file, "-ss", str(start_time), "-c", "copy", f"{res_filename}{segment_index}.wav"
        ])

    @_error_decorator()
    def browsefiles(self, org_dir):

        for pth in sorted(Path(org_dir).rglob('*.wav')):                        
                if pth.is_file(): 
                    self.treatfile(pth)
                      

    def main(self):
        try:
            self.init_main("splitsilence")          
            file_utils.clean_dir(self.result_sound_dir)
            input()
            self.browsefiles(self.org_sound_dir)

        
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

######
splitSilence = SplitSilence()
splitSilence.main()