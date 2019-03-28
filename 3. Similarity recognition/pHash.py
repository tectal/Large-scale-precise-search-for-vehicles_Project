import os
import math
import operator
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps



# 感知哈希算法
# 平均哈希算法过于严格，不够精确，更适合搜索缩略图，为了获得更精确的结果可以选择感知哈希算法，采用的是DCT（离散余弦变换）来降低频率的方法。



# 计数器
total = 0
# 相似度结果list，未排序
num1 = []



def get_code(List,middle):
	# 进一步减小DCT：大于平均值记录为1，反之记录为0。
	result = []

	for index in range(0,len(List)):
		if List[index] > middle:
			result.append("1")
		else:
			result.append("0")

	return result



def comp_code(code1,code2):
	# 对比指纹：计算两幅图片的指纹，计算汉明距离（从一个指纹到另一个指纹需要变几次），汉明距离越大则说明图片越不一致，反之，汉明距离越小则说明图片越相似，当距离为0时，说明完全相同。
	num = 0

	for index in range(0,len(code1)):
		if str(code1[index]) != str(code2[index]):
			num+=1

	return num 



def get_middle(List):
	# 计算平均值：计算缩小DCT后的所有像素点的平均值。
	li = List.copy()
	li.sort()
	value = 0

	if len(li)%2==0:
		index = int((len(li)/2)) - 1
		value = li[index]
	else:
		index = int((len(li)/2))
		value = (li[index]+li[index-1])/2

	return value



def get_matrix(image):
	# 得到矩阵的宽和高
	matrix = []
	size = image.size

	for height in range(0,size[1]):
		pixel = []
		for width in range(0,size[0]):
			pixel_value = image.getpixel((width,height))
			pixel.append(pixel_value)
		matrix.append(pixel)

	return matrix



def get_coefficient(n):
	# 对矩阵进行离散余弦变换
	matrix = []
	PI = math.pi
	sqr = math.sqrt(1/n)
	value = []

	for i in range(0,n):
		value.append(sqr)
	matrix.append(value)
	
	for i in range(1,n):
		value=[]
		for j in range (0,n):
			data = math.sqrt(2.0/n) * math.cos(i*PI*(j+0.5)/n);  
			value.append(data)
		matrix.append(value)

	return matrix



def get_transposing(matrix):
	# 矩阵变换得到新矩阵
	new_matrix = []

	for i in range(0,len(matrix)):
		value = []
		for j in range(0,len(matrix[i])):
			value.append(matrix[j][i])
		new_matrix.append(value)

	return new_matrix



def get_mult(matrix1,matrix2):
	# 计算DCT:DCT把图片分离成分率的集
	new_matrix = []

	for i in range(0,len(matrix1)):
		value_list = []
		for j in range(0,len(matrix1)): 
			t = 0.0
			for k in range(0,len(matrix1)):
				t += matrix1[i][k] * matrix2[k][j]
			value_list.append(t)
		new_matrix.append(value_list)

	return new_matrix



def DCT(double_matrix):
	# 计算DCT
	n = len(double_matrix)
	A = get_coefficient(n)
	AT = get_transposing(A)
	temp = get_mult(double_matrix, A)
	DCT_matrix = get_mult(temp, AT)

	return DCT_matrix
	


def sub_matrix_to_list(DCT_matrix,part_size):
	# 缩小DCT：DCT是32*32，保留左上角的8*8，这些代表的图片的最低频率
	w,h = part_size
	List = []

	for i in range(0,h):
		for j in range(0,w):
			List.append(DCT_matrix[i][j])

	return List



def classify_DCT(image1,image2,size=(32,32),part_size=(8,8)):
	# 缩小图片：32 * 32是一个较好的大小，这样方便DCT计算。
	# 转化为灰度图：把缩放后的图片转化为灰度图。
	# 得到信息指纹：组合64个bit位，顺序随意保持一致性即可。
	assert size[0]==size[1],"size error"
	assert part_size[0]==part_size[1],"part_size error"

	image1 = image1.resize(size).convert('L').filter(ImageFilter.BLUR)
	image1 = ImageOps.equalize(image1)
	matrix = get_matrix(image1)
	DCT_matrix = DCT(matrix)
	List = sub_matrix_to_list(DCT_matrix, part_size)
	middle = get_middle(List)
	code1 = get_code(List, middle)

	image2 = image2.resize(size).convert('L').filter(ImageFilter.BLUR)
	image2 = ImageOps.equalize(image2)
	matrix = get_matrix(image2)
	DCT_matrix = DCT(matrix)
	List = sub_matrix_to_list(DCT_matrix, part_size)
	middle = get_middle(List)
	code2 = get_code(List, middle)

	return comp_code(code1, code2)



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
		pre = classify_DCT(image1,image2,size=(32,32),part_size=(8,8))
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