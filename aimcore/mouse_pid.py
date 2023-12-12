import time
import pyautogui

class PID():
    Kp = 1.0
    Ki = 0.5
    Kd = 0.2
    tx = 0
    ty = 0
    last_error = 0.0
    integral = 0.0

    def __init__(self,Kp,Ki,Kd,Target_x,Target_y) -> None:
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.tx = Target_x
        self.ty = Target_y
        self.lx = 320
        self.ly = 320

    # def calculator(self,location):
    #     cur_x = cur_location[0]
    #     cur_y = cur_location[1]
    def calculator(self):
        cur_x = self.lx
        cur_y = self.ly
        error_x = self.tx - cur_x
        error_y = self.ty - cur_y
        self.integral += (error_x + error_y) * self.Ki

        # 计算微分项
        derivative_x = (error_x - self.last_error) * self.Kd
        derivative_y = (error_y - self.last_error) * self.Kd

        # 计算控制量
        output_x = self.Kp * error_x + self.integral + derivative_x
        output_y = self.Kp * error_y + self.integral + derivative_y

        self.lx = self.lx + output_x
        self.ly = self.ly + output_y

        self.last_error = error_x + error_y
        time.sleep(0.001)

        return [self.lx,self.ly,output_x,output_y]








def PID(paraP,paraI,paraD,dd_past,dd_now,dt,I_past):
    dd = [0,0]
    # dd_now[0]偏差量
    P = dd_now[0] * paraP
    I = I_past + dd_now[0] * paraI * dt
    # 抑制量
    D = (dd_now[0] - dd_past[0]) * paraD / dt
    # dd执行量
    dd[0] = P + I + D
    dd[1] = paraP * dd_now[1]
    return dd,I


















if __name__ == "__main__":
    pid = PID(0.2,1.0,0.005,400,450)

    while True:
        print(pid.calculator())
        pyautogui.moveTo



    



# # 设置PID控制器的参数
# Kp = 1.0  # 比例系数
# Ki = 0.5  # 积分系数
# Kd = 0.2  # 微分系数

# # 初始化误差
# last_error = 0.0
# integral = 0.0

# # 设置目标点
# target_x = 10.0
# target_y = 20.0

# # 初始化当前位置
# current_x = 0.0
# current_y = 0.0

# # 模拟控制循环
# while True:
#     # 计算当前误差
#     error_x = target_x - current_x
#     error_y = target_y - current_y

#     # 计算积分项
#     integral += (error_x + error_y) * Ki

#     # 计算微分项
#     derivative_x = (error_x - last_error) * Kd
#     derivative_y = (error_y - last_error) * Kd

#     # 计算控制量
#     output_x = Kp * error_x + integral + derivative_x
#     output_y = Kp * error_y + integral + derivative_y

#     # 更新位置
#     current_x += output_x
#     current_y += output_y

#     # 输出结果
#     print("x: {:.2f}, y: {:.2f}".format(current_x, current_y))

#     # 更新误差
#     last_error = error_x + error_y

#     # 等待一段时间
#     time.sleep(0.1)
