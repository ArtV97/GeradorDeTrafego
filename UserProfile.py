from random import uniform, randint
from math import sin

def behavior1(x):
    return (-x**2 + 86400*x)/1866000000

def behavior2(x):
    return (sin(x/1000))/2 + 0.5

def behavior3(x): # triangular
    desloc = 54000
    if(x >= desloc):
        ret = 1 - (x - desloc)/3600
    else:
        ret = 1 + (x - desloc)/3600
    if(ret >= 0):
        return ret
    else:
        return 0

def getBehavior(n):
    if n == 1:
        return behavior1
    elif n == 2:
        return behavior2
    elif n == 3:
        return behavior3

class UserProfile():
    def __init__(self, behavior, destinations):
        self.behavior = getBehavior(behavior)
        self.destinations = destinations


    # retorna None se o nao for para enviar o pacote
    # retorna a URL se for enviar
    def getDestination(self, seconds):
        if uniform(0,1) <= self.behavior(seconds):
            n = randint(0, len(self.destinations) - 1)
            return self.destinations[n]
        return None

if __name__ == "__main__":
    profile = UserProfile(3)
    for i in range(86400):
        v = profile.behavior(i)
        print("seconds: {} probabilitie: {}".format(i, v))
