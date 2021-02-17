from ctypes import *
import moviepy.editor as mpe
from ftplib import FTP
import socket
import configparser
import time
import sys
import os



class MyFTP:
    def __init__(self, host, port=21):
        """ 初始化 FTP 客户端
        参数:
                 host:ip地址

                 port:端口号
        """
        # print("__init__()---> host = %s ,port = %s" % (host, port))

        self.host = host
        self.port = port
        self.ftp = FTP()
        # 重新设置下编码方式
        self.ftp.encoding = 'gbk'
        self.log_file = open("log.txt", "a")
        self.file_list = []

    def login(self, username, password):
        """ 初始化 FTP 客户端
            参数:
                  username: 用户名

                 password: 密码
            """
        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)
            # 0主动模式 1 #被动模式
            self.ftp.set_pasv(False)
            # 打开调试级别2，显示详细信息
            #self.ftp.set_debuglevel(2)

            self.debug_print('开始尝试连接到 %s' % self.host)
            self.ftp.connect(self.host, self.port)
            self.debug_print('成功连接到 %s' % self.host)

            self.debug_print('开始尝试登录到 %s' % self.host)
            self.ftp.login(username, password)
            self.debug_print('成功登录到 %s' % self.host)

            self.debug_print(self.ftp.welcome)
        except Exception as err:
            self.deal_error("FTP 连接或登录失败 ，错误描述为：%s" % err)
            pass

    def is_same_size(self, local_file, remote_file):
        """判断远程文件和本地文件大小是否一致

           参数:
             local_file: 本地文件

             remote_file: 远程文件
        """
        try:
            remote_file_size = self.ftp.size(remote_file)
        except Exception as err:
            # self.debug_print("is_same_size() 错误描述为：%s" % err)
            remote_file_size = -1

        try:
            local_file_size = os.path.getsize(local_file)
        except Exception as err:
            # self.debug_print("is_same_size() 错误描述为：%s" % err)
            local_file_size = -1

        self.debug_print('local_file_size:%d  , remote_file_size:%d' % (local_file_size, remote_file_size))
        if remote_file_size == local_file_size:
            return 1
        else:
            return 0

    def download_file(self, local_file, remote_file):
        """从ftp下载文件
            参数:
                local_file: 本地文件

                remote_file: 远程文件
        """
        self.debug_print("download_file()---> local_path = %s ,remote_path = %s" % (local_file, remote_file))

        if self.is_same_size(local_file, remote_file):
            self.debug_print('%s 文件大小相同，无需下载' % local_file)
            return
        else:
            try:
                self.debug_print('>>>>>>>>>>>>下载文件 %s ... ...' % local_file)
                buf_size = 1024
                file_handler = open(local_file, 'wb')
                self.ftp.retrbinary('RETR %s' % remote_file, file_handler.write, buf_size)
                file_handler.close()
            except Exception as err:
                self.debug_print('下载文件出错，出现异常：%s ' % err)
                return

    def download_file_tree(self, local_path, remote_path):
        """从远程目录下载多个文件到本地目录
                       参数:
                         local_path: 本地路径

                         remote_path: 远程路径
        """
        print("download_file_tree()--->  local_path = %s ,remote_path = %s" % (local_path, remote_path))
        try:
            self.ftp.cwd(remote_path)
        except Exception as err:
            self.debug_print('远程目录%s不存在，继续...' % remote_path + " ,具体错误描述为：%s" % err)
            return

        if not os.path.isdir(local_path):
            self.debug_print('本地目录%s不存在，先创建本地目录' % local_path)
            os.makedirs(local_path)

        self.debug_print('切换至目录: %s' % self.ftp.pwd())

        self.file_list = []
        # 方法回调
        self.ftp.dir(self.get_file_list)

        remote_names = self.file_list
        self.debug_print('远程目录 列表: %s' % remote_names)
        for item in remote_names:
            file_type = item[0]
            file_name = item[1]
            local = os.path.join(local_path, file_name)
            if file_type == 'd':
                print("download_file_tree()---> 下载目录： %s" % file_name)
                self.download_file_tree(local, file_name)
            elif file_type == '-':
                print("download_file()---> 下载文件： %s" % file_name)
                self.download_file(local, file_name)
            self.ftp.cwd("..")
            self.debug_print('返回上层目录 %s' % self.ftp.pwd())
        return True

    def upload_file(self, local_file, remote_file):
        """从本地上传文件到ftp

           参数:
             local_path: 本地文件

             remote_path: 远程文件
        """
        if not os.path.isfile(local_file):
            self.debug_print('%s 不存在' % local_file)
            return

        if self.is_same_size(local_file, remote_file):
            self.debug_print('跳过相等的文件: %s' % local_file)
            return

        buf_size = 1024
        file_handler = open(local_file, 'rb')
        self.ftp.storbinary('STOR %s' % remote_file, file_handler, buf_size)
        file_handler.close()
        self.debug_print('上传: %s' % local_file + "成功!")

    def upload_file_tree(self, local_path, remote_path):
        """从本地上传目录下多个文件到ftp
           参数:

             local_path: 本地路径

             remote_path: 远程路径
        """
        if not os.path.isdir(local_path):
            self.debug_print('本地目录 %s 不存在' % local_path)
            return
        """
        创建服务器目录
        """
        try:
            self.ftp.cwd(remote_path)  # 切换工作路径
        except Exception as e:
            base_dir, part_path = self.ftp.pwd(), remote_path.split('/')
            for p in part_path[1:-1]:
                base_dir = base_dir + p + '/'  # 拼接子目录
                try:
                    self.ftp.cwd(base_dir)  # 切换到子目录, 不存在则异常
                except Exception as e:
                    print('INFO:', e)
                    self.ftp.mkd(base_dir)  # 不存在创建当前子目录
        self.ftp.cwd(remote_path)
        self.debug_print('切换至远程目录: %s' % self.ftp.pwd())

        local_name_list = os.listdir(local_path)
        self.debug_print('本地目录list: %s' % local_name_list)
        #self.debug_print('判断是否有服务器目录: %s' % os.path.isdir())

        for local_name in local_name_list:
            src = os.path.join(local_path, local_name)
            print("src路径=========="+src)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(local_name)
                except Exception as err:
                    self.debug_print("目录已存在 %s ,具体错误描述为：%s" % (local_name, err))
                self.debug_print("upload_file_tree()---> 上传目录： %s" % local_name)
                self.debug_print("upload_file_tree()---> 上传src目录： %s" % src)
                self.upload_file_tree(src, local_name)
            else:
                self.debug_print("upload_file_tree()---> 上传文件： %s" % local_name)
                self.upload_file(src, local_name)
        self.ftp.cwd("..")    #依据程序修改的
        self.ftp.cwd("..")
        self.ftp.cwd("..")
        self.ftp.cwd("..")
        self.ftp.cwd("..")

    def close(self):
        """ 退出ftp
        """
        self.debug_print("close()---> FTP退出")
        self.ftp.quit()
        self.log_file.close()

    def debug_print(self, s):
        """ 打印日志
        """
        self.write_log(s)

    def deal_error(self, e):
        """ 处理错误异常
            参数：
                e：异常
        """
        log_str = '发生错误: %s' % e
        self.write_log(log_str)
        sys.exit()

    def write_log(self, log_str):
        """ 记录日志
            参数：
                log_str：日志
        """
        time_now = time.localtime()
        date_now = time.strftime('%Y-%m-%d', time_now)
        format_log_str = "%s ---> %s \n " % (date_now, log_str)
        print(format_log_str)
        self.log_file.write(format_log_str)

    def get_file_list(self, line):
        """ 获取文件列表
            参数：
                line：
        """
        file_arr = self.get_file_name(line)
        # 去除  . 和  ..
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_file_name(self, line):
        """ 获取文件名
            参数：
                line：
        """
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr


