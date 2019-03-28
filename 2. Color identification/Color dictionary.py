import numpy as np  
import collections  

#定义字典存放颜色分量上下限  
#例如：{颜色: [min分量, max分量]}  
def getColorList():
    dict = collections.defaultdict(list)  
   
    lower_black = np.array([0, 0, 0])  
    upper_black = np.array([180, 255, 46])  
    color_list = []  
    color_list.append(lower_black)  
    color_list.append(upper_black)  
    dict['black'] = color_list  
   
    lower_gray = np.array([0, 0, 60])  
    upper_gray = np.array([180, 43, 220])  
    color_list = []  
    color_list.append(lower_gray)  
    color_list.append(upper_gray)  
    dict['gray']=color_list  

    lower_gray = np.array([0, 0, 30])  
    upper_gray = np.array([180, 23, 110])  
    color_list = []  
    color_list.append(lower_gray)  
    color_list.append(upper_gray)  
    dict['gray']=color_list  
  
    lower_white = np.array([0, 0, 160])  
    upper_white = np.array([180, 50, 255])  
    color_list = []  
    color_list.append(lower_white)  
    color_list.append(upper_white)  
    dict['white'] = color_list  
 
    lower_red = np.array([156, 43, 46])  
    upper_red = np.array([180, 255, 255])  
    color_list = []  
    color_list.append(lower_red)  
    color_list.append(upper_red)  
    dict['red']=color_list  

    lower_red = np.array([0, 43, 46])  
    upper_red = np.array([10, 255, 255])  
    color_list = []  
    color_list.append(lower_red)  
    color_list.append(upper_red)  
    dict['red'] = color_list  

    lower_orange = np.array([11, 43, 46])  
    upper_orange = np.array([25, 255, 255])  
    color_list = []  
    color_list.append(lower_orange)  
    color_list.append(upper_orange)  
    dict['red'] = color_list  
 
    lower_yellow = np.array([26, 43, 46])  
    upper_yellow = np.array([34, 255, 255])  
    color_list = []  
    color_list.append(lower_yellow)  
    color_list.append(upper_yellow)  
    dict['yellow'] = color_list  
  
    lower_green = np.array([35, 43, 46])  
    upper_green = np.array([77, 255, 255])  
    color_list = []  
    color_list.append(lower_green)  
    color_list.append(upper_green)  
    dict['blue'] = color_list  

    lower_cyan = np.array([78, 43, 46])  
    upper_cyan = np.array([99, 255, 255])  
    color_list = []  
    color_list.append(lower_cyan)  
    color_list.append(upper_cyan)  
    dict['blue'] = color_list  
 
    lower_blue = np.array([100, 43, 46])  
    upper_blue = np.array([124, 255, 255])  
    color_list = []  
    color_list.append(lower_blue)  
    color_list.append(upper_blue)  
    dict['blue'] = color_list  
  
    lower_purple = np.array([125, 43, 46])  
    upper_purple = np.array([155, 255, 255])  
    color_list = []  
    color_list.append(lower_purple)  
    color_list.append(upper_purple)  
    dict['red'] = color_list 
  
    return dict



if __name__ == '__main__':  
    color_dict = getColorList()  
    print(color_dict)  
  
    num = len(color_dict)  
    print('num=',num)  
  
    for d in color_dict:  
        print('key=',d)  
        print('value=',color_dict[d][1])