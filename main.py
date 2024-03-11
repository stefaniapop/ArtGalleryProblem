import matplotlib.pyplot as plt
import networkx as nx
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import Point

def two_coloring(G): #colorarea cu doua culori
    n = len(G)
    node_coloring = ["red"] * n #tabloul care salveaza culorile nodurilor
    for node in range(n):
        if node_coloring[node - 1] == "red": #daca nodul anterior este colorat cu rosu
            node_coloring[node] = "blue"    #nodul actual este colorat cu albastru
    return node_coloring

if __name__ == '__main__':
    ## constructia grafului ##
    G = nx.Graph()  #definirea grafului G
    elist = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1)] #lista muchiilor
    #elist = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 1)]
    G.add_edges_from(elist) #construirea grafului G pe baza muchiilor

    ## desenarea si afisarea grafului ##
    # coordonatele nodurilor
    fixed_positions = {1: (2, 10), 2: (5, 10), 3: (5, 5), 4: (10, 5), 5: (10, 3), 6: (7, 3), 7: (7, 2), 8: (2, 2)}
    #fixed_positions = {1: (2, 10), 2: (5, 10), 3: (5, 7), 4: (3, 7), 5: (3, 5), 6: (7, 5), 7: (7, 8), 8: (9, 8), 9: (9, 7), 10: (10, 7), 11: (10, 2), 12: (2, 2)}
    fixed_nodes = fixed_positions.keys()
    pos = nx.spring_layout(G, pos=fixed_positions, fixed=fixed_nodes)
    nx.draw_networkx(G, pos) #desenarea grafului
    plt.show()  #afisarea

    ## colorarea nodurilor ##
    node_coloring = two_coloring(G)

    ## redesenarea grafului cu nodurile colorate ##
    nx.draw_networkx(G, pos, node_color = node_coloring)
    plt.show()
    print(node_coloring)

    guards = []
    ## cadrangulare convexa (impartirea in patrulatere) ##
    for i in range(1, len(G) + 1):  #vizitarea fiecarui nod din G
        for j in range(i+3, len(G) + 1, 2): #vizitarea nodurilor colorate diferit de nodul i

            #verifica daca linia de la punctul i la punctul j respecta interiorul poligonului
            A, B = fixed_positions[i], fixed_positions[j]
            line = LineString([A, B])   #construirea segmentului AB
            to_add_edge = True
            polygon = Polygon(list(fixed_positions.values()))
            if (line.touches(polygon)):
                to_add_edge = False
            for k in range(len(G)): #pentru fiecare muchie din elist
                C = fixed_positions[elist[k][0]]    #C primeste primul punct din muchia k
                D = fixed_positions[elist[k][1]]    #D primeste al doilea punct din muchia k
                line2 = LineString([C, D])  #construirea segmentului CD

                # daca muchia creata de i si j intersecteaza muchiile grafului sau este identica cu una din ele
                if line.crosses(line2) or line.contains(line2) or line.contains(Point(C)) or line.contains(Point(D)):
                    to_add_edge = False     #muchia nu va fi adaugata
                    break

            ## adaugarea noilor muchii si redesenarea grafului ##
            if to_add_edge == True: #daca muchia trebuie adaugata
                if i not in guards: #daca nodurile muchiei nu sunt deja incluse in tabloul garzilor sunt adaugate
                    guards.append(i)
                if j not in guards:
                    guards.append(j)
                G.add_edge(i, j)    #adaugarea muchiei la graful G
                nx.draw_networkx(G, pos, node_color = node_coloring) #redesenarea grafului
                plt.show()  #afisarea

    print(guards)
    ## impartirea garzilor in fuctie de culoare ##
    red = []
    blue = []
    for g in guards:
        if node_coloring[g - 1] == "red":
            red.append(g)
        else:
            blue.append(g)

    ## afisarea solutiei care contine un numar mai mic de garzi ##
    if len(red) > len(blue):
        print("Numarul minim de gardieni: ", len(blue))
        print("Locurile in care e nevoie de gardieni: ", blue)
    else:
        print("Numarul minim de gardieni: ", len(red))
        print("Locurile in care e nevoie de gardieni: ", red)


