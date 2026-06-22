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

        self._model.build_graph(year_n)
        self._view.lista_visualizzazione.controls.clear()
        num_cc = self._model.get_num_connected_components()
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Il grafo ha {num_cc} componenti connesse."))
        self._view.lista_visualizzazione.controls.append(ft.Text("Di seguito il dettaglio sui nodi:"))
        for n in self._model.get_nodes():
            grado = self._model.get_num_neighbors(n)
            self._view.lista_visualizzazione.controls.append(ft.Text(f"{n} -- {grado} vicini."))
        self._view.lista_visualizzazione.update()

        self._fill_dropdown()

        self._view.update()

    def handle_raggiungibili(self, e):
        """Callback per il bottone 'Rifugi raggiungibili'."""
        if self._current_rifugio is None:
            self._view.show_alert("Seleziona prima un rifugio dal menu a tendina.")
            return
        print(self._current_rifugio)
        node=""
        for n in self._model.G.nodes:
            if n.id == int(self._current_rifugio):
                node = n
        print(f'questo è il nodo {node}')
        raggiungibili = self._model.get_reachable(node)
        print(f'questi sono i nodi raggiungibili : {raggiungibili} ')

        #raggiungibili.sort(key=lambda x: x.peso, reverse=True)

        self._view.lista_visualizzazione.controls.clear()
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Da '{node.nome}' è possibile raggiungere a piedi {len(raggiungibili)} rifugi:"))

        for r in raggiungibili:
            self._view.lista_visualizzazione.controls.append(ft.Text(f"{r}"))
            self._view.update()
        self._view.update()

    def _fill_dropdown(self):
        """Popola il dropdown con i rifugi presenti nel grafo."""
        self._view.dd_rifugio.options.clear()
        all_rifugi = self._model.get_nodes()
        print(f'tutti i rifugi {all_rifugi}')
        for r in all_rifugi:
            self._view.dd_rifugio.options.append(ft.dropdown.Option(key=  r.id, text=r.nome))

        self._view.dd_rifugio.update()

    def read_dd_rifugio(self, e):
        """Callback chiamato quando si seleziona un'opzione nel dropdown."""
        selected_option = e.control.value
        print(f' id rifugio selezionato {selected_option} ')

        self._current_rifugio = selected_option
        print(f'rifugio selezionato dal dd:  {selected_option}')
        self.handle_raggiungibili(e)


