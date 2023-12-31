import requests 
import sys
import json
import time
import math
import signal
import numpy as np
from .conn_db import *

ROBOTINOIP = "192.168.0.106"
PARAMS = {'sid':'example_circle'}
run = True

def signal_handler(sig, frame):
    global run
    print('You pressed Ctrl+C!')
    run = False
def rotate( vec, deg ):
    rad = 2 * math.pi / 360 * deg

    out = [0,0]

    out[0] = ( math.cos( rad ) * vec[0] - math.sin( rad ) * vec[1] )
    out[1] = ( math.sin( rad ) * vec[0] + math.cos( rad ) * vec[1] )

    return out
def set_vel(vel):
    OMNIDRIVE_URL = "http://" + ROBOTINOIP + "/data/omnidrive"
    r = requests.post(url = OMNIDRIVE_URL, params = PARAMS, json = vel )
    if r.status_code != requests.codes.ok:
        #print("Error: post to %s with params %s failed", OMNIDRIVE_URL, PARAMS)
        raise RuntimeError("Error: post to %s with params %s failed", OMNIDRIVE_URL, PARAMS)
def bumper():
    BUMPER_URL = "http://" + ROBOTINOIP + "/data/bumper"
    r = requests.get(url = BUMPER_URL, params = PARAMS)
    if r.status_code == requests.codes.ok:
        data = r.json()
        return data["value"]
    else:
        raise RuntimeError("Error: get from %s with params %s failed", BUMPER_URL, PARAMS)
def distances():
    DISTANCES_URL = "http://" + ROBOTINOIP + "/data/distancesensorarray"
    r = requests.get(url = DISTANCES_URL, params = PARAMS)
    if r.status_code == requests.codes.ok:
        data = r.json()
        return data
    else:
        raise RuntimeError("Error: get from %s with params %s failed", DISTANCES_URL, PARAMS)
def OdometryRead():
    ODOMETRY_URL = "http://" + ROBOTINOIP + "/data/odometry"
    r = requests.get(url = ODOMETRY_URL, params = PARAMS)
    if r.status_code == requests.codes.ok:
        data = r.json()
        return data
    else:
        raise RuntimeError("Error: get from %s with params %s failed", ODOMETRY_URL, PARAMS)
class PID:
    def __init__(self,kP,uAboveLimit,uUnderLimit):
        self.kP = kP
        self.uAboveLimit = uAboveLimit
        self.uUnderLimit = uUnderLimit
        
    def PidCal(self,Target,current):
        err = Target - current
        uP = self.kP * err
        u = uP
        
        if(u>self.uAboveLimit):
            u=self.uAboveLimit
        elif(u<self.uUnderLimit):
            u=self.uUnderLimit 
        else:
            u = u
        return u
# helper functions
def pt_to_pt_distance (pt1,pt2):
    distance = np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)
    return distance

# returns -1 if num is negative, 1 otherwise
def sgn (num):
  if num >= 0:
    return 1
  else:
    return -1
# Hàm sau nếu phát hiện hai biến bằng nhau thì xuất ra 
# Tại trong quá trình tính toán của MCU có thể xuất ra những giá trị xấp sỉ 
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
    elif (u>0 and equalCompare(v,0) == 1):
        return -1
    elif (u<0 and equalCompare(v,0) == 1):
        return -3
    elif (v<0 and equalCompare(u,0) == 1):
        return -2
    elif (v>0 and equalCompare(u,0) == 1):
        return -4
    else :
        return 0

def opstacleAvoid( CurrQuad):
    dis = distances()
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
        if HeadingDis[i] < 0.15: 
            Opsticle = 1
            break
        else :
            Opsticle = 0
    return Opsticle

