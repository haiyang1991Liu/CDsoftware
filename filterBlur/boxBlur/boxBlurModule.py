# -*- coding：utf-8 -*—
# @Author : Haiyang Liu
# @Time : 24/2/21 4:32 下午
"""
    方框滤波
"""
import cv2
def boxBlur(gammaPath):
    #读取图像
    img=cv2.imread(gammaPath)
    #转换灰度图像
    img_gray=cv2.normalize(img,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
    #方框滤波
    #kernal size(1,3)
    boxFilter=cv2.boxFilter(img_gray,-1,(1,3))
    return boxFilter
