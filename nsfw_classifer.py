import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = tf.keras.models.load_model('manhwa_classifier.h5')

# Dự đoán loại ảnh
def predict_image(input_image):
    image = cv2.resize(input_image, (128, 128))
    image = np.expand_dims(image, axis=0) / 255.0
    prediction = model.predict(image)
    return 'SFW' if np.argmax(prediction) == 0 else 'NSFW'