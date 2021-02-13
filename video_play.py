
import os


#视频播放函数
def Video_Play(path):
    os.startfile(r".\OutPutVideoFile\\"+path)


#Video_Play("2021-01-25-08_34_38output.mp4")


dirs = "D:/HK_Video/2021/202102/20210202/002"
if not os.path.exists(dirs):
    os.makedirs(dirs)



'''
print 'Push "enter" to play movie'
raw_input()

def filename():
   filename = movie.mp4
   os.system("start " + filename)

open(filename)
'''