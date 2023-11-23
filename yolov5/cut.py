import os
os.getcwd()
os.add_dll_directory('C:\\Users\\zhuzi\\Desktop\\yolov5\\DXGI.pyd')
import DXGI
from ctypes import windll
import cv2
import numpy as np
windll.winmm.timeBeginPeriod(1)
stop = windll.kernel32.Sleep
import cv2
# 把DXGI.pyd 复制到当前路径

import torch

model = torch.hub.load('.', 'custom', path='C:\\Users\\zhuzi\\Desktop\\yolov5\\runs\\train\\exp3\\weights\\best.pt',source='local')
model.conf = 0.4
hwnd_title = dict()


g = DXGI.capture(0, 0, 320, 320)  # 屏幕左上角 到 右下角  （x1, y1 ,x2 ,y2)

while True:
    current_time = time.time()
    img = g.cap()
    img = np.array(img)
    # # 将图片转 BGR
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    t = time.time()
    print (int(round(t * 1000)))    #毫秒级时间戳

    results = model(frame)
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

    

