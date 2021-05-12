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
    print("el tiempo promedio es ", average(data))
    print("la desviacion estándar es ", statistics.stdev(data))
    
def getTime(password):
    res = main(password)
    return res

def Average(lst):
    return sum(lst) / len(lst)


    
if __name__ == "__main__":
    readFile()
    