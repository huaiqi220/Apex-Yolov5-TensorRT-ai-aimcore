from ctypes import *
import cv2
import numpy as np
import numpy.ctypeslib as npct
import d3dshot.d3dshot as d3dshot
import time
import os
import aim
from python_trt import Detector,visualize
import pyautogui
import mouseController
os.getcwd()
os.add_dll_directory(r'D:\\zhuzi\\Desktop\\aimcore\\DXGI.pyd')
import DXGI
g = DXGI.capture(960, 480, 960 + 640, 480 + 640) 

det = Detector(model_path=b"./best.engine",dll_path="./yolov5.dll")  # b'' is needed
while True:
    start_time = time.time()

    frame = g.cap()
    frame = np.array(frame)
    capture_time = time.time()

    
    results = det.predict(frame)
    target = aim.chooseWho2Die(results,[320,320])
    print(target)
    if target != [-1,-1]:
        mouseController.Logitech.mouse.move(int(target[0] -320),int(target[1] - 320))
    
    predict_deal_time = time.time()
    frame = visualize(frame,results)

    final_time = time.time()
    fps_txt = 1/(final_time - start_time)
    cv2.putText(frame,str(round(fps_txt,2)),(50,50),cv2.FONT_ITALIC,1,(0,255,0),2)
    cv2.imshow("result",frame)
    
    cv2.setWindowProperty("result", cv2.WND_PROP_TOPMOST, 1)
    show_time = time.time()
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
    

