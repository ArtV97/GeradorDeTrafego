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

estacoes = []
rede.retorna_estacoes(estacoes)
# 24h = 86400 segundos
with open("trafego.txt", "w") as trafego:
    for seconds in range(1, 86401):
        for estacao in estacoes:
            dest = estacao[0].user_profile.getDestination(seconds)
            if dest:
                estacao[0].saveReq(dest, estacao[1], trafego)