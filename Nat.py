from Estacao import Estacao

class Nat():
    def __init__(self, ip):
        self.itens = [] # quem esta conectado ao Nat
        self.ip = ip

    def add_item(self, item):
        item.ip = self.ip

        # podemos atribuir o ip do item aqui ou 
        # instanciar o item já com um ip, isto é,
        # ler o ip do arquivo.

        self.itens.append(item)

    def gerar_trafego(self, trafego, ttlDecrement = 0):
        for item in self.itens:
            if (isinstance(item, Nat)):
                item.gerar_trafego(trafego, ttlDecrement + 1)
            else:
                pacote = item.gerar_pacote()
                pacote["ttl"] -= ttlDecrement
                trafego.append(pacote)
    
    def retorna_estacoes(self, estacoes, ttlDecrement = 0):
        for item in self.itens:
            if (isinstance(item, Nat)):
                item.retorna_estacoes(estacoes, ttlDecrement + 1)
            else:
                estacoes.append((item, ttlDecrement))
    
    # metodo para visualizar a topologia
    def percorre_rede(self, layer = 0, nat_count = 0):
        if (layer == 0 and nat_count == 0):
            print("### Rede ###")
        else:
            print("### Subrede Nat {}.{} ###".format(nat_count, layer - 1))
        nat_list = []
        line = ""
        for item in self.itens:
            if (isinstance(item, Estacao)):
                line += item.system.name + ", "
            else:
                nat_list.append(item)
        for i in range(len(nat_list)):
            line += "Nat {}.{}, ".format(i+1, layer)
        line = line[:len(line)-2] # remove a ultima virgula
        print(line)
        for nat in nat_list:
            nat.percorre_rede(layer + 1, nat_list.index(nat) + 1)
        if (layer == 0): print("========================================")
