import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, MaxPooling2D, Dropout, BatchNormalization, Add, Activation
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint



class JuegoCNN:
    def __init__(self, altura_frame, anchura_frame, canales, numero_de_acciones, learning_rate=0.001):
        # Inicialización de la clase JuegoCNN
        self.altura_frame = altura_frame
        self.anchura_frame = anchura_frame
        self.canales = canales
        self.numero_de_acciones = numero_de_acciones
        self.learning_rate = learning_rate
        self.model = self.crear_modelo()


    def entrenar(self, batch, gamma=0.99, callbacks=None):
        """Entrena la red con un lote de datos de juego."""
        estados, acciones, recompensas, siguientes_estados, terminados = zip(*batch)
        estados = np.array(estados)
        siguientes_estados = np.array(siguientes_estados)

        Q_actuales = self.model.predict(estados)
        Q_siguientes = self.model.predict(siguientes_estados)
        Q_objetivo = np.copy(Q_actuales)

        for i in range(len(batch)):
            Q_objetivo[i][acciones[i]] = recompensas[i] if terminados[i] else recompensas[i] + gamma * np.max(Q_siguientes[i])

        self.model.fit(estados, Q_objetivo, verbose=0, callbacks=callbacks)

    def predecir_accion(self, estado, epsilon):
        """Determina la acción a realizar basada en la política ε-greedy."""
        if np.random.rand() < epsilon:
            return random.randrange(self.numero_de_acciones)
        else:
            Q_values = self.model.predict(estado)
            return np.argmax(Q_values[0])


    def crear_bloque_residual(self, x, num_filtros):
        y = Conv2D(num_filtros, kernel_size=3, padding='same', activation='relu', kernel_regularizer=l2(0.001))(x)
        y = BatchNormalization()(y)
        y = Conv2D(num_filtros, kernel_size=3, padding='same', activation='relu', kernel_regularizer=l2(0.001))(y)
        y = BatchNormalization()(y)

        y = Add()([y, x])
        return Activation('relu')(y)

    def crear_modelo(self):
        inputs = Input(shape=(self.altura_frame, self.anchura_frame, self.canales))
        x = Conv2D(64, kernel_size=3, padding='same', activation='relu')(inputs)
        x = BatchNormalization()(x)

        # Añadir bloques residuales.
        for _ in range(3):  # Número de bloques residuales
            x = self.crear_bloque_residual(x, 64)

        x = MaxPooling2D(pool_size=(2, 2))(x)
        x = Conv2D(128, kernel_size=3, padding='same', activation='relu')(x)
        x = BatchNormalization()(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        x = Flatten()(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)
        outputs = Dense(self.numero_de_acciones)(x)

        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
