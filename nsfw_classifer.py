import cv2
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('manhwa_classifier.h5')

# Dự đoán loại ảnh
def predict_image(input_image):
    image = cv2.resize(input_image, (128, 128))
    image = np.expand_dims(image, axis=0) / 255.0
    prediction = model.predict(image)
    return 'SFW' if np.argmax(prediction) == 0 else 'NSFW'