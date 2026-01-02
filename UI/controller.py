import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._current_rifugio = None

    def handle_calcola(self, e):
        """Callback per il bottone 'Calcola sentieri'."""
        year = self._view.txt_anno.value
        try:
            year_n = int(year)
        except (ValueError, TypeError):
            self._view.show_alert("Inserisci un valore numerico nel campo anno.")
            return
        if year_n < 1950 or year_n > 2024:
            self._view.show_alert("Inserisci un valore compreso tra 1950 e 2024.")
            return

        # costruisce il grafo con il model
        self._model.build_graph(year_n)   #in output ho il grafo(self.G) correlato a tale anno
        # aggiorna l'area risultati
        self._view.lista_visualizzazione.controls.clear()
        # uso il metodo corretto per il numero di componenti
        num_cc = self._model.get_num_connected_components()
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Il grafo ha {num_cc} componenti connesse."))
        self._view.lista_visualizzazione.controls.append(ft.Text("Di seguito il dettaglio sui nodi:"))
        for n in self._model.get_nodes():
            # n è un oggetto rifugio; usiamo .nome come rappresentazione
            grado = self._model.get_num_neighbors(n)
            self._view.lista_visualizzazione.controls.append(ft.Text(f"{n} -- {grado} vicini."))
        self._view.lista_visualizzazione.update()
        '''
        # abilita dropdown e bottone raggiungibili (se erano disabilitati)
        self._view.dd_rifugio.disabled = False
        self._view.pulsante_raggiungibili.disabled = False

        # riempie il dropdown con i rifugi attuali
        self._fill_dropdown()
        self._view.update()

    def handle_raggiungibili(self, e):
        """Callback per il bottone 'Rifugi raggiungibili'."""
        if self._current_rifugio is None:
            self._view.show_alert("Seleziona prima un rifugio dal menu a tendina.")
            return

        raggiungibili = self._model.get_reachable(self._current_rifugio)
        self._view.lista_visualizzazione.controls.clear()
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Da '{self._current_rifugio.nome}' è possibile raggiungere a piedi {len(raggiungibili)} rifugi:"))
        for r in raggiungibili:
            # supponiamo che l'oggetto r abbia attributo nome
            self._view.lista_visualizzazione.controls.append(ft.Text(f"{r}"))

        self._view.update()

    def _fill_dropdown(self):
        """Popola il dropdown con i rifugi presenti nel grafo."""
        self._view.dd_rifugio.options.clear()
        all_rifugi = self._model.get_nodes()

        for r in all_rifugi:
            # Solo text e data: value non serve
            option = ft.dropdown.Option(text=r.nome)
            self._view.dd_rifugio.options.append(option)

        # aggiorna il dropdown
        self._view.dd_rifugio.update()

        # Associa callback on_change sul Dropdown (non sulle singole Option)
        self._view.dd_rifugio.on_change = self.read_dd_rifugio

    def read_dd_rifugio(self, e):
        """Callback chiamato quando si seleziona un'opzione nel dropdown."""

        selected_option = e.control.value
        if selected_option is None:
            self._current_rifugio = None
            return

        # selected_option è una stringa? in Flet moderno spesso è text, quindi cerchiamo l'oggetto data corrispondente
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break

        self._current_rifugio = found
        print("Rifugio selezionato:", self._current_rifugio)
        '''