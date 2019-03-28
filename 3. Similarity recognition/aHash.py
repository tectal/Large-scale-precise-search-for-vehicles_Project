import os
import operator
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps



# 平均哈希算法
# 基于比较灰度图每个像素与平均值来实现的，最适用于缩略图，放大图搜索。



# 计数器
total = 0
# 相似度结果list，未排序
num1 = []



def getCode(img,size):
	# 遍历将像素添加进list:pixel
	pixel = []
	
	for x in range(0,size[0]):
		for y in range(0,size[1]):
			pixel_value = img.getpixel((x,y))
			pixel.append(pixel_value)

	# 计算平均值： 计算进行灰度处理后图片的所有像素点的平均值。
	avg = sum(pixel)/len(pixel)

	cp = []

	for px in pixel:
		# 比较像素灰度值：遍历灰度图片每一个像素，如果大于平均值记录为1，否则为0。
		if px > avg:
			cp.append(1)
		else:
			cp.append(0)

	return cp



def compCode(code1,code2):
	# 对比指纹：计算两幅图片的指纹，计算汉明距离（从一个指纹到另一个指纹需要变几次），汉明距离越大则说明图片越不一致，反之，汉明距离越小则说明图片越相似，当距离为0时，说明完全相同。
	num = 0
	
	for index in range(0,len(code1)):
		if code1[index] != code2[index]:
			num+=1
	
	return num 



def classfiy_aHash(image1,image2,size=(8,8),exact=25):
	# 缩放图片：为了保留结构去掉细节，去除大小、横纵比的差异，把图片统一缩放到8*8，共64个像素的图片。
	# 转化为灰度图：把缩放后的图片转化为灰度图。
	# 得到信息指纹：组合64个bit位，顺序随意保持一致性即可。
	image1 = image1.resize(size).convert('L').filter(ImageFilter.BLUR)
	image1 = ImageOps.equalize(image1)
	code1 = getCode(image1, size)
	image2 = image2.resize(size).convert('L').filter(ImageFilter.BLUR)
	image2 = ImageOps.equalize(image2)
	code2 = getCode(image2, size)

	assert len(code1) == len(code2),"error"
	
	return compCode(code1, code2)



def getallfiles2(path2):
	# 按预测model高低顺序依次对文件夹内的图片读取200照片并将其地址储存在list:allfile2
	allfile2 = []
	
	for root, dirs, files in os.walk(path2):
		for name in files:
			if name.endswith('jpg'):
				global total
				if total < 200:
					total = total + 1
					allfile2.append(os.path.join(root,name))
	
	return allfile2,total



def result2(path1,path2):
	# 调用classfiy_aHash函数进行相似度比较并添加到list:num2
	allfile2,total = getallfiles2(path2)
	
	for img2 in allfile2:
		num2 = []
		image1 = Image.open(path1)
		image2 = Image.open(img2)
		pre = classfiy_aHash(image1,image2,size=(8,8),exact=25)
		num2.append(img2.split('/')[-1].split('.')[0])
		num2.append(pre)
		yield num2



def result1(path1,path2):
	# 按相似度从高到低排序
    global num1
    
    for e in result2(path1,path2):
        a = e
        num1.append(a)
    num1.sort(key=operator.itemgetter(1))
    if len(num1) == 200:
        a=(','.join(list(map(lambda x: x[0], num1))))
        b = a.split(",")
        
    	return b



def result(filename,modelIdList):
	# path1为val里面的一张图片地址filename
	# path2为train已分好类(不同类别)的文件夹地址modelIDList
	# 返回相似度比较结果
	
	for i in modelIdList:
		path2 = "./vehicle_recognition/images/train/" + i
		name2 = result1(filename, path2)
	
	return name2



if __name__ == '__main__':
	# path1为val里面的一张图片地址filename
	path1 = "/Users/yangguofeng/Downloads/ML_Data/2/val_4.jpg"
	modelIdList = ['2', '3', '4']
	name2 = result(path1,modelIdList)
	
	print(name2)



'''
# Different path
import sys
sys.path.append('../xxx')

or

# Same path
from aHash import *
'''