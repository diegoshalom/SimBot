'''
ACA vive todo

INSTALAR python-gasp

'''

import numpy as np
from time import sleep
from gasp import *
from source.robot import Robot
#from laberintos.laberinto_facil2 import Laberinto


class Ambiente():

    def __init__(self, robot, laberinto):
        '''
        entrada: 2-tuple
        salida: 2-tuple
        tamano_x: tamano de la cancha
        tamano_y: tamano de la cancha
        robot: el robot que vive en este ambiente
        matriz: np.array de de tamano_x por tamano_y que tiene:
            0: vacio
            1: paredes / obstaculos
            2: entrada
            3: salida
        '''
        
        #self.entrada = entrada 
        #self.salida = salida   
        #self.tamano_x = tamano_x 
        #self.tamano_y = tamano_y
        self.robot = robot
        self.laberinto = laberinto
        self.matriz = self.laberinto.hacer()

    def chequear_solucion(self):
        """
        Comprueba que tenga solucion, que se pueda ir caminando desde la 
                entrada a la salida
 
        Returns
        -------    
        bool
            True si se puede llegar de la entrada a la salida, False si no.
        """                
        una_matriz = self.matriz.copy()
        while True:
            aux=0
            tiene_solucion = 0
            for i in xrange(1,self.laberinto.tamano_x-1):
                for j in xrange(1,self.laberinto.tamano_y-1):
                    if  una_matriz[i,j]==2:
                        #chequeo si llegue a la solucion
                        if una_matriz[i,j+1]==3:
                            tiene_solucion = 1 
                        if una_matriz[i,j+1]==3:
                            tiene_solucion = 1 
                        if una_matriz[i,j+1]==3:
                            tiene_solucion = 1 
                        if una_matriz[i,j+1]==3:
                            tiene_solucion = 1 

                        #avanzo un paso para todos lados
                        if una_matriz[i,j+1]==0:
                            aux += 1
                            una_matriz[i,j+1] = 2
                            
                        if una_matriz[i,j-1]==0:
                            aux += 1
                            una_matriz[i,j-1] = 2

                        if una_matriz[i+1,j]==0:
                            aux += 1
                            una_matriz[i+1,j] = 2

                        if una_matriz[i-1,j]==0:
                            aux += 1
                            una_matriz[i-1,j] = 2
            if aux == 0:
                break
            if tiene_solucion == 1:
                break
        return tiene_solucion  
        
   
    def eco(self): 
        """
        Devuelve la cantidad de casillas libres por delante del robot
 
        Returns
        -------    
        int
            cantidad de casillas libres delante del robot (0 si esta mirando 
            la pared).
        """            
        '''
        distancia = 0
        posicion_sensada = self.robot.posicion  + self.robot.giroscopo
        #print posicion_sensada , self.matriz[tuple(posicion_sensada)]
        '''
        distancia = 0
        posicion_actual = self.robot.posicion.copy()
        posicion_sensada = self.robot.posicion  + self.robot.giroscopo
        #self.visualizar_mirada(posicion_actual, posicion_sensada,self.robot.giroscopo)
        while self.matriz[tuple(posicion_sensada)] != 1:
            posicion_sensada += self.robot.giroscopo
            distancia += 1
       
        return distancia

    def visualizar(self):        
        '''
        Funcion que muestra por pantalla el laberinto
        
        ENTRADA:
			Ambiente
        SALIDA:
			Imagen por pantalla
        '''
        
        h = (self.laberinto.tamano_y*32)-16
        for f in range(self.laberinto.tamano_x):
            w = 16
            for c in range(self.laberinto.tamano_y):
                if self.matriz[f][c] == 0:
                    Image("./img/grass.png", (w, h))
                elif self.matriz[f][c] == 1:
                    Image("./img/bloque.png", (w, h))
                elif self.matriz[f][c] == 2:
                    Image("./img/in.png", (w, h))
                    Image("./img/robot_up.png", (w, h))
                elif self.matriz[f][c] == 3:
                    Image("./img/grass.png", (w, h))
                    Image("./img/exit.png", (w, h))
                w += 32
            h -= 32

        sleep(2)

    def actualizar(self, posViejaRobot, posNuevaRobot, orientacion):
        '''
        Funcion que muestra por pantalla el recorrido del robot
        atraves del laberinto, hasta que llega a la salida
        
        ENTRADA:
			posicion:  punto en donde se encuentra el robot
        SALIDA:
			Imagen por pantalla
        '''
        print  posViejaRobot, self.robot.posicion
        if orientacion[0] == 1 and orientacion[1] == 0:
            print "abajo", orientacion
            imagen_orientacion = "./img/robot_down.png"
        elif orientacion[0] == 0 and orientacion[1] == 1:
            print "derecha", orientacion
            imagen_orientacion = "./img/robot_right.png"
        elif orientacion[0] == -1 and orientacion[1] == 0:
            print "arriba", orientacion
            imagen_orientacion = "./img/robot_up.png"
        elif orientacion[0] == 0 and orientacion[1] == -1:
            print "izquierda", orientacion
            imagen_orientacion = "./img/robot_left.png"

        w_viejo = 32*posViejaRobot[1] + 16
        h_viejo = (self.laberinto.tamano_y*32) - 16 - 32*posViejaRobot[0]        
        w_nuevo = 32*posNuevaRobot[1] + 16
        h_nuevo = (self.laberinto.tamano_y*32) - 16 - 32*posNuevaRobot[0]
        Image(imagen_orientacion,
              (32*posViejaRobot[1] + 16, (self.laberinto.tamano_y*32) - \
               16 - 32*posViejaRobot[0])) 


        if posViejaRobot[0] == self.laberinto.entrada[0] and \
           posViejaRobot[1] == self.laberinto.entrada[1]:
            Image("./img/in.png", (w_viejo, h_viejo)) 
            Image(imagen_orientacion, (w_nuevo, h_nuevo))
        elif posNuevaRobot[0] == self.laberinto.salida[0] and \
             posNuevaRobot[1] == self.laberinto.salida[1]:
            Image("./img/grass.png", (w_viejo, h_viejo))
            Image(imagen_orientacion, (w_nuevo, h_nuevo))

            Image("./img/grass.png", (w_nuevo, h_nuevo))
            Image("./img/ganar.png",
                  (int(((self.laberinto.tamano_y*32) - 16)/2),
                   int(((self.laberinto.tamano_y*32) - 16)/2)))

        else:   
            Image("./img/grass.png", (w_viejo, h_viejo))
            Image(imagen_orientacion, (w_nuevo, h_nuevo))
            
        #sleep(.01)    
        
        
    def visualizar_oscuridad(self):
        '''
    Funcion que muestra por pantalla el laberinto
      
    ENTRADA:
		Ambiente
        SALIDA:
			Imagen por pantalla
        '''
        h_min = 16 
        h_max = (self.laberinto.tamano_y*32)-16
        w=16
        for i in range(self.laberinto.tamano_x):
            Image("./img/bloque.png", (w, h_min))
            Image("./img/bloque.png", (w, h_max))
            w += 32
        w_min = 16
        w_max = (self.laberinto.tamano_x*32)-16
        h = 16
        for j in range(self.laberinto.tamano_y):
            w = 16
            Image("./img/bloque.png", (w_min, h))
            Image("./img/bloque.png", (w_max, h))
            h += 32
        sleep(2)
        
        w = 32 * self.laberinto.entrada[1]+16
        h = (self.laberinto.tamano_y*32) - 16 - 32 * self.laberinto.entrada[0]
        Image("./img/in.png", (w, h)) 
        Image("./img/robot_up.png", (w, h))
        
        return 0

    def visualizar_mirada(self, actual, mirada, orientacion):
        w_viejo=32*actual[1]+16
        h_viejo=(self.laberinto.tamano_y*32)-16-32*actual[0]        
        w_nuevo=32*mirada[1]+16
        h_nuevo=(self.laberinto.tamano_y*32)-16-32*mirada[0]
        w=32*mirada[1]+16
        h=(self.laberinto.tamano_y*32)-16-32*mirada[0]
                
        if orientacion[0] == 1 and orientacion[1] == 0:
            print "abajo", orientacion
            imagen_orientacion = "./img/robot_down.png"
        elif orientacion[0] == 0 and orientacion[1] == 1:
            print "derecha", orientacion
            imagen_orientacion = "./img/robot_right.png"
        elif orientacion[0] == -1 and orientacion[1] == 0:
            print "arriba", orientacion
            imagen_orientacion = "./img/robot_up.png"
        elif orientacion[0] == 0 and orientacion[1] == -1:
            print "izquierda", orientacion
            imagen_orientacion = "./img/robot_left.png"
        Image(imagen_orientacion, (32*actual[1]+16, (self.laberinto.tamano_y*32)-16-32*actual[0])) 
        #~ sleep(0.01)

        if self.matriz [tuple(mirada)] == 2:
            Image("./img/in.png", (w, h)) 
        elif self.matriz [tuple(mirada)] == 3:
            Image("./img/grass.png", (w, h))
            Image("./img/exit.png", (w, h))
        elif self.matriz [tuple(mirada)] == 1:
            Image("./img/bloque.png", (w, h))
        elif self.matriz [tuple(mirada)] == 0:
            Image("./img/grass.png", (w, h))
        sleep(1)            

    def estoy_fuera(self):
        """
        Comprueba si la posicion actual del robot es la casilla de salida
        
        Returns
        -------    
        bool
            True si el robot esta en la salida, False si no.
        """
        if self.robot.posicion[0] == self.laberinto.salida[0] and \
           self.robot.posicion[1] == self.laberinto.salida[1]:
            print "Libertad!!!"
            return True
        else:
            return False


    
