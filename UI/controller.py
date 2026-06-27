import flet as ft


class Controller:
    def __init__(self, view, model):
        # Il Controller tiene i collegamenti ai due attori principali
        self._view = view
        self._model = model

    def handle_analizza_aeroporti(self, e):
        """Metodo meccanico a 5 step per gestire la creazione del grafo."""

        # --- STEP 1: PULISCI ---
        # Svuotiamo l'area dei risultati dai click precedenti
        self._view._txtResult.controls.clear()

        # --- STEP 2: VALIDA ---
        # 2a. Leggiamo il valore dalla casella di testo
        soglia_str = self._view._txtIn.value

        # 2b. Verifichiamo che l'utente abbia scritto qualcosa
        if not soglia_str:
            self._view.create_alert("Inserire una soglia di distanza (x) per continuare.")
            return

        # 2c. Verifichiamo che sia un numero valido (intero o decimale)
        try:
            x_soglia = float(soglia_str)
        except ValueError:
            self._view.create_alert("La soglia deve essere un numero (es. 1500 o 2400.5).")
            return

        # --- STEP 3: DELEGA ---
        # Passiamo la soglia al Model, che costruirà il grafo filtrato
        self._model.crea_grafo(x_soglia)

        # Chiediamo al Model i dati statistici del grafo appena creato
        n_nodi = self._model.get_num_nodes()
        n_archi = self._model.get_num_edges()

        # --- STEP 4: IMPAGINA ---
        # 4a. Stampiamo il riassunto (Nodi e Archi)
        self._view._txtResult.controls.append(
            ft.Text(f"Grafo creato correttamente!", color="green", weight="bold")
        )
        self._view._txtResult.controls.append(ft.Text(f"Numero di vertici: {n_nodi}"))
        self._view._txtResult.controls.append(ft.Text(f"Numero di archi: {n_archi}"))

        # 4b. Stampiamo l'elenco di tutti gli archi (Punto c del PDF)
        # Usiamo il metodo che abbiamo creato nel Model per avere la lista pulita
        archi_pesati = self._model.get_tutti_gli_archi()

        self._view._txtResult.controls.append(
            ft.Text("Elenco delle rotte trovate:", weight="bold", color="blue")
        )

        for u, v, peso in archi_pesati:
            # u e v sono oggetti Airport, peso è la distanza media
            # Usiamo f-string per stampare una riga leggibile
            linea = f"{u.AIRPORT} -- {v.AIRPORT} | Distanza media: {peso:.2f} miglia"
            self._view._txtResult.controls.append(ft.Text(linea))

        # --- STEP 5: AGGIORNA ---
        # Diciamo alla View di rinfrescare lo schermo per mostrare i nuovi ft.Text
        self._view.update_page()
