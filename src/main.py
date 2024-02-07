# main.py
import cv2
import os
import time
import numpy as np
import pygetwindow
import pyautogui
import psutil
from controles import GameController
from captura import CapturaPantalla
import tensorflow as tf
from juego import JuegoCNN  # Asumiendo que la clase JuegoCNN está en juego.py

if __name__ == "__main__":
    captura = CapturaPantalla()
    controlador = GameController()
    # Dimensiones de los frames y número de acciones
    altura_frame = 200  # Ejemplo, ajustar según tu captura de pantalla
    anchura_frame = 200  # Ejemplo, ajustar según tu captura de pantalla
    canales = 3  # Para imágenes en color
    numero_de_acciones = 10  # Número de acciones que tu controlador puede realizar

    # Inicializar la red neuronal
    red_neuronal = JuegoCNN(altura_frame, anchura_frame, canales, numero_de_acciones)

    try:
        # Busca el proceso del emulador por su nombre
        emulador_process = None
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == 'snes9x-x64.exe':
                emulador_process = process
                break

        if emulador_process:
            # Obtiene el identificador (PID) del proceso del emulador
            emulador_pid = emulador_process.info['pid']

            # Busca la ventana del emulador por su título
            emulador_window = pygetwindow.getWindowsWithTitle("Super Mario World (U) [!] - Snes9x 1.60")[0]

            # Obtiene las coordenadas de la esquina superior izquierda y la esquina inferior derecha de la ventana
            x, y, width, height = emulador_window.left, emulador_window.top, emulador_window.width, emulador_window.height

            # Inicia la captura de pantalla
            captura.iniciar_captura()

            frame_count = 0  # Contador de frames
            
            frame_directory = 'src/modelo/frame'
            os.makedirs(frame_directory, exist_ok=True)  # Crea el directorio si no existe

            while True:
                # Obtén un frame de la pantalla correspondiente a la ventana del emulador
                captura_region = pyautogui.screenshot(region=(x, y, width, height))
                frame = cv2.cvtColor(np.array(captura_region), cv2.COLOR_RGB2BGR)

                if frame is not None:
                    # Redimensionar y normalizar el frame para la red neuronal
                    frame_redimensionado = cv2.resize(frame, (altura_frame, anchura_frame)) / 255.0
                    frame_path = os.path.join(frame_directory, f'frame_{frame_count}.png')

                    # Predecir la acción usando la red neuronal
                    accion_predicha = red_neuronal.model.predict(np.array([frame_redimensionado]))[0]
                    indice_accion = np.argmax(accion_predicha)
                    print("Acción predicha:", indice_accion)  # Imprime la acción predicha

                    # Ejecutar la acción predicha
                    controlador.ejecutar_accion(indice_accion)

                    # Guarda el frame en el archivo
                    # cv2.imwrite(frame_path, frame)
                    frame_count += 1

                    # Mostrar el frame en una ventana de OpenCV
                    cv2.imshow('Frame', frame)
                    cv2.waitKey(1)  # Espera un milisegundo
                else:
                    print("Error al obtener el frame")

                time.sleep(1 / 30) # Espera 1/30 segundos (30 FPS)

    except KeyboardInterrupt:
        print("Programa terminado por el usuario")
    finally:
        # Asegúrate de detener la captura antes de salir
        captura.detener_captura()
        cv2.destroyAllWindows()  # Cierra la ventana de OpenCV si la has utilizado
