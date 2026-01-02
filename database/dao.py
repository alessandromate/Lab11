from oauthlib.uri_validate import query
import database
from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def get_all_rifugi(year):
        from model.rifugio import Rifugio
        conn = DBConnect.get_connection()
        rifugi= {}
        cursor = conn.cursor(dictionary=True)
        query = '''SELECT DISTINCT r.id, r.nome, r.localita, r.altitudine, r.capienza, r.aperto
                                FROM connessione c,rifugio r
                                WHERE c.anno <= %s and (r.id = c.id_rifugio1 or r.id = c.id_rifugio2)              
                                ORDER BY c.anno'''
        cursor.execute(query, (year,))                #verifico esistenza nel WHERE del rifugio in tabella connessione
        for row in cursor:
            if row['id'] not in rifugi:               #verifico l esistenza dell'id che sto considerando della row dentro il dizionario
                rifugi[row['id']] = Rifugio(**row)          #spacchetta gli elementi del dizionario, inserendoli poi nel dizionario rifugi
        cursor.close()
        conn.close()
        return rifugi

    @staticmethod
    def get_connessioni(year, rifugi):
        from model.connessione import Connessione
        conn = DBConnect.get_connection()
        connessioni = {}
        cursor = conn.cursor(dictionary=True)
        query = '''SELECT DISTINCT id, id_rifugio1, id_rifugio2, distanza, difficolta, durata, anno
                FROM connessione 
                 WHERE anno <= %s'''
        cursor.execute(query, (year, ))
        for row in cursor:
            r1 = rifugi.get(row['id_rifugio1'])     #accedo al diz rifugi per id prendendo la riga che ha tale id come id_rif1 --> r1 diventa un oggetto
            r2 = rifugi.get(row['id_rifugio2'])     # //
            if r1 is not None and r2 is not None and (r1,r2) not in connessioni: #verifico l esistenza dell'id che sto considerando della row dentro il dizionario
                connessioni[r1.id , r2.id] = Connessione(r1, r2, row['distanza'], row['difficolta'], row['durata'])
        cursor.close()
        conn.close()

        return connessioni









