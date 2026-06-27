import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        # 1. Inizializziamo il grafo (semplice, non orientato e pesato)
        self._grafo = nx.Graph()

        # 2. Dizionario di supporto: ID_Aeroporto -> Oggetto_Airport
        # Indispensabile per collegare gli archi ai nodi corretti
        self._idMap = {}

        # 3. Cache degli aeroporti per evitare di interrogare il DB troppe volte
        self._all_airports = []

    def crea_grafo(self, soglia_x):
        """Metodo meccanico per costruire il grafo filtrato."""

        # Svuotiamo il grafo precedente (se l'utente preme il tasto più volte)
        self._grafo.clear()

        # STEP A: Gestione dei NODI
        # Carichiamo gli aeroporti solo se la lista è vuota (ottimizzazione)
        if len(self._all_airports) == 0:
            self._all_airports = DAO.get_all_airports()
            # Riempiamo la idMap: Chiave=ID, Valore=Oggetto
            for a in self._all_airports:
                self._idMap[a.ID] = a

        # Aggiungiamo tutti gli aeroporti come nodi del grafo
        self._grafo.add_nodes_from(self._all_airports)

        # STEP B: Gestione degli ARCHI (Filtraggio)
        # Recuperiamo tutte le medie calcolate con LEAST/GREATEST dal DAO
        tutte_le_connessioni = DAO.get_all_connessioni()

        for c in tutte_le_connessioni:
            # Applichiamo il filtro richiesto dal PDF
            if c.distanza_media > soglia_x:
                # Troviamo gli oggetti aeroporto reali dalla nostra idMap
                u = self._idMap.get(c.id_a1)
                v = self._idMap.get(c.id_a2)

                # Se entrambi esistono, creiamo l'arco pesato
                if u is not None and v is not None:
                    self._grafo.add_edge(u, v, weight=c.distanza_media)

    # ==========================================
    # METODI DI SERVIZIO PER IL CONTROLLER
    # ==========================================

    def get_num_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_edges(self):
        return self._grafo.number_of_edges()

    def get_tutti_gli_archi(self):
        """Restituisce una lista di tuple (u, v, peso) per la stampa a video."""
        result = []
        # .edges(data=True) restituisce i due nodi e il dizionario degli attributi
        for u, v, data in self._grafo.edges(data=True):
            result.append((u, v, data['weight']))
        return result