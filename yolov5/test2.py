import win32gui
from PyQt5.QtWidgets import QApplication
import sys
from PIL import Image
import numpy as np
import torch
import cv2
import time

 
hwnd_title = dict()


model = torch.hub.load('.', 'custom', path='C:\\Users\\zhuzi\\Desktop\\yolov5\\runs\\train\\exp3\\weights\\best.pt',source='local')
model.conf = 0.4
 
 
import mss



with mss.mss() as sct:
    monitor = {'top': 0, 'left': 0, 'width': 2560, 'height': 1440}
    fps_time = time.time()
    n = 400
    while True:
        region = 960,480,640,640
        frame = np.array(sct.grab(region)) 
        # frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        results = model(frame)
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

        

