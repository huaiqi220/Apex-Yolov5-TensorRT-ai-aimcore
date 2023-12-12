from ctypes import *
import cv2
import numpy as np
import numpy.ctypeslib as npct
import d3dshot.d3dshot as d3dshot
import time
import os

# os.getcwd()
# os.add_dll_directory(r'D:\\zhuzi\\Documents\\yolov5\\build\\Debug\\DXGI.pyd')
# import DXGI
# g = DXGI.capture(960, 480, 960 + 640, 480 + 640) 


class Detector():
    def __init__(self,model_path,dll_path):
        self.yolov5 = CDLL(dll_path,winmode=0)
        self.yolov5.Detect.argtypes = [c_void_p,c_int,c_int,POINTER(c_ubyte),npct.ndpointer(dtype = np.float32, ndim = 2, shape = (50, 6), flags="C_CONTIGUOUS")]
        self.yolov5.Init.restype = c_void_p
        self.yolov5.Init.argtypes = [c_void_p]
        self.yolov5.cuda_free.argtypes = [c_void_p]
        self.c_point = self.yolov5.Init(model_path)

    def predict(self,img):
        rows, cols = img.shape[0], img.shape[1]
        res_arr = np.zeros((50,6),dtype=np.float32)
        self.yolov5.Detect(self.c_point,c_int(rows), c_int(cols), img.ctypes.data_as(POINTER(c_ubyte)),res_arr)
        self.bbox_array = res_arr[~(res_arr==0).all(1)]
        return self.bbox_array

    def free(self):
        self.yolov5.cuda_free(self.c_point)

def visualize(img,bbox_array):
    for temp in bbox_array:
        bbox = [temp[0],temp[1],temp[2],temp[3]]  #xywh
        clas = int(temp[4])
        score = temp[5]
        cv2.rectangle(img,(int(temp[0]),int(temp[1])),(int(temp[0]+temp[2]),int(temp[1]+temp[3])), (105, 237, 249), 2)
        img = cv2.putText(img, "class:"+str(clas)+" "+str(round(score,2)), (int(temp[0]),int(temp[1])-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (105, 237, 249), 1)
    return img

# det = Detector(model_path=b"./best.engine",dll_path="./yolov5.dll")  # b'' is needed
# d = d3dshot.D3DShot()
# while True:
#     start_time = time.time()

#     # frame = g.cap()
#     # frame = np.array(frame)
#     frame = d.screenshot(region=(960, 480, 960 + 640, 480 + 640))
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
#     capture_time = time.time()

    
#     results = det.predict(frame)
#     print(results)
#     predict_deal_time = time.time()
#     frame = visualize(frame,results)

#     final_time = time.time()
#     fps_txt = 1/(final_time - start_time)
#     cv2.putText(frame,str(round(fps_txt,2)),(50,50),cv2.FONT_ITALIC,1,(0,255,0),2)
#     cv2.imshow("result",frame)
    
#     cv2.setWindowProperty("result", cv2.WND_PROP_TOPMOST, 1)
#     show_time = time.time()
#     if cv2.waitKey(10) & 0xFF == ord("q"):
#         break
    
#     print("capture time : " + str(int(round(capture_time * 1000)) - int(round(start_time * 1000)))) 
#     print("predict time : " + str(int(round(predict_deal_time * 1000)) - int(round(capture_time * 1000)))) 
#     print("final time : " + str(int(round(final_time * 1000)) - int(round(predict_deal_time * 1000)))) 
#     print("show time : " + str(int(round(show_time * 1000)) - int(round(final_time * 1000)))) 

# d.stop()