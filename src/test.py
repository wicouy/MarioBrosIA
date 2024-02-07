from logging import captureWarnings
import cv2
import time
import numpy as np
import pygetwindow
import pyautogui
import psutil
from controles import GameController
from captura import CapturaPantalla


# Imprime todos los títulos de las ventanas disponibles
window_titles = pygetwindow.getAllTitles()
for title in window_titles:
    print(title)


