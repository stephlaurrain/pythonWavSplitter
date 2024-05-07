     @_error_decorator()
        def treat_wave_old(self, pwavefile_path, paudio):                
                self.trace(inspect.stack())  
                dest_dir_name = self.set_version_dir(pwavefile_path)  
                self.log.lg(paudio.duration_seconds)
                velocities = self.jsprms.prms['velocities']
                sounds = self.jsprms.prms['sounds']                
                expected_nb_sounds = (self.jsprms.prms['mulab_length']-1)/self.jsprms.prms['mulab_step']
                self.log.lg(f"expected sounds = {expected_nb_sounds} / number of sounds = {len(sounds)}")
                if len(sounds)!= expected_nb_sounds:
                       raise ValueError('Expected number of sounds <> number of sounds.')
                split_time = self.jsprms.prms['split_time']
                split_threshold = -self.jsprms.prms['split_dbfs_threshold']                 
                sample_number = len(velocities)*len(sounds)
                extract_size = paudio.duration_seconds / sample_number *1000
                self.log.lg(f"sample_number = {sample_number}")
                self.log.lg(f"extract_size = {extract_size}")                
                self.log.lg(f"audio segment RMS = {paudio.dBFS}")
                idx = 0
                for cpt_sound in range(len(sounds)):
                        for cpt_velocity in range(len(velocities)):
                                extract = paudio[idx:extract_size+idx]
                                # non séparé dest_dir = f"{self.result_sound_dir}{os.path.sep}{dest_dir_name}"
                                dest_dir = f"{self.result_sound_dir}{os.path.sep}{dest_dir_name}{os.path.sep}{cpt_sound}{sounds[cpt_sound]}"                                                                                  
                                export_file_path = f"{dest_dir}{os.path.sep}{dest_dir_name}-{cpt_sound}{self.drumkit_name}-{velocities[cpt_velocity]}-{sounds[cpt_sound]}.wav"                                        
                                # export_file_path_org = f"{dest_dir}{os.path.sep}{velocities[cpt_velocity]}-{sounds[cpt_sound]}_org.wav"
                                # extract.export(export_file_path_org, format="wav")
                                end_trim = self.detect_leading_silence(sound=extract.reverse(), silence_threshold=split_threshold, chunk_size=split_time)
                                
                                self.log.lg(f"end_trim = {end_trim}")
                                if end_trim < extract_size:
                                        final_sound = extract[:extract_size-end_trim]
                                        self.log.lg(f"export_file_path = {export_file_path}")
                                        self.log.lg(f"final_sound segment RMS = {final_sound.dBFS}")                                                
                                        if final_sound.dBFS < split_threshold or final_sound.duration_seconds < self.jsprms.prms['duration_threshold']:
                                                self.log.lg(f"TOO WEAK = export_file_path = {export_file_path}")        
                                                #input ("VERIFIE")
                                        else:
                                                if not os.path.exists(dest_dir):
                                                        os.mkdir(dest_dir)
                                                #final_sound.fade_out(16) # final_sound.duration_seconds / 2)
                                                fade_in_percent = self.jsprms.prms['fade_percent']['in']
                                                fade_out_percent = self.jsprms.prms['fade_percent']['out']
                                                if fade_in_percent > 0 or fade_out_percent > 0:
                                                        final_sound = self.treat_fade(final_sound, fade_in_percent, fade_out_percent)                                                                                           
                                                final_sound.export(export_file_path, format="wav") 
                                else:                                        
                                        self.log.lg(f"SILENT = export_file_path = {export_file_path}")
                                idx += extract_size