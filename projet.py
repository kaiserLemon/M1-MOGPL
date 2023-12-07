##### Projet
import numpy as np
import copy
import toolbox
############# Projet #############

########## BELLMAN FORD ##########

def bellmanFordRec(G_Sommets, G_Arcs, nbIter=0, predecesseur=None, distance=None, Affichage=False):
    """
    G_Sommets : ordre de traitement des sommets
    G_Arcs : Liste des arcs au format (depart, arrive, cout)
    nbIter : nombre d'Iterations
    predecesseur : liste des predecesseurs
    distance : liste des distance
    Affichage : boolean permettant l'affichage d'infos supplémentaires
    """
    if Affichage:
        print("NB ITE =", nbIter)
        print("\tDistance k : ", distance)
        print("\tPredecesseurs : ", predecesseur)
    if nbIter == len(G_Sommets):
        if(Affichage):
            print("\t\t\tTIMEOUT, CONVERGENCE NON ATTEINTE, PRESENCE CIRCUIT ABSORBANT")
        return False
    # Initialisation
    if nbIter == 0:
        if(Affichage):
            print("########## Initializing BellmanFord ##########")
            print()
        dist, pred = toolbox.initBellmanFord(G_Sommets.index(G_Sommets[0]), len(G_Sommets))
        if(Affichage):
            print("########## BellmanFord Initialized ##########")
        return bellmanFordRec(G_Sommets, G_Arcs, nbIter + 1, pred, dist, Affichage)
    
    else:
        distanceap, nouvpred = toolbox.calculNouvDistanceFULL(G_Sommets, G_Arcs, distance, predecesseur)
        # Cas d'arrêt : on converge
        if distance == distanceap:
            chemin = toolbox.constructChemin(predecesseur, distance, G_Sommets, G_Arcs)
            if(Affichage):
                print("nbIte FINAL : ", nbIter)
                print("Chemin TROUVE : ", chemin)
            return nbIter, chemin,distance
        else:
            return bellmanFordRec(G_Sommets, G_Arcs, nbIter + 1, nouvpred, distanceap, Affichage)
        
########## GLOUTON FAS ##########

def Glouton_Fas(G_sommets, G_arcs,Affiche=False):
    """
    G_sommets : liste des sommets d'un graphe
    G_arcs : Liste des arcs au format (depart, arrive, cout)
    Affiche : boolean permettant l'affichage d'infos supplémentaires
    """
    cp_sommets = copy.deepcopy(G_sommets)
    cp_arcs = copy.deepcopy(G_arcs)
    # Initialisation
    if(Affiche):
        print("########## Initializing Glouton Fas ##########")
    s1 = []
    s2 = []
    cpt=0
    if(Affiche):
        print("########## Glouton Fas Initialized ##########")
    while len(cp_sommets) > 0:
        l_source = toolbox.getListeSources(cp_sommets, cp_arcs)
        # print(l_source)
        # Remplir S1
        if(Affiche):
            print("------- FINDING SOURCES -------")
        while (l_source!=[]):
            for source in l_source:
                s1.append(source)
                cp_sommets, cp_arcs = toolbox.supprimerSommet(source, cp_sommets, cp_arcs)
            l_source = toolbox.getListeSources(cp_sommets, cp_arcs)
        if(Affiche):
            print("------- SOURCES FOUND -------")
            print("S1= ",s1)
        # Remplir S2
        if(Affiche):
            print("------- FINDING PITS -------")
        l_puits = toolbox.getListepuits(cp_sommets, cp_arcs)
        # print(l_puits)
        while (l_puits!=[]):
            for puit in l_puits:
                s2.insert(0, puit)
                cp_sommets, cp_arcs = toolbox.supprimerSommet(puit, cp_sommets, cp_arcs)
            l_puits = toolbox.getListepuits(cp_sommets, cp_arcs)
        if(Affiche):
            print("------- PITS FOUND -------")
            print("S2= ",s2)
        # Remplir sommets restants
        if(Affiche):
            print("At this Stage : CPT= ",cpt," len(cp_sommets)=", len(cp_sommets))
            print("S1=",s1, "\tS2=",s2)
            print("CP_Sommets=",cp_sommets)
        if(len(cp_sommets)==0):
            break
        chosenVertice = cp_sommets[0]
        maxFound = toolbox.nbArcsSortants(chosenVertice, cp_arcs) - toolbox.nbArcsEntrants(chosenVertice, cp_arcs)

        for sommet in cp_sommets[1:]:
            du=toolbox.nbArcsSortants(sommet, cp_arcs) - toolbox.nbArcsEntrants(sommet, cp_arcs)
            if(Affiche):
                print("\t\tTested : ",sommet, "  du= ",du)
            if (du> maxFound):
                if(Affiche):
                    print("\t\tChanging : ", maxFound,"-->",du," New sommet",sommet)
                maxFound = du
                chosenVertice = sommet
        if(Affiche):
            print("\tAppended : ",chosenVertice)
        s1.append(chosenVertice)
        cp_sommets, cp_arcs = toolbox.supprimerSommet(chosenVertice, cp_sommets, cp_arcs)
        cpt+=1
    if(Affiche):
        print("BEFORE THE END")
        print("S1= ",s1)
        print("S2= ",s2)
    return s1 + s2

