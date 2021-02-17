import mysql.connector

try :      
    mydb = mysql.connector.connect(
    host="47.107.236.236",       # 数据库主机地址
    user="junglyfly",    # 数据库用户名
    passwd="0121",   # 数据库密码
    database="hkvs_md_database"
    )
except:
    print("database connection error")

else :
    print("database connection ok")

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE sites (number INT(12),name VARCHAR(255), url VARCHAR(255))")



