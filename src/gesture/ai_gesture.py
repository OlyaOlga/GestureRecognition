from typing import Tuple

import numpy as np
import tensorflow as tf
import cv2

from . import Gesture
from .gesture_detector_base import GestureDetectorBase

class AiDetector(GestureDetectorBase):

    def recognize(self, frame: np.ndarray) -> Tuple[Gesture, np.ndarray]:
        ipt = cv2.resize(frame, (150, 150))/255
        ipt = np.expand_dims(ipt, axis=0)
        res = self.model(ipt)
        res = res.numpy()[0]
        return Gesture(np.argmax(res)), res


    def __init__(self):
        self.model: tf.keras.models.Sequential = None
        # self.create_model()
        # self.model.build(input_shape=(1, 75, 50, 3))
        #
        # self.model.load_weights('./data/my_rps_model_weights')
        MODEL_PATH = './data/rps.h5'

        # Load your trained model
        self.model = tf.keras.model.load_model(MODEL_PATH)

    def create_model(self):
        self.model = tf.keras.models.Sequential()

        self.model.add(tf.keras.layers.Conv2D(16, (3, 3)))
        self.model.add(tf.keras.layers.ReLU())
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
        self.model.add(tf.keras.layers.Dropout(0.2))

        self.model.add(tf.keras.layers.Conv2D(16, (5, 5)))
        self.model.add(tf.keras.layers.ReLU())
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
        self.model.add(tf.keras.layers.Dropout(0.2))

        self.model.add(tf.keras.layers.Conv2D(16, (9, 9)))
        self.model.add(tf.keras.layers.ReLU())
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
        self.model.add(tf.keras.layers.Dropout(0.2))

        self.model.add(tf.keras.layers.Flatten())

        self.model.add(tf.keras.layers.Dense(128))
        self.model.add(tf.keras.layers.ReLU())
        self.model.add(tf.keras.layers.Dropout(0.2))
        self.model.add(tf.keras.layers.Dense(128))
        self.model.add(tf.keras.layers.ReLU())
        self.model.add(tf.keras.layers.Dense(64))
        self.model.add(tf.keras.layers.ReLU())
        self.model.add(tf.keras.layers.Dense(64))
        self.model.add(tf.keras.layers.ReLU())
        self.model.add(tf.keras.layers.Dense(4, activation='softmax'))

        self.model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=["acc"])

