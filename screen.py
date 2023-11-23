import time
import os
from PIL import ImageGrab
import win32con
import win32gui
import win32print

current_path = os.getcwd()
save_path = os.path.join(current_path,"image")
print("本脚本用于apex数据采集, 每秒截取屏幕中央640 * 640 尺寸图像。")
print("游戏前打开, 游戏后关闭此脚本, 并将目录下image文件夹压缩发给三叶")

if not os.path.exists(save_path):
    os.makedirs(save_path)

def getScreenResolution():
        """
        得到屏幕的真实分辨率
        :return:
        """
        sx = win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPHORZRES)
        sy = win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPVERTRES)
        return sx, sy

width, height = getScreenResolution()
width =width / 2
height = height / 2
print(width,height)
bbox = (width - 320,height - 320,width + 320, height + 320)
while True:
    cur_screen = ImageGrab.grab(bbox)
    cur_screen.save(os.path.join(save_path,str(time.time()) + ".jpg"))
    print(str(time.time()) + ":  " + str(time.time()) + ".jpg" +"已保存")
    time.sleep(1)

