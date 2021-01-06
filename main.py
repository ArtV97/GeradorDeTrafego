from Estacao import Estacao, System
from Nat import Nat
import json

'''
def inicializaRede(lines, layer = 0):
    line = lines[layer].rstrip().split(" ")
    rede = Nat()
    nat_count = 0
    for item in line:
        if (item != "N"):
            rede.add_item(Estacao(System(int(item))))
        else:
            nat_count += 1
    for i in range(nat_count):
        rede.add_item(inicializaRede(lines, layer + i + 1))
    return rede
with open("entrada.json", "r") as file:
    var = file.readlines()
rede = Nat()
rede = inicializaRede(var)
rede.percorre_rede()
trafego = []
rede.gerar_trafego(trafego)
for pacote in trafego: print(pacote)
'''

def inicializaRede(obj_rede, ip):
    rede = Nat(ip)
    for obj in obj_rede:
        if obj["Device"] != "N": # Estacao
            rede.add_item(Estacao(System(int(obj["Device"])), obj["User Agent"], obj["behavior"]))
        else: # Nat
            rede.add_item(inicializaRede(obj["subrede"], ip))
    return rede

# read json file
with open('v0.json', 'r') as myfile:
    data = myfile.read()

obj = json.loads(data)
rede = inicializaRede(obj["rede"], obj["public Ip"])
rede.percorre_rede()
trafego = []
rede.gerar_trafego(trafego)
#for pacote in trafego: print(pacote)

estacoes = []
rede.retorna_estacoes(estacoes)
for estacao in estacoes: print("Sistema:" + estacao[0].system.name, "ttl:" + str(estacao[0].ttl - estacao[1]), "behavior:", estacao[0].behavior)