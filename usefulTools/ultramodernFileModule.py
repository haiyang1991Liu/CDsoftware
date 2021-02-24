# code:utf-8
import os
import sys
"""
    该模块用于文件夹内最新的文件
"""
def ultramodern(search_folder):
    print(search_folder)
    lists = os.listdir(search_folder)
    # 列出目录的下所有问价和文件夹保存到lists
    print(lists)
    # 按时间顺序排序
    lists.sort(key=lambda fn:os.path.getmtime(search_folder+fn))
    #获取最新的文件保存到file_new
    file_new=os.path.join(search_folder,lists[-1])
    print(file_new)
    return file_new
def judgeImageChannel(img):
    print("进入judgeImageChannel函数")
    print(img.ndim)
    if img.ndim == 2:               #2维度表示长宽
        channels = 1                #单通道(grayscale)
        return channels
    elif img.ndim == 3:
        channels = img.shape[-1]	#第三维度表示通道，应为3
        if(channels != 3):	        #应该是三才对
            return -1
    else:					        #异常维度，不是图片了
        return "图片纬度异常"

if __name__=="__main__":
    # 测试主函
    # 测试文件夹地址
    cutstepPath = os.path.abspath('..')+"/outputResults/cutStep/"
    print("打印图片剪切保存路径",cutstepPath)
    retval=ultramodern(cutstepPath)
    print(retval)