import requests
import sys
import json
import time 
import math
import signal
import numpy as np


class robot():
    def __init__(self,IP,PARAM,radius):
        self.ip = IP
        self.Param = PARAM
        self.lookAheadDis = radius
        self.run = False 

    def signal_handler(sig, frame):
        global run
        print('You pressed Ctrl+C!')
        run = False
    
    def set_vel(self,vel):
        OMNIDRIVE_URL = "http://" + self.ip + "/data/omnidrive"
        r = requests.post(url = OMNIDRIVE_URL, params = self.Param, json = vel )
        if r.status_code != requests.codes.ok:
            #print("Error: post to %s with params %s failed", OMNIDRIVE_URL, PARAMS)
            raise RuntimeError("Error: post to %s with params %s failed", OMNIDRIVE_URL, self.Param)
    
    def bumper(self):
        BUMPER_URL = "http://" + self.ip + "/data/bumper"
        r = requests.get(url = BUMPER_URL, params = self.Param)
        if r.status_code == requests.codes.ok:
            data = r.json()
            return data["value"]
        else:
            raise RuntimeError("Error: get from %s with params %s failed", BUMPER_URL, self.Param)
        
    def distances(self,):
        DISTANCES_URL = "http://" + self.ip + "/data/distancesensorarray"
        r = requests.get(url = DISTANCES_URL, params = self.Param)
        if r.status_code == requests.codes.ok:
            data = r.json()
            return data
        else:
            raise RuntimeError("Error: get from %s with params %s failed", DISTANCES_URL, self.Param)
    
    def OdometryRead(self):
        ODOMETRY_URL = "http://" + self.ip + "/data/odometry"
        r = requests.get(url = ODOMETRY_URL, params = self.Param)
        if r.status_code == requests.codes.ok:
            data = r.json()
            return data
        else:
            raise RuntimeError("Error: get from %s with params %s failed", ODOMETRY_URL, self.param)
        
    def pt_to_pt_distance (pt1,pt2):
        distance = np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)
        return distance
    
    def sgn (num):
        if num >= 0:
            return 1
        else:
            return -1
    
    def equalCompare(Value,ComValue):
        if(abs(Value - ComValue) < 0.0001):
            return 1
        else :
            return 0
        

    def QuadRantCheck(u,v):
        if(u>0 and v < 0) :
            return 1
        elif (u<0 and v <0) :
            return 2
        elif (u<0 and v >0):
            return 3
        elif (u>0 and v>0) :
            return 4
        elif (u>0 and robot.equalCompare(v,0) == 1):
            return -1
        elif (u<0 and robot.equalCompare(v,0) == 1):
            return -3
        elif (v<0 and robot.equalCompare(u,0) == 1):
            return -2
        elif (v>0 and robot.equalCompare(u,0) == 1):
            return -4
        else :
            return 0
    
    def opstacleAvoid(self,CurrQuad):
        dis = robot.distances()
        dis1 = dis[0]
        dis2 = dis[1]
        dis3 = dis[2]
        dis4 = dis[3]
        dis5 = dis[4]
        dis6 = dis[5]
        dis7 = dis[6]
        dis8 = dis[7]
        dis9 = dis[8]
        Opsticle = 0
        if (CurrQuad == -1):
            HeadingDis = [dis2,dis1,dis9]
        elif (CurrQuad == 1):
            HeadingDis = [dis1,dis9,dis8]
        elif (CurrQuad == -2):
            HeadingDis = [dis9,dis8,dis7]
        elif (CurrQuad == 2):
            HeadingDis = [dis8,dis7,dis6]
        elif (CurrQuad == -3):
            HeadingDis = [dis6,dis5]
        elif (CurrQuad == 3):
            HeadingDis = [dis5,dis4,dis3]
        elif (CurrQuad == -4):
            HeadingDis = [dis4,dis3,dis2]
        elif (CurrQuad == 4):
            HeadingDis = [dis3,dis2,dis1]
        else:
            return 0
            
        for i in range(len(HeadingDis)):
            if HeadingDis[i] < 0.3: 
                Opsticle = 1
                break
            else :
                Opsticle = 0
        return Opsticle 
        
    def osticaleAvoid2(self,v,u):
        alpha =np.arctan2(v,u)*180/np.pi

        # print(alpha)
        dis = robot.distances(self)
        # print(dis)
        dis1 = dis[0]
        dis2 = dis[1]
        dis3 = dis[2]
        dis4 = dis[3]
        dis5 = dis[4]
        dis6 = dis[5]
        dis7 = dis[6]
        dis8 = dis[7]
        # dis8 = 
        dis9 = dis[8]
        Opsticle = 0
        if (20>=alpha>-20):
            # print("ss1")
            HeadingDis = [dis1]
        elif (20<=alpha<60):
            # print("ss2")
            HeadingDis = [dis2]
        elif (60<=alpha<100):
            # print("ss3")
            HeadingDis = [dis3]
        elif (100<=alpha<140):
            # print("ss4")
            HeadingDis = [dis4]
        elif (140<=alpha<180)or(-180< alpha <= -140):
            # print("ss56")
            HeadingDis = [dis6,dis5]
        elif (-140<=alpha<-100):
            # print("ss7")
            HeadingDis = [dis7]
        elif (-100<=alpha<-60):
            # print("ss8")
            HeadingDis = [dis8]
        elif (-60<=alpha<-20):
            # print("ss9")
            HeadingDis = [dis9]
        else:
            return 0

        
        for i in range(len(HeadingDis)):
            if HeadingDis[i] < 0.15: 
                Opsticle = 1
                break
            else :
                Opsticle = 0
        return Opsticle 

    def pure_pursuit_step(self,path,CurrentPos,LFindex) :
        goalPt = [0,0]
        currentX = CurrentPos[0]
        currentY = CurrentPos[1]
        lookAheadDis = self.lookAheadDis
        lastFoundIndex = LFindex
        intersection = False
        startingIndex = lastFoundIndex
        for i in range (startingIndex,len(path) - 1):
        # Các điểm 1 2 lần lượt là các điểm ở trong mảng path sẽ tạo ra các đường thẳng 
            x1 = path[i][0] - currentX
            y1 = path[i][1] - currentY
            x2 = path[i+1][0] - currentX
            y2 = path[i+1][1] - currentY
            # Các công thức tính ra khoảng cách giữa hai điểm
            # Và công thức xác định xem có cắt đường tròn không
            dx = x2 - x1
            dy = y2 - y1
            dr = math.sqrt (dx**2 + dy**2)
            D = x1*y2 - x2*y1
            # discriminant để xác định xem có cắt vào đường tròn hay không
            # discriminant > 0 có cắt 
            # discriminant < 0 không cắt
            # discriminant = 0 tiếp tuyến
            discriminant = (lookAheadDis**2) * (dr**2) - D**2
            if discriminant >= 0:
                # Tìm các điểm cắt trên đường thẳng
                sol_x1 = (D * dy + robot.sgn(dy) * dx * np.sqrt(discriminant)) / dr**2
                sol_x2 = (D * dy - robot.sgn(dy) * dx * np.sqrt(discriminant)) / dr**2
                sol_y1 = (- D * dx + abs(dy) * np.sqrt(discriminant)) / dr**2
                sol_y2 = (- D * dx - abs(dy) * np.sqrt(discriminant)) / dr**2

                # Đưa các điểm tìm được vào mảng và đưa nó về toạ độ thực bằng cách cộng vào các trục thực
                sol_pt1 = [sol_x1 + currentX, sol_y1 + currentY]
                sol_pt2 = [sol_x2 + currentX, sol_y2 + currentY]

                #Xác định các giá trị X Y mút giữa hai điểm trên quỷ đạo để xác định xem điểm cắt có nằm trong khoảng đó hay không
                minX = min(path[i][0], path[i+1][0])
                minY = min(path[i][1], path[i+1][1])
                maxX = max(path[i][0], path[i+1][0])
                maxY = max(path[i][1], path[i+1][1])
                # Xác định xem có điểm nào trong khoảng giữa hai điểm hay không
                # Nếu có thì kích biến intersectFound lên 1
                if (
                    (minX <= sol_pt1[0] <= maxX and minY <= sol_pt1[1] <= maxY) 
                    or (robot.equalCompare(sol_pt1[0],minX) == 1 or robot.equalCompare(sol_pt1[0],maxX) == 1 
                    or robot.equalCompare(sol_pt1[1],minY) == 1 or robot.equalCompare(sol_pt1[1],maxY) == 1) 
                    or (minX <= sol_pt2[0] <= maxX and minY <= sol_pt2[1] <= maxY) 
                    or (robot.equalCompare(sol_pt2[0],minX) == 1 or robot.equalCompare(sol_pt2[0],maxX) == 1 
                    or robot.equalCompare(sol_pt2[1],minY) == 1 or robot.equalCompare(sol_pt2[1],maxY) == 1)) :
                    intersectFound = True 
                    # TH 1 : Nếu cả hai điểm ở trong đều ở trong khoảng điểm :
                    if (
                    (minX <= sol_pt1[0] <= maxX and minY <= sol_pt1[1] <= maxY) 
                    or (robot.equalCompare(sol_pt1[0],minX) == 1 or robot.equalCompare(sol_pt1[0],maxX) == 1 
                    or robot.equalCompare(sol_pt1[1],minY) == 1 or robot.equalCompare(sol_pt1[1],maxY) == 1) 
                    and (minX <= sol_pt2[0] <= maxX and minY <= sol_pt2[1] <= maxY) 
                    or (robot.equalCompare(sol_pt2[0],minX) == 1 or robot.equalCompare(sol_pt2[0],maxX) == 1 
                    or robot.equalCompare(sol_pt2[1],minY) == 1 or robot.equalCompare(sol_pt2[1],maxY) == 1)) :# Chúng ta sẽ kiểm tra xem điểm nào gần điểm tiếp theo cần đến trong quỷ đạo hơn :
                        if robot.pt_to_pt_distance(sol_pt1, path[i+1]) < robot.pt_to_pt_distance(sol_pt2, path[i+1]):
                            goalPt = sol_pt1
                        else:
                            goalPt = sol_pt2

                    # TH2 : Nếu chỉ có 1 trong hai điểm nằm trong khoảng :
                    else :
                        if (
                        (minX <= sol_pt1[0] <= maxX and minY <= sol_pt1[1] <= maxY) 
                        or (robot.equalCompare(sol_pt1[0],minX) == 1 or robot.equalCompare(sol_pt1[0],maxX) == 1 
                        or robot.equalCompare(sol_pt1[1],minY) == 1 or robot.equalCompare(sol_pt1[1],maxY) == 1) ):
                            goalPt = sol_pt1
                        else:
                            goalPt = sol_pt2
                    
                    # Tính xem là khoảng cách của setpoint tới điểm tiếp theo xem có gần hơn với vị trí robot hay không :
                    # Thoát giữ index để biết là hiện tại đang ở đoạn nào 
                    
                    if robot.pt_to_pt_distance (goalPt, path[i+1]) < robot.pt_to_pt_distance ([currentX, currentY], path[i+1]):
                        lastFoundIndex = i
                        # goalPt = [path[lastFoundIndex][0], path[lastFoundIndex][1]]
                        break
                    else :
                        if (lastFoundIndex == len(path)-1):
                            goalPt = [path[lastFoundIndex][0], path[lastFoundIndex][1]]
                        lastFoundIndex = i+1
                # Nếu không có điểm nào cắt :
                else :
                    foundIntersection = False
                    goalPt = [path[lastFoundIndex][0], path[lastFoundIndex][1]]
        
        
        return goalPt,lastFoundIndex