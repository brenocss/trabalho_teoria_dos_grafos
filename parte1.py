import numpy as np
import argparse
import statistics
from timeit import default_timer as timer
from queue import Queue
from queue import LifoQueue
import bisect

class grafo_generico():
    def __init__(self,arestas,numero_vertices):
        self.numero_vertices = numero_vertices
        self.lista_graus = np.zeros(numero_vertices)
        self.numero_arestas = len(arestas)
        

    def gera_vertices_adjacentes(self,vertice_origem):
        for vertice in range(self.numero_vertices):
                yield vertice
        
    def calcula_maior_grau(self):
        return max(self.lista_graus)

    def calcula_menor_grau(self):
        return min(self.lista_graus)

    def calcula_media_grau(self):
        return statistics.mean(self.lista_graus)

    def calcula_mediana_grau(self):
        return statistics.median(self.lista_graus)

    def gera_arvore_largura(self, vertice_raiz):  
        vetor_nivel_arvore = np.zeros(self.numero_vertices)
        vetor_pai_vertice = np.full(self.numero_vertices,None)
        vetor_pai_vertice[vertice_raiz] = None
        def funcao_auxiliar(vertice_filho, vertice_pai):
            vetor_pai_vertice[vertice_filho] = vertice_pai
            vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
            return None
        self.busca_largura( vertice_raiz, funcao_auxiliar)
        # onde tiver 0 e nao for raiz = none em vetor nivel arvore
        for vertice in range(self.numero_vertices):
            if vetor_nivel_arvore[vertice] == 0 and vertice != vertice_raiz:
                vetor_nivel_arvore[vertice] = None
        return list(vetor_pai_vertice), list(vetor_nivel_arvore)

    def busca_largura(self, vertice_raiz, funcao_auxiliar = lambda x,y:0, condicao_parada = False):
        vetor_explorados = np.zeros(self.numero_vertices)#vetor nivel do vertice    
        vetor_explorados[vertice_raiz] = 1
        fila = Queue(maxsize=self.numero_vertices)
        fila.put(vertice_raiz)
        retorno_func_auxiliar = None
        while (not fila.empty()) and ((retorno_func_auxiliar == None) or (not condicao_parada)):
            vertice_sendo_explorado = fila.get()
            for vertice_adjacente in self.gera_vertices_adjacentes(vertice_sendo_explorado):
                if vetor_explorados[vertice_adjacente] == 0:
                        retorno_func_auxiliar = funcao_auxiliar(vertice_adjacente,vertice_sendo_explorado)
                        vetor_explorados[vertice_adjacente] = 1
                        fila.put(vertice_adjacente)                          
                if retorno_func_auxiliar != None and condicao_parada:
                    break

        return retorno_func_auxiliar
        
    def gera_arvore_profundidade(self,vertice_raiz):
        vetor_nivel_arvore = np.zeros(self.numero_vertices)
        vetor_pai_vertice = np.full(self.numero_vertices,None)
        vetor_pai_vertice[vertice_raiz] = None

        vetor_explorados = np.zeros(self.numero_vertices)#vetor nivel do vertice    
        pilha = LifoQueue(maxsize=0)
        pilha.put(vertice_raiz)
        while not pilha.empty():
            vertice_sendo_explorado = pilha.get()
        
            if vetor_explorados[vertice_sendo_explorado] == 0:
                vetor_explorados[vertice_sendo_explorado] = 1
                for vertice_adjacente in self.gera_vertices_adjacentes(vertice_sendo_explorado,True):
                    if (vetor_explorados[vertice_adjacente] == 0) and (vertice_adjacente != vertice_raiz):
                        vetor_pai_vertice[vertice_adjacente] = vertice_sendo_explorado
                        vetor_nivel_arvore[vertice_adjacente] = vetor_nivel_arvore[vertice_sendo_explorado] + 1
                    pilha.put(vertice_adjacente) 

        # onde tiver 0 e nao for raiz = none em vetor nivel arvore
        for vertice in range(self.numero_vertices):
            if vetor_nivel_arvore[vertice] == 0 and vertice != vertice_raiz:
                vetor_nivel_arvore[vertice] = None
        return list(vetor_pai_vertice), list(vetor_nivel_arvore)
        #retorna árvore no arquivo de saída

    def calcula_distancia_vertices(self,vertice1,vertice2):
        vetor_nivel_arvore = np.zeros(self.numero_vertices)
        vetor_pai_vertice = np.full(self.numero_vertices,None)
        def funcao_auxiliar(vertice_filho, vertice_pai):
            vetor_pai_vertice[vertice_filho] = vertice_pai
            vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
            if vertice_filho == vertice2:
                return vetor_nivel_arvore[vertice_filho]
            return None

        distancia = self.busca_largura(vertice1, funcao_auxiliar,True)
        return distancia
        

    def calcula_diametro_grafo(self):
        diametro = [0]
        for vertice_raiz in range(self.numero_vertices):
            vetor_nivel_arvore = np.zeros(self.numero_vertices)
            vetor_pai_vertice = np.full(self.numero_vertices,None)
            
            def funcao_auxiliar(vertice_filho, vertice_pai):
                vetor_pai_vertice[vertice_filho] = vertice_pai
                vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
                diametro[0] = max(vetor_nivel_arvore[vertice_filho],diametro[0])
                return None
            self.busca_largura(vertice_raiz, funcao_auxiliar,False)

        return diametro[0]
        
    def descobre_componentes_conexas(self):
        '''
        Componentes conexos. Sua biblioteca deve ser capaz descobrir as componentes conexas
        de um grafo. O numero de componentes conexos, assim como o tamanho (em vertices) de
        cada componente e a lista de vertices pertencentes a componente. Os componentes devem
        estar listados em ordem decrescente de tamanho (listar primeiro o componente com o maior
        numero de vertices, etc).
        '''
        vertices_conhecidos = np.zeros(self.numero_vertices)
        lista_componentes = [[-1]] # o '-1' e so pra corrigir o problema do ultimo for n rodar por a lista estar vazia
        componente_conexa = [0]
        def funcao_auxiliar(vertice_filho,vertice_pai):
            componente_conexa[0] += 1
            componente_conexa.append(vertice_filho)
            vertices_conhecidos[vertice_filho] = 1
            return None

        for vertice_raiz in range(self.numero_vertices):
            if vertices_conhecidos[vertice_raiz] == 0:
                self.busca_largura(vertice_raiz,funcao_auxiliar)
                componente_conexa[0] += 1  #acrescentando e contabilizando a raiz que faltava  
                componente_conexa.append(vertice_raiz)

                for index in range(len(lista_componentes)):
                    if componente_conexa[0] >= lista_componentes[index][0]:
                        lista_componentes.insert(index,componente_conexa)
                        break
                componente_conexa = [0]

        lista_componentes.pop() # remove 0 '[-1]' pois ele sempre sera o ultimo elemento
        return lista_componentes 