path1 = np.array([[0,0],[0.5,0],[1,0.5],[2,-0.2],[3,0],[0,0]])
# path1 = np.array([[0,0],[0.5,0.5],[0,1],[-1,0],[0,-1],[0.5,-0.5],[0,0]])
#path1 = [[0.0, 0.0], [0.571194595265405, -0.4277145118491421], [1.1417537280142898, -0.8531042347260006], [1.7098876452457967, -1.2696346390611464], [2.2705328851607995, -1.6588899151216996], [2.8121159420106827, -1.9791445882187304], [3.314589274316711, -2.159795566252656], [3.7538316863009027, -2.1224619985315876], [4.112485112342358, -1.8323249172947023], [4.383456805594431, -1.3292669972090994], [4.557386228943757, -0.6928302521681386], [4.617455513800438, 0.00274597627737883], [4.55408382321606, 0.6984486966257434], [4.376054025556597, 1.3330664239172116], [4.096280073621794, 1.827159263675668], [3.719737492364894, 2.097949296701878], [3.25277928312066, 2.108933125822431], [2.7154386886417314, 1.9004760368018616], [2.1347012144725985, 1.552342808106984], [1.5324590525923942, 1.134035376721349], [0.9214084611203568, 0.6867933269918683], [0.30732366808208345, 0.22955002391894264], [-0.3075127599907512, -0.2301742560363831], [-0.9218413719658775, -0.6882173194028102], [-1.5334674079795052, -1.1373288016589413], [-2.1365993767877467, -1.5584414896876835], [-2.7180981380280307, -1.9086314914221845], [-3.2552809639439704, -2.1153141204181285], [-3.721102967810494, -2.0979137913841046], [-4.096907306768644, -1.8206318841755131], [-4.377088212533404, -1.324440752295139], [-4.555249804461285, -0.6910016662308593], [-4.617336323713965, 0.003734984720118972], [-4.555948690867849, 0.7001491248072772], [-4.382109193278264, 1.3376838311365633], [-4.111620918085742, 1.8386823176628544], [-3.7524648889185794, 2.1224985058331005], [-3.3123191098095615, 2.153588702898333], [-2.80975246649598, 1.9712114570096653], [-2.268856462266256, 1.652958931009528], [-1.709001159778989, 1.2664395490411673], [-1.1413833971013372, 0.8517589252820573], [-0.5710732645795573, 0.4272721367616211], [0, 0], [0.571194595265405, -0.4277145118491421]]
# path1 = np.array([[0,0],[0.5,0],[1,1],[1.5,0.5],[1,0],[-1.5,0.5],[1,-1],[0.5,0],[0,0]])
def osticaleAvoid2(v,u):
    alpha =np.arctan2(v,u)*180/np.pi

    # print(alpha)
    dis = distances()
    # print(dis)
    dis1 = dis[0]
    dis2 = dis[1]
    dis3 = dis[2]
    dis4 = dis[3]
    dis5 = dis[4]
    dis6 = dis[5]
    dis7 = dis[6]
    dis8 = dis[7]
    # dis8 = 0.4
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
        if HeadingDis[i] < 0.25: 
            Opsticle = 1
            break
        else :
            Opsticle = 0
    return Opsticle 


