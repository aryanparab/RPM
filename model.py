

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from pathlib import Path
import os

def make_model():
  IMAGE_SIZE = [224,224]

  #train_path = 'images/mask_nomask/'
  #valid_path = 'images/mask_nomask_test/'

  vgg = VGG16(input_shape=IMAGE_SIZE + [3],weights ='imagenet',include_top = False)

  for layer in vgg.layers:
      layer.trainable = False
          
  folders = glob('faces/train/*')

  x = Flatten()(vgg.output)

  prediction = Dense(1,activation = 'sigmoid')(x)



  model= Model(inputs=vgg.input , outputs = prediction)

  model.summary()

  model.compile(loss = 'binary_crossentropy',
                optimizer = 'adam',
                metrics =['accuracy']
                )

  from keras.preprocessing.image import ImageDataGenerator

  train_datagen = ImageDataGenerator(rescale = 1./255,
                                     shear_range = 0.2,
                                     zoom_range = 0.2,
                                     horizontal_flip = True)

  test_datagen = ImageDataGenerator(rescale = 1./255)

  training_set = train_datagen.flow_from_directory('faces/train',
                                                   target_size = (224,224),
                                                   batch_size = 32,
                                                   class_mode = 'binary')

  test_set = test_datagen.flow_from_directory('faces/test',
                                              target_size = (224,224),
                                              batch_size = 32,
                                              class_mode = 'binary')

  '''r=model.fit_generator(training_set,
                           samples_per_epoch = 8000,
                           nb_epoch = 5,
                           validation_data = test_set,
                           nb_val_samples = 2000)'''

  # fit the model

  r = model.fit(
    training_set,
    validation_data=test_set,
    epochs=1,
    steps_per_epoch=len(training_set),
    validation_steps=len(test_set)
  )
  import tensorflow as tf

  from keras.models import load_model

  model.save('sface_recog.h5')



