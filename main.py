from Estacao import Estacao, System
from Nat import Nat
from Dns import Dns
from userAgentUtils import load_user_agents, check_user_agent_dic, att_user_agents_file
import json
import datetime
import sys, getopt, os

def inicializaRede(obj_rede, ip):
    rede = Nat(ip)
    for obj in obj_rede:
        if obj["Device"] != "N": # Estacao
            rede.add_item(Estacao(System(obj["Device"]), obj["User Agent"], obj["user"]))
        else: # Nat
            rede.add_item(inicializaRede(obj["subrede"], ip))
    return rede

def help():
    print("\nLista de Parâmetros\n")
    print("\t-t or --topologia: nome do arquivo JSON de topologia a ser carregado. Este parâmetro é obrigatório!")
    print("\t-b or --begin: horário de início da simulação. Default = 09:00:00")
    print("\t\tExample: python main.py -t topologia.json -b 14:30:00")
    print("\t-e or --end: horário de término da simulação. Default = 00:00:00")
    print("\t\tExample: python main.py -t topologia.json -e 19:30:00")
    print("\t-c or --count: número de pacotes coletados. Default = None")
    print("\t\tExample: python main.py -t topologia.json -c 3000\n")

topologia = None
begin = 32400 # 9h
end = 86400 # 00h
maxCount = None
date = datetime.date.today()
try:
    opts, args = getopt.getopt(sys.argv[1:],"ho:t:b:e:c:",["help","topologia=","begin=","end=","count="])
except getopt.GetoptError as err:
    print(err)
    print('HINT: main.py -t <arq topologia>')
    print('MORE INFO: main.py --help')
    sys.exit(1)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        help()
        sys.exit(0)
    elif opt in ("-t", "--topologia"):
        topologia = arg
    elif opt in ("-b", "--begin"):
        temp = datetime.time.fromisoformat(arg)
        begin = temp.hour * 3600 + temp.minute * 60 + temp.second
    elif opt in ("-e", "--end"):
        temp = datetime.time.fromisoformat(arg)
        end = temp.hour * 3600 + temp.minute * 60 + temp.second
    elif opt in ("-c", "--count"):
        maxCount = int(arg)
if(topologia == None):
    print("Error: Missing Argument")
    print('HINT: main.py -t <arq topologia>')
    print("\tO parâmetro -t é obrigatório!!!")
    print('MORE INFO: main.py --help')
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

dnsServer = Dns()

# 24h = 86400 segundos
with open("trafego.txt", "w") as trafego:
    if maxCount == None:
        for seconds in range(begin, end):
            for estacao in estacoes:
                url = estacao[0].user_profile.getDestination(seconds)
                if url:
                    timestamp = str(date) + " " + str(datetime.timedelta(seconds=seconds))
                    userAgentHash = check_user_agent_dic(estacao[0].user_agent, indice, arq)
                    estacao[0].saveDnsReq(dnsServer, url, estacao[1], trafego, timestamp, userAgentHash)
                    #estacao[0].saveReq(dest, estacao[1], trafego, timestamp, userAgentHash)
    else:
        count = 0
        while count < maxCount:
            for seconds in range(begin, end):
                for estacao in estacoes:
                    url = estacao[0].user_profile.getDestination(seconds)
                    if count < maxCount and url:
                        timestamp = str(date) + " " + str(datetime.timedelta(seconds=seconds))
                        userAgentHash = check_user_agent_dic(estacao[0].user_agent, indice, arq)
                        estacao[0].saveDnsReq(dnsServer, url, estacao[1], trafego, timestamp, userAgentHash)
                        #estacao[0].saveReq(dest, estacao[1], trafego, timestamp, userAgentHash)
                        count += 2
                    else:
                        break
            date += datetime.timedelta(days=1)
            begin = 0
arq.close()
att_user_agents_file()
