from dataclasses import dataclass
import datetime
from model.rifugio import Rifugio

@dataclass(frozen=True)
class Connessione:
    r1: Rifugio         # tipo rifugio perche l ho agganciato cosi nel DAO (riga 35)
    r2: Rifugio            # //  (riga 36)
    distanza: float
    difficolta: str
    durata: datetime.time = datetime.time(0,0,0)            ###

    def __str__(self):
        id1 = self.r1.id
        id2 = self.r2.id
        return f"{id1} - {id2}"

    def __repr__(self):
        id1 = self.r1.id
        id2 = self.r2.id
        return f"{id1} - {id2}"
