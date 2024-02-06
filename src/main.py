import cv2
import time
import numpy as np
import pygetwindow
import pyautogui
import psutil
from controles import GameController
from captura import CapturaPantalla

if __name__ == "__main__":
    captura = CapturaPantalla()
    controlador = GameController()

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

            while True:
                # Obtén un frame de la pantalla correspondiente a la ventana del emulador
                captura_region = pyautogui.screenshot(region=(x, y, width, height))
                frame = cv2.cvtColor(np.array(captura_region), cv2.COLOR_RGB2BGR)

                if frame is not None:
                    # Guarda el frame en un archivo
                    cv2.imwrite(f'frame_{frame_count}.png', frame)
                    frame_count += 1

                    # Aquí puedes realizar cualquier procesamiento de imagen que necesites
                    # Por ejemplo, podrías mostrar el frame en una ventana de OpenCV
                    cv2.imshow('Frame', frame)
                    cv2.waitKey(1)  # Espera un milisegundo
                else:
                    print("Error al obtener el frame")

                # ... Aquí puedes realizar otras acciones o procesamiento según sea necesario
                controlador.mover_arriba()
                controlador.mover_abajo()
                controlador.mover_izquierda()
                controlador.mover_derecha()
                controlador.presionar_b()
                # ... y así sucesivamente para los otros botones
                time.sleep(1 / 120)

    except KeyboardInterrupt:
        print("Programa terminado por el usuario")
    finally:
        # Asegúrate de detener la captura antes de salir
        captura.detener_captura()
        cv2.destroyAllWindows()  # Cierra la ventana de OpenCV si la has utilizado
