import copy
import numpy as np
##########################################
#------------ FORMAT DONNEES ------------#
##########################################
def matToGraphe(mat):
    """
    Transforme un graphe sous forme de matrice
    en coupe (liste_sommets,liste_arcs)
    mat : matrice d'adjacence du graphe
    """
    taille = len(mat)
    # init liste sommets
    l_sommets = []
    for i in range(taille):
        l_sommets.append(i)
    # init liste arcs
    l_arcs = []
    for i in range(taille):
        for j in range(taille):
            cout = mat[i][j]
            if cout != np.inf:
                dep = i
                end = j
                l_arcs.append((dep, end, cout))
    return (l_sommets, l_arcs)


def matAdjacenceToList(mat):
    """
    transforme un graphe sous forme de matrice d'adjacence
    en graphe sous forme de liste d'adjacence
    mat : Graphe sous forme de matrice d'adjacence
    """
    rep = []
    for i in range(0, len(mat[0])):
        add = []
        for j in range(0, len(mat[0])):
            test = mat[i][j]
            if test != np.inf:
                add.append(j)
        rep.append(add)
    return rep


def listAdjacenceToMat(lst):
    """
    transforme un graphe sous forme de liste d'adjacence
    en graphe sous forme de matrice d'adjacence
    lst : graphe sous forme de liste d'adjacence
    """
    rep = np.zeros((len(lst), len(lst)))
    rep.fill(np.inf)
    for i in range(0, len(lst)):
        sublist = lst[i]
        for j in sublist:
            rep[i][j] = 1
    return rep

##########################################
#------------ BELLMAND FORD -------------#
##########################################

def initBellmanFord(depart, nbsommets):
    """
    initialise BellmanFord
    depart : sommet de départ
    nbsommets : nombre de sommets dans le graphe
    """
    distance = []
    predecesseur = []
    for i in range(nbsommets):
        distance.append(np.inf)
        predecesseur.append(None)
    distance[depart] = 0
    return distance, predecesseur


def constructChemin(pred, distance, l_sommets, l_arcs):
    """
    Construit le plus court chemin dans le graphe à partir
    de la liste de distance et des prédécesseurs

    pred: liste des predecesseurs
    distance : liste des distance une fois convergence atteinte
    l_sommets : liste des sommets d'un graphe G
    l_arcs: listes des arcs d'un graphe G
    """
    chemin = []
    for i in range(len(l_sommets)):
        if distance[i] != 0:
            for (u, v, c) in l_arcs:
                # On check si un sommet v a pour predesseur le sommet u
                # dans la liste des arcs
                if (u == pred[i]) and (v == l_sommets[i]):
                    chemin.append((u, v, c))
                    break
    return chemin


def calculNouvDistanceFULL(G_sommets, G_arcs, distance, predecesseur):
    """
    Calcule la nouvelle distance pour chaque sommet en direct
    
    G_sommets : liste des sommets d'un graphe
    G_arcs : Liste des arcs au format (depart, arrive, cout)
    distance : la liste des distances
    predecesseur : liste des predecesseurs
    """
    d_add = copy.deepcopy(distance)
    # print(d_add)
    pred = copy.deepcopy(predecesseur)
    # print(pred)
    for u in G_sommets:
        iu = G_sommets.index(u)
        for arc in G_arcs:
            if(arc[1]==u):
                iv = G_sommets.index(arc[0])
                cost= arc[2]
                if d_add[iu] > d_add[iv] + cost:
                    d_add[iu] = d_add[iv] + cost
                pred[iu] = arc[0]
    # print (d_add)
    # print (pred)
    return d_add, pred


