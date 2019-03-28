import os
import operator
from PIL import Image



# 颜色直方图
# 与histogram.py的那个不同的是, histogram_split.py会把图片分隔成16个小块，然后分别比较，最后综合比较结果，从而提高比较的准确率。



# 计数器
total = 0
# 相似度结果list，未排序
num1 = []



def calculate(image1, image2):
	# 分别计算各块的颜色直方图并比较不同亮度下的对应的像素数量即重合程度
	g = image1.histogram()
	s = image2.histogram()
	assert len(g) == len(s), "error"
	data = []

	for index in range(0, len(g)):
		if g[index] != s[index]:
			data.append(1 - abs(g[index] - s[index]) / max(g[index], s[index]))
		else:
			data.append(1)

	return sum(data) / len(g)



def split_imgae(image, part_size):
	# 将图片均分成为16块，每块大小为64*64。
	pw, ph = part_size
	w, h = image.size
	sub_image_list = []
	assert w % pw == h % ph == 0, "error"

	for i in range(0, w, pw):
		for j in range(0, h, ph):
			sub_image = image.crop((i, j, i + pw, j + ph)).copy()
			sub_image_list.append(sub_image)

	return sub_image_list



def classfiy_histogram_with_split(image1, image2, size=(256, 256), part_size=(64, 64)):
	# 缩放图片：为了保留结构去掉细节，去除大小、横纵比的差异，把图片统一缩放到256*256。
	image1 = image1.resize(size).convert("RGB")
	sub_image1 = split_imgae(image1, part_size)
	image2 = image2.resize(size).convert("RGB")
	sub_image2 = split_imgae(image2, part_size)
	sub_data = 0;

	for im1, im2 in zip(sub_image1, sub_image2):
		sub_data += calculate(im1, im2)
	x = size[0] / part_size[0]
	y = size[1] / part_size[1]
	pre = round((sub_data / (x * y)), 3)

	return pre



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
		pre = classfiy_histogram_with_split(image1, image2, size=(256, 256), part_size=(64, 64))
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