def pure_pursuit_step (path, currentPos, lookAheadDis, LFindex,LastgoalPt) :
    # goalPt = [0,0]
    goalPt = LastgoalPt
    #Đầu tiên là chúng ta sẽ lấy giá trị hiện tại của robot về để tính toán 
    currentX = currentPos[0]
    currentY = currentPos[1]
    #Cập nhật các biến lastIndex và startIndex để robot biết đã qua những đoạn đường nào 
    #Biến intersection 
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
        # Đoạn code tìm điểm cắt 
        if discriminant >= 0:
            # Tìm các điểm cắt trên đường thẳng
            sol_x1 = (D * dy + sgn(dy) * dx * np.sqrt(discriminant)) / dr**2
            sol_x2 = (D * dy - sgn(dy) * dx * np.sqrt(discriminant)) / dr**2
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
                or (equalCompare(sol_pt1[0],minX) == 1 or equalCompare(sol_pt1[0],maxX) == 1 
                or equalCompare(sol_pt1[1],minY) == 1 or equalCompare(sol_pt1[1],maxY) == 1) 
                or (minX <= sol_pt2[0] <= maxX and minY <= sol_pt2[1] <= maxY) 
                or (equalCompare(sol_pt2[0],minX) == 1 or equalCompare(sol_pt2[0],maxX) == 1 
                or equalCompare(sol_pt2[1],minY) == 1 or equalCompare(sol_pt2[1],maxY) == 1)) :
                intersectFound = True 

                # TH 1 : Nếu cả hai điểm ở trong đều ở trong khoảng điểm :
                if (
                ((minX <= sol_pt1[0] <= maxX and minY <= sol_pt1[1] <= maxY) 
                or (equalCompare(sol_pt1[0],minX) == 1 or equalCompare(sol_pt1[0],maxX) == 1 
                or equalCompare(sol_pt1[1],minY) == 1 or equalCompare(sol_pt1[1],maxY) == 1)) 
                and ((minX <= sol_pt2[0] <= maxX and minY <= sol_pt2[1] <= maxY) 
                or (equalCompare(sol_pt2[0],minX) == 1 or equalCompare(sol_pt2[0],maxX) == 1 
                or equalCompare(sol_pt2[1],minY) == 1 or equalCompare(sol_pt2[1],maxY) == 1))) :# Chúng ta sẽ kiểm tra xem điểm nào gần điểm tiếp theo cần đến trong quỷ đạo hơn :
                    if pt_to_pt_distance(sol_pt1, path[i+1]) < pt_to_pt_distance(sol_pt2, path[i+1]):
                        goalPt = sol_pt1
                    else:
                        goalPt = sol_pt2

                # TH2 : Nếu chỉ có 1 trong hai điểm nằm trong khoảng :
                else :
                    if (
                    (minX <= sol_pt1[0] <= maxX and minY <= sol_pt1[1] <= maxY) 
                    or (equalCompare(sol_pt1[0],minX) == 1 or equalCompare(sol_pt1[0],maxX) == 1 
                    or equalCompare(sol_pt1[1],minY) == 1 or equalCompare(sol_pt1[1],maxY) == 1) ):
                        goalPt = sol_pt1
                    else:
                        goalPt = sol_pt2
                
                # Tính xem là khoảng cách của setpoint tới điểm tiếp theo xem có gần hơn với vị trí robot hay không :
                # Thoát giữ index để biết là hiện tại đang ở đoạn nào 
                
                if pt_to_pt_distance (goalPt, path[i+1]) < pt_to_pt_distance ([currentX, currentY], path[i+1]):
                    lastFoundIndex = i
                    break
                else :
                    lastFoundIndex = i+1
                    # if (lastFoundIndex == len(path -1)):
                    #     goalPt = [path[lastFoundIndex][0], path[lastFoundIndex][1]]
                    #     break
            # Nếu không có điểm nào cắt :
            else :
                foundIntersection = False
                goalPt = [path[lastFoundIndex][0], path[lastFoundIndex][1]]

    # goalPt.append(path[lastFoundIndex][2])
    
    return goalPt,lastFoundIndex
    

def init():
    #Khai báo thông số Robot :
    global currentPos,lastFoundIndex,lookAheadDis
    lastFoundIndex = 0
    currentPos = [0, 0]
    lastFoundIndex = 0
    lookAheadDis = 0.15

    #Khai báo cờ phục vụ việc dừng robot :
    global msecsElapsed,goaltheta,msecStop,WaitFlag,StopFlag,EndFlag,DemonStrateFlag,msecDemon
    msecsElapsed = 0 
    goaltheta = 0
    msecStop= 0
    WaitFlag = 0
    StopFlag = 0
    EndFlag = 0
    msecDemon = 0
    DemonStrateFlag = 0
    
    #Khai báo thông số robot :
    global vec,pidX,pidY,pidTheta,goalPt
    vec = [0,0,0]
    pidX = PID(1.5,0.6,-0.6)
    pidY = PID(1.5,0.6,-0.6)
    pidTheta = PID(0.05,0.3,-0.3) 
    goalPt = [0,0]
    