def calculNouvDistance(G_sommets, G_arcs, distance, predecesseur):
    """
    Calcule la nouvelle distance pour chaque sommet comme dans le cours
    [OBSOLETTE]
    G_sommets : liste des sommets d'un graphe
    G_arcs : Liste des arcs au format (depart, arrive, cout)
    distance : la liste des distances
    predecesseur : liste des predecesseurs
    """
    d_add = copy.deepcopy(distance)
    # print(d_add)
    pred = copy.deepcopy(predecesseur)
    # print(pred)
    for u in G_sommets:
        iu = G_sommets.index(u)
        for arc in G_arcs:
            if(arc[1]==u):
                iv = G_sommets.index(arc[0])
                cost= arc[2]
                if distance[iu] > distance[iv] + cost:
                    d_add[iu] = distance[iv] + cost
                pred[iu] = arc[0]
    # print (d_add)
    # print (pred)
    return d_add, pred

##########################################
#------------- GLOUTON FAS --------------#
##########################################
def supprimerSommet(sommet, G_sommets, G_arcs):
    """
    Supprime le sommet sommet du graphe (G_sommets,G_arcs)
    
    sommet : sommet à supprimer
    G_sommets : liste des sommets d'un graphe
    G_arcs : Liste des arcs au format (depart, arrive, cout)
    """
    if sommet in G_sommets:
        G_sommets.remove(sommet)
    G_arcs = [(u, v, c) for (u, v, c) in G_arcs if u != sommet and v != sommet]
    return G_sommets, G_arcs


def getListeSources(G_sommets, G_arcs):
    """
    Retourne la liste des sources du graphe (G_sommets,G_arcs)

    G_sommets : liste des sommets d'un graphe
    G_arcs : Liste des arcs au format (depart, arrive, cout)
    """
    sources = [sommet for sommet in G_sommets if all(v != sommet for (_, v, _) in G_arcs)]
    return sources


def getListepuits(G_sommets, G_arcs):
    """
    Retourne la liste des puits du graphe (G_sommets,G_arcs)

    G_sommets : liste des sommets d'un graphe
    G_arcs : Liste des arcs au format (depart, arrive, cout)
    """
    puits = [sommet for sommet in G_sommets if all(u != sommet for (u, _, _) in G_arcs)]
    return puits


def nbArcsSortants(sommet, G_arcs):
    """
    Cacule la somme des arcs sortants d'un sommet

    sommet : sommet à calculer
    G_arcs : Liste des arcs au format (depart, arrive, cout)
    """
    return sum(1 for (u, _, _) in G_arcs if u == sommet)


def nbArcsEntrants(sommet, G_arcs):
    """
    Cacule la somme des arcs entrants d'un sommet

    sommet : sommet à calculer
    G_arcs : Liste des arcs au format (depart, arrive, cout)
    """
    return sum(1 for (_, v, _) in G_arcs if v == sommet)

##########################################
#--------- GENERATION GRAPHES -----------#
##########################################

def changeCostGraphe(l_arcs):
    """
    Change le cout des arcs d'une liste d'arcs

    l_arcs : Liste des arcs au format (depart, arrive, cout)
    """
    newl_arcs=[]
    for (u,v,_) in l_arcs:
        newCost=np.random.randint(-3,11)
        newarc=(u,v,newCost)
        newl_arcs.append(newarc)
    return newl_arcs

##########################################
#------- TEST D'UNION/COMPARAISON -------#
##########################################
def formatUnionChemin(union):
    """
    Retire les doublons qui ne sont pas necessaires pour Glouton Fas

    union : liste contenant l'aborescence des chemins les plus courts
    des divers graphes appris  
    """
    newUnion=[]
    appended=[]
    #print(union)
    for (u,v,c) in union:
        test=(u,v)
        if(test not in appended):
            newUnion.append((u,v,c))
            appended.append(test)
    return newUnion

def getOrdreAlea(l_sommets):
    """
    Retourne un ordre aléatoire d'une liste de sommets 
    en conservant la même source

    l_sommets : liste de sommets 
    """
    cp_sommets=copy.deepcopy(l_sommets)
    newOrder=[]
    newOrder.append(cp_sommets[0])
    cp_sommets.remove(cp_sommets[0])
    np.random.shuffle(cp_sommets)
    return newOrder+list(cp_sommets)