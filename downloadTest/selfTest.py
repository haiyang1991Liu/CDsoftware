import os
import cv2
import time
import imutils
import numpy as np
from PIL import Image
from skimage import morphology, data, color
from skimage import img_as_float
from skimage import img_as_ubyte

def create_black_background(img,width="",height=""):
    print("come into create_black_background fucntion")
    outputPath = rootPath+"/outputResults/"
    currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("图片保存路径：",outputPath)
    # img2=Image.open(imagePath+r"image6.jpg")
    # width,height=img2.size
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

def judgeImageChannel(img):
    print("进入judgeImageChannel函数")
    print(img.ndim)
    if img.ndim == 2:		#2维度表示长宽
        channels = 1 #单通道(grayscale)
        return channels
    elif img.ndim == 3:
        channels = img.shape[-1]	#第三维度表示通道，应为3
        if(channels != 3):	#应该是三才对
            return -1
    else:					#异常维度，不是图片了
        return "图片纬度异常"
currentTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

rootPath=os.path.abspath('..')
print("根目录为：",rootPath)
imagePath=rootPath+"/inputResources/"
outputPath = rootPath+"/outputResults/"
# 读取照片
# image =cv2.imread(imagePath+"image2.jpg")
# image = cv2.imread(imagePath+"image3.png")
# image =cv2.imread(imagePath+"image4.png")
# image = cv2.imread(imagePath+"image5.png")
image =cv2.imread(imagePath+"image6.jpg")
# 获取图片长宽高

(h,w,d) = image.shape
create_black_background(image,width=w,height=h)
image =cv2.imread(imagePath+"image6.jpg")
print("width={},height={},depth={}".format(w,h,d))

# 做区域裁剪
imgorgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
# 做淹膜
mask = np.zeros(image.shape[:2],np.uint8)
bgd = np.zeros((1,65),np.float64) #背景
fgd = np.zeros((1,65),np.float64) #前景
# 划定区域
# mask[ymin:ymax,xmin:xmax]=1
# mask[0:908,457:693]=1 #image3的划定区域
# mask[738:951,0:1682]=1 #image2的划定区域
mask[1033:1525,1:1598]=1 #image6的划定区域
# 函数返回值mask,bgdModel,fgdModel
cv2.grabCut(image,mask,None,bgd,fgd,5,cv2.GC_INIT_WITH_MASK)
# 0 和 2 做背景
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = image*mask2[:,:,np.newaxis]
cv2.imshow("裁剪图像",img)
print("裁剪图像")
#--- 在这里做输出---
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 生成自适应均横化图像
# 创建CLAHE 对象
clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
# 格式转换
# img_transfer=cv2.normalize(img,None,0,255,cv2.NORM_MINMAX, cv2.CV_8U)
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# 限制对比读的自适应域值均衡化
clahe_img = clahe.apply(img_gray)
cv2.imshow('clahe',clahe_img)
print("限制对比度，自适应均衡化")
# ---在这里做输出---
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# clahe_img=clahe_img*2
# clahe_img[clahe_img>255]=255
# # 数据类型转化
# outputStretch=np.round(clahe_img)
# outputStretch=outputStretch.astype(np.uint8)
# print("拉伸图片")
# cv2.imshow("stretch_img",outputStretch)
# # ---在这里做输出---
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.waitKey(1)
# 伽马转换
gamma = 0.3
# gamma = 0.6
# gamma=0.8
# gamma=0.9
# gamma=1
# 图像归一化
fI = clahe_img/255

gamma_img=np.power(fI,gamma)

