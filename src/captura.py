# captura.py
import cv2
import numpy as np

class CapturaPantalla:
    def __init__(self):
        self.captura = None

    def iniciar_captura(self):
        # Inicia la captura de pantalla
        self.captura = cv2.VideoCapture(0)

    def detener_captura(self):
        # Detiene la captura de pantalla
        if self.captura:
            self.captura.release()

    def obtener_frame(self):
        # Captura un frame de la pantalla y lo devuelve como una imagen en formato numpy
        ret, frame = self.captura.read()
        if ret:
            return frame
        else:
            return None
