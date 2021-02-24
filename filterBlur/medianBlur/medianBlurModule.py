# -*- coding：utf-8 -*—
# @Author : Haiyang Liu
# @Time : 24/2/21 1:50 下午
import cv2
"""
    中值滤波
"""
def medianBlur(gammaPath):
    #读取图像
    img=cv2.imread(gammaPath)
    #转换灰度图像
    img_gray=cv2.normalize(img,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
    #中值滤波
    medianFilter=cv2.medianBlur(img_gray,7)
    return medianFilter
