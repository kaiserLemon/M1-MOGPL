##Test projet
import numpy as np
import projet


s_G0 = [1, 2, 3, 4, 5, 6, 7, 8]
a_G0 = [
    (1, 2, 1),(1, 3, 1),
    (2, 3, 1),
    (3, 4, 1),
    (4, 5, 1),(4, 6, 1),(4, 7, 1),
    (5, 7, 1),
    (6, 5, 1),(6, 8, 1),
    (7, 1, 1),
    (8, 3, 1),(8, 2, 1),
]
G0 = (s_G0, a_G0)
s_G0_1 = [0, 1, 2, 3, 4]
a_G0_1 = [
    (0, 1, -1), (0, 2, 4), 
    (1, 2, 3), (1, 3, 2), (1, 4, 2), 
    (3, 2, 3), 
    (4, 3, -3)]
G0_1 = (s_G0_1, a_G0_1)

s_G0_1_2 = ["A", "B", "C", "D", "E"]
a_G0_1_2 = [
    ("A", "B", -1),
    ("A", "C", 4),
    ("B", "C", 3),
    ("B", "D", 2),
    ("B", "E", 2),
    ("D", "C", 3),
    ("E", "D", -3),
]
G0_1_2 = (s_G0_1_2, a_G0_1_2)

def testBellemanFord():
    nbIte, chemin,distance = projet.bellmanFordRec(s_G0, a_G0)
    print("Chemin = ",chemin," trouve en ",nbIte," iterations")
    return

def testGloutonFas():
    newOrder = projet.Glouton_Fas(s_G0, a_G0)
    newIte, newWay,dist= projet.bellmanFordRec(newOrder,a_G0)
    testBellemanFord()
    print("Nouveau Chemin = ",newWay, " trouve en ", newIte," iterations")
    return

nbGraphes=10
nbSommets=14
probabilite=0.45
def testUnion(nbGraphes=3,nbSommets=10, probabilite=0.4):
    #print("------------ UNION TEST START ------------")
    #print("------------ ORIGIN INIT ------------")
    GrapheOrigin=projet.genOriginGraphe(nbSommets,probabilite)
    origin_S,origin_A=GrapheOrigin
    #print("------------ ORIGIN INITIALIZED ------------")
    #print("------------ LIST GRAPHES INIT ------------")
    l_graphe=projet.genGraphes(nbGraphes,origin_S,origin_A)
    #print("------------ LIST GRAPHES INITIALIZED ------------")
    #print("------------ STARTING GRADUAL TEST ------------")
    projet.testUnion(GrapheOrigin,l_graphe,nbGraphes,Affiche=True)
    #print("------------ GRADUAL TEST FINISHED ------------")
    #print("------------ UNION TEST END ------------")
    return

def traitementQ10(nbGraphes,nbSommets,probabilite):
    print("------------ Q10 START ------------")
    print("------------ ORIGIN INIT ------------")
    GrapheOrigin=projet.genOriginGraphe(nbSommets,probabilite)
    origin_S,origin_A=GrapheOrigin
    print("------------ ORIGIN INITIALIZED ------------")
    print("------------ LIST GRAPHES INIT ------------")
    l_graphe=projet.genGraphes(nbGraphes,origin_S,origin_A)
    print("------------ LIST GRAPHES INITIALIZED ------------")
    #print(l_graphe)
    print("------------ STARTING GRADUAL TEST ------------")
    projet.testUnionGraduel(GrapheOrigin,l_graphe,nbGraphes,Affiche=True)
    print("------------ GRADUAL TEST FINISHED ------------")
    print("------------ Q10 END ------------")
    return

nbrepet=5
def execXQ10(nbGraphes,nbSommets,probabilite,nbrepet):
    for i in range(nbrepet):
        traitementQ10(nbGraphes,nbSommets,probabilite)
    return

#testBellemanFord()
#testGloutonFas()
testUnion()
#traitementQ10(nbGraphes,nbSommets,probabilite)
#execXQ10(nbGraphes,nbSommets,probabilite,nbrepet)
#Q11 Les sommets du niveau j sont les sources du niveau j+1 donc GloutonFas n'a pas d'intéret à réordonner les sommets puisque que les parcourrait déjà dans l'ordre