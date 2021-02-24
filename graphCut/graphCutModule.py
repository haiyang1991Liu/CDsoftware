# code:utf-8
import os
import sys
import cv2
# 导入time模块
import time
import numpy as np
sys.path.append("../usefulTools")
'''
    用于图像背景分割,所有命名都是驼峰命名法
'''


def regionCut(inputPath,coordinate,outputPath):
    # 打印时间为后续保存时间戳做准备
    currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print("图片保存路径：",inputPath)
    print("显示传入图片名称:",outputPath)
    print("显示传入坐标:",coordinate)
    # 读取图像
    img = cv2.imread(inputPath)
    imgorgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    mask = np.zeros(img.shape[:2],np.uint8)
    bgd = np.zeros((1,65),np.float64)
    fgd = np.zeros((1,65),np.float64)
    # 划定区域ff
    mask[coordinate[0]:coordinate[1],coordinate[2]:coordinate[3]]=1
    #函数返回值为mask,bgdModel,fgdModel
    cv2.grabCut(img,mask,None,bgd,fgd,5,cv2.GC_INIT_WITH_MASK)
    #0和2做背景
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    #使用蒙板来获取前景区域
    img = img*mask2[:,:,np.newaxis]
    cv2.imshow('cutgraph',img)
    cv2.imwrite(outputPath+"cutStep/img_{}.jpg".format(currentTime),img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    return "the region has been successfully cut"
if __name__=="__main__":
    # 测试主函
    # 测试文件夹地址
    coordinate=[0,908,457,693]
    outputPath="/Users/haiyang/Desktop/work/CDsoftware/outputResults"
    regionCut("/Users/haiyang/Desktop/work/CDsoftware/inputResources/image3.png",coordinate,outputPath)

