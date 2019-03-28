from keras.applications import VGG16
from keras import models
from keras import layers
from keras import optimizers

# some global parameters
image_size = 224
train_batchsize = 100
val_batchsize = 10
nb_classes= 223
nb_epoch = 60
train_dir = './vehicle_recognition/model_image/train'
validation_dir = './vehicle_recognition/model_image/val'

#Load the VGG model
vgg_conv = VGG16(weights='imagenet', include_top=False, input_shape=(image_size, image_size, 3)

# Freeze the layers except the last 4 layers
for layer in vgg_conv.layers[:-4]:
    layer.trainable = False
 
# Check the trainable status of the individual layers
for layer in vgg_conv.layers:
    print(layer, layer.trainable)

# Create the model
model = models.Sequential()
 
# Add the vgg convolutional base model
model.add(vgg_conv)
 
# Add new layers
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(nb_classes, activation='softmax'))

# Show a summary of the model. Check the number of trainable parameters
model.summary()

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])
			  
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
	rescale=1./255,
	rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')
 
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
	train_dir,
	target_size=(image_size, image_size),
	batch_size=train_batchsize,
	class_mode='categorical')
 
validation_generator = validation_datagen.flow_from_directory(
	validation_dir,
    target_size=(image_size, image_size),
	batch_size=val_batchsize,
    class_mode='categorical',
    shuffle=False)

# Train the model
history = model.fit_generator(
    train_generator,
    steps_per_epoch=train_generator.samples/train_generator.batch_size ,
    epochs=nb_epoch,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples/validation_generator.batch_size,
    verbose=1)

# Save the model
model.save('vgg16_vehicle_recognition2.h5')
