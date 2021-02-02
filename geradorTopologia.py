import json
from random import randint
from enum import Enum

class System(Enum):
    Windows = 1
    Linux = 2
    Mac = 3

# GLOBALS
MAX_HEIGHT = 5 # altura máxima da topologia
PERCENT = 60 # os itens de uma subrede tem este valor % de chance de ser uma estação
NUMBER_OF_BEHAVIORS = 3 # numero de comportamentos de usuários existentes em UserProfile.py

# 1 : user agent Windows
# 2 : user agent Linux
# 3 : user agent Mac

user_agent = {
    "1": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "2": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "3": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
}

def geraDest(maxDestines):
    dest = [
        "www.google.com",
        "www.globo.com.br",
        "www.youtube.com",
        "www.facebook.com",
        "www.twitter.com",
        "www.uff.br",
        "www.instagram.com",
        "www.github.com",
        "www.ligamagic.com.br",
        "www.nytimes.com",
        "www.theguardian.com",
        "www.imdb.com",
        "www.washingtonpost.com",
        "www.mercedes-benz.com.br",
        "www.ferrari.com"
    ] # 15 destinos diferentes
    stationDestines = []
    numberOfDestines = randint(1, maxDestines)
    while len(stationDestines) < numberOfDestines and len(dest) != 0:
        stationDestines.append(dest.pop(randint(0, len(dest) - 1)))
    return stationDestines

def geraUser(maxDestines):
    user = {
        "behavior": randint(1,NUMBER_OF_BEHAVIORS),
        "destinations": geraDest(maxDestines)
    }
    return user

def geraEstacao(maxDestines, id = "0"):
    device = randint(1, 3)
    return {
            "Device": device,
            "id": id,
            "User Agent": user_agent[str(device)],
            "user": geraUser(maxDestines)
            }

def geraSubrede(maxItens, maxDestines, prefix = "", height = 0):
    subrede = []
    numberOfItens = randint(1, maxItens)
    while len(subrede) < numberOfItens:
        id = prefix + str(len(subrede)+1)
        if randint(0,100) > PERCENT and height < MAX_HEIGHT:
            subrede.append(
                {"Device": "N",
                "id": id,
                "subrede": geraSubrede(maxItens, maxDestines, id + ".", height + 1)})
        else:
            subrede.append(geraEstacao(maxDestines, id ))
    return subrede

def resumo_topologia(topologia, summaryFile, layer = 0, subredeId = ""):
    indent = 2 * layer * " "
    if (layer == 0):
        print("### Rede ###", file=summaryFile)
    else:

        print(indent + "### Subrede Nat {} ###".format(subredeId), file=summaryFile)
    nat_list = []
    line = indent + ""
    for item in topologia:
        if item["Device"] != "N":
            line += System(int(item["Device"])).name + ":" + item["id"] + ", "
        else:
            nat_list.append(item)
            line += "Nat:" + item["id"] + ", "
    line = line[:len(line)-2] # remove a ultima virgula
    print(line + "\n", file=summaryFile)
    for nat in nat_list:
        resumo_topologia(nat["subrede"], summaryFile, layer + 1, nat["id"])
    if (layer == 0): print("========================================", file=summaryFile)

if __name__ == '__main__':
    import sys, getopt, os
    maxItens = None
    maxDestines = None
    try:
        opts, args = getopt.getopt(sys.argv[1:],"i:d:",["maxItens=","maxDestines="])
    except getopt.GetoptError as err:
        print(err)
        print('HINT: geradorTopologia.py -i <int> -d <int>')
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-i", "--maxItens"):
            maxItens = int(arg)
        elif opt in ("-d", "--maxDestines"):
            maxDestines = int(arg)
    if(maxItens == None or maxDestines == None):
        print("Error: Missing Argument")
        print('HINT: geradorTopologia.py -i <int> -d <int>')
        print("maxItens(i) = numero maximo de itens de cada subrede")
        print("maxDestines(d) = numero maximo de destinos de cada estacao")
        sys.exit(1)

    topologia = {
        "public Ip": "179.181.250.21",
        "rede": geraSubrede(maxItens, maxDestines)
    }

    fileName = "topologia"
    fileCount = 1
    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            if "topologia" + str(fileCount) in name:
                fileCount += 1
    fileName = fileName + str(fileCount) + ".json"
    with open(fileName, "w") as f:
        json.dump(topologia, f, indent=2)

    fileName = "resumo"
    fileName = fileName + str(fileCount) + ".txt"
    with open(fileName, "w") as summaryFile:
        resumo_topologia(topologia["rede"], summaryFile)

    print("Topologia gerada!")
