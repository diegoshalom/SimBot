import numpy as np
from gasp import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import matplotlib.animation

from source.ambiente import Ambiente
from source.robot import Robot
from source.laberintos.deep_first_search import Laberinto

from source.estrategias.hamster import Hamster
from source.estrategias.buscador_por_derecha import Buscador_por_derecha


tamano_x, tamano_y = (30,30)
entrada = (1,1)
salida = (tamano_x-2,tamano_y-2)
salida = (tamano_x-1,tamano_y-1)

pos_robot = np.array(entrada)
ori_robot = np.array((0,1))

hamster = Hamster()
buscador_por_derecha = Buscador_por_derecha()

carga_inicial = 100

robot = Robot(ori_robot, pos_robot, hamster, carga_inicial)
robot = Robot(ori_robot, pos_robot, buscador_por_derecha, carga_inicial)

laberinto = Laberinto(entrada, salida, tamano_x, tamano_y)
ambiente = Ambiente(robot, laberinto)



# Chequea que tenga salida el laberinto
#print "El laberinto tiene salida?", ambiente.chequear_solucion()

width = len(ambiente.matriz)*32
height = len(ambiente.matriz[0])*32
#begin_graphics(width=width, height=height, title="SimBot")

#~ ambiente.visualizar()
#ambiente.visualizar_oscuridad()
robot.salir_del_laberinto(ambiente)

print ambiente.matriz

#chequeo que no camine por las paredes
for i in robot.historia_posiciones:
    if ambiente.matriz[tuple(i)] == 1:
        print "OOPS el robot paso por arriba de una pared en ", i


#end_graphics()



fig = plt.figure(figsize= (5,5))
ax = fig.add_subplot(111)
cont = 0
for i in robot.historia_posiciones:
    i=robot.historia_posiciones[cont]
    mat=ambiente.matriz.copy()
    mat[i[0],i[1]] = 4
    ax.imshow(mat)
    fig.show()
    time.sleep(.1)
    cont += 1
    if cont>10:
        break

    
    
    
