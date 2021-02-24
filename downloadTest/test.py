import os
import cv2
import time
import imutils
import numpy as np
from skimage import morphology, data, color
from skimage import img_as_float
from skimage import img_as_ubyte

currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

rootPath=os.path.abspath('..')
print("根目录为：",rootPath)
imagePath=rootPath+"/inputResources/"
# 读取照片
image = cv2.imread(imagePath+"image3.png")

# 获得图片长宽高
(h, w, d) = image.shape
print("width={}, height={}, depth={}".format(w, h, d))

# image = cv2.resize(image,None,fx=0.2,fy=0.05)

#把图片转化成灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_copy = image.copy()
print("打灰度转化图像像:")
cv2.imshow('show', gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 生成自己适应均衡化
cache = cv2.createCLAHE(3, (8, 8))
dst = cache.apply(gray)
print("打印自适应均衡化图像:")
cv2.imshow('CLAHE', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 高斯过滤
gauss = cv2.GaussianBlur(image, (3, 3), 0)
print("打印高斯过滤:")
cv2.imshow('Gaus', gauss)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 画轮毂
canny = cv2.Canny(gauss, 75, 255)
print("打印画轮毅:")
cv2.imshow('Canny', canny)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 画核 -- 形态学处理
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 膨胀
dilated = cv2.dilate(canny, kernel, iterations=1)
print("打印膨胀:")
cv2.imshow("Dilated Image", dilated)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 打印腐蚀

erode = cv2.erode(canny, kernel, iterations=1)
print("打印腐蚀")
cv2.imshow('erode', erode)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 先进行膨胀，在进行腐蚀操作
closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
print("打印先膨胀在腐蚀的操作:")
cv2.imshow("Closed", closed)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 找寻轮廓
contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


#cv2.drawContours(closed, contours, -1, (0, 255, 255), 1)
print("打印寻找轮廓:")
cv2.imshow('contours', closed)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
print("number of contours:",contours)
print("hierarchy:",hierarchy)

area = []
for index in range(len(contours)):
    area.append(cv2.contourArea(contours[index]))
max_index = np.argmax(area)
max_area = cv2.contourArea(contours[max_index])

for index in range(len(contours)):
    if index != max_index:
        cv2.fillPoly(closed, [contours[index]], 0)

# 打印连通contour
print("打印连通轮廓:")
cv2.imshow('connect area', closed)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

image = img_as_float(closed)

# 抽取骨架
skeleton = morphology.skeletonize(image)
print("打印抽取骨架")
v_image = img_as_ubyte(skeleton)
cv2.imshow('skeleton', v_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
