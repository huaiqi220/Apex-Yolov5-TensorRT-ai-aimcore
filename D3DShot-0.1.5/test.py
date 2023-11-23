import d3dshot.d3dshot as d3dshot
import time
import cv2
import torch 

model = torch.hub.load('.', 'custom', path='C:\\Users\\zhuzi\\Desktop\\yolov5\\runs\\train\\exp3\\weights\\best.pt',source='local')
model.conf = 0.4
hwnd_title = dict()

d = d3dshot.D3DShot()
while True:
    start_time = time.time()
    frame = d.screenshot(region=(960, 480, 960 + 640, 480 + 640))

    capture_time = time.time()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    
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
    cv2.imshow("result",frame)
    # cv2.resizeWindow("result",400,400)
    
    cv2.setWindowProperty("result", cv2.WND_PROP_TOPMOST, 1)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
    
    print("capture time : " + str(int(round(capture_time * 1000)) - int(round(start_time * 1000)))) 
    print("predict time : " + str(int(round(predict_deal_time * 1000)) - int(round(capture_time * 1000)))) 
    print("final time : " + str(int(round(final_time * 1000)) - int(round(predict_deal_time * 1000)))) 

d.stop()