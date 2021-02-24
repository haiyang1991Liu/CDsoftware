import os
import sys
import cv2
import math
# 导入time模块
import time

import numpy as np
from PIL import Image
currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
rootPath=os.path.abspath('..')
print("根目录为：",rootPath)
# 读取第一张图片
img1 = cv2.imread(rootPath+"/outputResults/templateResults/back.jpg")
# 读取第二张图片(叠加范围图片）
img2 = cv2.imread(rootPath+"/outputResults/templateResults/median_skeleton.jpg")


# roi=img1[1033:1525,1:1598]
img2gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

img2gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
# 左坐标➕1，有坐标➖1 去边框

img2gray1[1034:1524,2:1597]=img2gray2[1034:1524,2:1597]
# cv2.imshow('res',img2gray1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.waitKey(1)

#算方格长宽数量范围，计算方格长宽多少
width,heights=img2gray2.shape
item_width_number = int(width/100)
print("框长i:",item_width_number)
item_width=width/item_width_number
item_height_number = int(heights/100)
item_height=heights/item_height_number
x=[]
#返回病害坐标
for i in range(0,item_height_number):
    for j in range(0,item_width_number):
        box =(j*item_width,i*item_height,(j+1)*item_width,(i+1)*item_height)
        sqrItem=img2gray1[i:(i+1)*int(item_height),j:(j+1)*int(item_width)]
        # region = img2gray1.crop(box)
        if sqrItem.__contains__(255):
            x.append(box)
            # print(box)

print(x)