########## GENERATION GRAPHES ##########
def generateGraphe(nbSommets,probabilite):
    """
    Génère un graphe non pondéré
    nbSommets : nombre de sommets voulu dans le graphe
    probabilite : flotant déterminant la probabilité d'apparition d'un arc
    """
    #print(nbSommets,probabilite)
    l_sommets=[i for i in range(nbSommets)]
    l_arcs=[]
    for sommet in  l_sommets:
        for successeur in l_sommets:
            if(sommet!=successeur):
                alea=np.random.random()
                if(alea > probabilite):
                    arc=(sommet,successeur,1)
                    l_arcs.append(arc)
    return l_sommets,l_arcs



def genOriginGraphe(nbSommets,probabilite):
    """
    Génère un graphe pondéré H et vérifie que la source atteint au moins la moitiée des sommets
    nbSommets : nombre de sommets voulu dans le graphe
    probabilite : flotant déterminant la probabilité d'apparition d'un arc
    """
    correct=False
    origin_A=None
    origin_S=None
    while(not correct):
        origin_S,origin_A=generateGraphe(nbSommets,probabilite)
        #print(origin_S,origin_A)
        origin_A=toolbox.changeCostGraphe(origin_A)
        res=bellmanFordRec(origin_S,origin_A)
        while(res==False) :
            origin_A=toolbox.changeCostGraphe(origin_A)
            res=bellmanFordRec(origin_S,origin_A)
        #print("Candidat sans circuit absorbant")
        _,_,dist=res
        #dist=distance
        #print(dist)
        cpt=0
        for d in range(1,len(dist)):
            test=dist[d]
            if(test!=np.inf):
                cpt+=1
        #print(cpt)
        if(cpt>nbSommets/2):
            #print("Candidat atteignant la moitiée des sommets ")
            correct=True
        
    return (origin_S,origin_A)

def genGraphes(nbGraphes,origin_S,origin_A):
    """
    Génère une liste de graphes pondérés à partir d'un graphe d'origine 
    et vérifie qu'il n'y a pas de circuits absorbants
    nbGraphes : nombre de graphes voulus
    origin_S : liste des sommets du graphe d'origine
    origin_A : liste des arcs du graphe d'origine au format (depart, arrive, cout)
    """
    l_Graphes=[]  
    while(len(l_Graphes)!=nbGraphes):
        test_arcs=toolbox.changeCostGraphe(origin_A)
        res=bellmanFordRec(origin_S,test_arcs)
        if(res!=False):
            newG=(origin_S,test_arcs)
            print("\tNew Graphe Appended")
            l_Graphes.append(newG)
    return l_Graphes

########## TEST UNION/COMPARAISONs ##########    

def testUnion(grapheOrigin,l_Graphes,nbfront,Affiche=False):
    """
    Trouve l'union des arborescences des plus courts chemins 
    pour nbfront graphes contenus dans l_Graphes 
    et compare le nombre d'itérations via ordre donne par Glouton Fas
    avec un ordre tire aleatoirement

    grapheOrigin : couple (liste_sommets, liste_arcs) du graphe d'origine
    l_Graphes : liste des graphes pondérés générés à partir de H(qui est implicitement généré à partir de G
    nbfront : nombre de graphes appris
    Affiche : boolean permettant d'obtenir des affichages supplémentaires
    """
    union=[]
    for i in range(nbfront):
        ls_test,la_test=l_Graphes[i]
        _,chemin,_=bellmanFordRec(ls_test,la_test)
        union+=chemin
    #print(l_Graphes)
    union=toolbox.formatUnionChemin(union)
    l_sommets,l_arcs=grapheOrigin
    #Ordre de GloutonFas
    ordre=Glouton_Fas(l_sommets,union)
    nbite,_,_=bellmanFordRec(ordre,l_arcs)
    #Ordre Aleatoire
    ordreAlea=toolbox.getOrdreAlea(l_sommets)
    nbiteA,_,_=bellmanFordRec(ordreAlea,l_arcs)
    #Test
    nbApprentissage=nbfront
    if(Affiche): 
        print("With GloutonFas found in ",nbite," for ",nbApprentissage," graphes learned")
        print("With Alea found in ",nbiteA)
    #recup amélioration différence itérations
    rep=0
    rep=nbiteA-nbite
    return rep

def testUnionGraduel(grapheOrigin,l_Graphes,nbfront,Affiche=False,AfficheDetail=False):
    """
    Effectue des tests d'unions de manière progressive pour graphe H grapheOrigin 
    et la liste l_Graphes et récupère l'amélioration ou non du nombre d'itérations
    données par la comparaison entre pré-traitement et aléatoire
    grapheOrigin : Graphe de test H
    l_Graphes : liste des graphes générés à partir de H (implicitement généré à partir de G)
    nbfront : nombre de graphes à apprendre au total
    Affiche : affiche des détails sur l'améliorations en fonction du nombre de graphes appris
    AfficheDetail : affiche les détails des divers tests d'union
    """
    toComp=[]
    for i in range(nbfront):
        toAdd=testUnion(grapheOrigin,l_Graphes,i,AfficheDetail)
        toComp.append(toAdd)
        if(Affiche):
            print("Amelioration de ",toAdd," for ",i+1," Graphes learned")
    return toComp