# 读取我的海康威视库
HK_dll = windll.LoadLibrary("./HK_dll_lib_Proj/x64/Debug/HK_dll_lib.dll")

class HKVS_Camera_Record:
    def __init__(self,ip = '192.168.1.64',port = 8000,username = 'admin',password = 'a12345678',phone_port = "001" ):
        self.ip =  bytes(ip, "ascii")
        self.port = port
        self.username =  bytes(username, "ascii")
        self.password =  bytes(password, "ascii")
        self.phone_port = phone_port



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



config = configparser.ConfigParser() # 类实例化
# 配置文件路径
Ini_File_path = r'./System_Configuration_File.ini'

# 第一种读取ini文件方式,通过read方法
config.read(Ini_File_path,encoding='utf-8')
ALL_Cam_Rec_Number = int(config['Camera_Recording']['ALL_Cam_Rec_Number'])
print(ALL_Cam_Rec_Number)
print(type(ALL_Cam_Rec_Number))


FTP_IP = config['FTP']['FTP_Ip']
FTP_Port = int(config['FTP']['FTP_Port'])
FTP_username = config['FTP']['FTP_Username']
FTP_password = config['FTP']['FTP_Password']

print(FTP_IP,FTP_Port,FTP_username,FTP_password)

ALL_Camera_Num = []
#存储所有用户信息
for i_temp in range(ALL_Cam_Rec_Number):
    section   = 'Camera_user_0' + str(i_temp)
    ip        = config[section]['ip']
    port      = int(config[section]['port'])
    username  = config[section]['username']
    password  = config[section]['password']
    phone_port= config[section]['phone_port']
    Camera_Use_temp = HKVS_Camera_Record(ip,port,username,password,phone_port)
    ALL_Camera_Num.append(Camera_Use_temp)

