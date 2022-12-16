from Animal import Animal
import threading
import random
import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)#Para poder comprobar de manera correcta cada hilo

class Carnivoro(Animal):

    def actualizarManada(self,puntuacion):#Metodo con implementación particular en hienas y leones
        pass
    def comer(self):#Obtenemos las coordenadas de la casilla en la que está el animal
        casillaN = self.casillaN
        casillaM = self.casillaM

        # Obtenemos las casillas adyacentes ocupadas, las libres y un booleano que nos dira si hay alguna libre
        listaAdyaLi, listaAdyaOc, bool = self.sabana.getAdyacente(casillaN,casillaM)  # En este caso solo nos interesa listaAdyaOc
        if len(listaAdyaOc) == 0:#Si no hay ocupadas entonces no puede comer
            self.sabana.acquireLockES()
            especie=self.printEspecie()
            print(especie+ " en N: %d" %self.casillaN+" M: %d"%self.casillaM+" no puede comer, no tiene animales a su alrededor")
            self.sabana.releaseLockES()
            return
        else:#En caso contrario se elige una casilla aleatoria a comer
            nrandom = random.randint(0, len(listaAdyaOc) - 1)
            casillaRandom = self.sabana.getCasilla(listaAdyaOc[nrandom].getCasillaN(), listaAdyaOc[nrandom].getCasillaM())  # Pillamos una casilla random de la lista de ocupadas
            puedeComer = self.puedeComer(casillaRandom)  # Comprobamos si puede comer, metodo con implementacion particular en leon y hiena

            if (puedeComer == False):  # si no puede comer entonces se manda a vivir
                self.sabana.acquireLockES()
                especie=self.printEspecie()
                print(especie + " en N: %d" % self.casillaN + " M: %d" % self.casillaM + " no puede comer, no cumple condiciones")
                self.sabana.releaseLockES()
                return

            self.sabana.acquireLockES()
            especie=self.printEspecie()
            especieComer=casillaRandom.getAnimal().printEspecie()
            print(especie + " en casilla N= %d" % casillaN + " casilla M: %d" % casillaM + " se quiere comer a " + especieComer + " en N= %d" % casillaRandom.getCasillaN() + " M: %d" % casillaRandom.getCasillaM())
            self.sabana.releaseLockES()

            casillaRandom.acquireLock()  #bloqueamos casilla del que comemos, matamos al animal y la desocupamos
            casillaRandom.getAnimal().setVivo(False)  # poner animal a muerto
            animalComido = casillaRandom.getAnimal()
            casillaRandom.desOcuparCasilla()

            # Desocupamos casilla origen
            self.sabana.getCasilla(casillaN, casillaM).acquireLock()
            self.sabana.desOcuparCasilla(casillaN, casillaM)

            casillaRandom.ocuparCasilla(self.sabana.getCasilla(casillaN, casillaM).getAnimal())  # Ocupamos la casilla del animal comido
            self.sabana.getCasilla(casillaRandom.getCasillaN(), casillaRandom.getCasillaM()).releaseLock()  #liberamos lock de casilla destino
            self.sabana.getCasilla(casillaN, casillaM).releaseLock()# liberamos lock de casilla origen

            puntuacion = self.añadirPunto(animalComido)# Obtenemos la puntuacion que le corresponde al animal por comerse al otro
            puntuacionAux=self.actualizarManada(puntuacion)# Obtenemos la puntuacion de la manada tras comerse al animal y la actualizamos

            if (animalComido.getEspecie() == "cebra"):  # Si te comes una cebra se crea otro hilo
                logging.debug('Se CREA HILO DE CEBRA')
                animalNuevo = self.sabana.añadirAnimal(animalComido.getManada())  # Creamos animal e hilo
                animalNuevo.start()

            # Bloqueamos mutex, actualizamos valor de actual ganador si es necesario y desbloqueamos
            self.sabana.acquireLockActualGanador()
            if (puntuacionAux > self.sabana.getActualGanador()[1] and self.sabana.getActualGanador()[1] < 20):#Si la puntuación de la manada es mayor y no ha habido ganador se actualiza actual ganador
                self.sabana.actualGanador[0] = self.getManada()
                self.sabana.actualGanador[1] = puntuacionAux
                self.sabana.actualGanador[2] = self.getEspecie()
            self.sabana.releaseLockActualGanador()

        self.sabana.acquireLockES()
        especie=self.printEspecie()
        print(especie + " se mueve a casilla N= %d" % casillaRandom.getCasillaN() + " casilla M: %d" % casillaRandom.getCasillaM())
        self.sabana.releaseLockES()


