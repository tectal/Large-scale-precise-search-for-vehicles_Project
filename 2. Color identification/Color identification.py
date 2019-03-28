import cv2
import os
import numpy as np  
import Color dictionary 



def get_color(frame):
    # 将图片颜色转为HSV  
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maxsum = -100  
    color = None  
    color_dict = Color_identification.getColorList()
   
    for d in color_dict:
        # 使用cv2.inRange()函数进行背景颜色过滤
        mask = cv2.inRange(hsv,color_dict[d][0],color_dict[d][1])
        cv2.imwrite(d+'.jpg',mask)  
        # 将过滤后的颜色进行二值化处理
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        # 进行形态学腐蚀膨胀，cv2.dilate()
        binary = cv2.dilate(binary,None,iterations=2)
        img, cnts, hiera = cv2.findContours(binary.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        sum = 0  
        
        for c in cnts:  
            sum+=cv2.contourArea(c)  
        if sum > maxsum:
            # 统计不同颜色区域面积，如果使用某种颜色分量过滤背景后，出现车辆的轮廓且可视面积最大，则可认为车辆为该颜色
            maxsum = sum  
            color = d  
  
    return color  



def getallfiles1(path1):
    # 获取/Users/yangguofeng/Downloads/ML_Data/val文件夹中每张图片的地址并添加进list:allfile1
    allfile1 = []

    for root, dirs, files in os.walk(path1):
        for name in files:
            if name.endswith('jpg'):
                allfile1.append(os.path.join(root, name))

    return allfile1



def reasult(path1):
    allfile1 = getallfiles1(path1)
    print(allfile1)
    # 图片颜色识别结果list:num1
    num1 = []
    
    for img1 in allfile1:
        # 分别读取待识别颜色图片
        print(img1.split('/')[-1].split('.')[0])
        frame = cv2.imread(img1)
        num1.append(get_color(frame))
    
    return num1



if __name__ == '__main__':
    path1 = "/Users/yangguofeng/Downloads/ML_Data/val"
    num1 = reasult(path1)
    
    print(num1)



'''
# Different path
import sys
sys.path.append('../xxx')
from Color_identification2 import *

or

# Same path
from Color_identification2 import *
'''