import networkx as nx
import matplotlib.pyplot as plt
import random

fig,ax = plt.subplots(1, 2, figsize=(80,10)) # полотно
    
#######################  Функция отрисовки  ################################


def draw():
    ax[0].set(title = f'Алгоритм Прима')
    ax[1].set(title = f'Алгоритм Краскала')
    nx.draw(GP, post, node_color = colorP, with_labels = True, edge_color = edge_colorP, ax = ax[0])         
    nx.draw_networkx_edges(GP, post, edge_color = edge_colorP, width = 10, ax = ax[0])                  
    nx.draw_networkx_edge_labels(GP, post, edge_labels = labels, ax = ax[0])
    plt.axis('off')
    
    nx.draw_networkx(GK, post, node_color = colorK, with_labels = True, edge_color = edge_colorK, ax = ax[1])
    nx.draw_networkx_edges(GK, post, edge_color = edge_colorK, width = 10, ax = ax[1])                
    nx.draw_networkx_edge_labels(GK, post, edge_labels = labels, ax = ax[1])
    plt.axis('off')
    
    
GP = nx.Graph() # граф для Прима отрисовка

GK = nx.Graph() # граф для Краскала отрисовка


#################################### ввод ##############################

with open('Graph.txt', 'r') as f:
    n,m = map(int, f.readline().split() )

    Gn = [ [] for i in range(n)] #
    Gw = [ [] for i in range(n)] # граф для Прима

    Gkr = [[] for i in range(m)] # граф для Краскала


    for i in range( m ):
        a, b, c = map(int, f.readline().split() )
        Gn[a-1].append(b-1)
        Gw[a-1].append(c)
        Gn[b-1].append(a-1)
        Gw[b-1].append(c)
        GP.add_edge(a, b, weight = c)
        GK.add_edge(a, b, weight = c)
        Gkr[i].append(c)
        Gkr[i].append(a)
        Gkr[i].append(b)

############################# Настройка отрисовки графа ########################### 
post = nx.spring_layout(GP, weight = 'None', iterations=1000)
labels = nx.get_edge_attributes(GP,'weight')

edgeG = list(GP.edges())
node = list(GP.nodes())
edge_colorP = ['black' for i in range(m)]      # цвет ребра прима
colorP = ['yellow' for i in range( n )]   # цвет вершины прима


colorK = [(random.random(), random.random(), random.random() ) for i in range( n )] # цвет вершины краскала
edge_colorK = ['black' for i in range(m)] # цвет ребра краскала

draw()
plt.pause(0.001)
draw()
plt.pause(3)
#########################################################################

edge = [[] for i in range(m)]
d = [10**9 for i in range(n)]
used = [0 for i in range(n)]
d[0] = 0
ans1 = 0
Gkr.sort()
ans = 0
color = [-1 for i in range(n+1)]
size = [1 for i in range(n+1)]
k = 0
po = 0

for i  in range(1,n+1):
        color[i] = i     

while True:
    
    if k + po == m+n:
        break
    
###################         Алгоритм Прима       ################################    

    if k < n:
    
        mn = 10**9
        pos = -1
    
        for i in range( n ):
            
            if not(used[i]) and (d[i]<mn):
                mn = d[i]
                pos = i
            
        used[pos] = 1
        ans1 += d[pos]
        for i in range( len(Gn[pos]) ):
            to = Gn[pos][i]
            if d[to] > Gw[pos][i]:
                d[to] = Gw[pos][i]
                if not([pos+1,to+1] in edge) and not([to+1,pos+1] in edge):
                    edge[to-1] = [pos+1,to+1] # сохранение нужного ребра
                    for i in range(m):
                        for j in range( len(edgeG)):
                            if edge[i] != []:
                                if (edge[i][0] == edgeG[j][0] and edge[i][1] == edgeG[j][1]) or (edge[i][0] == edgeG[j][1] and edge[i][1] == edgeG[j][0]):
                                    edge_colorP[j] = 'green'
                                    colorP[node.index(edgeG[j][1])] = 'red'
                                    colorP[node.index(edgeG[j][0])] = 'red'
                                    
        edge_colorP = ['black' for i in range(m)]
    
    for i in range(m):
        for j in range( len(edgeG)):
            if edge[i] != []:
                if (edge[i][0] == edgeG[j][0] and edge[i][1] == edgeG[j][1]) or (edge[i][0] == edgeG[j][1] and edge[i][1] == edgeG[j][0]):
                    edge_colorP[j] = 'green'

                
###################         Алгоритм Краскала       ################################                            


    if po < m:
        ta = Gkr[po][1]
        tb = Gkr[po][2]
        if color[ta] !=color[tb]:
            ans += Gkr[po][0]
        
            if (size[color[ta]] < size[color[tb]]):
                ta,tb = tb,ta
            
            for i in range(len(edgeG)):
                if (ta == edgeG[i][0] and tb == edgeG[i][1]) or (tb == edgeG[i][0] and ta == edgeG[i][1]):
                    edge_colorK[i] = 'green'

            size[color[ta]] += size[color[tb]]
            oldcolor = color[tb]

        
            for j in range(1,n+1):
                if color[j] == oldcolor:
                    color[j] = color[ta]
                    colorK[node.index(j)] = colorK[node.index(ta)]       
    
          
    draw()
    
    if k == n:
        ax[0].set(title = f'Алгоритм Прима \n Минимальный остов {ans1}')

    if po == m:
        ax[1].set(title = f'Алгоритм Краскала \n Минимальный остов {ans}')
        
    plt.pause(1)


    if k != n:
        k += 1
    if po != m:
        po += 1
    
draw()
ax[0].set(title = f'Алгоритм Прима \n Минимальный остов {ans1}')
ax[1].set(title = f'Алгоритм Краскала \n Минимальный остов {ans}')
plt.show()
