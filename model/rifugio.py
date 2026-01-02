from dataclasses import dataclass

@dataclass(frozen=True)
class Rifugio:
    id: int
    nome: str
    localita: str
    altitudine: int
    capienza:int
    aperto:bool

    def __str__(self):
        return f"[{self.id}] {self.nome} ({self.localita})"

    def __repr__(self):
        return f"{self.id} : {self.nome}"
