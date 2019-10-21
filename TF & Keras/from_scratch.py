import cv2
import numpy as np
import os

from sklearn.preprocessing import label_binarize #For creating one hot labels

from keras import models, layers, optimizers #Importing modules from Keras that will help us create a model

from keras.applications.mobilenet_v2 import MobileNetV2 as mblv2 #Importing the model

#Methods of MobileNet for making changing the input to the required shape and then decoding the output
from keras.applications.mobilenet_v2 import decode_predictions, preprocess_input


image_rows = 256
image_columns = 256
filter_size = 3

all_data = np.zeros((150,256,256,1))
all_labels = []

def reading_data_and_labels():
    """
    This function is intended to pre process the data so that it can be fed into the network for training
    """
    global all_data
    global all_labels
    data_folder = 'C:/Users/Asad/Google Drive/Demos/Data/Images'
    path_to_label_file = 'C:/Users/Asad/Google Drive/Demos/Data/labels.csv'

    for counter,filename in enumerate(os.listdir(data_folder)):
        img = cv2.imread(os.path.join(data_folder, filename), 0)
        if img is not None:
            all_data[counter,:,:,0] = img

    all_labels = np.loadtxt(path_to_label_file)
    all_labels = label_binarize(all_labels, classes=[0,1,2])

    print("Done")


def main():

    global all_data
    global all_labels
    reading_data_and_labels()


    #Adding layers to a model
    my_model = models.Sequential()

    #Each block will look something like this:
    my_model.add(layers.Conv2D(8, (filter_size,filter_size), padding= "SAME", activation='relu',
                               input_shape=(image_rows, image_columns, 1)))
    my_model.add(layers.MaxPooling2D(pool_size=(2,2), strides=(2,2)))

    my_model.add(layers.Conv2D(16, (filter_size, filter_size), padding="SAME", activation='relu'))
    my_model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    my_model.add(layers.Conv2D(32, (filter_size, filter_size), padding="SAME", activation='relu'))
    my_model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    my_model.add(layers.Conv2D(32, (filter_size, filter_size), padding="SAME", activation='relu'))
    my_model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    my_model.add(layers.Conv2D(32, (filter_size, filter_size), padding="SAME", activation='relu'))
    my_model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    my_model.add(layers.Flatten())
    my_model.add(layers.Dense(1024, activation='relu'))
    my_model.add(layers.Dense(3, activation='softmax'))

    #Displaying the summary of the model to check whether it is what we want
    my_model.summary()

    #Compiling the model
    my_model.compile(loss="categorical_crossentropy", optimizer = optimizers.Adam(lr=0.001), metrics=['acc'])

    #Training the model
    my_history = my_model.fit(all_data[0:120,:,:,:], all_labels[0:120,:], batch_size=8, epochs=15, validation_split=0.2)

    #Making predictions on the test data
    my_predictions = my_model.predict(all_data[120:150,:,:,:])
    print(my_predictions)

    #Evaluating loss and other matrics
    my_loss_and_metrics = my_model.evaluate(all_data[120:151,:,:,:], all_labels[120:151,:], batch_size=16)
    #print(my_loss_and_metrics)



main()