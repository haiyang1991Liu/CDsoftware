# coding:UTF-8
# 将导入图片 分成长38 宽20的方格
import os
import sys
import cv2
import numpy as np
import tkinter as tk
from PIL import Image

# 读取照片
# 获取root 目录路径
# 图像全黑
def create_black_background(img,width="",height=""):
    print("come into create_black_background fucntion")
    img2=Image.open(imagePath+r"image2.jpg")
    width,height=img2.size
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
    return img[i,j]

def subregion_image(image,outputPath):
    print("come into subregion function")
    width,height = image.size
    print(image.size)
    item_width_number = int(width/100)
    print("框长i:",item_width_number)
    item_width=width/item_width_number
    item_height_number = int(height/100)
    item_height=height/item_height_number
    print("框宽j:",item_height_number)
    box_list =[]
    for i in range(0,item_height_number):
        for j in range(0,item_width_number):
            box =(j*item_width,i*item_height,(j+1)*item_width,(i+1)*item_height)
            region = image.crop(box)
            # print(outputPath+'subregion/{}.{}.png'.format(i,j))
            region.save(outputPath+'subregion/{}_{}.png'.format(i,j),'PNG')
    return item_width_number,item_height_number
# 主函数
if __name__ == '__main__':
    print("come into main function")
    rootPath=os.path.abspath('..')
    print("根目录为：",rootPath)
    imagePath=rootPath+"/inputResources/"
    print("图片路径为：",imagePath)
    # print(imagePath+"image3")
    outputPath = rootPath+"/outputResults/"
    print("图片保存路径：",outputPath)
    # img=cv2.imread(imagePath+'image2.jpg')
    # img=Image.open(imagePath+r"image2.jpg")
    img1 =cv2.imread(imagePath+"image2.jpg")
    # width_number,height_number=subregion_image(img,outputPath)
    # print("打印长:",width_number)
    # print("打印宽:",height_number)
    ret_back=create_black_background(img1)
    print("ret_bakc:",ret_back)
