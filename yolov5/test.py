import d3dshot.d3dshot as d3dshot
import time
import cv2
import win32api
import win32con


model = torch.hub.load('.', 'custom', path='C:\\Users\\zhuzi\\Desktop\\yolov5\\runs\\train\\exp3\\weights\\best.engine',source='local')
model.conf = 0.4
hwnd_title = dict()


def PID(paraP,paraI,paraD,dd_past,dd_now,dt,I_past):
    dd = [0,0]
    P = dd_now[0] * paraP
    I = I_past + dd_now[0] * paraI * dt
    D = (dd_now[0] - dd_past[0]) * paraD / dt
    dd[0] = P + I + D
    dd[1] = paraP * dd_now[1]
    return dd,I

deskx = int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN)/2)
desky = int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN)/2)

top = int(desky - 320)
left = int(deskx - 320)

rate = 0.2
width_after = 400
heighe_after = int(640 * width_after / 640)
cn = [320,320]

yzpare = 0.5
flag = -1
div = 2


I = 0
dd = [0,0]
dt = 0.03























d = d3dshot.D3DShot()
while True:
    start_time = time.time()
    frame = d.screenshot(region=(960, 480, 960 + 640, 480 + 640))

    capture_time = time.time()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

    
    results = model(frame)

    predict_deal_time = time.time()

    results_ = results.pandas().xyxy[0].to_numpy()
    i = 0
    for box in results_:
        l,t,r,b = box[:4].astype('int')
        confidence = str(round(box[4]*100,2))+"%"
        cls_name = box[6]

        if cls_name == "partner":
            i += 1
        cv2.rectangle(frame,(l,t),(r,b),(0,255,0),2)
        cv2.putText(frame,cls_name + "-" + confidence,(l,t),cv2.FONT_ITALIC,1,(255,0,0),2)
    
    cv2.putText(frame, "person:"+str(i), (10, 20), cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

    final_time = time.time()
    fps_txt = 1/(final_time - start_time)
    cv2.putText(frame,str(round(fps_txt,2)),(50,50),cv2.FONT_ITALIC,1,(0,255,0),2)
    cv2.imshow("result",frame)
    # cv2.resizeWindow("result",400,400)
    
    cv2.setWindowProperty("result", cv2.WND_PROP_TOPMOST, 1)
    show_time = time.time()
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
    
    print("capture time : " + str(int(round(capture_time * 1000)) - int(round(start_time * 1000)))) 
    print("predict time : " + str(int(round(predict_deal_time * 1000)) - int(round(capture_time * 1000)))) 
    print("final time : " + str(int(round(final_time * 1000)) - int(round(predict_deal_time * 1000)))) 
    print("show time : " + str(int(round(show_time * 1000)) - int(round(final_time * 1000)))) 

d.stop()