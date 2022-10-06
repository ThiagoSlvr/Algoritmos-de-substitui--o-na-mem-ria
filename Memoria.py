#FIFO - FIRST IN FIRST OUT, MRU - Menos Recentemente Usada, NUF - Não usado Frequentemente, Ótimo
#ENTRADA:
#Número de molduras de página na memória|número de páginas do processo|sequência em que as páginas são acessadas
#4|8|1 2 2 2 3 4 3 4 5 5 6 1 3 2 6 7 7 7 8
#SAIDA:
#Número de trocas de página no algoritmo FIFO|Número de trocas de página no algoritmo MRU|
#|Número de trocas de página no algoritmo NUF|Número de trocas de página no algoritmo ótimo|nome do algoritmo com desempenho mais próximo do ótimo
#12|12|11|9|NUF

#Thiago Chim Silvera - 110668, Nicolas Daltrozo - 112871

from operator import attrgetter


def FIFO(entrada):
    #Inicializa as variaveis para moldura e contador de trocas
    moldura = []
    miss_count = 0
    #Para cada valor na Sequencia de entradas:
    for seq in entrada["Sequencia"]:
        #Se ela já não estiver dentro da moldura:
        if not seq in moldura:
            #Se não houver espaço dentro da moldura:
            if len(moldura) >= entrada["Moldura"]:
                moldura.pop(0)
            moldura.append(seq)
            miss_count += 1
    return miss_count


#classe pagina para armazenar o nome e a quantidade de vezes que foi utilizado
class pagina:
	def __init__(self, nome, temp):
		self.nome = nome
		self.temp = temp
	def __repr__ (self):
		return '(' + str(self.nome) + ' ' + str(self.temp) + ')'

#funçao de nao utilizado frequentemente
def MRU(entrada):

	mem=[]
	processos=[pagina(i, None) for i in range(1, entrada['Paginas']+1)]
	relogio=0
	error=0

	#percorre a lista  de processos a serem chamados para memoria
	for seq in entrada['Sequencia']:
		#verifica se o processo esta na memoria
		if not processos[seq-1] in mem:
			error+=1
			#verifica se o tamanho da memoria é o maior ou igual da moldura
			if (len(mem) >= entrada['Moldura']):
				mem.remove(min(mem, key=attrgetter('temp')))
			mem.append(processos[seq-1])
		processos[seq-1].temp=relogio
		relogio+=1
	return error

#funçao de nao utilizado frequentemente
def NUF(entrada):

	mem=[]
	processos=[pagina(i, 0) for i in range(1, entrada['Paginas']+1)]
	error=0
	
	#percorre a lista  de processos a serem chamados para memoria
	for seq in entrada['Sequencia']:
		#verifica se o processo esta na memoria
		if not processos[seq-1] in mem:
			error+=1
			#verifica se o tamanho da memoria é o maior ou igual da moldura
			if (len(mem) >= entrada['Moldura']):
				mem.remove(min(mem, key=attrgetter('quant')))
			mem.append(processos[seq-1])
			processos[seq-1].quant=0
		processos[seq-1].quant+=1
	return error

def Otimo(entrada):
    #Inicializa as variaveis para moldura e contador de trocas
    moldura = []
    miss_count = 0
    max_dist = 0
    #Para cada entrada na Sequencia de entradas:
    for i in range(len(entrada["Sequencia"])):
        #Se ela já não estiver dentro da moldura:
        if not entrada["Sequencia"][i] in moldura:
            miss_count += 1
            #Se não houver espaço dentro da moldura:
            if len(moldura) >= entrada["Moldura"]:
                max_dist = 0
                max_dist_index = 0
                #De 0 até o tamanho total da moldura:
                for j in range(len(moldura)):
                    dist = 0
                    #De i até o tamanho total da entrada:
                    for k in range(i, len(entrada["Sequencia"])):
                        dist += 1
                        #Se o processo dentro da moldura for igual a entrada atual:
                        if (moldura[j] == entrada["Sequencia"][k]):
                            if (dist > max_dist):
                                max_dist = dist
                                max_dist_index = j
                            break
                        #Se k+1 for igual ao tamanho total da entrada:
                        elif ((k+1) == len(entrada["Sequencia"])):
                            max_dist = len(entrada["Sequencia"])   
                            max_dist_index = j
                            break
                moldura.pop(max_dist_index)
            moldura.append(entrada["Sequencia"][i])
    return miss_count

def main():
    a = open("inMemoria", "r")
    txt = a.read().splitlines()
    a.close()
    for linha in (txt):
        linha = linha.split("|")
        entrada={"Moldura":int(linha[0]),"Paginas":int(linha[1]),"Sequencia":[int(v) for v in linha[2].split(" ")]}
        FIFO_Count = FIFO(entrada)
        MRU_Count = MRU(entrada)
        NUF_Count = NUF(entrada)
        Otimo_Count = Otimo(entrada)
        best = min(FIFO_Count, MRU_Count, NUF_Count)
        if (NUF_Count > FIFO_Count and FIFO_Count < MRU_Count):
            best = "FIFO"
        elif (FIFO_Count > NUF_Count and NUF_Count < MRU_Count):
            best = "NUF"
        elif (NUF_Count > MRU_Count and MRU_Count < FIFO_Count):
            best = "MRU"
        else:
            best = "empate"
        print (FIFO_Count,"|", MRU_Count,"|", NUF_Count,"|", Otimo_Count,"|", best)

main()