def PathFollowing2(data):
    global msecsElapsed,goaltheta,msecStop,msecDemon,WaitFlag,StopFlag,EndFlag,DemonStrateFlag
    global currentPos,lastFoundIndex,lookAheadDis,goalPt,pathOdering
    global vec,pidX,pidY,pidTheta,goalPt
    try:
        Dataout = np.array(data)
        Dataout[:, 1] = -Dataout[:, 1]
        pathDesiried = Dataout.astype(float)
        pathDesiried*=0.4

        preErr = np.array([[0,0],[0,0]])
        returnCheckpointError = np.array([[1,0],[0,0]]).tolist()
        checkpoint = 0
        ErrorFlag = 0
        signal.signal(signal.SIGINT, signal_handler)
        init()     
        while False == bumper() and True == run:
            # Đọc ví trí robot từ bộ đo đường 
            OdoX = OdometryRead()[0] 
            OdoY = OdometryRead()[1] 
            OdoR = OdometryRead()[2]

            # Cập nhật vị trí robot để đưa vào tính toán 
            currentPos = [OdoX,OdoY]
            goalPt,lastFoundIndex = pure_pursuit_step (pathDesiried, currentPos, lookAheadDis, lastFoundIndex,goalPt)


            # Đưa thông số vào bộ PID để tính toán cho robot chạy bám theo quỷ đạo 
            u = pidX.PidCal(goalPt[0],OdoX)
            v = pidY.PidCal(goalPt[1],OdoY)
            goaltheta = 0
            
            
            # Sử dụng ma trận xoay để robot chạy xoay trên một đường thẳng 
            uControl = (math.cos(-OdoR)*u - math.sin(-OdoR)*v)
            vControl = (math.sin(-OdoR)*u + math.cos(-OdoR)*v)
            MoveFlag = osticaleAvoid2( vControl,uControl)

            vec[0] = uControl
            vec[1] = vControl
            vec[2] = pidTheta.PidCal(goaltheta,OdoR*180/math.pi)

            if(checkpoint < len(data)):
                if(abs(OdoX - pathDesiried[checkpoint,0])<0.15 and abs(OdoY - pathDesiried[checkpoint,1])<0.15):
                    returnCheckpoint = np.array(data[checkpoint]).tolist()
                    print("returnchekpoint",returnCheckpoint)
                    returnCheckpoint 
                    update_target_coordinates("Tensorbot",returnCheckpoint)
                    checkpoint += 1
                
                
            if (lastFoundIndex == len(pathDesiried)-1):
                if (abs(goalPt[0] - OdoX)<0.05 and abs(goalPt[1] - OdoY)<0.05 ):
                    if EndFlag == 0:
                        EndFlag = 1 
                else :
                    EndFlag = 0
                    msecStop = msecsElapsed

            if((checkpoint) < len(data)-1) and (MoveFlag == 1):
                ErrorFlag = 1
                returnCheckpointError =  np.array([data[checkpoint],data[checkpoint+1]]).tolist()
                print("returnCheckpointError", returnCheckpointError)
                update_target_coordinates("Tensorbot",returnCheckpointError[0])
                break
                    
            if (msecsElapsed - msecStop > 1000) and EndFlag == 1 :
                break
            time.sleep(0.05)
            msecsElapsed += 50
            
            set_vel(vec)
        pathOdering  = np.array([[0,0]])
        set_vel([0,0,0])
    except Exception as e:
        print(e)
        return 1
    if(ErrorFlag == 1):
        return returnCheckpointError
    else :
        return 0
    
