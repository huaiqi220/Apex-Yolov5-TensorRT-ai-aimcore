from pynput import mouse
from threading import Thread
from ctypes import *
import d3dshot.d3dshot as d3dshot
import os
import aim
from python_trt import Detector,visualize
import time
import numpy as np
import cv2
import mouse_pid
import pid
import threading
import mice_thread

def init():
    os.getcwd()
    os.add_dll_directory(r'D:\\zhuzi\\Desktop\\aimcore\\DXGI.pyd')

    import DXGI
    g = DXGI.capture(960, 480, 960 + 640, 480 + 640) 

    det = Detector(model_path=b"./best-5_9_2.engine",dll_path="./yolov5.dll")  # b'' is needed

    return det,g


def listen():
    print("开始监听前侧键")
    def on_click(x, y, button, pressed):
        global FLAG
        if button == mouse.Button.x2 and pressed:
            pid.PID.FLAG = not pid.PID.FLAG
            
    
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

class ListenThread(Thread):

    def __init__(self):
        super().__init__()
    
    def run(self):
        listen()



    
if __name__ == "__main__":
    print("启动监听进程")
    listenThread = ListenThread()
    listenThread.start()

    print("启动控制进程")
    thread1 = threading.Thread(target=mice_thread.controller_thread,args=(),daemon=True)
    thread1.start()

    det,g = init()
    while True:
        start_time = time.time()

        frame = g.cap()
        frame = np.array(frame)
        capture_time = time.time()
        results = det.predict(frame)
        target = aim.chooseWho2Die(results,[320,320])
        print(target)
        if target != [-1,-1] :
            target_location = [int(target[0] -320),int(target[1] - 320)]
            pid.PID.setTarget(target_location[0],target_location[1])
        
        predict_deal_time = time.time()
        controller_time = predict_deal_time
        frame = visualize(frame,results)

        final_time = time.time()
        fps_txt = 1/(final_time - start_time)
        print(fps_txt)
        cv2.putText(frame,str(round(fps_txt,2)),(50,50),cv2.FONT_ITALIC,1,(0,255,0),2)
        cv2.imshow("result",frame)
        
        cv2.setWindowProperty("result", cv2.WND_PROP_TOPMOST, 1)
        show_time = time.time()
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
