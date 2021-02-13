import os
import time


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




class HKVS_Camera_Record:
    def __init__(self,ip = '192.168.1.64',port = 8000,username = 'admin',password = 'a12345678',phone_port = "001" ):
        self.ip =  bytes(ip, "ascii")
        self.port = port
        self.username =  bytes(username, "ascii")
        self.password =  bytes(password, "ascii")
        self.phone_port = phone_port



localtime = time.localtime(time.time())

#得到该目录下所有.wav 组成的一个列表
#Voice_filename = Get_Voice_FileName("./VioceFile",".wav")

Voice_filename = []
Last_Voice_filename = []
user_id = []
temo = [5]
#根据有多少摄像机创建列表
for i in range(8):
    user_id.append(i)
    Voice_filename.append(temo)
    Last_Voice_filename.append(temo)

print(user_id)
print(Voice_filename[4])
print(Last_Voice_filename[3])




