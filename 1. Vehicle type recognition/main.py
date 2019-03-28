import sys
import os
#yang add
from aHash import *

#--------------------------------------------------------
if len(sys.argv) == 1:
    print('Usage: python3.5 main.py [directory_to_your_imagefiles]')
    sys.exit()

#--------------------------------------------------------
# to store [class -> label] mapping
dict = {}
# image file path
fileInputPrex = sys.argv[1]
# output file path
fileOutputPrex = './outputs/'

#--------------------------------------------------------    
# get all file names to be processed    
filenames = os.listdir(fileInputPrex)

# Get the class to label mapping from mapping.xml
import  xml.dom.minidom
from xml.dom.minidom import Document
dom = xml.dom.minidom.parse('mapping.xml')
root = dom.documentElement
items = root.getElementsByTagName('item')
for item in items:
    index = int(item.getAttribute('index'))
    label = item.getAttribute('label')
    dict[index] = label
    
#--------------------------------------------------------
import keras
import numpy as np
from keras.utils import np_utils
from keras.models import load_model
from keras.applications import vgg16

# load previously trained model
model = load_model('./models/vgg16_vehicle_recognition.h5')

#--------------------------------------------------------
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array

#--------------------------------------------------------
# create output xml file for the query
doc = Document()
root = doc.createElement('Message')
root.setAttribute('Version', "1.0")
doc.appendChild(root)
info = doc.createElement('Info')
info.setAttribute('evaluateType', "6")
info.setAttribute('mediaFile', "vehicle_retrieval_val")
root.appendChild(info)

for filename in filenames:
    print("processing image: " + fileInputPrex + filename)
    # load an image in PIL format
    original = load_img(fileInputPrex+filename, target_size=(224, 224))
    # convert the PIL image to a numpy array
    # IN PIL - image is in (width, height, channel)
    # In Numpy - image is in (height, width, channel)
    numpy_image = img_to_array(original)
    # Convert the image / images into batch format
    # expand_dims will add an extra dimension to the data at a particular axis
    # We want the input matrix to the network to be of the form (batchsize, height, width, channels)
    # Thus we add the extra dimension to the axis 0.
    image_batch = np.expand_dims(numpy_image, axis=0)
    
    # prepare the image for the VGG model
    processed_image = vgg16.preprocess_input(image_batch.copy())
 
    # get the predicted probabilities for each class
    predictions = model.predict(processed_image)
    # 这里的index就是filename这张图片经过vgg_model之后，在223个类别上的概率函数的降序排列
    predictions = np.argsort(-predictions)
    index = predictions[0]
    
    modelIDList = []
    for i in index:
        modelIDList.append(dict[i])
    #--------------------------------------------------------
    # fetching 200 images, this is the interface that you will implement
    output_names = result(fileInputPrex+filename, modelIDList)
    
    # 为当前的query生成xml文件项
    text = '\n'
    for i in range(len(output_names)):
        text = text + output_names[i] + ' '
        if i % 10 == 9:
            text = text + '\n'
    item = doc.createElement('Item')
    item.setAttribute('imageName', filename[:-4])
    item.appendChild(doc.createTextNode(text))
    root.appendChild(item)
#--------------------------------------------------------
f= open(fileOutputPrex + 'output.xml', 'w')    
doc.writexml(f, addindent=' ', newl='\n')
f.close()
