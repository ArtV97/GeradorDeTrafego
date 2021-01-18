from random import randint

# Globals
SMALL_FLOW = [10, 25]
MEDIUM_FLOW = [5, 10]
INTENSE_FLOW = [2, 5]
flow = {"s": SMALL_FLOW, "m": MEDIUM_FLOW, "i": INTENSE_FLOW, "n": [0, 0]}

def randomFlows():
    flows = ["n", "s", "m", "i"]
    randomFlow = []
    while len(randomFlow) < 3:
        n = randint(0, len(flows)-1)
        randomFlow.append(flows[n])
    return randomFlow

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
    stationDest = [[], [], []]
    period = 0 # 0 = morning, 1 = afternoon, 2 = night
    while True:
        maxDest = randint(1, 4)
        while len(stationDest[period]) < maxDest:
            stationDest[period].append(dest.pop(randint(0, len(dest) - 1)))
        period += 1
        if period > 2:
            return stationDest

class UserProfile():
    def __init__(self, flows = randomFlows(), destinations = randomDest()):
        # possiveis valores de flows i(intense), m(medium), s(small), n(null)
        self.usage = {"morning": randint(flow[flows[0]][0], flow[flows[0]][1]),
                      "afternoon": randint(flow[flows[1]][0], flow[flows[1]][1]),
                      "night": randint(flow[flows[2]][0], flow[flows[2]][1])
                      }
        #           morning afternoon night
        # segunda      i        i       n
        #self.usage = {
        #    "monday": {"morning": 1, "afternoon": None, "night": None},
        #    "tuesday ": {"morning": None, "afternoon": 1, "night": None},
        #    "wednesday ": {"morning": None, "afternoon": None, "night": 1},
        #    "thursday ": {"morning": 1, "afternoon": None, "night": None},
        #    "friday": {"morning": None, "afternoon": 1, "night": None}
        #    }
        self.destinations = {"morning": destinations[0], "afternoon": destinations[1], "night": destinations[2]} # lista dos destinos com os quais este usuário se comunica


    # retorna None se o usuario estiver inativo naquele periodo do dia
    # retorna None se o minuto n for multiplo do clock daquele periodo
    def getDestination(self, minute):
        hour = minute / 60
        if 7.00 <= hour < 12.00:
            period = "morning"
        elif 12.00 <= hour < 18.00:
            period = "afternoon"
        else:
            period = "night"
        if self.usage[period] == 0: return None
        send = minute % self.usage[period]
        if send:
            n = randint(0, len(self.destinations[period]) - 1)
            destination = self.destinations[period][n]
            return destination
        return None

if __name__ == "__main__":
    profile = UserProfile(["s", "i", "s"],
        [
            ["206.160.74.213", "128.28.110.71", "186.254.39.192"],
            ["75.96.27.18", "87.208.74.154"],
            ["23.104.179.123"]
        ])
    print("morning flow:", profile.usage["morning"])
    print("morning destines:", profile.destinations["morning"])
    print("afternoon flow:", profile.usage["afternoon"])
    print("afternoon destines:", profile.destinations["afternoon"])
    print("night flow:", profile.usage["night"])
    print("night destines:", profile.destinations["night"])
    print("_________________ Random User ________________")
    profile = UserProfile()
    print("morning flow:", profile.usage["morning"])
    print("morning destines:", profile.destinations["morning"])
    print("afternoon flow:", profile.usage["afternoon"])
    print("afternoon destines:", profile.destinations["afternoon"])
    print("night flow:", profile.usage["night"])
    print("night destines:", profile.destinations["night"])
