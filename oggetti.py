class Militare:
    def __init__(self, matricola, nome, cognome, grado):
        self.matricola = matricola
        self.nome = nome
        self.cognome = cognome
        self.grado = grado


class Veicolo:
    def __init__(self, targa, marca, modello):
        self.targa = targa
        self.marca = marca
        self.modello = modello


class Pattuglia:
    def __init__(self, primo_militare, secondo_militare, targa_veicolo):
        self.targaa_veicolo = targa_veicolo
        self.primo_militare = primo_militare
        self.secondo_militare = secondo_militare


class TurnoDiPattuglia:
    def __init__(self, data, inizio_turno, fine_turno, pattuglia):
        self.inizio_turno = inizio_turno
        self.fine_turno = fine_turno
        self.data = data
        self.pattuglia = pattuglia
