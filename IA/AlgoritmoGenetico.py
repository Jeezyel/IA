# -*- coding: utf-8 -*-
"""
Algoritmo Genético


"""
import numpy as np 

import matplotlib.pyplot as plt

class AlgoritmoGenetico:
    def __init__(self, TAM_POP, TAM_GENE, numero_geracoes = 100):
        print("Algoritmo Genético. Executado pro Jeezyel")
        self.TAM_POP = TAM_POP
        self.TAM_GENE = TAM_GENE
        self.POP = []
        self.POP_AUX = []
        self.aptidao = []
        self.aptidao_perc = []  # porcentagem
        self.numero_geracoes = numero_geracoes
        self.grafico = []  # Inicializa lista para armazenar os dados para o gráfico
        self.melhor_individuo = None  # Para armazenar o melhor indivíduo
        self.melhor_aptidao = -float('inf')  # Para armazenar a melhor aptidão
        self.melhor_geracao = 0  # Para armazenar a geração do melhor indivíduo
        self.populacao_inicial()

    def populacao_inicial(self):
        print("Criando população inicial!")
        for i in range(self.TAM_POP):
            self.POP.append(np.random.randint(0, 2, self.TAM_GENE))

    def pre_roleta(self):
        aptidao_total = sum(self.aptidao)
        self.aptidao_perc = []
        for i in range(self.TAM_POP):
            x = (self.aptidao[i] * 100) / aptidao_total
            self.aptidao_perc.append(x)

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
        tx_cruzamento_uniforme = 60
        tx_mutacao = 2
        tx_elitismo = 10

        for geracao in range(self.numero_geracoes):
            self.POP_AUX = []
            self.avaliacao()
            q, apt = self.pegar_melhor_individuo()
            self.exibe_grafico_evolucao(geracao, apt)

            # Verifica se é a melhor aptidão já encontrada
            if apt > self.melhor_aptidao:
                self.melhor_aptidao = apt
                self.melhor_individuo = q
                self.melhor_geracao = geracao

            self.pre_roleta()

            # Cruzamento simples
            qtd = (self.TAM_POP * tx_cruzamento_simples) / 100
            for i in range(int(qtd)):
                pai1 = self.roleta()
                pai2 = self.roleta()
                while pai1 == pai2:
                    pai2 = self.roleta()
                self.cruzamento_simples(pai1, pai2)

            # Cruzamento uniforme
            qtd = (self.TAM_POP * tx_cruzamento_uniforme) / 100
            for i in range(int(qtd)):
                pai1 = self.roleta()
                pai2 = self.roleta()
                while pai1 == pai2:
                    pai2 = self.roleta()
                self.cruzamento_uniforme(pai1, pai2)

            # Elitismo
            qtd = (self.TAM_POP * tx_elitismo) / 100
            self.elitismo(qtd)

            # Garantir o tamanho populacional
            while len(self.POP_AUX) < self.TAM_POP:
                self.POP_AUX.append(self.POP[np.random.randint(0, self.TAM_POP)])

            # Mutação
            qtd = (self.TAM_POP * tx_mutacao) / 100
            for i in range(int(qtd)):
                quem = np.random.randint(0, self.TAM_POP)
                self.mutacao(quem)

            self.substituicao()

        # Exibe o melhor indivíduo após todas as gerações
        self.exibe_melhor_individuo_final()

    def cruzamento_simples(self, pai1, pai2):
        desc1 = np.zeros(self.TAM_GENE, dtype=int)
        desc2 = np.zeros(self.TAM_GENE, dtype=int)

        for i in range(self.TAM_GENE):
            if i < self.TAM_GENE / 2:
                desc1[i] = self.POP[pai1][i]
                desc2[i] = self.POP[pai2][i]
            else:
                desc1[i] = self.POP[pai2][i]
                desc2[i] = self.POP[pai1][i]

        self.POP_AUX.append(desc1)
        self.POP_AUX.append(desc2)

    def cruzamento_uniforme(self, pai1, pai2):
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

    def mutacao(self, i):
        g = np.random.randint(0, self.TAM_GENE)
        self.POP_AUX[i][g] = 1 - self.POP_AUX[i][g]

    def elitismo(self, qtd):
        aptidao_index = []
        for i in range(self.TAM_POP):
            aptidao_index.append([self.aptidao[i], i])

        ord_aptidao = sorted(aptidao_index, key=lambda x: x[0], reverse=True)

        for i in range(int(qtd)):
            eleito = np.zeros(self.TAM_GENE, dtype=int)
            for g in range(self.TAM_GENE):
                eleito[g] = self.POP[ord_aptidao[i][1]][g]
            self.POP_AUX.append(eleito)

    def substituicao(self):
        self.POP = self.POP_AUX.copy()

    def avaliacao(self):
        livros = [0.6, 1.6, 0.8, 0.7, 1.2, 0.3, 0.1, 1.4, 1.3, 0.5]

        self.aptidao = []

        for i in range(self.TAM_POP):
            peso = 0.0
            for g in range(self.TAM_GENE):
                peso += (self.POP[i][g] * livros[g])
            self.aptidao.append(peso)

    def pegar_melhor_individuo(self):
        apt = max(self.aptidao)
        quem = self.aptidao.index(apt)
        return quem, apt

    def exibe_melhor_individuo_final(self):
        print(f"Geração: {self.melhor_geracao} | Indivíduo: {self.melhor_individuo} | Aptidão: {self.melhor_aptidao}")

    def exibe_grafico_evolucao(self, g, apt):
        self.grafico.append((g, apt))
        plt.plot(*zip(*self.grafico), marker='o')
        plt.xlabel('Geração')
        plt.ylabel('Aptidão')
        plt.title('Evolução da Aptidão')
        plt.pause(0.01)