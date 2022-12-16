
from Sabana import Sabana
import time

cadena = "bienvenido al juego".capitalize()
cadena=cadena.upper()
print( cadena.center(50, "="))

valorDefecto=input("Siendo una matriz NxM, desea utilizar valores por defecto N=75, M=75?(Y/N): ")
valorDefecto=valorDefecto.upper()

while(valorDefecto != "N" and valorDefecto !="Y"):
    valorDefecto = input("Siendo una matriz NxM, desea utilizar valores por defecto N=75, M=75?(Y/N): ")
    valorDefecto = valorDefecto.upper()

if(valorDefecto=="N"):
    # Introducir los valores de la matriz M y N
    print("Siendo una matriz NxM, seleccione los siguientes valores: Nótese que N*M>=20 y N o M distintos de 1 para un correcto funcionamiento")
    N = input("Indique el valor de n:")
    M = input("Indique el valor de M:")
else:
    N=75
    M=75

try:#Control de errores a la hora de definir tamaño de la sabana
    N=int(N)#Casting de string a int
    M=int(M)
except:
    N=0
    M=0

while(N*M<20 or (N==1 or M==1)):#Si M*N<20 se introducen los valores de nuevo
    print("Valores incorrectos, siendo una matriz NxM, seleccione los siguientes valores: Nótese que N*M>=20 y N o M distintos de 1")
    N = input("Indique el valor de n:")
    M = input("Indique el valor de M:")
    try:
        N = int(N)  # Casting de string a int
        M = int(M)
    except:
        N = 0
        M = 0

sabana = Sabana(N,M)#Creamos la sabana
cebras, hienas, leones,manadasCebras,manadasHienas,manadasLeones = sabana.iniciarSabana()#Inicializamos la sabana
hilos = []  #Iremos añadiendo los hilos

print()
print("El estado actual de la sabana es el siguiente: ")
print("El numero de leones es %d" %len(leones)+" , el numero de hienas es %d"%len(hienas)+", el numero de cebras es %d" %len(cebras))
for fila in sabana.getMatriz():
    for valor in fila:
        if(valor.getOcupada()==True):
            especie=valor.getAnimal().printEspecie()
            print("\t", especie, end=" ")
        else:
            print("\t", "\033[1;35m"+"-----\033[0m", end=" ")
    print()
time.sleep(0.5)#para poder ver el estado correctamente


for i in leones:
    hilos.append(i)#añadimos el hilo
for i in cebras:
    hilos.append(i)
for i in hienas:
    hilos.append(i)

for i in hilos:#Comenzamos la ejecución de cada hilo
    i.start()

for i in hilos:#Sincronizamos los hilos
    i.join()


for fila in sabana.getMatriz():
    for valor in fila:
        if(valor.getOcupada()==True):
            especie=valor.getAnimal().printEspecie()
            print("\t", especie, end=" ")
        else:
            print("\t", "\033[1;35m"+"-----\033[0m", end=" ")
    print()

print("\033[1;34m"+"La manada ganadora pertenece a la especie: "+sabana.getActualGanador()[2].upper()+", de la manada: %d"%sabana.getActualGanador()[0]+"\033[0m")

