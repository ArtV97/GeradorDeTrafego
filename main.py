from Estacao import Estacao, System
from Nat import Nat
from userAgentUtils import load_user_agents, check_user_agent_dic, att_user_agents_file
import json
import datetime
import sys, getopt, os

def inicializaRede(obj_rede, ip):
    rede = Nat(ip)
    for obj in obj_rede:
        if obj["Device"] != "N": # Estacao
            rede.add_item(Estacao(System(int(obj["Device"])), obj["User Agent"], obj["behavior"]))
        else: # Nat
            rede.add_item(inicializaRede(obj["subrede"], ip))
    return rede

topologia = None
begin = 32400 # 9h
end = 86400
try:
    opts, args = getopt.getopt(sys.argv[1:],"t:b:e:",["topologia=","hour=","end="])
except getopt.GetoptError as err:
    print(err)
    print('HINT: main.py -t <arq topologia> -b <hh:mm:ss> -e <hh:mm:ss> ')
    sys.exit(1)
for opt, arg in opts:
    if opt in ("-t", "--topologia"):
        topologia = arg
    elif opt in ("-b", "--hour"):
        temp = datetime.time.fromisoformat(arg)
        begin = temp.hour * 3600 + temp.minute * 60 + temp.second
    elif opt in ("-e", "--end"):
        temp = datetime.time.fromisoformat(arg)
        end = temp.hour * 3600 + temp.minute * 60 + temp.second
if(topologia == None):
    print("Error: Missing Argument")
    print('HINT: main.py -t <arq topologia> -b <hh:mm:ss> -e <hh:mm:ss>')
    print("O parâmetro -t(arquivo topologia) é obrigatório!!!")
    sys.exit(1)

# read json file
with open(topologia, 'r') as myfile:
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
    for seconds in range(begin, end):
        for estacao in estacoes:
            dest = estacao[0].user_profile.getDestination(seconds)
            if dest:
                timestamp = str(datetime.date.today()) + " " + str(datetime.timedelta(seconds=seconds))
                userAgentHash = check_user_agent_dic(estacao[0].user_agent, indice, arq)
                estacao[0].saveReq(dest, estacao[1], trafego, timestamp, userAgentHash)
arq.close()
att_user_agents_file()
