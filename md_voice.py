import numpy as np
import soundfile
import moviepy.editor as mpe
import time
import os



def Get_Voice_FileName(file_path,suffix):
    # 获取指定目录下的所有指定后缀的文件名返回一个列表
    input_template_All=[]
    f_list = os.listdir(file_path)#返回该目录下所有文件名组成一个列表
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名  返回一个元组 元组里面 0元素代表文件名 1元素代表后缀名 
        if os.path.splitext(i)[1] == suffix :
            input_template_All.append(i)
            #print(i)
    return input_template_All


#音频文件目录结构：D:\MD_recording\2021\202102\20210202\001
local_day_time = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))   #得到今天的时间

local_year = local_day_time[0:4]
local_moth = local_day_time[5:7]
local_days = local_day_time[8:10]

#得到今天port端口该目录下的wav文件构成的文件列表
Voice_filename = Get_Voice_FileName("D:/MD_recording/"+local_year+"/"+local_year+local_moth+"/"+local_year+local_moth+local_days+"/001",".wav")

print(Voice_filename)

for v_f in Voice_filename :
    Now_Process_recording_file = v_f
    print("Now Process File ->>",Now_Process_recording_file)
    #得到该录音的开始录音时间
    voice_start_year   = int(Now_Process_recording_file[0:4])
    voice_start_mouth  = int(Now_Process_recording_file[4:6])
    voice_start_day    = int(Now_Process_recording_file[6:8])
    voice_start_hour   = int(Now_Process_recording_file[8:10])
    voice_start_minute = int(Now_Process_recording_file[10:12])
    voice_start_second = int(Now_Process_recording_file[12:14])
    voice_type         = Now_Process_recording_file[15:17]   #录音类型---是out 播出  in 拨入 (播出类型记录了电话号码，拨入没有记录)
    if voice_type == 'ou':
        voice_port = int(Now_Process_recording_file[19:22])
        voice_phone_number = Now_Process_recording_file[26:-4]
    else:
        voice_port = int(Now_Process_recording_file[18:21])

    print("音频开始时间",voice_start_year,voice_start_mouth,voice_start_day,voice_start_hour,voice_start_minute,voice_start_second,voice_type,"音频端口号",voice_port)

    #读取音频
    voice_audio = mpe.AudioFileClip("D:/MD_recording/"+local_year+"/"+local_year+local_moth+"/"+local_year+local_moth+local_days+"/"+"001/"+Now_Process_recording_file)

    print("音频",Now_Process_recording_file,"时长",voice_audio.duration)
    #获得音频时长
    voide_spand      = int(voice_audio.duration)
    #计算音频结束时间
    m,s = divmod(voide_spand,60)
    h,m = divmod(m,60)
    d,h = divmod(h,24)

    if voice_start_second + s >= 60 :
        voice_end_second = voice_start_second + s - 60
        m += 1
    else:
        voice_end_second = voice_start_second + s

    if voice_start_minute + m >= 60 :
        voice_end_minute = voice_start_minute + m - 60
        h += 1
    else:
        voice_end_minute = voice_start_minute + m

    if voice_start_hour + h >= 24 :
        voice_end_hour = voice_start_hour + h - 24 
        d += 1
    else:
        voice_end_hour = voice_start_hour + h

    voice_end_year   = voice_start_year
    voice_end_mouth  = voice_start_mouth
    voice_end_day    = voice_start_day + d

    print("音频结束时间",voice_end_year,voice_end_mouth,voice_end_day,voice_end_hour,voice_end_minute,voice_end_second)


                
'''
#读取音频
voice_audio = mpe.AudioFileClip("D:/MD_recording/"+local_year+"/"+local_year+local_moth+"/"+local_year+local_moth+local_days+"/001/"+Voice_filename[i]) 

print(voice_audio.duration)

voide_spand      = int(voice_audio.duration)
m,s = divmod(voide_spand,60)
h,m = divmod(m,60)
d,h = divmod(h,24)
voice_end_year   = voice_start_year
voice_end_mouth  = voice_start_mouth
voice_end_day    = voice_start_day + d
voice_end_hour   = voice_start_hour + h
voice_end_minute = voice_start_minute + m
voice_end_second = voice_start_second + s

print(voice_end_day,voice_end_hour,voice_end_minute,voice_end_second)
'''

'''
audio = mpe.AudioFileClip("./VioceFile/20210108221558-out-004( )-777.wav")
video1 = mpe.VideoFileClip("./GetVideoFile/tttest.mp4",audio = False,verbose = True)

#音频时长
#audio.duration
final = video1.set_audio(audio)
final.write_videofile("./OutPutVideoFile/output.mp4",codec= 'mpeg4' ,audio_codec='libvorbis')

'''
