import time
from matplotlib import pyplot as plt
import numpy as np




class PID():
    Targetx = 100
    Targety = 100
    FLAG = False
    def __init__(self,Kp,Ki,Kd) -> None:
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.recentTime = 0
        self.Ix = 0
        self.Iy = 0
        pass

    def controller(self,Target_x, Target_y,current_time):
        if self.recentTime == 0:
            self.recentTime = int(round(time.time() * 1000)) - 2
        current_time = int(round(current_time* 1000))
        PControllerx = self.Kp * Target_x
        IControllerx = self.Ki * (current_time - self.recentTime) * Target_x + self.Ix
        self.Ix = IControllerx
        DControllerx = self.Kd * Target_x / (current_time - self.recentTime)

        Controllerx = PControllerx + IControllerx + DControllerx

        PControllery = self.Kp * Target_y
        IControllery = self.Ki * (current_time - self.recentTime) * Target_y + self.Iy
        self.Iy = IControllery
        DControllery = self.Kd * Target_y / (current_time - self.recentTime)
        self.recentTime = current_time

        Controllery = PControllery + IControllery + DControllery

        # time.sleep(0.002)
        return [Controllerx,Controllery,PControllerx,IControllerx,DControllerx,PControllery,IControllery,DControllery]
        
    # def setTarget(self,x,y):
    #     self.Targetx = x
    #     self.Targety = y

    def setTarget(x,y):
        PID.Targetx = x
        PID.Targety = y


# if __name__ == "__main__":
#     # pid = PID(0.5,0.001,0.01)
#     #pid = PID(0.7,0.0006,0.01)
#     pid = PID(0.9,0.0006,0.01)


#     cur_tx = 0
#     cur_ty = 0
#     cur_x = []
#     cur_y = []
#     targetx = 200
#     targety = 200
#     for i in range(10):
#         cont =  pid.controller(targetx - cur_tx,targety - cur_ty,time.time())
#         print(targetx -cur_tx)
#         cur_tx = cur_tx + cont[0]
#         print(targety -cur_ty)
#         cur_ty = cur_ty + cont[1]
#         # print(cur_tx)
#         cur_x.append(int(cur_ty))
#         # cur_y.append(target)
#     plt.axhline(y=targetx,linestyle="-.",)
#     plt.plot(cur_x,color='red')
#     plt.show()  