class grafo_matriz_adjacencia(grafo_generico):
    def __init__(self,arestas,numero_vertices):
        self.numero_vertices = numero_vertices
        self.numero_arestas = len(arestas)
        self.matriz = np.zeros([numero_vertices, numero_vertices])
        self.lista_graus = np.zeros(numero_vertices)
        for aresta in arestas:
            if aresta[0] == aresta[1]:
                print("aresta não pode ir de um vertice para ele mesmo")
            if (self.matriz[aresta[0]][aresta[1]] == 1 or self.matriz[aresta[1]][aresta[0]] == 1):
                print("Aresta "+str(aresta)+"já existe no grafo")
                return None
            self.matriz[aresta[0]][aresta[1]] = 1
            self.matriz[aresta[1]][aresta[0]] = 1
            
            self.lista_graus[aresta[1]]+= 1
            self.lista_graus[aresta[0]]+= 1

    def gera_vertices_adjacentes(self,vertice_origem,reverter = False):
        gerador = range(self.numero_vertices)
        if reverter: gerador = reversed(gerador)
        for vertice in gerador:
            if self.matriz[vertice_origem][vertice] == 1:
                yield vertice

class grafo_matriz_esparsa(grafo_generico):
    def __init__(self,arestas,numero_vertices):
        self.numero_vertices = numero_vertices
        self.numero_arestas = len(arestas)
        self.esparsa = set()
        self.lista_graus = np.zeros(numero_vertices)
        for aresta in arestas:
            if aresta[0] == aresta[1]:
                print("aresta não pode ir de um vertice para ele mesmo")
            if ((aresta[0],aresta[1]) in self.esparsa) or ((aresta[1],aresta[0]) in self.esparsa):
                print("Aresta "+str(aresta)+"já existe no grafo")
                return None

            self.esparsa.add((aresta[0],aresta[1])) 
            self.esparsa.add((aresta[1],aresta[0])) 
            
            self.lista_graus[aresta[1]]+= 1
            self.lista_graus[aresta[0]]+= 1

    def gera_vertices_adjacentes(self,vertice_origem,reverter = False):
        gerador = range(self.numero_vertices)
        if reverter: gerador = reversed(gerador)
        for vertice in gerador:
            if (vertice_origem,vertice) in self.esparsa:
                yield vertice


