import os
import time
os.getcwd()
os.add_dll_directory(r'D:\\zhuzi\\Documents\\yolov5\\build\\Debug\\DXGI.pyd')
from ctypes import windll
import cv2
import numpy as np

# 把DXGI.pyd 复制到当前路径
import DXGI
g = DXGI.capture(0, 0, 640, 640) 
import datetime

 # 屏幕左上角 到 右下角  （x1, y1 ,x2 ,y2)

while True:
    current_time = time.time()
    img = g.cap()
    img = np.array(img)
    # # 将图片转 BGR
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    t = time.time()
    print (int(round(t * 1000)))    #毫秒级时间戳


    

