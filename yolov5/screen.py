import time
import os
from PIL import ImageGrab
import win32con
import win32gui
import win32print
import torch
import cv2
import numpy as np

model = torch.hub.load('.', 'custom', path='C:\\Users\\zhuzi\\Desktop\\yolov5\\runs\\train\\exp3\\weights\\best.pt',source='local')
model.conf = 0.4

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
    fps_time = time.time()
    cur_screen = ImageGrab.grab(bbox)
    # cur_screen.save(os.path.join(save_path,str(time.time()) + ".jpg"))
    # print(str(time.time()) + ":  " + str(time.time()) + ".jpg" +"已保存")
    frame = cv2.cvtColor(np.asarray(cur_screen), cv2.COLOR_RGB2BGR)
    results = model(cur_screen)
    # print(results.pandas().xyxy[0].to_numpy())# tensor-to-numpy
    results_ = results.pandas().xyxy[0].to_numpy()
    i = 0
    for box in results_:
        l,t,r,b = box[:4].astype('int')
        confidence = str(round(box[4]*100,2))+"%"
        cls_name = box[6]

        if cls_name == "person":
            i += 1
        cv2.rectangle(frame,(l,t),(r,b),(0,255,0),2)
        cv2.putText(frame,cls_name + "-" + confidence,(l,t),cv2.FONT_ITALIC,1,(255,0,0),2)
    cv2.putText(frame, "person:"+str(i), (10, 20), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

    now = time.time()
    fps_txt = 1/(now - fps_time)
    fps_time = now

    cv2.putText(frame,str(round(fps_txt,2)),(50,50),cv2.FONT_ITALIC,1,(0,255,0),2)

    cv2.imshow("result",frame)
    # cv2.resizeWindow("result",400,400)
    
    cv2.setWindowProperty("result", cv2.WND_PROP_TOPMOST, 1)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

