import threading
import random
import time


class Animal(threading.Thread):
    especie=""
    tipo=""
    casillaN=0
    casillaM=0
    manada=0
    vivo=True

    def __init__(self, especie,sabana):#Se inicializa un animal indicando la especie y la sabana
        self.especie = especie
        if(especie=="leon" or especie=="hiena"):#dependiendo de la especie, pertenece a herbivoro o no
            self.tipo = "carnivoro"
        elif(especie=="cebra"):
            self.tipo="herbivoro"
        self.sabana=sabana

    def run(self):
        while self.sabana.getActualGanador()[1] < 20 and self.getVivo() == True:
            accion = self.accionRealizar()#método con implementación distinta dependiendo del animal
            if accion == 0:  # Si el numero aleatorio es 0 puede moverse
                time.sleep(self.getVelocidad())  # Cada animal tiene una velocidad dependiente de la especie y la manada
                self.moverse()
            elif accion == 1:  # Si el numero aleatorio es 1 descansa
                self.descansar()#método con implementación distinta dependiendo de la especie
            elif accion == 2:  # Si el numero aleatorio es 2 come
                self.comer()#método con implementación distinta dependiendo de la especie
            else:
                pass
        return
    #Metodo usado para imprimir por pantalla la especie de cada animal con colores
    def printEspecie(self):
        pass
    #Métodos para indicar donde se encuentra el animal
    def setCasillaN(self,N):
        self.casillaN=N
    def setCasillaM(self,M):
        self.casillaM=M

    #Saber si el animal está vivo
    def getVivo(self):
        return self.vivo

    #Para poner el animal a muerto
    def setVivo(self,bool):
        self.vivo = bool

    #Indicar la manada del animal
    def setManada(self,manada):
        self.manada=manada
    def getManada(self):
        return self.manada

    #Saber donde se encuentra el animal
    def getCasillaN(self):
        return self.casillaN
    def getCasillaM(self):
        return self.casillaM

    # Método genérico pero con implementación particular
    def comer(self):
        pass

    #Saber la especie del animal
    def getEspecie(self):
        return self.especie

    #Devolver el tipo de animal
    def setTipo(self,tipo):
        self.tipo=tipo

    def setEspecie(self,especie):
        self.especie=especie
    def getTipo(self):
        return self.tipo

    # Método genérico pero con implementación particular
    def accionRealizar(self):  # comer,mover,descansar
        pass

    # Método genérico pero con implementación particular
    def getVelocidad(self):
        pass

    #todos los animales descansan u ntiempo aleatorio
    def descansar(self):
        self.sabana.acquireLockES()
        especie=self.printEspecie()
        print("Descansa "+especie+ " en N: %d" %self.casillaN+" M: %d"%self.casillaM)
        self.sabana.releaseLockES()
        time.sleep(random.uniform(0,1)) #descansan entre 0 y 1 segundos(un float)

    def moverse(self):#Todos se mueven igual
        casillaN=self.casillaN
        casillaM=self.casillaM
        listaAdyaLi,listaAdyaOc,bool=self.sabana.getAdyacente(casillaN,casillaM)#obtenemos las adyacentes
        if len(listaAdyaLi) == 0:# Si no hay posicion libre el animal no se mueve
            self.sabana.acquireLockES()
            especie=self.printEspecie()
            print(especie+ " se queda en la misma posicion con n " + str(casillaN) + " y m " + str(casillaM))
            self.sabana.releaseLockES()
            return
        else: #si hay casillas libres entonces pilla una aleatoria
            nrandom= random.randint(0,len(listaAdyaLi)-1)
            casillaRandom=self.sabana.getCasilla(listaAdyaLi[nrandom].getCasillaN(), listaAdyaLi[nrandom].getCasillaM())#Representará la casilla aleatoria
            self.sabana.acquireLockES()
            especie=self.printEspecie()
            print(especie + " en casilla N= %d" % casillaN + " casilla M: %d" % casillaM + " se quiere mover a N= %d" % casillaRandom.getCasillaN() + " M: %d" % casillaRandom.getCasillaM())
            self.sabana.releaseLockES()

            self.sabana.getCasilla(self.casillaN,self.casillaM).acquireLock()#bloqueamos mutex de casilla origen
            self.sabana.getCasilla(self.casillaN,self.casillaM).desOcuparCasilla()#Desocupar casilla origen
            self.sabana.getCasilla(self.casillaN, self.casillaM).releaseLock()#desbloqueamos mutex casilla origen

            self.sabana.getCasilla(casillaRandom.getCasillaN(),casillaRandom.getCasillaM()).acquireLock()#Bloquear mutex de casilla destino y ocuparla
            self.sabana.getCasilla(casillaRandom.getCasillaN(),casillaRandom.getCasillaM()).ocuparCasilla(self)
            self.sabana.getCasilla(self.casillaN,self.casillaM).releaseLock()#desbloqueamos mutex casilla origen

            self.sabana.acquireLockES()
            especie=self.printEspecie()
            print(especie+" se mueve a casilla N= %d"%casillaRandom.getCasillaN()+" casilla M: %d"%casillaRandom.getCasillaM())
            self.sabana.releaseLockES()
        return






