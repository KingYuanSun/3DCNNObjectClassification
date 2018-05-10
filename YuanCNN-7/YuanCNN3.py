"""
Trains and evaluates a 3D CNN on ModelNet10.
See below for usage.
"""

import sys

import numpy as np
np.random.seed(1)

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Reshape
from keras.layers.convolutional import (Conv2D, MaxPooling3D, Conv3D,
MaxPooling2D)

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.utils import shuffle
from keras.utils import plot_model

# Parse arguments
if len(sys.argv) != 3:
    print('Usage: python main.py <modelnet-npz-file> <logs-dir>')
    sys.exit(1)
modelnet_file, log_dir = sys.argv[1:]

# Load the data
data = np.load(modelnet_file)
X, Y = shuffle(data['X_train'], data['y_train'])
X_test, Y_test = shuffle(data['X_test'], data['y_test'])

# One-hot encode training targets
Y = keras.utils.to_categorical(Y, num_classes=7)

# Build the network
model = Sequential()
model.add(Reshape((38, 38, 38, 1), input_shape=(38, 38, 38)))  # 1 in-channel
model.add(Conv3D(16, 6, strides=2, activation='relu'))
model.add(Conv3D(64, 5, strides=2, activation='relu'))
model.add(Conv3D(64, 5, strides=2, activation='relu'))
model.add(Flatten())
# model.add(Dense(1024))
# model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))


# model = Sequential()
# model.add(Conv3D(32, (3,3,3), activation='relu', input_shape=(38, 38, 38, 38)))
# model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(1, 2, 2)))
# model.add(Conv3D(64, (3,3,3), activation='relu'))
# model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(1, 2, 2)))
# model.add(Conv3D(128, (3,3,3), activation='relu'))
# model.add(Conv3D(128, (3,3,3), activation='relu'))
# model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(1, 2, 2)))
# model.add(Conv3D(256, (2,2,2), activation='relu'))
# model.add(Conv3D(256, (2,2,2), activation='relu'))
# model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(1, 2, 2)))
# model.add(Flatten())
# model.add(Dense(1024))
# model.add(Dropout(0.5))
# model.add(Dense(1024))
# model.add(Dropout(0.5))
# model.add(Dense(5, activation='softmax'))






# Train
model.compile(loss='categorical_crossentropy',
              optimizer=keras.optimizers.Adam(lr=1e-4))
model.fit(X, Y, batch_size= 6, epochs=30, verbose=2,
          callbacks=[keras.callbacks.TensorBoard(log_dir=log_dir)],
          validation_split=0.1, shuffle=True)

# Show test accuracy
Y_test_pred = np.argmax(model.predict(X_test), axis=1)
print('Test accuracy: {:.3f}'.format(accuracy_score(Y_test, Y_test_pred)))


plot_model(model, to_file='model.png')

# Show confusion matrix and average per-class accuracy
conf = confusion_matrix(Y_test, Y_test_pred)
avg_per_class_acc = np.mean(np.diagonal(conf) / np.sum(conf, axis=1))
print('Confusion matrix:\n{}'.format(conf))
#print('Average per-class accuracy: {:.3f}'.format(avg_per_class_acc))
