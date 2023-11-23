import win32gui
from PyQt5.QtWidgets import QApplication
import sys
from PIL import Image
import numpy as np
import torch
import cv2
import

 
hwnd_title = dict()


 
 
def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
 
win32gui.EnumWindows(get_all_hwnd, 0)
# print(hwnd_title.items())
for h, t in hwnd_title.items():
    if t != "":
        print(h, t)
 
# 程序会打印窗口的hwnd和title，有了title就可以进行截图了。
hwnd = win32gui.FindWindow(None, 'C:\Windows\system32\cmd.exe')
app = QApplication(sys.argv)
while True:
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    size = img.size()
    s = img.bits().asstring(size.width() * size.height() * img.depth() // 8)  # format 0xffRRGGBB

    array = np.fromstring(s, dtype=np.uint8).reshape((size.height(), size.width(), img.depth() // 8))

    image = Image.fromarray(array)
    frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
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

    

