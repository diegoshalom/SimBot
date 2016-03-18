import numpy as np 
#from gasp import *
from time import sleep

class Grafico():

    def __init__(self, tiempo, matriz, punto_entrada, punto_salida, robot_up="./img/robot_up.png",
		robot_down="./img/robot_down.png",robot_left="./img/robot_left.png",
		robot_right="./img/robot_right.png", entrada = "./img/in.png", 
		pasto = "./img/grass.png", salida = "./img/exit.png", 
		bloque = "./img/bloque.png"):
              
        self.entrada = entrada
        self.salida = salida
        self.pasto = pasto
        self.bloque = bloque
        self.robot_up = robot_up
        self.robot_down = robot_down
        self.robot_left = robot_left
        self.robot_right = robot_right
        self.punto_entrada = punto_entrada
        self.punto_salida = punto_salida
        self.matriz = matriz
        self.tiempo = tiempo
        self.tamano_x = len(self.matriz)
        self.tamano_y = len(self.matriz[0])
    
    def girar_robot_dibujo(self, orientacion):        
        if orientacion[0] == 1 and orientacion[1] == 0:
            imagen_orientacion = self.robot_down
        elif orientacion[0] == 0 and orientacion[1] == 1:
            imagen_orientacion = self.robot_right
        elif orientacion[0] == -1 and orientacion[1] == 0:
            imagen_orientacion = self.robot_up
        elif orientacion[0] == 0 and orientacion[1] == -1:
            imagen_orientacion = self.robot_left
        return imagen_orientacion
    
    def visualizar(self):        
        '''
        Funcion que muestra por pantalla el laberinto
        
        ENTRADA:
			
        SALIDA:
			Imagen por pantalla
        '''
        
        h = (self.tamano_y*32)-16
        for f in range(self.tamano_x):
            w = 16
            for c in range(self.tamano_y):
                if self.matriz[f][c] == 0:
                    Image(self.pasto, (w, h))
                elif self.matriz[f][c] == 1:
                    Image(self.bloque, (w, h))
                elif self.matriz[f][c] == 2:
                    Image(self.entrada, (w, h))
                    Image(self.robot_up, (w, h))
                elif self.matriz[f][c] == 3:
                    Image(self.pasto, (w, h))
                    Image(self.salida, (w, h))
                w += 32
            h -= 32

        sleep(self.tiempo)

    def actualizar(self, posicion_vieja, posicion_nueva, orientacion):
        '''
        Funcion que muestra por pantalla el recorrido del robot
        atraves del laberinto, hasta que llega a la salida
        
        ENTRADA:
			posicion_vieja:  punto en donde se encuentra el robot
			posicion_nueva:  punto hacia adonde avanzaria el robot
        SALIDA:
			Actualizacion por pantalla
        '''
        imagen_orientacion = self.girar_robot_dibujo(orientacion) 
        w_viejo = 32*posicion_vieja[1] + 16
        h_viejo = (self.tamano_y*32) - 16 - 32*posicion_vieja[0]        
        w_nuevo = 32*posicion_nueva[1] + 16
        h_nuevo = (self.tamano_y*32) - 16 - 32*posicion_nueva[0]
        Image(imagen_orientacion,(w_viejo, h_viejo))


        if posicion_vieja[0] == self.punto_entrada[0] and \
           posicion_vieja[1] == self.punto_entrada[1]:
            Image(self.entrada, (w_viejo, h_viejo)) 
            Image(imagen_orientacion, (w_nuevo, h_nuevo))
        elif posicion_nueva[0] == self.punto_salida[0] and \
             posicion_nueva[1] == self.punto_salida[1]:
            Image(self.pasto, (w_viejo, h_viejo))
            Image(imagen_orientacion, (w_nuevo, h_nuevo))

            Image(self.pasto, (w_nuevo, h_nuevo))
            Image("./img/ganar.png",
                  (int(((self.tamano_y*32) - 16)/2),
                   int(((self.tamano_y*32) - 16)/2)))

        else:   
            Image(self.pasto, (w_viejo, h_viejo))
            Image(imagen_orientacion, (w_nuevo, h_nuevo))
            
        sleep(self.tiempo)
        
        
    def visualizar_oscuridad(self):
        '''
        Funcion que muestra por pantalla el laberinto a oscuras
      
        ENTRADA:

        SALIDA:
			Laberinto a oscuras
        '''
        h_min = 16 
        h_max = (self.tamano_y*32)-16
        w=16
        for i in range(self.tamano_x):
            Image(self.bloque, (w, h_min))
            Image(self.bloque, (w, h_max))
            w += 32
        w_min = 16
        w_max = (self.tamano_x*32)-16
        h = 16
        for j in range(self.tamano_y):
            w = 16
            Image(self.bloque, (w_min, h))
            Image(self.bloque, (w_max, h))
            h += 32
        
        
        w = 32 * self.punto_entrada[1]+16
        h = (self.tamano_y*32) - 16 - 32 * self.punto_entrada[0]
        Image(self.entrada, (w, h)) 
        Image(self.robot_up, (w, h))
        sleep(self.tiempo)
        return 0

    def visualizar_mirada(self, actual, mirada, orientacion):
        w_viejo=32*actual[1]+16
        h_viejo=(self.tamano_y*32)-16-32*actual[0]        
        w_nuevo=32*mirada[1]+16
        h_nuevo=(self.tamano_y*32)-16-32*mirada[0]

        imagen_orientacion = self.girar_robot_dibujo(orientacion) 
        Image(imagen_orientacion, (w_viejo, h_viejo))
        
        if self.matriz[tuple(mirada)] == 2:
            Image(self.entrada, (w_nuevo, h_nuevo)) 
        elif self.matriz[tuple(mirada)] == 3:
            Image(self.pasto, (w_nuevo, h_nuevo))
            Image(self.salida, (w_nuevo, h_nuevo))
        elif self.matriz[tuple(mirada)] == 1:
            Image(self.bloque, (w_nuevo, h_nuevo))
        elif self.matriz[tuple(mirada)] == 0:
            Image(self.pasto, (w_nuevo, h_nuevo))
        sleep(self.tiempo)
