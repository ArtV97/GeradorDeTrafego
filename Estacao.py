from random import randint
from enum import Enum

class System(Enum):
    Windows = 1
    Linux = 2
    Mac = 3

class Estacao():
    def __init__(self, system, user_agent, behavior):
        self.system = system
        if self.system is System.Windows:
            self.ttl = 128
        else:
            self.ttl = 64
        self.user_agent = user_agent
        self.behavior = behavior
        self.ip = None

    def gerar_pacote(self):
        #gera pacote
        return {"system": self.system.name, "Ip": self.ip, "user agent": self.user_agent, "ttl": self.ttl}
