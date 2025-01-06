# -*- coding: utf-8 -*-

"""
Created on Thu Mar 28 02:21:09 2019

Algoritmo Genético

@author: Marco
"""

# from AlgoritmoGeneticoSudoku import AlgoritmoGenetico as AG

from AlgoritmoGenetico import AlgoritmoGenetico as AG

import matplotlib.pyplot as plt

ag = AG(TAM_POP=10, TAM_GENE=10, numero_geracoes=50)
ag.operadores_geneticos()

plt.show()