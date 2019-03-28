
车辆颜色识别的代码说明

1、项目主要使用了numpy、collections、cv2、os机器学习库。

2、车辆颜色识别的代码是Color dictionary.py和Color identification.py这两个文件，其中Color dictionary.py定义了颜色字典，Color identification.py文件通过引用Color dictionary.py文件函数实现颜色定义，接着按照HSV颜色空间识别模型进行处理，统计结果得到车辆识别颜色。