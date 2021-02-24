#! /usr/bin/env3.7/python
# -*- coding：utf-8 -*—
# @Author : Haiyang Liu
# @Time : 24/2/21 1:50 下午


import os
import sys
import cv2
import math
# 导入time模块
import time
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
"""
如果要import 一个不同目录的文件，
首先需要使用sys.path.append 方法将b.py 所在的目录加入到
搜索目录中，然后进行import，for example：import sys.path.append('c:\\xxx\\b.py')
"""
"""
控制主函数脚本
"""

sys.path.append("./graphCut")
sys.path.append("./usefulTools")
sys.path.append("./gammaTrans")
sys.path.append("./blackBackground")
sys.path.append("./filterBlur")
from blackBackground import create_black_background
from graphCut import region_cut
from gammaTrans import gamma_transfer
from usefulTools import ultra_modern
from filterBlur import *
root_path=os.path.abspath('.')
print("当前根路径:"+root_path)
# 选中图片进行裁剪
# 这里面定下俩个便利 直接获取裁剪坐标和配套图片名称
# 测试主函
# 这里需要有段代码，让图对应裁剪坐标

# 测试图片和坐标代码
coordinate=[0,908,457,693]
outputPath=root_path+"/outputResults"
inputPath =root_path+"/inputResources/image3.png"

# 先把照片赋值成黑色
ret_black_str=create_black_background(inputPath,outputPath)
# 裁剪
ret_cut_str=region_cut(inputPath,coordinate,outputPath)

#伽马转化-包含了灰度直方图自适均值化
cutstepPath = root_path+"/outputResults/cutStep/"
ret_gamma_str = gamma_transfer(cutstepPath,outputPath)

#中值、双边、高斯过滤
if ret_gamma_str:
    print("进入过滤")
    gammaPath=root_path+"/outputResults/gammaStep/"
    # 找到路径中最新生成的文件
    retPath = ultra_modern(gammaPath)
    print(retPath)
    ret_bilater_filter=bilateral_blur(retPath)
    ret_median_filter=median_blur(retPath)
    ret_gauss_filter=gauss_blur(retPath)
    ret_box_filter=box_blur(retPath)
else:
    print("something wrong in gammastep")
print("打印四种滤波结果")
cv2.imshow("gaussBlur",ret_gauss_filter)
cv2.imshow("bilateralBlur",ret_bilater_filter)
cv2.imshow("boxFilter1*3",ret_box_filter)
cv2.imshow("medianBlur",ret_median_filter)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 二值化转换
ret_gauss, gauss_binary = cv2.threshold(ret_gauss_filter, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
ret_median, median_binary = cv2.threshold(ret_median_filter, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
ret_box, box_binary = cv2.threshold(ret_box_filter,0,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
ret_bilater, bilater_binary=cv2.threshold(ret_bilater_filter,0,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
print("gauss_ret",ret_gauss)
print("meodian_ret",ret_median)
print("box_ret",ret_box)
print("bilater_ret",ret_bilater)
print("中值、双边、高斯的二值化转化")
cv2.imshow("gauss_binary",gauss_binary)
cv2.imshow("median_binary",median_binary)
cv2.imshow("box_binary",box_binary)
cv2.imshow("bilater_binary",bilater_binary)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)


"""
<-- 界面 -->
"""
# class Application():
#     def __init__(self):
#         # 创建主窗口
#         self.window=tk.Tk()
#         # 设定窗口显示大小
#         self.window.geometry('800x800')
#         # 设置窗口最小值
#         self.window.minsize(500,500)
#         self.window.title("横纵裂痕展示界面")
#         # 添加主件
#         self.addComponents()
#         # 进入消息循环,主窗口循环显示    z
#         self.window.mainloop()
#
#         # 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，
#         # 如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，
#         # mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，
#         # 所以我们必须要有循环所有的窗口文件都必须有类似的mainloop函数，
#         # mainloop是窗口文件的关键的关键
#
#     def button_clicked(self):
#         print("按钮被摁了")
#     def addComponents(self):
#         my_frame = tk.Frame(self.window)
#         my_frame.pack(side=tk.TOP)
#         # 创建按钮
#         my_button = tk.Button(my_frame,text="点我",command=self.button_clicked)
#         my_button.pack(side=tk.LEFT)
#         # 创建canvas
#         my_Canvas=tk.Canvas(my_frame,bg="white")
#         my_Canvas.create_rectangle(50,50,150,150,outline='red',fill="blue",width=5)
#         my_Canvas.pack(side=tk.RIGHT)
#
#         #创建复选框
#         my_apple=tk.Checkbutton(my_frame,text="苹果")
#         my_apple.pack(side=tk.TOP)
#
#         #创建单行文本
#         name=tk.Label(my_frame,text='姓名')
#         name.pack(side=tk.LEFT)
#         name_value=tk.Entry(my_frame,bd=5)
#         name_value.pack(side=tk.RIGHT)
#
#
#
# if __name__=="__main__":
#     Application()