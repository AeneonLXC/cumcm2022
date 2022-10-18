import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# table 3 极坐标

n = 10
v_0 = np.random.rand(10)*5
desired_dis = np.zeros((n,n))

def polar(r0,th0):
    #极坐标转换为直角坐标 
    x_ = r0*np.cos(np.deg2rad((th0)))
    y_ = r0*np.sin(np.deg2rad((th0)))
    return x_,y_

def dis(x0,y0,x1,y1):
    #欧氏距离求解
    return np.sqrt(np.square(x0 - x1) + np.square(y0 - y1))

def p_ij(point,i,j):
    #势函数 chan算法
    r0 = point[int(point[i,4]),0]
    th0 = point[int(point[i,4]),1]
    r1 = point[int(point[j,4]),0]
    th1 = point[int(point[j,4]),1]
    
    x0, y0 = polar(r0, th0)
    x1, y1 = polar(r1, th1)
    
    x_ij = dis(x0, y0, x1, y1)
    
    r00 = point[int(point[j,5]),0]
    th00 = point[int(point[j,5]),0]
    
    x00, y00 = polar(r00, th00)
    d_ij = desired_dis[j,int(point[j,5])]
    
    return np.log(np.square(x_ij)) + np.square(d_ij) / np.square(x_ij)
    
def uav(point,i,tv,ts,vc,sc):
    vi = point[int(point[i,4]),6]
    s = point[int(point[i,4]),1]
    
    point[int(point[i,4]),7] = vi * np.cos(np.deg2rad(s)) + point[int(point[i,4]),0]
    point[int(point[i,4]),8] = vi * np.sin(np.deg2rad(s)) + point[int(point[i,4]),0]
    point[int(point[i,4]),6] = (1 / tv) * (vc - vi)
    point[int(point[i,4]),1] = (1 / ts) * (sc - s) + s
    
    x = point[int(point[i,4]),7]
    y = point[int(point[i,4]),8]
    v = point[int(point[i,4]),6]
    s = point[int(point[i,4]),1]
    return x,y,v,s

def solve_uav(point,i,tv,ts):
    #鸽群模型转uav
    s = point[int(point[i,4]),1]
    vi = point[int(point[i,4]),6]
    ui_1 = vi * np.cos(np.deg2rad(point[int(point[i,4]),9]))
    ui_2 = vi * np.sin(np.deg2rad(point[int(point[i,4]),10]))
    
    point[int(point[i,4]),9] = ui_1
    point[int(point[i,4]),10] = ui_2
    
    vc = (tv * (ui_1 * np.cos(np.deg2rad(s)) + ui_2 * np.sin(np.deg2rad(s)))) + vi
    sc = ((ts / vi) * (ui_2 * np.cos(np.deg2rad(s)) - ui_1 * np.sin(np.deg2rad(s)))) + s + 0.01
        
    return vc,sc

def ui_12(point,i,kp,kv,pij,w1):
    xi_1 = point[int(point[i,4]),7]
    xi_2 = point[int(point[i,4]),8]
    
    ui_1 = point[int(point[i,4]),9]
    ui_2 = point[int(point[i,4]),10]
    ui_0 = point[int(point[0,4]),10]
    
    vi_1 = (-kp * xi_1 * pij * np.random.randn(1)[0]  - kv * ui_1 - (ui_1 - ui_0) * w1) + ui_1
    vi_2 = (-kp * xi_2 * pij * np.random.randn(1)[0] - kv * ui_2 - (ui_2 - ui_0) * w1) + ui_2
    point[int(point[i,4]),9] = vi_1
    point[int(point[i,4]),10] = vi_2
    # return vi_1,vi_2

tv = 3
ts = 0.75
kv = 1
kp = 120
w1 = 0.1

epoch = 1000
point = np.array(
    [
      [0, 0, 0, 0, 0, 0, v_0[0], 0, 0, 0, 0],
      [100, 0, 100, 0, 1, 0, v_0[1], 0, 0, 0, 0],
      [98, 40.10, 100, 40, 2, 0, v_0[2], 0, 0, 0, 0],
      [112, 80.21, 100, 80, 3, 0, v_0[3], 0, 0, 0, 0],
      [105, 119.75, 100, 120, 4, 0, v_0[4], 0, 0, 0, 0],
      [98, 159.86, 100, 160, 5, 0, v_0[5], 0, 0, 0, 0],
      [112, 199.96, 100, 200, 6, 0, v_0[6], 0, 0, 0, 0],
      [105, 240.07, 100, 240, 7, 0, v_0[7], 0, 0, 0, 0],
      [98, 280.17, 100, 280, 8, 0, v_0[8], 0, 0, 0, 0],
      [112, 320.28, 100, 320, 9, 0, v_0[9], 0, 0, 0, 0]
      ])
while epoch:
    img = np.ones((600,600,3))

    
    for i in range(desired_dis.shape[0]):
        for j in range(desired_dis.shape[0]):
            x0 = point[i,0]
            y0 = point[i,1]
            x1 = point[i,2]
            y1 = point[i,3]
            desired_dis[i,j] = dis(x0,y0,x1,y1)
            
    for i in range(1,point.shape[0]):
        for j in range(i,point.shape[0]):
            x_, y_ = polar(point[int(point[i,4]),8],point[int(point[i,4]),1])
            x0, y0 = polar(point[0,0],point[0,1])
            cv.circle(img, (int(x_ + 200),int(y_ + 200)), 2, (0,0,255),-1)
            cv.circle(img, (int(x0 + 200),int(y0 + 200)), 100, (0,0,0),2)
            cv.imshow("not people air", img)
            cv.waitKey(50)
            pij = p_ij(point, i, j)
            vc,sc = solve_uav(point, i, tv, ts)
            x,y,v,s = uav(point,i,tv,ts,vc,sc)
            # ui_12(point, i, kp, kv, pij, w1)
        print(vc,sc)
    epoch -= 1
    cv.imshow("not people air", img)
