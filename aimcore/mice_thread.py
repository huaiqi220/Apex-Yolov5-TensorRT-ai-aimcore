import threading
import pid
import time
import mouseController



def controller_thread():
    pid_class = pid.PID(0.7,0.0006,0.01)
    log = open("pid.log","w+")
    log.write("targetx targety x y px ix dx py iy dy")

    while True:
        # if pid.PID.FLAG and abs(pid.PID.Targetx) > 3 and abs(pid.PID.Targety) > 3:
        if pid.PID.FLAG :
            cont = pid_class.controller(pid_class.Targetx,pid_class.Targety,time.time())
            line = " ".join([str(pid.PID.Targetx),str(pid.PID.Targety),str(cont[0]),str(cont[1]),str(cont[2]),str(cont[3]),str(cont[4]),str(cont[5]),str(cont[6]),str(cont[7])])
            log.write(line + "\n")
            # 给五个像素的提前量
            movex = int(cont[0])
            if movex > 5:
                movex = movex + 5
            elif movex < -5:
                movex = movex - 5

            mouseController.Logitech.mouse.move(int(cont[0]),int(cont[1]))
            pid.PID.setTarget(pid_class.Targetx - int(cont[0]),pid_class.Targety - int(cont[1]))
            print(cont)
        time.sleep(0.00001)



if __name__ == "__main__":
    thread1 = threading.Thread(target=controller_thread,args=(),daemon=True)
    thread1.start()
    time.sleep(1)
    pid.PID.setTarget(300,0)
    time.sleep(1)
    pid.PID.setTarget(200,0)
    time.sleep(1)