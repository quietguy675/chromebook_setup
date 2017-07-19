#!/usr/bin python3

import os
import subprocess
from math import ceil

class FFMPEG_Thread():
    def start_ffmpeg(self, save_location, date, record_length=600, include_webcam=True):
        
        increment_int = 0
        temp_filename = ""
        while True:
            if increment_int == 0:
                temp_filename = os.path.join(save_location, 'recorded_vid_'+str(date)+'.m4v')
            else:
                temp_filename = os.path.join(save_location, 'recorded_vid_'+str(date)+'_'+str(increment_int)+'.m4v')

            if not os.path.isfile(temp_filename):
                save_location = temp_filename 
                break
            increment_int = increment_int + 1
        
        ffmpeg_command_line = ''
        if include_webcam:
            ffmpeg_command_line = 'ffmpeg -f v4l2 -video_size 800x600 -framerate 10 -i /dev/video0 -f x11grab -video_size 1366x768 -framerate 2 -i :0.0 -f alsa -i hw:1,0 -filter_complex {} -framerate 30 -vcodec libx264 -preset ultrafast -crf 26 -acodec aac -strict -2 -t {record_length} {output_location}'
            ffmpeg_command_line = ffmpeg_command_line.format("{}", output_location=save_location, record_length=record_length)
        else:
            ffmpeg_command_line = 'ffmpeg -f x11grab -video_size 1366x768 -framerate 2 -i :0.0 -f alsa -i hw:1,0 -framerate 30 -vcodec libx264 -preset ultrafast -crf 26 -acodec aac -strict -2 -t {record_length} {output_location}'  
            ffmpeg_command_line = ffmpeg_command_line.format(output_location=save_location, record_length=record_length)
        
        ffmpeg_split = ffmpeg_command_line.split()
        complex_filter = "[1]scale=iw/5:ih/5 [pip]; [0][pip] overlay=main_w-overlay_w-10:main_h-overlay_h-10"
        for index, thing in enumerate(ffmpeg_split):
            if thing == '{}':
                ffmpeg_split[index] = complex_filter
        p = subprocess.Popen(ffmpeg_split)
        return save_location        
