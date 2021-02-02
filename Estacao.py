##from scapy.all import sr1, send, IP, TCP
from enum import Enum
from UserProfile import UserProfile
from random import randint
from ip_to_nome_lat_lon import site_from_ip_addr


class System(Enum):
    Windows = 1
    Linux = 2
    Mac = 3


class Estacao():
    def __init__(self, system, user_agent, user):
        self.system = system
        if self.system is System.Windows:
            self.ttl = 128
        else:
            self.ttl = 64
        self.user_agent = user_agent
        self.user_profile = UserProfile(user["behavior"], user["destinations"])
        self.ip = None

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

    def saveDnsReq(self, dnsServer, url, ttlDif, arq, timestamp, userAgentHash):
        ipDest = dnsServer.resolveDnsReq(url)
        port = "53"
        proto = randint(0, 100)
        if proto < 70:
            proto = 17
        else: proto = 6
        try:
            s = site_from_ip_addr(self.ip.split("."))
        except:
            print("Error:",self.ip)
        # yyyy-mm-dd hh:nn:00;ipDnsServer;lat;lon;1;id_cliente;val_ttl;proto;port_dst;id_user_agent;count
        line = (
            timestamp + ";" + dnsServer.ip + ";" + s[4] + ";" + s[5] + ";1;" + s[6] + ";" +
            str(self.ttl - ttlDif)  + ";" + str(proto) + ";" + port + ";" + str(userAgentHash) + ";1\n"
        )
        arq.write(line)
        self.saveReq(ipDest, ttlDif, arq, timestamp, userAgentHash)

    # yyyy-mm-dd hh:nn:00; lat; lon; 1; id_cliente; val_ttl; proto; port_dst; id_user_agent;count
    def saveReq(self, ipDest, ttlDif, arq, timestamp, userAgentHash):
        ip = self.ip.split(".")
        try:
            s = site_from_ip_addr(ip)
        except:
            print("Error:",ip)
        p= randint(6,7)
        if (p==7):p = p+10
        line = timestamp + ";"
        line += s[4] + ";" +  s[5] + ";1;" + s[6]+ ";"
        line += str(self.ttl - ttlDif)  + ";"
        line += str(p)+ ";"
        line += ipDest.split(".")[4]+";"
        line += str(userAgentHash) +";"
        line += "1\n"
        arq.write(line)