class grafo_lista_adjacencia(grafo_generico): 
    def __init__(self,arestas,numero_vertices):  
        self.numero_vertices = numero_vertices
        self.numero_arestas = len(arestas)
        self.lista_adjacencias = []
        for lista in range(self.numero_vertices):self.lista_adjacencias.append([])
        self.lista_graus = np.zeros(numero_vertices)
        for aresta in arestas:
            if aresta[0] == aresta[1]:
                print("aresta não pode ir de um vertice para ele mesmo")
            if (aresta[1] in self.lista_adjacencias[aresta[0]] or aresta[0] in self.lista_adjacencias[aresta[1]]):
                print("Aresta "+str(aresta)+"já existe no grafo")
                return None
            self.lista_adjacencias[aresta[0]].append(aresta[1])
            self.lista_adjacencias[aresta[1]].append(aresta[0])
            
            bisect.insort(self.lista_adjacencias[aresta[1]],aresta[0])
            bisect.insort(self.lista_adjacencias[aresta[0]],aresta[1])


            self.lista_graus[aresta[1]]+= 1
            self.lista_graus[aresta[0]]+= 1

    def gera_vertices_adjacentes(self,vertice_origem,reverter = False):
        gerador = self.lista_adjacencias[vertice_origem]
        if reverter: gerador = gerador[::-1]        
        for vertice in gerador:
            yield vertice

    



parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile", help = "Path Input File") 
parser.add_argument("-k", "--kind", help = "Representacao das arestas em  matriz de adjacencia(1) ou lista de adjacencia(2) ")
args = parser.parse_args()


## Processar Arquivo Entrada
'''
Sua biblioteca deve ser capaz de ler um grafo de um arquivo texto. O formato do
grafo no arquivo sera o seguinte. 
A primeira linha informa o numero de vertices do grafo.
Cada linha subsequente informa as arestas. Um exemplo de um grafo e seu respectivo arquivo
'''
def processarArquivoEntrada(arquivoentrada):
    f = open(arquivoentrada, "r")
    nvertices=f.readline() # primeira linha
    arestas=[]
    while(1):
        line = f.readline()
        if (line != ''):
            line=line.replace('\n',"")
            line=line.replace('\r',"")
            aresta=line.split(" ", 1)
            aresta=[int(aresta[0])-1,int(aresta[1])-1]
            arestas.append(aresta)
        else:
            break
    f.close()
    return arestas,int(nvertices)
