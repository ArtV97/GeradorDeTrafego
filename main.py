from Estacao import Estacao, System
from Nat import Nat
from userAgentUtils import load_user_agents, check_user_agent_dic, att_user_agents_file
import json
import datetime

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
### Estações ###
estacoes = []
rede.retorna_estacoes(estacoes)
### User Agent Control ###
indice = {} # dicionario de User-agents
load_user_agents(indice)
arq = open("user_agents2.txt", "w") # arquivo para os novos user_agents

# 24h = 86400 segundos
with open("trafego.txt", "w") as trafego:
    for seconds in range(86400):
        for estacao in estacoes:
            dest = estacao[0].user_profile.getDestination(seconds)
            if dest:
                timestamp = str(datetime.date.today()) + " " + str(datetime.timedelta(seconds=seconds))
                userAgentHash = check_user_agent_dic(estacao[0].user_agent, indice, arq)
                estacao[0].saveReq(dest, estacao[1], trafego, timestamp, userAgentHash)
arq.close()
att_user_agents_file()
