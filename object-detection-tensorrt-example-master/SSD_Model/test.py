import tensorrt as trt
import numpy as np
import cv2

import pycuda.autoinit
import pycuda.driver as cuda
import time
import utils.inference as inference
import cv2
import torch
import time
import numpy as np

model = torch.hub.load('.', 'custom', path='C:\\Users\\zhuzi\\Desktop\\yolov5\\runs\\train\\exp3\\weights\\best.pt',source='local')
model.conf = 0.4

cap = cv2.VideoCapture(0)

fps_time = time.time()


while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    img_cvt = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = model(img_cvt)
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
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


