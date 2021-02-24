# -*- coding：utf-8 -*—
# @Author : Haiyang Liu
# @Time : 24/2/21 1:50 下午

import cv2
"""
    双边过滤函数
"""
def bilateralBlur(gammaPath):
    #先读取图片
    img=cv2.imread(gammaPath)
    #转换灰度图像
    img_gray=cv2.normalize(img,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
    #双边滤波
    bilateralFilter=cv2.bilateralFilter(img_gray,25,50,100)
    return bilateralFilter