class Militare:
    def __init__(self, matricola, nome, cognome, grado):
        self.matricola = matricola
        self.nome = nome
        self.cognome = cognome
        self.grado = grado


class TurnoDiPattuglia:
    def __init__(self, matricola_militare, inizio_turno, fine_turno, data, targa_veicolo):
        self.matricola_militare = matricola_militare
        self.inizio_turno = inizio_turno
        self.fine_turno = fine_turno
        self.data = data
        self.targaa_veicolo = targa_veicolo


class Veicolo:
    def __init__(self, targa, marca, modello):
        self.targa = targa
        self.marca = marca
        self.modello = modello
