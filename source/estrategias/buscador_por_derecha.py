'''
Camina siguiendo una pared (a la derecha)
'''

from estrategia import Estrategia
from random import random

class Buscador_por_derecha(Estrategia):

    def decidir(self, robot,un_ambiente):
        self.robot = robot


        self.robot.rotar("derecha")        
        sensar_derecha = self.robot.sensar(un_ambiente)       
        if sensar_derecha > 0:
            self.robot.mover(un_ambiente)
        else:
            self.robot.rotar("izquierda")
            sensar_adelante = self.robot.sensar(un_ambiente)       
            if sensar_adelante > 0:
                self.robot.mover(un_ambiente)
            else:
                self.robot.rotar("izquierda")

'''                
        if self.robot.sensar(un_ambiente) == 0:                
            self.robot.rotar("izquierda")
            self.robot.mover(un_ambiente)



        if self.robot.sensar(un_ambiente) == 0:
            self.robot.rotar("izquierda")
            self.robot.mover(un_ambiente)
            
        else:
            self.robot.rotar("derecha")
            if self.robot.sensar(un_ambiente) == 0:
                self.robot.rotar("izquierda")
                self.robot.mover(un_ambiente)
            else:
                self.robot.mover(un_ambiente)
'''


def rotacion_aleatoria(robot):
    numero = random()
    if numero > 1/2.:
        robot.rotar("izquierda")
    else:
        robot.rotar("derecha")                    
