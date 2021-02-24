# -*- coding：utf-8 -*—
# @Author : Haiyang Liu
# @Time : 24/2/21 1:50 下午
import os
import cv2
import time
import imutils
import numpy as np
from PIL import Image
from skimage import morphology, data, color
from skimage import img_as_float
from skimage import img_as_ubyte
"""
该模块用于将背景赋值成黑色
"""
def createBlackBackground(inputPath,outputPath):
    print("come into create_black_background fucntion")
    currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("图片输入路径:",inputPath)
    img =cv2.imread(inputPath)
    # 获取图片长宽高
    (height,width,depth) = img.shape
    print(type(img))
    print("width",width)
    print("height",height)
    for i in range(0,height):
        for j in range(0,width):
            # print("img{}.{}".format(i,j))
            img[i,j]=0
            # print("img{}.{}".format(i,j))
    cv2.imshow('res',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    retval = cv2.imwrite(outputPath+"templateResults/img_{}.jpg".format(currentTime),img)
    return retval