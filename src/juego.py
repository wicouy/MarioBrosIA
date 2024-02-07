import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D

class JuegoCNN:
    def __init__(self, altura_frame, anchura_frame, canales, numero_de_acciones):
        self.altura_frame = altura_frame
        self.anchura_frame = anchura_frame
        self.canales = canales
        self.numero_de_acciones = numero_de_acciones
        self.model = self.crear_modelo()

    def crear_modelo(self):
        model = Sequential()
        model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(self.altura_frame, self.anchura_frame, self.canales)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(32, kernel_size=3, activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dense(self.numero_de_acciones, activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def entrenar_modelo(self, datos_entrenamiento, etiquetas, numero_de_epochs):
        self.model.fit(datos_entrenamiento, etiquetas, epochs=numero_de_epochs)