# 显示原图和伽马转化的效果
cv2.imshow("gamma0.9",gamma_img)
print("伽马转化输出")
# ---在这里做输出---
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
img_gray=cv2.normalize(gamma_img,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
print(img_gray.dtype)
# 以下生成四种滤波结果( 方框、中值、双边, 高斯）
print(judgeImageChannel(img_gray))


#方框滤波->dst = cv2.boxFilter(src, ddepth,ksize,anchor,normalize,borderType)
boxFilter1_3=cv2.boxFilter(img_gray,-1,(1,3)) #kernel size (1,3)

#中值滤波

medianBlur7=cv2.medianBlur(img_gray,7)
#双边滤波
bilateralFilter=cv2.bilateralFilter(img_gray,25,50,100)

# 高斯
gaussBlur = cv2.GaussianBlur(img_gray, (5, 5), 0)
print("打印四种滤波结果")
cv2.imshow("gaussBlur",gaussBlur)
cv2.imshow("bilateralFilter",bilateralFilter)
cv2.imshow("boxFilter1*3",boxFilter1_3)
cv2.imshow("medianBlur7",medianBlur7)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
# 二值化转换
ret3, gauss_binary = cv2.threshold(gaussBlur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
ret3, medianBlur7_binary = cv2.threshold(medianBlur7, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
ret3, boxFilter1_3_binary = cv2.threshold(boxFilter1_3,0,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
print("gauss_ret3",ret3)
# median_binary = cv2.adaptiveThreshold(medianBlur7,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,3,3)
print("中值、双边、高斯的二值化转化")
cv2.imshow("gauss_binary",gauss_binary)
cv2.imshow("median_binary",medianBlur7_binary)
cv2.imshow("boxFilter1_3",boxFilter1_3_binary)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 画轮廓
gauss_canny = cv2.Canny(gauss_binary,75,255)
medianBlur_canny=cv2.Canny(medianBlur7_binary,75,255)
boxFilter1_3_canny=cv2.Canny(boxFilter1_3_binary,75,255)
print("打印画轮毅:")
cv2.imshow('meidan_Canny', medianBlur_canny)
cv2.imshow('boxFilter_Canny', boxFilter1_3_canny)
cv2.imshow('gauss_Canny', gauss_canny)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 画核 -- 形态学处理
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# 膨胀
dilated_gauss = cv2.dilate(gauss_canny, kernel, iterations=1)
dilated_median = cv2.dilate(medianBlur_canny,kernel,iterations=1)
dilated_box=cv2.dilate(boxFilter1_3_canny,kernel,iterations=1)
print("打印膨胀:")
cv2.imshow("Dilated gauss Image", dilated_gauss)
cv2.imshow("Dilated median Image", dilated_median)
cv2.imshow("Dilated box Image",dilated_box)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 先进行膨胀，在进行腐蚀操作
closed_gauss = cv2.morphologyEx(dilated_gauss, cv2.MORPH_CLOSE, kernel)
closed_median = cv2.morphologyEx(dilated_median, cv2.MORPH_CLOSE, kernel)
closed_box =cv2.morphologyEx(dilated_box, cv2.MORPH_CLOSE, kernel)
print("打印先膨胀在腐蚀的操作:")
cv2.imshow("Closed gauss Image", closed_gauss)
cv2.imshow("Closed median Image", closed_median)
cv2.imshow("Closed box Image", closed_box)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 找寻轮廓
contours, hierarchy = cv2.findContours(closed_gauss, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours1, hierarchy1= cv2.findContours(closed_median, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours2, hierarchy2= cv2.findContours(closed_box, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

print("打印寻找轮廓:")
cv2.imshow('gauss_contours', closed_gauss)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# print("number of contours:",contours)
# print("hierarchy:",hierarchy)

# area = []
# for index in range(len(contours)):
#     area.append(cv2.contourArea(contours[index]))
# max_index = np.argmax(area)
# max_area = cv2.contourArea(contours[max_index])
#
# for index in range(len(contours)):
#     if index != max_index:
#         cv2.fillPoly(closed, [contours[index]], 0)

# 打印连通contour
print("打印连通轮廓:")
cv2.imshow('connect closed gauss', closed_gauss)
cv2.imshow('connect closed median',closed_median)
cv2.imshow('connect closed box',closed_box)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

image = img_as_float(closed_gauss)
image1 = img_as_float(closed_median)
image2 = img_as_float((closed_box))

# 抽取骨架
gauss_skeleton = morphology.skeletonize(image)
median_skeleton = morphology.skeletonize(image1)
box_skeleton = morphology.skeletonize(image2)
print("打印抽取骨架")
gauss_skeleton_image = img_as_ubyte(gauss_skeleton)
median_skeleton_image =img_as_ubyte(median_skeleton)
box_skeleton_img=img_as_ubyte(box_skeleton)

cv2.imshow('gauss_skeleton', gauss_skeleton_image)
cv2.imshow('median_skeleton',median_skeleton_image)
cv2.imshow('box_skeleton',box_skeleton_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
retval = cv2.imwrite(outputPath+"templateResults/median_skeleton_{}.jpg".format(currentTime),median_skeleton_image)