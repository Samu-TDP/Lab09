from database.DB_connect import DBConnect
from model.airport import Airport
from dataclasses import dataclass


# Mini-struttura dati per trasportare i dati dell'arco dal Database al Model
@dataclass
class Connessione:
    id_a1: int
    id_a2: int
    distanza_media: float


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_airports():
        """Estrae tutti gli aeroporti. Questi diventeranno i NODI del grafo."""
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM airports"
        cursor.execute(query)

        for row in cursor:
            # Sfruttiamo **row per riempire automaticamente i campi della Dataclass
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_connessioni():
        """Estrae tutte le rotte tra aeroporti e la loro distanza media (ARCHI)."""
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)

        # ==========================================
        # LA QUERY "TRUCCHETTO" PER GLI ARCHI NON ORIENTATI
        # ==========================================
        # Il testo chiede di calcolare la media di TUTTI i voli tra A e B,
        # sia quelli da A verso B, sia quelli da B verso A.
        # Come facciamo a dire a SQL di raggrupparli insieme?
        # Usiamo le funzioni LEAST() e GREATEST()!
        # LEAST(origine, destinazione) prenderà sempre l'ID più piccolo.
        # GREATEST(origine, destinazione) prenderà sempre l'ID più grande.
        # In questo modo, sia il volo 10->20 che il volo 20->10 verranno
        # considerati come la stessa identica rotta: (10, 20).

        query = """
            SELECT 
                LEAST(ORIGIN_AIRPORT_ID, DESTINATION_AIRPORT_ID) as a1, 
                GREATEST(ORIGIN_AIRPORT_ID, DESTINATION_AIRPORT_ID) as a2, 
                AVG(DISTANCE) as media
            FROM flights
            GROUP BY a1, a2
        """
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(row["a1"], row["a2"], row["media"]))

        cursor.close()
        conn.close()
        return result
