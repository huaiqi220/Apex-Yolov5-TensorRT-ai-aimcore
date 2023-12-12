import win32con
import win32gui
import win32print
import math


def getScreenResolution():
        """
        得到屏幕的真实分辨率
        :return:
        """
        sx = win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPHORZRES)
        sy = win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPVERTRES)
        return sx, sy




def getDistance(center,target):
     """
     计算目标离准心距离
     """
     return math.sqrt(pow(target[0] - center[0],2) + pow(target[1] - center[1],2))



def chooseWho2Die(target_bbox,center):
    """"
    get model results
    choose the most closed one
    return bbox xyxy

    根据模型输出结果，综合自瞄逻辑，输出唯一目标
    
    """
    MIN_TARGET_SIZE = 100
    MIN_SCORE = 0.4
    # print(target_bbox)
    target_bbox = [target for target in target_bbox if target[4] == 1 and target[5] > MIN_SCORE]

    


    # 100像素都没有的目标不锁
    # 置信度太低目标不锁
    
    # print(target_bbox)

    if len(target_bbox) == 0:
        """
        场景无敌人，不移动鼠标
        """

        return [-1,-1]


    if len(target_bbox) == 1:
        """
        only one target
        只有一个目标
        """
        target = target_bbox[0]
        bbox = [target[0],target[1],target[2],target[3]] # xywh

        return [bbox[0] + bbox[2] / 2 , bbox[1] + bbox[3] / 2]
    
    cur_distance = 200
    cur_target = [-1,-1]
    for target in target_bbox:
        bbox = [target[0],target[1],target[2],target[3]] # xywh
        location = [bbox[0] + bbox[2] / 2 , bbox[1] + bbox[3] / 2]
        if bbox[2] * bbox[3] < MIN_TARGET_SIZE:
            continue
        
        dis = getDistance(center,location)
        """
        目前策略，太小不锁，锁离准心最近的
        """
        if dis < cur_distance:
             cur_target = location


    return cur_target