## Processar arquivo Saida
'''
Saida. Sua biblioteca deve ser capaz de gerar um arquivo texto com as seguintes informacoes
sobre o grafo: numero de vertices, numero de arestas, grau minimo, grau maximo, grau medio,
e mediana de grau. Alem disso, imprimir informacoes sobre as componentes conexas (ver
abaixo).
'''
def processarArquivoSaida(grafo,arquivosaida):
    f = open(arquivosaida, "a")
    f.write("Numero de Vertices:"+str(grafo.numero_vertices)+"\n")
    f.write("Numero de Arestas:"+str(grafo.numero_arestas)+"\n")
    
    f.write("Maior Grau:"+str(grafo.calcula_maior_grau())+"\n")
    f.write("Menor Grau:"+str(grafo.calcula_menor_grau())+"\n")
    f.write("Media Grau:"+str(grafo.calcula_media_grau())+"\n")
    f.write("Mediana Grau:"+str(grafo.calcula_mediana_grau())+"\n")
    # 4
    arvore_busca1BFS=grafo.gera_arvore_largura(0)
    arvore_busca2BFS=grafo.gera_arvore_largura(1)
    arvore_busca3BFS=grafo.gera_arvore_largura(2)
    arvore_busca1DFS=grafo.gera_arvore_profundidade(0)
    arvore_busca2DFS=grafo.gera_arvore_profundidade(1)
    arvore_busca3DFS=grafo.gera_arvore_profundidade(2)
    ## BFS
    f.write("Pai do vertice 10 na busca BFS em 1:"+str(arvore_busca1BFS[0][9])+"\n")
    f.write("Pai do vertice 20 na busca BFS em 1:"+str(arvore_busca1BFS[0][19])+"\n")
    f.write("Pai do vertice 30 na busca BFS em 1:"+str(arvore_busca1BFS[0][29])+"\n")
    f.write("Pai do vertice 10 na busca BFS em 2:"+str(arvore_busca2BFS[0][9])+"\n")
    f.write("Pai do vertice 20 na busca BFS em 2:"+str(arvore_busca2BFS[0][19])+"\n")
    f.write("Pai do vertice 30 na busca BFS em 2:"+str(arvore_busca2BFS[0][29])+"\n")
    f.write("Pai do vertice 10 na busca BFS em 3:"+str(arvore_busca3BFS[0][9])+"\n")
    f.write("Pai do vertice 20 na busca BFS em 3:"+str(arvore_busca3BFS[0][19])+"\n")
    f.write("Pai do vertice 30 na busca BFS em 3:"+str(arvore_busca3BFS[0][29])+"\n")
    f.write("Pai do vertice 10 na busca DFS em 1:"+str(arvore_busca1DFS[0][9])+"\n")
    f.write("Pai do vertice 20 na busca DFS em 1:"+str(arvore_busca1DFS[0][19])+"\n")
    f.write("Pai do vertice 30 na busca DFS em 1:"+str(arvore_busca1DFS[0][29])+"\n")
    f.write("Pai do vertice 10 na busca DFS em 2:"+str(arvore_busca2DFS[0][9])+"\n")
    f.write("Pai do vertice 20 na busca DFS em 2:"+str(arvore_busca2DFS[0][19])+"\n")
    f.write("Pai do vertice 30 na busca DFS em 2:"+str(arvore_busca2DFS[0][29])+"\n")
    f.write("Pai do vertice 10 na busca DFS em 3:"+str(arvore_busca3DFS[0][9])+"\n")
    f.write("Pai do vertice 20 na busca DFS em 3:"+str(arvore_busca3DFS[0][19])+"\n")
    f.write("Pai do vertice 30 na busca DFS em 3:"+str(arvore_busca3DFS[0][29])+"\n")
    # 5
    f.write("Distancia vertice 10 20:"+str(grafo.calcula_distancia_vertices(10,20))+"\n")
    f.write("Distancia vertice 10 30:"+str(grafo.calcula_distancia_vertices(10,30))+"\n")
    f.write("Distancia vertice 20 20:"+str(grafo.calcula_distancia_vertices(20,30))+"\n")
    # 6
    componentes_conexas=grafo.descobre_componentes_conexas()
    f.write("Componentes Conexas:"+str(componentes_conexas)+"\n")
    f.write("Numero Componentes Conexas:"+str(len(componentes_conexas))+"\n")
    f.write("Tamanho da Maior Componente Conexa:"+str(componentes_conexas[0][0])+"\n")
    f.write("Tamanho da Menor Componente Conexa:"+str(componentes_conexas[-1][0])+"\n")
    f.close()
 
