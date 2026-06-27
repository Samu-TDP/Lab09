from dataclasses import dataclass

@dataclass
class Airport:
    ID: int
    IATA_CODE: str
    AIRPORT: str
    CITY: str
    STATE: str
    COUNTRY: str
    LATITUDE: float
    LONGITUDE: float
    TIMEZONE_OFFSET: float

    # ==========================================
    # REGOLE D'ORO PER NETWORKX
    # ==========================================

    # 1. Metodo __eq__ (Uguaglianza)
    # Diciamo a Python che due aeroporti sono lo stesso aeroporto
    # SE E SOLO SE hanno lo stesso ID univoco.
    def __eq__(self, other):
        return self.ID == other.ID

    # 2. Metodo __hash__ (La Carta d'Identità)
    # Fondamentale per inserire gli oggetti come Nodi nel Grafo di NetworkX.
    def __hash__(self):
        return hash(self.ID)

    # 3. Metodo __str__ (Per la stampa grafica)
    def __str__(self):
        return f"{self.AIRPORT} ({self.IATA_CODE})"