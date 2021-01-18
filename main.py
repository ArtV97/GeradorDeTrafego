from Estacao import Estacao, System
from Nat import Nat
import json

def inicializaRede(obj_rede, ip):
    rede = Nat(ip)
    for obj in obj_rede:
        if obj["Device"] != "N": # Estacao
            rede.add_item(Estacao(System(int(obj["Device"])), obj["User Agent"], obj["behavior"]))
        else: # Nat
            rede.add_item(inicializaRede(obj["subrede"], ip))
    return rede

# read json file
with open('topologia1.json', 'r') as myfile:
    data = myfile.read()

obj = json.loads(data)
rede = inicializaRede(obj["rede"], obj["public Ip"])
#rede.percorre_rede()

estacoes = []
rede.retorna_estacoes(estacoes)
# 7h = 420 minutos
# 23h = 1380 minutos
with open("trafego.txt", "w") as trafego:
    for minute in range(420, 1380):
        for estacao in estacoes:
            dest = estacao[0].user_profile.getDestination(minute)
            if dest:
                estacao[0].saveReq(dest, estacao[1], trafego)