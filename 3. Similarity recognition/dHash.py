import os
import operator
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps



# 差异哈希算法
# 相比pHash，dHash的速度要快的多，相比aHash，dHash在效率几乎相同的情况下的效果要更好，它是基于渐变实现的。



# 计数器
total = 0
# 相似度结果list，未排序
num1 = []



def getCode(img,size):

	result = []
	x_size = size[0]-1
	y_size = size[1]

	for x in range(0,x_size):
		# 计算差异值：dHash算法工作在相邻像素之间，这样每行9个像素之间产生了8个不同的差异，一共8行，则产生了64个差异值。
		for y in range(0,y_size):
			now_value = img.getpixel((x,y))
			next_value = img.getpixel((x+1,y))
			if next_value < now_value:
				# 获得指纹：如果左边的像素比右边的更亮，则记录为1，否则为0。
				result.append(1)
			else:
				result.append(0)

	return result



def compCode(code1,code2):
	# 对比指纹：计算两幅图片的指纹，计算汉明距离（从一个指纹到另一个指纹需要变几次），汉明距离越大则说明图片越不一致，反之，汉明距离越小则说明图片越相似，当距离为0时，说明完全相同。
	num = 0

	for index in range(0,len(code1)):
		if code1[index] != code2[index]:
			num+=1

	return num 



def classfiy_dHash(image1,image2,size=(9,8)):
	# 缩小图片：收缩到9*8的大小，它有72的像素点。
	# 转化为灰度图：把缩放后的图片转化为256阶的灰度图。
	image1 = image1.resize(size).convert('L')
	code1 = getCode(image1, size)
	image2 = image2.resize(size).convert('L')
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
		pre = classfiy_dHash(image1,image2,size=(9,8))
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