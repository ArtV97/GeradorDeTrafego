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
rede.percorre_rede()

estacoes = []
rede.retorna_estacoes(estacoes)
with open("trafego.txt", "w") as trafego:
    for clock in range(1, 1000):
        for estacao in estacoes:
            for i in range(len(estacao[0].behavior)):
                if (clock % estacao[0].behavior[i]["clock"] == 0):
                    estacao[0].saveReq(estacao[0].behavior[i]["dest"], estacao[1], trafego)
