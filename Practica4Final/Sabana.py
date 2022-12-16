from Casilla import Casilla
import random
from Herbivoro import  Cebra
from Carnivoro import Leon,Hiena
from threading import Thread, Lock

class Sabana:
    matriz=[]
    dimensionN=0
    dimensionM=0

    def __init__(self,n=75,m=75):#Por defecto la matrix tiene una dimension de 75x75
        self.dimensionN=n
        self.dimensionM=m
        for i in range(n):#Creamos una matrix bidimensional con ceros
            aux=[Casilla(0,0)]*m
            self.matriz.append(aux)
        for i in range(n):#Introducimos una casilla en cada posicion, inicializadas con el valor de i,iaux(representa la coordenada de cada casilla)
            for iaux in range(m):
                self.matriz[i][iaux]=Casilla(i,iaux)

        self.listaManadasHiena= []#representará las manadas de hienas
        self.listaManadasLeones = []#representará las manadas de leones
        self.lockManadasLeones = Lock() #Representa el mutex de la lista que contiene las puntuaciones de cada manada de leones
        self.lockManadasHienas = Lock() #Representa el mutex de la lista que contiene las puntuaciones de cada manada de Hienas
        self.actualGanador=[0,0,""] #representa manada, puntuacion, especie de animal
        self.lockActualGanador=Lock()#Representa el mutex que contiene al ganador en cada momento
        self.lockES=Lock()#Mutex para la entrada salida de texto


    def getManadasLeones(self):
        return self.listaManadasLeones
    def getManadasHienas(self):
        return self.listaManadasHiena


    def getActualGanador(self):
        return self.actualGanador
    def acquireLockManadasHiena(self):
        self.lockManadasHienas.acquire()

    def releaseLockManadasHiena(self):
        self.lockManadasHienas.release()

    def acquireLockManadasLeones(self):
        self.lockManadasLeones.acquire()

    def releaseLockManadasLeones(self):
        self.lockManadasLeones.release()

    def acquireLockActualGanador(self):
        self.lockActualGanador.acquire()

    def releaseLockActualGanador(self):
        self.lockActualGanador.release()

    def acquireLockES(self):
        self.lockES.acquire()

    def releaseLockES(self):
        self.lockES.release()


    def getMatriz(self):#Devuelve la matriz
        return self.matriz


    def getAdyacente(self,casillaN,casillaM):#Nos devuelve las casillas adyacentes a una coordenada dada
        listaAdyaLi=[]
        listaAdyaOc= []
        bool=False
        for i in range(casillaN - 1, casillaN + 2, 1):
            for j in range(casillaM - 1, casillaM + 2, 1):
                if i == casillaN and j == casillaM:
                    continue
                if i == self.dimensionN or j == self.dimensionM:
                    break
                if i >= 0 and j >= 0:
                    self.matriz[i][j].acquireLock()#bloqueamos casilla y añadimos animal a lista
                    if(self.matriz[i][j].getOcupada()==True):
                        listaAdyaOc.append(self.matriz[i][j])
                    if(self.matriz[i][j].getOcupada() ==False):
                        listaAdyaLi.append(self.matriz[i][j])
                        bool=True
                    self.matriz[i][j].releaseLock()#desbloqueamos casilla

        return listaAdyaLi,listaAdyaOc,bool#Devuelve lista con casilals libres, lista conj ocupadas y si una de las casillas adyacentes esta libre avisa con bool

    def getCasilla(self,casillaN,casillaM):
        return self.matriz[casillaN][casillaM]

    def iniciarSabana(self):#Inicializa la sabana creando y posicionando los animales
        #Lista con los animales correspondientes a cada especie
        lista_leones=[]
        lista_hienas=[]
        lista_cebras=[]
        num_max_animales=self.dimensionN*self.dimensionM #Num max de animales
        num_max_leones=int(num_max_animales/10) #La cantidad de leones es la parte entera de esa div
        leonesRandom=random.randint(2,num_max_leones) #pilla un numero de leones logico, min 2 porque min 2 manadas
        num_cebras=leonesRandom*6
        num_hienas=leonesRandom*3
        #el mínimo numero de manadas es 2
        manadas_leones=random.randint(2,leonesRandom)-1
        manadas_cebras=random.randint(2,num_cebras)-1
        manadas_hienas=random.randint(2,num_hienas)-1

        #casilla aleatoria
        nAleatorio = random.randint(0, self.dimensionN - 1)
        mAleatorio = random.randint(0, self.dimensionM - 1)

        for i in range(0,leonesRandom):
            #Creamos un leon
            leon=Leon(self)
            lista_leones.append(leon)
            #buscamos casilla desocupada y la ocupamos
            while(self.matriz[nAleatorio][mAleatorio].getOcupada()==True):
                nAleatorio = random.randint(0, self.dimensionN - 1)
                mAleatorio = random.randint(0, self.dimensionM - 1)
            leon.setManada(random.randint(0,manadas_leones))#Le asignamos una manada
            self.matriz[nAleatorio][mAleatorio].ocuparCasilla(leon)

        nAleatorio = random.randint(0, self.dimensionN - 1)
        mAleatorio = random.randint(0, self.dimensionM - 1)

        for i in range(0,num_cebras):
            #Creamos cebra
            cebra=Cebra(self)
            lista_cebras.append(cebra)
            #buscamos casilla desocupada y la ocupamos
            while (self.matriz[nAleatorio][mAleatorio].getOcupada() == True):
                nAleatorio = random.randint(0, self.dimensionN - 1)
                mAleatorio = random.randint(0, self.dimensionM - 1)

            cebra.setManada(random.randint(0, manadas_cebras))#Le asignamos una manada
            self.matriz[nAleatorio][mAleatorio].ocuparCasilla(cebra)

        nAleatorio = random.randint(0, self.dimensionN - 1)
        mAleatorio = random.randint(0, self.dimensionM - 1)
        for i in range(0,num_hienas):
            #Creamos una hiena
            hiena=Hiena(self)
            lista_hienas.append(hiena)
            # buscamos casilla desocupada y la ocupamos
            while (self.matriz[nAleatorio][mAleatorio].getOcupada() == True):
                nAleatorio = random.randint(0, self.dimensionN - 1)
                mAleatorio = random.randint(0, self.dimensionM - 1)
            hiena.setManada(random.randint(0, manadas_hienas))#Le asignamos una manada
            self.matriz[nAleatorio][mAleatorio].ocuparCasilla(hiena)

        self.listaManadasHiena= [0 for x in range(manadas_hienas+1)]#Inicializamos un array con 0, cada posición representará la puntuación que vaya acumulando cada manada(posicion 0 es manada 0)
        self.listaManadasLeones = [0 for x in range(manadas_leones+1)]


        return lista_cebras,lista_hienas,lista_leones,manadas_cebras,manadas_hienas,manadas_leones#Devolvemos las listas de animales y la cantidad de manadas de cada especie

    def añadirAnimal(self,manada):#nos devuelve una cebra ya posicionada
        nAleatorio = random.randint(0, self.dimensionN - 1)
        mAleatorio = random.randint(0, self.dimensionM - 1)

        self.matriz[nAleatorio][mAleatorio].acquireLock()#Bloqueamos mutex casilla a mirar
        while (self.matriz[nAleatorio][mAleatorio].getOcupada() == True):#En este bucle buscamos la casilla en la que poner el nuevo animal
            self.matriz[nAleatorio][mAleatorio].releaseLock()#Desbloqueamos mutex de casilla que se ha mirado
            nAleatorio = random.randint(0, self.dimensionN - 1)
            mAleatorio = random.randint(0, self.dimensionM - 1)
            self.matriz[nAleatorio][mAleatorio].acquireLock()#bloqueamos mutex de siguiente casilla a revisar

        animal=Cebra(self)
        animal.setManada(manada)
        self.matriz[nAleatorio][mAleatorio].setAnimal(animal)
        self.matriz[nAleatorio][mAleatorio].ocuparCasilla(animal)
        self.matriz[nAleatorio][mAleatorio].releaseLock()#Desbloqueamos mutex de la casilla que hemos ocupado(la ultima que se mira en el while)

        return animal

    def desOcuparCasilla(self,casillaN,casillaM):#Desocupamos la casilla
        self.matriz[casillaN][casillaM].desOcuparCasilla()