class Hiena(Carnivoro,threading.Thread):

    def __init__(self, sabana):
        super().__init__("hiena", sabana)  # Inicializo la especie a Hiena
        threading.Thread.__init__(self)  #Inicializar thread

    def actualizarManada(self,puntuacion):#Metodo que se utiliza para actualizar la puntuación de la manada tras comerse a un animal
        self.sabana.lockManadasHienas.acquire()
        self.sabana.getManadasHienas()[self.getManada()] = self.sabana.getManadasHienas()[self.getManada()] + puntuacion
        puntuacionAux = self.sabana.getManadasHienas()[self.getManada()]
        self.sabana.lockManadasHienas.release()
        return puntuacionAux

    def printEspecie(self):
        return '\033[93m'+self.getEspecie()+'\033[0m'
    #El método nos devuelve los puntos que le corresponden al animal por comérse a otro, hiena solo come cebra
    def añadirPunto(self,animal):
        puntuacion=1
        return puntuacion

    def accionRealizar(self):#comer,moer,desca
        accion= random.randint(0,2)# una hiena hace lo que sea
        return accion

    def getVelocidad(self):
        return self.getManada() / 85000+0.000003#hiena el 3º que se mueve más deprisa, velocidad para cada manada es distinta, así que depende de la manada en la que está

    def puedeComer(self,casillaAComer):#Una hiena come sólo cebras
        casillaActual = self.sabana.getCasilla(self.casillaN, self.casillaM)
        if (casillaAComer.getAnimal().getEspecie() == "cebra"):  # Para comerse a una cebra hace falta superioridad numérica
            listaAdyaLi, listaAdyaOc, bool = self.sabana.getAdyacente(casillaActual.getCasillaN(),casillaActual.getCasillaM())
            contadorHiena = 1
            contadorCebra = 0
            for i in listaAdyaOc:#Contamos cantidad de hienas y cebras
                if (i.getAnimal().getEspecie() == "hiena"):
                    contadorHiena = contadorHiena + 1
                elif (i.getAnimal().getEspecie() == "cebra"):
                    contadorCebra = contadorCebra + 1
            if (contadorHiena > contadorCebra):
                return True
        return False






class Leon(Carnivoro,threading.Thread):
    def __init__(self, sabana):
        super().__init__("leon", sabana)  #especie a Leon
        threading.Thread.__init__(self)  #Inicializar thread

    def actualizarManada(self,puntuacion):#Metodo que se utiliza para actualizar la puntuación de la manada tras comerse a un animal
        self.sabana.lockManadasLeones.acquire()
        self.sabana.getManadasLeones()[self.getManada()] = self.sabana.getManadasLeones()[self.getManada()] + puntuacion
        puntuacionAux = self.sabana.getManadasLeones()[self.getManada()]
        self.sabana.lockManadasLeones.release()
        return puntuacionAux

    def printEspecie(self):
        return '\033[91m'+self.getEspecie()+'\033[0m'
    #El método nos devuelve los puntos que le corresponden al animal por comérse a otro
    def añadirPunto(self,animal):
        if (animal.getEspecie()=="cebra"):
            puntuacion=1
        else:
            puntuacion= 2
        return puntuacion

    def getVelocidad(self):
        return self.getManada()/100000+0.000001#leon se mueve más deprisa, velocidad para cada manada es distinta, así que depende de la manada en la que está

    def accionRealizar(self):#comer,moer,desca
        accionLeon=random.randint(0,100)
        if(accionLeon<60):#el 60% de las veces el leon descansará
            accion=1
        else:
            accion = random.choice((0,2))#el 40% de las veces o come o se mueve
        return accion

    def puedeComer(self,casillaAComer):
        if (casillaAComer.getAnimal().getEspecie() == "cebra"):  # Siempre que un leon se quiera comer a una cebra puede
            return True
        casillaActual = self.sabana.getCasilla(self.casillaN, self.casillaM)
        if (casillaAComer.getAnimal().getEspecie() == "hiena"):  # Si el numero de leones es mayor o igual al de hienas adyacentes a él, se la puede comer
            listaAdyaLi, listaAdyaOc, bool = self.sabana.getAdyacente(casillaActual.getCasillaN(),casillaActual.getCasillaM())
            contadorhiena = 0
            contadorLeon = 1
            for i in listaAdyaOc:  # contar leones y hienas adyacentes
                if (i.getAnimal().getEspecie() == "hiena"):
                    contadorhiena = contadorhiena + 1
                elif (i.getAnimal().getEspecie() == "leon"):
                    contadorLeon = contadorLeon + 1
            if (contadorLeon >= contadorhiena):
                return True
        return False