### Debug
# matrizteste=grafo_matriz_adjacencia(arg1,arg2)
# listateste = grafo_lista_adjacencia(arg1,arg2)
# esparsateste = grafo_matriz_esparsa(arg1,arg2)
# # print(matrizteste.matriz)
# print(matrizteste.gera_arvore_largura(3))
# print(matrizteste.calcula_distancia_vertices(1,5))
# print(matrizteste.calcula_diametro_grafo())
# print(listateste.calcula_diametro_grafo())
# print(listateste.gera_arvore_profundidade(4))
# ##########
#

cleanfilename=args.inputfile.split("/")[-1]
arg1,arg2 = processarArquivoEntrada(args.inputfile)
if args.kind == "1":
    representacao="Matriz_Adjacencia"
    grafo=grafo_matriz_esparsa(arg1,arg2)
    ## Busca Largura
    vertices_com_adjacencia=[]
    limitador=0
    for i in grafo.esparsa:
        variavelauxiliar=i[1]
        if variavelauxiliar not in vertices_com_adjacencia:
            vertices_com_adjacencia.append(variavelauxiliar)
            limitador+=1
        if limitador > 999:
            break
    while len(vertices_com_adjacencia) < 1000:
        for i in range(grafo.numero_vertices):
            if i not in vertices_com_adjacencia:
                vertices_com_adjacencia.append(i)
            if len(vertices_com_adjacencia) == 1000:
                break
        for i in range(grafo.numero_vertices):
            vertices_com_adjacencia.append(i)
            if len(vertices_com_adjacencia) == 1000:
                break
    start = timer()
    for vertice in vertices_com_adjacencia:
        grafo.gera_arvore_largura(vertice)
    end = timer()
    print("saida:{};{};{}".format(representacao,"Largura", end-start/1000))  
    ## Busca Profundidade
    start = timer() 
    for vertice in vertices_com_adjacencia:
        grafo.gera_arvore_profundidade(vertice)
    end = timer()
    print("saida:{};{};{}".format(representacao,"Profundidade", end-start/1000))
    processarArquivoSaida(grafo,cleanfilename+"-"+representacao+"-informacoesgrafo.txt")        
elif args.kind == "2":
    representacao="Lista_Adjacencia"
    grafo=grafo_lista_adjacencia(arg1,arg2)
    ## Busca Largura
    vertices_com_adjacencia=[]
    limitador=0
    for i in grafo.lista_adjacencias:
        if len(i)>0:
            if i[0] not in vertices_com_adjacencia:
                vertices_com_adjacencia.append(i[0])
            limitador+=1
        if limitador > 999:
            break
    while len(vertices_com_adjacencia) < 1000:
        for i in range(grafo.numero_vertices):
            if i not in vertices_com_adjacencia:
                vertices_com_adjacencia.append(i)
            if len(vertices_com_adjacencia) == 1000:
                break
        for i in range(grafo.numero_vertices):
            vertices_com_adjacencia.append(i)
            if len(vertices_com_adjacencia) == 1000:
                break
    start = timer()
    for vertice in vertices_com_adjacencia:
        grafo.gera_arvore_largura(vertice)
    end = timer()
    print("saida:{};{};{}".format(representacao,"Largura", end-start/1000))  
    ## Busca Profundidade
    start = timer() 
    for vertice in vertices_com_adjacencia:
        grafo.gera_arvore_profundidade(vertice)
    end = timer()
    print("saida:{};{};{}".format(representacao,"Profundidade", end-start/1000))
    processarArquivoSaida(grafo,cleanfilename+"-"+representacao+"-informacoesgrafo.txt")  