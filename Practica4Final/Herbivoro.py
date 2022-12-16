import random
import time
from Animal import Animal
from threading import Thread
import logging

class Herbivoro(Animal):
    def comer(self):#Una cebra come hierba
        self.sabana.acquireLockES()
        especie=self.printEspecie()
        print(especie+" en N: %d"%self.casillaN+" M: %d"%self.casillaM+" está comiendo hierba porque es herbivoro")
        self.sabana.releaseLockES()

    def printEspecie(self):
       return '\033[92m'+self.getEspecie()+'\033[0m'
    def accionRealizar(self):#comer,mover,descansar
        accion = random.randint(0,2)
        return accion

class Cebra(Herbivoro,Thread):

    def __init__(self, sabana):
        super().__init__("cebra",sabana)  # Inicializo la especie a cebra
        Thread.__init__(self)  #Inicializar thread

    def getVelocidad(self):#La velocidad de la cebra
        return (self.getManada() / 99000+0.000002)  # cebra el 2º que se mueve más deprisa, velocidad para cada manada es distinta, así que depende de la manada en la que está


