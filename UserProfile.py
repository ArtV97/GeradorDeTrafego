from random import randint

# Globals
SMALL_FLOW = [10, 25]
MEDIUM_FLOW = [5, 10]
INTENSE_FLOW = [2, 5]
flow = {"s": SMALL_FLOW, "m": MEDIUM_FLOW, "i": INTENSE_FLOW, "n": [0, 0]}

class UserProfile():
    def __init__(self, destinations):
        # uso de acordo com o horario(manha [07 - 12], tarde [12 - 18] e noite[18 - 21]).
        # exemplos: ["i", "m", "s"], ["n", "i", "m"]
        # possiveis valores i(intense), m(medium), s(small), n(null)
        # usage poderia tambem ser uma matriz
        #           morning afternoon night
        # segunda      i        i       n
        #self.usage = {"morning": None, "afternoon": None, "night": None}
        self.usage = {
            "monday": {"morning": 1, "afternoon": None, "night": None},
            "tuesday ": {"morning": None, "afternoon": 1, "night": None},
            "wednesday ": {"morning": None, "afternoon": None, "night": 1},
            "thursday ": {"morning": 1, "afternoon": None, "night": None},
            "friday": {"morning": None, "afternoon": 1, "night": None}
            }
        self.destinations = {"morning": destinations[0], "afternoon": destinations[1], "night": destinations[2]} # lista dos destinos com os quais este usuário se comunica

    def getDestination(self, timestamp):
        if 7.00 <= timestamp < 12.00:
            period = "morning"
        elif 12.00 <= timestamp < 18.00:
            period = "afternoon"
        else:
            period = "night"
        flow_intensity = flow[self.usage[period]]
        send = timestamp % randint(flow_intensity[0], flow_intensity[1]) == 0
        if send:
            n = randint(0, len(self.destinations[period]) - 1)
            destination = self.destinations[period][n]
            return destination
        return None

if __name__ == "__main__":
    profile = UserProfile([["Lista de ips manha"], ["Lista de ips tarde"], ["Lista de ips noite"]])
    print(profile.usage["monday"])
    for day in profile.usage:
        print(day)
