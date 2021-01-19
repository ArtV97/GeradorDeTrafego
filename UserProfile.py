from random import uniform, randint
from math import sin

def randomDest():
    dest = [
        "206.160.74.213",
        "128.28.110.71",
        "186.254.39.192",
        "75.96.27.18",
        "87.208.74.154",
        "125.40.123.136",
        "130.125.99.157",
        "220.171.28.94",
        "92.170.228.200",
        "133.188.176.251",
        "108.96.103.167",
        "16.221.8.140",
        "23.104.179.123",
        "215.144.163.221",
        "39.229.161.77"
    ] # 15 destinos diferentes
    stationDest = []
    maxDest = randint(1, 6)
    while len(stationDest) < maxDest:
        stationDest.append(dest.pop(randint(0, len(dest) - 1)))
    return stationDest

def behavior1(x):
    return (-x**2 + 86400*x)/1866000000

def behavior2(x):
    return (sin(x/1000))/2 + 0.5

def getBehavior(n):
    if n == 0:
        return behavior1
    elif n == 1:
        return behavior2

class UserProfile():
    def __init__(self, behavior = randint(0,1), destinations = randomDest()):
        # segunda      i        i       n
        #self.usage = {
        #    "monday": {"morning": 1, "afternoon": None, "night": None},
        #    "tuesday ": {"morning": None, "afternoon": 1, "night": None},
        #    "wednesday ": {"morning": None, "afternoon": None, "night": 1},
        #    "thursday ": {"morning": 1, "afternoon": None, "night": None},
        #    "friday": {"morning": None, "afternoon": 1, "night": None}
        #    }
        self.behavior = getBehavior(behavior)
        self.destinations = destinations


    # retorna None se o nao for para enviar o pacote
    # retorna o destino se for enviar
    def getDestination(self, seconds):
        if uniform(0,1) <= self.behavior(seconds):
            n = randint(0, len(self.destinations) - 1)
            return self.destinations[n]
        return None

if __name__ == "__main__":
    profile = UserProfile()
    for i in range(86400):
        v = profile.behavior(i)
        print(v)
