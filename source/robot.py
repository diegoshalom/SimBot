'''
Aca tenemos a HAL
'''
import matplotlib.pyplot as plt
import matplotlib as mpl
class Robot():
    '''
    Clase robot
    '''
    
    def __init__(self, orientacion, posicion, estrategia, carga_inicial):
        '''
		Inicializa el objeto Robot con su posicion, orientacion y un objeto Estrategia asociado.
		Parametros
		----------
		orientacion: List(int,int)
			Lista con la orientacion (x,y) del Robot en la matriz del Ambiente (laberinto).
		posicion: List(int,int)
			Lista correspondiente a las orientaciones "arriba" (0,1), "abajo" (0,-1), "izquierda" (-1,0) y "derecha" (1,0)
		estrategia: objeto Estrategia
			Objeto Estrategia inicializado por main que decidira las acciones del Robot.

        '''
        self.giroscopo = orientacion
        # TODO hacer la posicion un array
        self.posicion = posicion
        self.historia_posiciones = []
        self.historia_acciones = []
        self.carga_inicial = carga_inicial
        self.bateria = carga_inicial
        self.mi_estrategia = estrategia
        self.fig, self.axes = plt.subplots(figsize=(4,4))
    def rotar(self, giro):
        '''
		Cambia la orientacion del Robot.
		Parametros
		----------
		giro: str
			Valores posibles: "derecha" e "izquierda"
		'''
        if giro == "derecha":
			a = self.giroscopo[0]
			self.giroscopo[0] = self.giroscopo[1]
			self.giroscopo[1] = -a
			self.historia_acciones.append('r')		
        if giro == "izquierda":
			a = self.giroscopo[1]
			self.giroscopo[1] = self.giroscopo[0]
			self.giroscopo[0] = -a
			self.historia_acciones.append('l')
        self.consumo_bateria('rotar')
       

    def mover(self,un_ambiente):
         '''
		Cambia la posicion del Robot en el Ambiente (laberinto). Agrega el
         movimiento a la lista historia_posiciones.
         
		Parametros
		----------
		un_ambiente: objeto Ambiente
			Instancia del objeto Ambiente creada por main. Es el laberinto
         en el cual se mueve el robot
          '''
         
         if self.sensar(un_ambiente) != 0:
             self.posicion[0] += self.giroscopo[0]
             self.posicion[1] += self.giroscopo[1]
             self.consumo_bateria('mover')
             self.historia_acciones.append('f')
         else:
             # Choca contra la pared
             self.consumo_bateria('chocar')
             self.historia_acciones.append('x')
             
         self.historia_posiciones.append(list(self.posicion))
         
    def sensar(self,un_ambiente):        
         '''
		Obtiene la distancia del robot al proximo obstaculo del laberinto en la
         orientacion actual. 
		Parametros
		----------
		un_ambiente: objeto Ambiente
			Instancia del objeto Ambiente creada por main. Es el laberinto en el
         cual se mueve el robot.		
		Devuelve
		--------
		un_ambiente.eco(): int
			Distancia (en pasos) al proximo obstaculo del laberinto.
         '''
         self.consumo_bateria('sensar')
         self.historia_acciones.append('s')

         return un_ambiente.eco()         
         
    def salir_del_laberinto(self,un_ambiente):
        '''
		Envia a Estrategia el estado actual (posicion y orientacion) del robot y
        la distancia al proximo obstaculo obtenida por su sensor y recibe
        instrucciones para la proxima accion.
        
		Parametros
		-----------
		un_ambiente: objeto Ambiente
			Instancia del objeto Ambiente creada por main. Es el laberinto en el
        cual se mueve el robot.
        '''

        posicion_sin_avanzar=self.posicion.copy()
        giro = self.giroscopo.copy()
        while not un_ambiente.estoy_fuera() and \
              (self.carga_inicial == 0 or self.bateria > 0):            
            self.mi_estrategia.decidir(self,un_ambiente)
            posicion_sin_avanzar=self.posicion.copy()
            giro = self.giroscopo.copy()
            #visualiza_ascii(un_ambiente)
            #visualiza_mpl(un_ambiente)
    
    def consumo_bateria(self,accion):
        '''
        Maneja el consumo de bateria del robot.
        Si carga_inicial es cero, no hay manejo de bateria, o sea hay bateria infinita.

		Parametros
		-----------
		accion: string 'rotar', 'mover', 'chocar', 'sensar'
        '''
        if self.carga_inicial > 0:            
            gasto_por_mover   = 2
            gasto_por_rotar   = 1
            gasto_por_chocar  = 4
            gasto_por_sensar  = 1 
            if accion == 'rotar':
                 self.bateria -= gasto_por_rotar
            elif accion == 'mover':
                 self.bateria -= gasto_por_mover
            elif accion == 'chocar':
                 self.bateria -= gasto_por_chocar
            elif accion == 'sensar':
                 self.bateria -= gasto_por_sensar
            if self.bateria <= 0:
                print 'Me quede sin bateria!!!'

def visualiza_ascii(un_ambiente):
    '''
    Visualiza el laberinto en modo texto.     
    
    Parametros
    -----------
    un_ambiente: objeto Ambiente
			Instancia del objeto Ambiente creada por main. Es el laberinto en el
        cual se mueve el robot.
    '''
    sizex, sizey = un_ambiente.matriz.shape 
    print " "
    print " "
    print " "
    print " "
    for i in xrange(sizex):
        for j in xrange(sizey):
            if  un_ambiente.robot.posicion[0]==i and un_ambiente.robot.posicion[1]==j:
                print "R",
            else:
                if un_ambiente.matriz[i,j] == 0:
                    print " ",
                else:                    
                    print un_ambiente.matriz[i,j],
        print " "

def visualiza_mpl(un_ambiente):    
    '''
    Visualiza el laberinto en modo texto.     
    
    Parametros
    -----------
    un_ambiente: objeto Ambiente
			Instancia del objeto Ambiente creada por main. Es el laberinto en el
        cual se mueve el robot.
    '''
    import time
    #mpl.interactive(True)
    #axes=un_ambiente.robot.axes    


    fig,axes=plt.subplots(figsize=(4,4))
    #fig=un_ambiente.robot.fig
    #plt.cla
    #plt.clf
    
    
    #axes.set_xlabel('posx')
    #axes.set_ylabel('posy')
    #axes.set_title('laberinto')
    plt.xticks([])
    plt.yticks([])
    mat=un_ambiente.matriz.copy()
    pos=un_ambiente.robot.posicion
    mat[pos[0],pos[1]] = 4
    plt.set_cmap('gray')
    plt.imshow(mat)
    axes.set_position([0,0,1,1])
    
    img_name = './anim/im%04d.png' % len(un_ambiente.robot.historia_posiciones)
    t = time.time()
    fig.savefig(img_name)
    print len(un_ambiente.robot.historia_posiciones),time.time() - t
    
    