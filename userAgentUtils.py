import sys
import os

def load_user_agents(indice):
	try:
		with open("user_agents.txt","r") as fr:
			for line in fr:
				user_agent = line.strip()
				indice[user_agent] = len(indice) + 1
	except FileNotFoundError:
		f = open("user_agents.txt", "x") # cria o arquivo se ele não existe
		f.close()

def check_user_agent_dic(user_agent, indice, arq):
	if user_agent not in indice:
		indice[user_agent] = len(indice) + 1
		arq.write(user_agent + "\n")
	return indice[user_agent]

def att_user_agents_file():
	with open("user_agents.txt","r") as f1, open("user_agents2.txt","r") as f2, open("user_agents3.txt","w") as f3:
		for line in f1:
			f3.write(line)
		for line in f2:
			f3.write(line)
	os.remove("user_agents.txt")
	os.rename(r'{}'.format(os.path.join("user_agents3.txt")), r'{}'.format(os.path.join("user_agents.txt")))