print("摄像机总数",len(ALL_Camera_Num))



My_ftp = MyFTP(FTP_IP,FTP_Port)                 #创建我的FTP对象
My_ftp.login(FTP_username,FTP_password)  #登录FTP
ftp_status = 1


Voice_filename = []
Last_Voice_filename = []
user_id = []
temp = [1]
#根据有多少摄像机创建列表
for i in range(ALL_Cam_Rec_Number):
    user_id.append(i)
    Voice_filename.append(temp)
    Last_Voice_filename.append(temp)

del temp

#大循环确保程序一直运行
while True:

    HK_dll.HK_SDK_Init()  #摄像头sdk 初始化
    #大循环轮询处理各个端口
    for i_temp in range(ALL_Cam_Rec_Number):
        time.sleep(6)
        #登录摄像头
        print("i_temp = ",i_temp)
        user_id[i_temp] = HK_dll.HK_USER_Login(ALL_Camera_Num[i_temp].ip,ALL_Camera_Num[i_temp].port,ALL_Camera_Num[i_temp].username,ALL_Camera_Num[i_temp].password)

        #if ftp_status == 0 :
        My_ftp.login(FTP_username,FTP_password)  #登录FTP
        ftp_status = 1
        print(".....")
        #音频文件目录结构：D:\MD_recording\2021\202102\20210202\001
        local_day_time = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))   #得到今天的时间
        local_year = local_day_time[0:4]
        local_moth = local_day_time[5:7]
        local_days = local_day_time[8:10]
        try:
            #得到今天port端口该目录下的所有wav文件构成的文件列表
            Last_Voice_filename[i_temp] = Get_Voice_FileName("D:/MD_recording/"+local_year+"/"+local_year+local_moth+"/"+local_year+local_moth+local_days+"/"+ ALL_Camera_Num[i_temp].phone_port,".wav")
            print("Last_Voice_filename[i_temp] = ",Last_Voice_filename[i_temp])
        except:
            print("端口",ALL_Camera_Num[i_temp].phone_port,"录音文件夹异常")
            continue
        print("开始处理",ALL_Camera_Num[i_temp].phone_port,"端口")
        try :
            for v_f in Last_Voice_filename[i_temp] :
                if v_f not in Voice_filename[i_temp] :   #v_f是新增的音频文件
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
                    '''
                    if voice_type == 'ou':
                        voice_port = Now_Process_recording_file[19:22]
                        voice_phone_number = Now_Process_recording_file[26:-4]
                    else:
                        voice_port = Now_Process_recording_file[18:21]
                    '''

                    print("音频开始时间",voice_start_year,voice_start_mouth,voice_start_day,voice_start_hour,voice_start_minute,voice_start_second)

                    #读取音频
                    voice_audio = mpe.AudioFileClip("D:/MD_recording/"+local_year+"/"+local_year+local_moth+"/"+local_year+local_moth+local_days+"/"+ALL_Camera_Num[i_temp].phone_port+"/"+Now_Process_recording_file)

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

                    #创建一个保存从海康威视摄像头下载视频的文件夹
                    dirs = "D:/HK_Video/"+local_year+"/"+local_year+local_moth+"/"+local_year+local_moth+local_days+"/"+ALL_Camera_Num[i_temp].phone_port
                    if not os.path.exists(dirs):
                        os.makedirs(dirs)

                    SavePath_unico = dirs + "/" + Now_Process_recording_file + ".mp4"  #定义一个保存视频的文件名
                    SavePath_assii = bytes(SavePath_unico,"ascii")
                    #按时间从海康威视摄像头下载录像文件

                    download_flag = HK_dll.HK_GetFileByTime(user_id[i_temp],voice_start_year,voice_start_mouth,voice_start_day,voice_start_hour,voice_start_minute,voice_start_second,voice_end_year,voice_end_mouth,voice_end_day,voice_end_hour,voice_end_minute,voice_end_second,SavePath_assii)

                    if download_flag != 1:
                        print("download defeat")
                        #用户退出
                        HK_dll.HK_Logout(user_id[i_temp])
                        #释放海康威视sdk资源
                        HK_dll.HK_Cleanup()
                        time.sleep(3)
                        HK_dll.HK_SDK_Init()  #sdk 初始化
                        print("摄像头SDK重新初始化")
                        #登录摄像头
                        user_id[i_temp] = HK_dll.HK_USER_Login(ALL_Camera_Num[i_temp].ip,ALL_Camera_Num[i_temp].port,ALL_Camera_Num[i_temp].username,ALL_Camera_Num[i_temp].password)
                        print("重新登录摄像头")
                        raise Exception('下载失败！！抛出异常')
                        continue  #结束本次循环

                    download_flag = 0  #标志清除
                    #下载完成后进行音视频合成
                    video1 = mpe.VideoFileClip(SavePath_unico,audio = False,verbose = True)
                    #音视频合成
                    final = video1.set_audio(voice_audio)
                    dirs = "D:/MD_HK_OutPut_Video/"+local_year+"/"+local_year+local_moth+"/"+local_year+local_moth+local_days+"/"+ALL_Camera_Num[i_temp].phone_port
                    if not os.path.exists(dirs):
                        os.makedirs(dirs)

                    final.write_videofile(dirs+"/"+Now_Process_recording_file+"-output.mp4",codec= 'mpeg4' ,audio_codec='libvorbis')  #文件保存到本地
                    print("保存本地成功、开始FTP传输")
                    time.sleep(1)
                    try:
                        My_ftp.upload_file_tree(dirs+"/",dirs[2:]+"/")   #将文件由FTP上传至服务器  该函数会自动略过ftp服务器中相等的文件   #某次传输异常不要紧下次继续可以传输
                    except:
                        time.sleep(1)
                        print("FTP upload Error")
                        My_ftp.close()  #关闭FTP
                        #raise Exception('FTP 上传失败！！抛出异常')
                        #ftp_status = 0    
                        continue

        except (RuntimeError, TypeError, NameError):
            print("RuntimeError, or TypeError, or  NameError")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            continue
        else:
            Voice_filename[i_temp] = Last_Voice_filename[i_temp]   #若下载视频、处理视频、上传视频这些步骤都没有问题、则更新文件列表

        HK_dll.HK_Logout(user_id[i_temp])
    #释放海康威视sdk资源
    HK_dll.HK_Cleanup()
    time.sleep(3)



My_ftp.close()  #关闭FTP
#用户退出
HK_dll.HK_Logout(user_id)
#释放海康威视sdk资源
HK_dll.HK_Cleanup()





