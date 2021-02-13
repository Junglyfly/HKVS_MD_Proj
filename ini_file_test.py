# 导包
import configparser

class HKVS_Camera_Record:
    def __init__(self,ip = '192.168.1.64',port = 8000,username = 'admin',password = 'a12345678',phone_port = "001" ):
        self.ip =  bytes(ip, "ascii")
        self.port = port
        self.username =  bytes(username, "ascii")
        self.password =  bytes(password, "ascii")
        self.phone_port = phone_port

config = configparser.ConfigParser() # 类实例化
# 定义文件路径
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

ALL_Camera_Use = []
print("vvv",len(ALL_Camera_Use))
#存储所有用户信息
for i_temp in range(ALL_Cam_Rec_Number):
    section   = 'Camera_user_0' + str(i_temp)
    ip        = config[section]['ip']
    port      = int(config[section]['port'])
    username  = config[section]['username']
    password  = config[section]['password']
    phone_port= config[section]['phone_port']
    Camera_Use_temp = HKVS_Camera_Record(ip,port,username,password,phone_port)
    ALL_Camera_Use.append(Camera_Use_temp)

print(len(ALL_Camera_Use))
print(ALL_Camera_Use[7].phone_port)

'''
# 第二种读取ini文件方式，通过get方法
value = config.get('select','url')
print('第二种方法读取到的值：',type(value))

# 第三种读取ini文件方式，读取到一个section中的所有数据，返回一个列表
value = config.items('connect_mysql')
print('第三种方法读取到的值：',value)




# 将数据写入到ini文件中
config.add_section('login') # 首先添加一个新的section
config.set('login','username','admin')  # 写入数据
config.set('login','password','123456') # 写入数据
config.write(open(path,'a'))            #保存数据

# 读取ini文件中所有的section
section = config.sections()
print(section)
'''
