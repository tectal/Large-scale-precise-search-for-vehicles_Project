
车辆型号识别的代码说明

1、项目的实验平台是keras1.8

2、车辆型号识别模型的代码是inception3、resnet50和vgg16这三个文件，
运行这三个文件就可以在当前目录中生成models文件夹，模型就在models文件夹中。

3、mapping.xml记录了模型的类号与实际的车辆模型编码的映射关系，
它会在main.py中加载。

4、main.py是query运行的主函数，调用的方法是python main.py filepath,
代码会在当前目录下生成outputs文件夹，里面的output.xml文件就是实际的执行结果。