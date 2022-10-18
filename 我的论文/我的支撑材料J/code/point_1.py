import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# table 3 极坐标
img = np.zeros((600,600,3))
point = np.array(
    [
      [0, 0, 0, 0, 0, 0],
      [100, 0, 100, 0, 1, 0],
      [98, 40.10, 100, 40, 2, 0],
      [112, 80.21, 100, 80, 3, 0],
      [105, 119.75, 100, 120, 4, 0],
      [98, 159.86, 100, 160, 5, 0],
      [112, 199.96, 100, 200, 6, 0],
      [105, 240.07, 100, 240, 7, 0],
      [98, 280.17, 100, 280, 8, 0],
      [112, 320.28, 100, 320, 9, 0]
      ])
point_ = np.zeros((point.shape[0],2))
# x = rcos%,y=rsin%
# x^2 + y^2 = r^2, y/x = tan%
for i in range(point.shape[0]):
    point_[i,0] = point[i,0] * np.cos(np.deg2rad(point[i,1]))
    point_[i,1] = point[i,0] * np.sin(np.deg2rad(point[i,1]))
p_ = []
for i in range(1,5):
    x_ = 100*np.cos(np.deg2rad((i-1)*40))
    y_ = 100*np.sin(np.deg2rad((i-1)*40))
    p_.append([x_,y_])

plt.plot(x_, y_ )
plt.scatter(point_[:,0], point_[:,1], lw=1, label='Distribution of UAV')
plt.legend()
plt.show()
