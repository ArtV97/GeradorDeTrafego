##from scapy.all import sr1, send, IP, TCP
from enum import Enum


class System(Enum):
    Windows = 1
    Linux = 2
    Mac = 3


class Estacao():
    def __init__(self, system, user_agent, frequence, clock):
        self.system = system
        if self.system is System.Windows:
            self.ttl = 128
        else:
            self.ttl = 64
        self.user_agent = user_agent
        self.frequence = frequence
        self.clock = clock
        self.ip = None

    def gerar_pacote(self):
        # gera pacote
        return {"system": self.system.name, "Ip": self.ip, "user agent": self.user_agent, "ttl": self.ttl}

    ## def sendReq (self, ttldif, dest):
    ##    syn = IP(dst=dest, ttl=(self.ttl-ttldif), id=37) / TCP(dport=80, flags='S')
    ##    syn_ack = sr1(syn)
    ##    ack = IP(dst=dest, ttl=(self.ttl-ttldif), id=37) / TCP(dport=80, sport=syn_ack[TCP].dport,
    ##                                                           seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1,
    ##                                                           flags='A')
    ##    out_ack = send(ack)
    ##    getStr = 'GET / HTTP/1.0\r\nHost:45.0.0.2\r\nUser-agent:' + str(self.userAgent) + '\r\n\r\n'

    ##   req = IP(dst=dest, ttl=(self.ttl-ttldif), id=37) / TCP(dport=80, sport=syn_ack[TCP].dport,
    ##                                                           seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1,
    ##                                                           flags='A') / getStr
    ##    send(req)

    def saveReq(self, ipDest, ipOrig, ttlDif):
        a = str(ipOrig) + " >> " + str(ipDest) + ";" + str(self.ttl - ttlDif) + ";\"" + self.user_agent + "\"\n"
        f = open("demoSaida.txt", "a")
        f.write(a)
        f.close()
