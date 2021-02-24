# coding:utf-8
import os
import sys
import cv2
import math
# 导入time模块
import time
import numpy as np
sys.path.append("../usefulTools")
from usefulTools import ultra_modern
'''
    该脚本用于伽马转换
    伽马 大于0 and 小于1的时候（如果图像整体或者感兴趣区域较暗，可以增加图像对比度，
    如果图像整体或者感兴趣区域较亮，大于1，则正价对比度）
'''
def gammaTransfer(inputPath,outputPath):
    currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    #读取图片
    retval=ultra_modern(inputPath)
    print(retval)
    img = cv2.imread(retval)
    # 生成自适应均横化图像
    # 创建CLAHE 对象
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    # 格式转换
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # 限制对比读的自适应域值均衡化
    clahe_img = clahe.apply(img_gray)
    cv2.imshow('clahe',clahe_img)
    print("限制对比度，自适应均衡化")
    # ---在这里做输出---
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    # 图像虚化比
    gamma = 0.7
    # 图像归一化
    fI = clahe_img/255
    gamma_output=np.power(fI, gamma)
    # 显示原图和伽马变化后的效果
    cv2.imshow("original",img)
    cv2.imshow("gamma0.7",gamma_output)

    print("打印gamma 照片的type",gamma_output.dtype)
    # 打印输出后float64 图像显示不了 要做图像格式转化
    img_transfer=cv2.normalize(gamma_output,None,0,255,cv2.NORM_MINMAX, cv2.CV_8U)
    print("打印输出路径:",outputPath+"/gammaStep/")
    cv2.imwrite(outputPath+"/gammaStep/{}.jpg".format(currentTime),img_transfer)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    return "gammaTransfer script has been done"


if __name__=="__main__":
    # 测试主函
    # 测试文件夹地址
    outputPath="/Users/haiyang/Desktop/work/CDsoftware/outputResults"
    cutstepPath = os.path.abspath('..')+"/outputResults/cutStep/"
    print("打印图片剪切保存路径",cutstepPath)
    retval=gammaTransfer(cutstepPath,outputPath)
    print(retval)