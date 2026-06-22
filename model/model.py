import networkx as nx
#from statsmodels.sandbox.regression.runmnl import modes
from database.dao import DAO


class Model:
    def __init__(self):
        self.rifugi = None
        self.connessioni = None
        self.G = nx.Graph()

    def build_graph(self, year: int):
        """Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        self.rifugi = DAO.get_all_rifugi(year)
        print(f' rifugi: {self.rifugi}')
        self.connessioni = DAO.get_connessioni(year, self.rifugi)
        print(f' connessioni: {self.connessioni}')

        self.G.clear()
        self.G.add_nodes_from(self.rifugi.values())
        for connection in self.connessioni.values():
            self.G.add_edge(connection.r1, connection.r2)
        return self.G

    def get_nodes(self):
        """Restituisce la lista dei rifugi presenti nel grafo.:return: lista dei rifugi presenti nel grafo."""
        nodi = list(self.G.nodes)
        return nodi

    def get_num_neighbors(self, node):  #in input il nodo di cui voglio i vicini
        """Restituisce il grado (numero di vicini diretti) del nodo rifugio.:param node: un rifugio (cioè un nodo del grafo):return: numero di vicini diretti del nodo indicato"""
        return len(list(self.G.neighbors(node)))
    def get_num_connected_components(self):
        """Restituisce il numero di componenti connesse del grafo.:return: numero di componenti connesse"""
        return nx.number_connected_components(self.G)
    def get_reachable(self, start):
        """Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo: per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.:param start: nodo di partenza, da non considerare nell'elenco da restituire
        ESEMPIO (a = self.get_reachable_bfs_tree(start)
                b = self.get_reachable_iterative(start)
                b = self.get_reachable_recursive(start)
                return a"""
        a = self.get_reachable_bfs_tree(start)
        return a
    def get_reachable_bfs_tree(self, start):
        tree = nx.bfs_tree(self.G, start)  #costruisco albero con origine e grafo completo
        nodes = list(tree.nodes())      #trovo i nodi dell albero e li metto in una lista
        if start in nodes:
            nodes.remove(start)                 #rimuovo origine dai nodi raggiungibili da esso
        return nodes
    def get_reachable_dfs_tree(self, start):
        tree = nx.dfs_tree(self.G, start)
        nodes = list(tree.nodes())  # trovo i nodi dell albero e li metto in una lista
        if start in nodes:
            nodes.remove(start)  # rimuovo origine dai nodi raggiungibili da esso
        return nodes

    def get_reachable_iterative(self, start):
        visited = []
        self._recursive_visit(start, visited)
        if start in visited:
            visited.remove(start)
        return visited
    def _recursive_visit(self,node, visited):
        visited.append(node)
        for vicino in self.G.neighbors(node):             #prendo vicini dir di nodo iniziale (=start)
            if vicino not in visited:
                self._recursive_visit(vicino, visited)

    def reachable_iterative(self, start):
        '''metodo double ended queue, ossia coda a doppia entrata: si gestiscono le due estremità della coda in contemporanea (fila alle poste:quello all inizio è servito e
        quello alla fine è entrata; '''
        visited = []
        from collections import deque
        to_be_visited = deque() #creo coda
        visited.append(start)
        to_be_visited.extend(self.G.neighbors(start))   #prendo vicini e li metto in coda , i quali sono i primi da visitare
        while to_be_visited:  #finche non è vuoto
            temp = to_be_visited.popleft()  #prendo quello piu a sx (immagino la coda che va da dx a sx): quello aspetta da di piu e lo tolgo e visito
            visited.append(temp)                #aggiungo quell elemento ai visitati
            vicini= list(self.G.neighbors(temp))        #prendo i vicini di quello eliminato
            vicini = [n for n in vicini if n not in visited]  #se ho un elemento tra i suoi vicini non tra i visitati allora lo lascio
            vicini= [n for n in vicini if n not in to_be_visited] #tra gli elementi risultanti da prima, se non sono tra i to_be_visited, li lascio
            to_be_visited.extend(vicini)  #aggiungo i nuovi vicini scoperti in fondo alla fila

        if start in visited:
            visited.remove(start)
        return visited

