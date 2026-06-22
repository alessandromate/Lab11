import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab11"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK
        # Alert
        self.alert = AlertManager(page)
        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)
    def set_controller(self, controller):
        self.controller = controller
    def update(self):
        self.page.update()
    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # Intestazione
        self.txt_titolo = ft.Text(value="Gestione Sentieri di Montagna", size=38, weight=ft.FontWeight.BOLD)
        # Riga 1 con campo anno e pulsante calcola
        self.txt_anno = ft.TextField(label="Anno (1950-2024)", width=200)
        pulsante_calcola = ft.ElevatedButton(
            text="Calcola sentieri",
            on_click=self.controller.handle_calcola,
            width=200)
        row1 = ft.Row([self.txt_anno, pulsante_calcola], alignment=ft.MainAxisAlignment.CENTER)

        # Riga 2 con dropdown rifugio e pulsante raggiungibili
        self.dd_rifugio = ft.Dropdown(
            label="Rifugio",
            width=300,
            on_change=self.controller.read_dd_rifugio if self.controller else None
        )

        self.pulsante_raggiungibili = ft.ElevatedButton(
            text="Rifugi raggiungibili",
            on_click=self.controller.handle_raggiungibili if self.controller else None,
            width=200
        )
        row2 = ft.Row([self.dd_rifugio, self.pulsante_raggiungibili], alignment=ft.MainAxisAlignment.CENTER)

        # ListView dove stampare i risultati
        self.lista_visualizzazione = ft.ListView(expand=10, spacing=20, auto_scroll=False)

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            ft.Divider(),

            row1,
            row2,
            ft.Divider(),
            self.lista_visualizzazione
        )
        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
