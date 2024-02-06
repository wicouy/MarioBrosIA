# controles.py
import pyautogui
import time

class GameController:
    DELAY_BETWEEN_COMMANDS = 0.1

    def __init__(self):
        # Se podrían agregar más atributos de ser necesario
        pass

    def presionar_tecla(self, tecla):
        """Simula la presión y liberación de una tecla."""
        pyautogui.keyDown(tecla)
        time.sleep(self.DELAY_BETWEEN_COMMANDS)
        pyautogui.keyUp(tecla)

    def mover_arriba(self):
        self.presionar_tecla('up')

    def mover_abajo(self):
        self.presionar_tecla('down')

    def mover_izquierda(self):
        self.presionar_tecla('left')

    def mover_derecha(self):
        self.presionar_tecla('right')

    def presionar_b(self):
        self.presionar_tecla('b')

    def presionar_a(self):
        self.presionar_tecla('s')

    def presionar_y(self):
        self.presionar_tecla('y')

    def presionar_x(self):
        self.presionar_tecla('x')

    def presionar_l(self):
        self.presionar_tecla('l')

    def presionar_r(self):
        self.presionar_tecla('r')

    def presionar_start(self):
        self.presionar_tecla('enter')

    def presionar_select(self):
        self.presionar_tecla('space')
