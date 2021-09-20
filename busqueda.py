from tkinter import *
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import random

import numpy as np
from queue import PriorityQueue 
import math

        
#Clase Grafo
class Graph():
    G = nx.Graph()
    coordinates ={} #para impresion
    size_x=0
    size_y=0
    table=np.zeros((size_x, size_y))

    def __init__(self, x, y):
        cont=0
        self.size_x=x
        self.size_y=y
        self.table=np.zeros((self.size_x, self.size_y))

        for i in range(0,self.size_x):
            for j in range(0,self.size_y):
                self.G.add_node(cont)
                self.table[i][j]=cont
                self.G.nodes[cont]['coords']=(i,j)
                self.G.nodes[cont]['path']=False
                self.coordinates[cont]=(i,j)
                cont+=1
        self.hacer_conexiones()

    def neighbors(self, rowNumber, columnNumber, radius):
        return [[self.table[i][j] if  i >= 0 and i < len(self.table) and j >= 0 and j < len(self.table[0]) else -1
                 for j in range(columnNumber-1-radius, columnNumber+radius)]
                    for i in range(rowNumber-1-radius, rowNumber+radius)]

    
    def get_key(self,val,dist_neighbors): 
        for key, value in dist_neighbors.items(): 
             if val == value: 
                 return key 
        return "key doesn't exist"

    def hacer_conexiones(self):
        for k in list(self.G.nodes()):
            neigh=np.zeros((3, 3))
            neigh=self.neighbors(self.G.nodes[k]['coords'][0],self.G.nodes[k]['coords'][1],1)

            if(neigh[1][1] != -1):
                self.G.add_edge(k,neigh[1][1],color='green')

            if(neigh[1][2] != -1):
                self.G.add_edge(k,neigh[1][2],color='green')

            if(neigh[2][1] != -1):
                self.G.add_edge(k,neigh[2][1],color='green')

            if(neigh[1][2] != -1 and neigh[2][1] != -1):
                self.G.add_edge(neigh[1][2],neigh[2][1],color='green')

    def print_grafo(self):
        plt.figure(num=None, figsize=(20, 20), dpi=80)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G,pos=self.coordinates,node_size=16)
        edges=self.G.edges()
        colors=[self.G[u][v]['color']for u,v in edges]
        nx.draw_networkx_edges(self.G,pos=self.coordinates,edge_color=colors)
        plt.tight_layout()
        plt.show()
        
    def eliminar_nodos(self):
        cant_nodos=self.size_x*self.size_y
        nodos_borrados={}
        for i in range(int(cant_nodos*0.2)):
            while(True):
                try:
                    index=random.randint(0,cant_nodos-1)
                    self.G.remove_node(index)
                    nodos_borrados[i]=self.coordinates[index]
                except :
                    pass
                else:
                    break
        return nodos_borrados
##################################################################################################################################################
#Heuristica
    def heuristic(self, a, b):
        aX = (a)[0]
        aY = (a)[1]
        bX = (b)[0]
        bY = (b)[1]
        return math.sqrt((bX - aX) ** 2 + (bY - aY) ** 2)

    def A_star(self, StartX, StartY, EndX, EndY):
        #Hallar nodo en si
        INICIO=0
        FIN=0
        for i in self.coordinates:
            if(self.coordinates[i][0]==EndX and self.coordinates[i][1]==EndY):
                FIN=i
                break
        for i in self.coordinates:
            if(self.coordinates[i][0]==StartX and self.coordinates[i][1]==StartY):
                INICIO=i
                break
        Pawn=PriorityQueue()
        Pawn.put(INICIO,0)
        came_from={}
        score={}
        came_from[INICIO]=None
        score[INICIO]=0
        while not Pawn.empty():
            current=Pawn.get()
            if current==FIN:
                break
            for Next in self.G.neighbors(current):
                tentative_score=score[current]+self.heuristic(self.coordinates[current],self.coordinates[FIN])
                if Next not in score or tentative_score<score[Next]:
                    score[Next]=tentative_score
                    fscore=tentative_score+self.heuristic(self.coordinates[FIN],self.coordinates[Next])
                    Pawn.put(Next,fscore)
                    came_from[Next]=current
        returnPath={}
        returner=FIN
        pathsize=0
        while returner is not INICIO:
            returnPath.update({returner: came_from[returner]})
            #print(self.coordinates[returner])
            self.G.add_edge(returner,came_from[returner],color='red',weight=20)
            returner=came_from[returner]
            pathsize=pathsize+1
        #print(self.coordinates[INICIO])
    



###################################################################################################################################################
#Ciega
    def DFS(self,StartX, StartY, EndX, EndY):
        INICIO=0
        FIN=0
        for i in self.coordinates:
            if(self.coordinates[i][0]==EndX and self.coordinates[i][1]==EndY):
                FIN=i
                break
        for i in self.coordinates:
            if(self.coordinates[i][0]==StartX and self.coordinates[i][1]==StartY):
                INICIO=i
                break
        path = []
        nodossinhijos = []
        path.append(INICIO)
        nodossinhijos.append(INICIO)
        current = path[0]
        while current != FIN:
            vecinos = []
            for i in self.G.neighbors(current):
                if i not in path and i not in nodossinhijos:
                    vecinos.append(i)
            if len(vecinos) > 0:
                current = vecinos[0]
                path.append(current)
            else:
                nodossinhijos.append(current)
                path.pop(-1)

        returnPath = path
        returnPath.reverse()
        returner = returnPath[0]
        i = 0
        while i < len(returnPath) - 1:
            if i == 0 or i == len(returnPath) - 2:
                self.G.add_edge(returner, returnPath[i + 1], color='blue')
            else:
                self.G.add_edge(returner, returnPath[i + 1], color='red')
            returner = returnPath[i + 1]
            i = i + 1
        return len(returnPath)

def flujo_principal(valor,x,y,sx,sy,n):
    if(valor==1):
        grafo=Graph(int(n),int(n))
        nd_deleted=grafo.eliminar_nodos()
        ax=int(x)
        ay=int(y)
        grafo.A_star(int(sx),int(sy),ax,ay)
        grafo.print_grafo()
    elif(valor==0):
        grafo=Graph(int(n),int(n))
        nd_deleted=grafo.eliminar_nodos()
        ax=int(x)
        ay=int(y)
        grafo.DFS(int(sx),int(sy),ax,ay)
        grafo.print_grafo()

      

n=int(input("ingrese n: "))
print("Nodo inicial")
x1=int(input("ingrese x1: "))
y1=int(input("ingrese y1: "))
print("Nodo final")
x2=int(input("ingrese x2: "))
y2=int(input("ingrese y2: "))




flujo_principal(0,x2,y2,x1,y1,n)

flujo_principal(1,x2,y2,x1,y1,n)