def init():
    #Khai báo thông số Robot :
    global currentPos,lastFoundIndex,lookAheadDis
    lastFoundIndex = 0
    currentPos = [0, 0]
    lastFoundIndex = 0
    lookAheadDis = 0.15

    #Khai báo cờ phục vụ việc dừng robot :
    global msecsElapsed,goaltheta,msecStop,WaitFlag,StopFlag,EndFlag,DemonStrateFlag,msecDemon
    msecsElapsed = 0 
    goaltheta = 0
    msecStop= 0
    WaitFlag = 0
    StopFlag = 0
    EndFlag = 0
    msecDemon = 0
    DemonStrateFlag = 0
    
    #Khai báo thông số robot :
    global vec,pidX,pidY,pidTheta,goalPt
    vec = [0,0,0]
    pidX = PID(1.5,0.6,-0.6)
    pidY = PID(1.5,0.6,-0.6)
    pidTheta = PID(0.05,0.3,-0.3) 
    goalPt = [0,0]
    
def PathFollowing(data):
    global msecsElapsed,goaltheta,msecStop,msecDemon,WaitFlag,StopFlag,EndFlag,DemonStrateFlag
    global currentPos,lastFoundIndex,lookAheadDis,goalPt,pathOdering
    global vec,pidX,pidY,pidTheta,goalPt
    try:
        Dataout = np.array(data)
        Dataout[:, 1] = -Dataout[:, 1]
        pathDesiried = Dataout.astype(float)
        pathDesiried*=0.4
        
        signal.signal(signal.SIGINT, signal_handler)
        init()     
        while False == bumper() and True == run:
            # Đọc ví trí robot từ bộ đo đường 
            OdoX = OdometryRead()[0] 
            OdoY = OdometryRead()[1] 
            OdoR = OdometryRead()[2]

            # Cập nhật vị trí robot để đưa vào tính toán 
            currentPos = [OdoX,OdoY]
            goalPt,lastFoundIndex = pure_pursuit_step (pathDesiried, currentPos, lookAheadDis, lastFoundIndex,goalPt)
            print(goalPt)

            # Đưa thông số vào bộ PID để tính toán cho robot chạy bám theo quỷ đạo 
            u = pidX.PidCal(goalPt[0],OdoX)
            v = pidY.PidCal(goalPt[1],OdoY)
            goaltheta = 0
            
            
            # Sử dụng ma trận xoay để robot chạy xoay trên một đường thẳng 
            uControl = (math.cos(-OdoR)*u - math.sin(-OdoR)*v)
            vControl = (math.sin(-OdoR)*u + math.cos(-OdoR)*v)
            MoveFlag = opstacleAvoid( QuadRantCheck(uControl,vControl))
            
                
            if (lastFoundIndex == len(pathDesiried)-1):
                # print([msecStop,msecsElapsed,EndFlag])
                goalPt = pathDesiried[len(pathDesiried)-1]
                if (abs(goalPt[0] - OdoX)<0.05 and abs(goalPt[1] - OdoY)<0.05 ):
                    if EndFlag == 0:
                        EndFlag = 1 
                else :
                    EndFlag = 0
                    msecStop = msecsElapsed
                    
            if (msecsElapsed - msecStop > 1000) and EndFlag == 1 :
                break

            
            # Đưa độ lớn của 3 vector tính toán được vào mảng để điều khiển robot 
            if (MoveFlag == 0):
                vec[0] = uControl
                vec[1] = vControl
                vec[2] = pidTheta.PidCal(goaltheta,OdoR*180/math.pi)
            else :
                StopFlag = 1
                msecStop = msecsElapsed
            
            if StopFlag == 1 :
                vec[0] = 0
                vec[1] = 0
                vec[2] = 0
                if (msecsElapsed - msecStop > 1000):
                    StopFlag = 0

            # Thời gian lấy mẫu
            time.sleep(0.05)
            msecsElapsed += 50
            
            set_vel(vec)
        pathOdering  = np.array([[0,0]])
        set_vel([0,0,0])
    except Exception as e:
        print(e)
        return 1
    return 0


if __name__ == "__main__":
    # OriginPathFollow()
    # OriginPathFollow(path1,4)
    # backhome()
    print("Task Finished")
