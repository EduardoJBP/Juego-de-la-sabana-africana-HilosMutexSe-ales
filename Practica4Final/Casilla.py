import random
from threading import Lock, Condition


class Casilla:
    ocupada=False
    casillaN=0
    casillaM=0

    def __init__(self,n,m):#Una casilla pertenece a la coordenada (n,m) de la matriz de la sabana
        self.ocupada=False #Atributo que nos indica si una casilla esta ocupada o no
        self.casillaN=n
        self.casillaM=m
        self.lock=Lock()#Inicializamos el Mutex de la casilla

    def ocuparCasilla(self,animal):#Actualizamos la casilla con el nuevo animal
        self.ocupada=True
        animal.setCasillaN(self.casillaN)
        animal.setCasillaM(self.casillaM)
        self.animal=animal

    def getCasillaN(self):
        return self.casillaN
    def getCasillaM(self):
        return self.casillaM
    def getLock(self):
        return self.lock

    def desOcuparCasilla(self):
        self.ocupada=False

    def getCond(self):
        return self.condition

    def getOcupada(self):
        return self.ocupada

    def getAnimal(self):
        return self.animal


    def acquireLock(self):
        self.lock.acquire()

    def releaseLock(self):
        self.lock.release()

    def getAnimal(self):
        return self.animal

    def setAnimal(self,animal):
        self.animal=animal