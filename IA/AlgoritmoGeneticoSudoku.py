# -*- coding: utf-8 -*-
"""

Algoritmo Genético
"""
import numpy as np

import matplotlib.pyplot as plt

class AlgoritmoGenetico:
    def __init__(self, TAM_POP, TAM_GENE, numero_geracoes = 100):
        print("Algoritmo Genético")
        self.TAM_POP = TAM_POP
        self.TAM_GENE = TAM_GENE
        self.TAM_MATRIZ = int(TAM_GENE ** (1/2))
        self.POP = []
        self.POP_AUX = []
        self.aptidao = []
        self.aptidao_perc = [] #porcentagem
        self.numero_geracoes = numero_geracoes
        self.populacao_inicial()
        self.aptidao_coluna = []
        self.aptidao_quadrante = []
        #self.grafico = plt.plot([],[])
    
    def populacao_inicial(self):
        print("Criando pupulação inicial!")
        
        for k in range(self.TAM_POP):
            individuo = np.zeros(self.TAM_GENE, dtype=int)
            for j in range(0, 4):
                alelo = []
                alelo_ord = []
                for i in range(1, 5):
                    alelo.append([i, np.random.uniform(0.1, 1)])
                alelo_ord = sorted(alelo, key=lambda alelo:alelo[1])
                for i in range(1, 5):
                    individuo[(j * 4) + (i - 1)] = alelo_ord[i-1][0]
            self.POP.append(individuo)

        ## Gerador de alelos
        
        
        #for i in range(self.TAM_POP):
        #    self.POP.append(np.random.randint(1, 5, self.TAM_GENE))

    def pre_roleta(self):
        aptidao_total = sum(self.aptidao)
        self.aptidao_perc = []
        
        for i in range(self.TAM_POP):
            x = (self.aptidao[i] * 100)/aptidao_total
            self.aptidao_perc.append(x)
            x = 0

    def roleta(self):
        sorteado = np.random.uniform(0.1, 100.1)
        quintal = 0.0
        for i in range(self.TAM_POP):
            quintal += self.aptidao_perc[i]   
            if quintal > sorteado:
                return i
        return 0

    def operadores_geneticos(self):
        tx_cruzamento_simples = 30
        tx_cruzamento_uniforme = 70
        tx_elitismo = 0
        tx_mutacao = 2
        tx_elitismo = 10
        
        for geracao in range(self.numero_geracoes):
            self.POP_AUX = []
            
            self.avaliacao()
            q, apt = self.pegar_melhor_individuo()
            #self.exibe_grafico_evolucao(geracao, apt)
            #self.exibe_melhor_individuo(geracao)
            
            self.pre_roleta()
            
            ## cruzamento simples
            qtd = (self.TAM_POP * tx_cruzamento_simples)/100
            for i in range(int(qtd)):
                pai1 = self.roleta()
                pai2 = self.roleta()
                while pai1 == pai2:
                    pai2 = self.roleta()
                self.cruzamento_simples(pai1, pai2)
            
            ## cruzamento uniforme
            qtd = (self.TAM_POP * tx_cruzamento_uniforme)/100
            for i in range(int(qtd)):
                pai1 = self.roleta()
                pai2 = self.roleta()
                while pai1 == pai2:
                    pai2 = self.roleta()
                self.cruzamento_uniforme(pai1, pai2)  
            
            #elitismo
            qtd = (self.TAM_POP * tx_elitismo)/100
            print("Elitismo")
            #self.elitismo(qtd)
            
            ## GARANTIR O TAMANHO POPULACIONAL.
            
             ## mutação
            qtd = (self.TAM_POP * tx_mutacao)/100
            for i in range(int(qtd)):
                quem = np.random.randint(0, self.TAM_POP)
                self.mutacao(quem)
            
            self.substituicao()
        #self.grafico.show()
        
    def cruzamento_simples(self, pai1, pai2):
        #print("Cruzamento com 1 ponto de corte.")
        
        desc1 = np.zeros(self.TAM_GENE, dtype=int)
        desc2 = np.zeros(self.TAM_GENE, dtype=int)
        
        for i in range(self.TAM_GENE):
            if i < self.TAM_GENE/2:
                desc1[i] = self.POP[pai1][i]
                desc2[i] = self.POP[pai2][i]
            else:
                desc1[i] = self.POP[pai2][i]
                desc2[i] = self.POP[pai1][i]
                
        self.POP_AUX.append(desc1)
        self.POP_AUX.append(desc2)
                
    def cruzamento_uniforme(self, pai1, pai2):
        #print("Cruzamento uniforme.")
        
        desc1 = np.zeros(self.TAM_GENE, dtype=int)
        desc2 = np.zeros(self.TAM_GENE, dtype=int)
        
        for i in range(self.TAM_GENE):
            if 0 == np.random.randint(0, 2):
                desc1[i] = self.POP[pai1][i]
                desc2[i] = self.POP[pai2][i]
            else:
                desc1[i] = self.POP[pai2][i]
                desc2[i] = self.POP[pai1][i]
                
        self.POP_AUX.append(desc1)
        self.POP_AUX.append(desc2)    
    
    ## Função de mutação. Deve ser utilizada na POP_AUX
    ## após sua população estar completa.
    def mutacao(self, i):
        g = np.random.randint(0, self.TAM_GENE)
        if self.POP_AUX[i][g] == 0:
            self.POP_AUX[i][g] = 1
        else:
            self.POP_AUX[i][g] = 0

    def elitismo(self, qtd):
        ## ordenação por aptidão
        aptidao_index = []
        for i in range(self.TAM_POP):
            aptidao_index.append([self.aptidao[i], i])
            
        ord_aptidao = sorted(aptidao_index, key=lambda aptidao_index:aptidao_index[0], reverse=True)
        
        for i in range(int(qtd)):
            eleito = np.zeros(self.TAM_GENE, dtype=int)
            for g in range(self.TAM_GENE):
                eleito[g] = self.POP[ord_aptidao[i][1]][g]
            self.POP_AUX.append(eleito)
            
            
    def substituicao(self):
        self.POP = self.POP_AUX.copy()
        
    def avaliacao(self):

        ###
        #g1: avaliar os alelos
        #lucas, *mateus, diego, lonardo
        for j in range(0, 4):
            avaliacao_linha = 0
            for i in range(0, 4):
                avaliacao_linha += (self.POP[0][((j * 4) + i)])
            if avaliacao_linha != 10:
                self.aptidao = 0
            ##print(avaliacao_linha)
        
        #g2: avaliar colunas
        #patrícia, nilvan, *samuel
        for i in range(self.TAM_POP):
            self.somacoluna(i)
        #g3: avaliar quadrantes
        #matheus, *thalyson, vagner
        self.avaliar_quadrante()
        #g4: juntar tudo e atribuir a aptidao.
        # pensar em possibilidades de calcular 
        # quando um indivíduo é melhor q outro
        #julieta, *rafael, igor, thais
        
        #mateusasevedo
        #sanka01
        #thalysonlira
        #flamolino
                
        ###
        self.aptidao = []
        self.atribuir_aptidao()
        
        # for i in range(self.TAM_POP):
        #     peso = 0.0
        #     for g in range(self.TAM_GENE):
        #         peso += (self.POP[i][g] * livros[g])
        #     self.aptidao.append(peso)


    def somacoluna(self,ind):
        aptidao_coluna_individuo =  np.zeros(4, dtype=int)
        for j in range(4):

            for i in range(4):
                # print("I: {} | J: {} | X: {}".format(i, j, (i)*4+j))
                aptidao_coluna_individuo[j] += self.POP[ind][(i)*4+j]
        self.aptidao_coluna.append(aptidao_coluna_individuo)
        
    # 3 - Avaliacao da aptidao do quadrante
    def avaliar_quadrante(self):
        raiz = int(self.TAM_MATRIZ ** (1/2))      
        for p in range(self.TAM_POP):
            x = 0 
            y = 0
            aptidao = 10
            individuo = self.POP[p]
            for k in range(self.TAM_MATRIZ):
              soma = 0
              for j in range(raiz):
                for i in range(raiz):
                  soma += individuo[(((j + y) * 4) + (i + x))]
              if x < self.TAM_MATRIZ - raiz:
                x += raiz
              else:
                x = 0
                y += raiz

              if soma > 10:
                aptidao = 0
                break
            self.aptidao_quadrante.append(aptidao)

    # Grupo 4 - Atribuindo aptidao
    def atribuir_aptidao(self):
        for p in range(self.TAM_POP):
            ind = self.POP[p]

            g1 = ind[0]
            g2 = ind[1]
            g3 = ind[2]
            g4 = ind[3]
            aptidao = 0
            # regra
            # quanto mais distante o melhor gene (4) está do pior gene (1) melhor, 
            # e quanto mais proximo o melhor gene está do segundo melhor gene (3), melhor     [1][2][3][4] ou [4][3][2][1] (melhores individuos)       
            if g1 > g4 and g1 > g3 and g1 > g2:
                if g1 == 4 and g4 == 1:
                    if g2 == 3:
                        # individuo ótimo
                        aptidao = 10
                    else:
                        #individuo bom
                        aptidao = 10 / 2
                else:
                    #individio ruim
                    aptidao = 10 / 4
            elif g4 > g1 and g4 > g3 and g4 > g2:
                if g4 == 4 and g1 == 1:
                    if g3 == 3:
                        # melhor individio
                        aptidao = 10
                    else:
                        # individio bom
                        aptidao = 10 / 2
                else:
                    # individio ruim
                    aptidao = 10 / 4
            else: 
                # individuo péssimo
                aptidao = 1
            
            self.aptidao.append(aptidao)



    def pegar_melhor_individuo(self):
        apt = max(self.aptidao)
        quem = self.aptidao.index(apt)
        return quem, apt
    
    def exibe_melhor_individuo(self, geracao):
        apt = max(self.aptidao)
        quem = self.aptidao.index(apt)
        
        print("Geração: {} | Indivíduo: {} | Aptidão: {}".format(geracao, quem, apt))

    def exibe_grafico_evolucao(self, g, apt):
        pass
        #self.grafico.plot(g, apt)
