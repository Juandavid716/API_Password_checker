from app.main import main
from numpy import average
import statistics
def readFile():
    data = []
    with open("./app/tiempos.txt") as fname:
        lines = fname.readlines()
        for line in lines:
             res = getTime(line)
             data.append(res)
    print(data)
    print("el tiempo promedio es ", average(data))
    print("la desviacion estándar es ", statistics.stdev(data))
    
def getTime(password):
    res = main(password)
    return res

def Average(lst):
    return sum(lst) / len(lst)

def getEnumerationTime(numbits):
    intelIPC = int(2**(30))*109
    numbits = int(2**(numbits))

    res = numbits / intelIPC
    # dias
    if(res >= 31536000):
        res = res/ 31536000
        res = round(res,0) 
        res = str(res) + " años"
    elif(res >= 86400):
        res = res / 86400
        res = round(res,0) 
        res = str(res) + " días"
    elif (res > 3600):
        res = res / 3600
        res = round(res,0) 
        res = str(res) + " horas"
    elif (res > 60):
        res = res / 60
        res = round(res,0) 
        res = str(res) + " minutos"
    else:
        res = round(res,4) 
        res = str(res) + " segundos"
    return res 


    
if __name__ == "__main__":
    print(getEnumerationTime(30.0))
    