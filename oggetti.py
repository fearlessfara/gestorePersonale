class Militare:
    def __init__(self, matricola, nome, cognome, grado):
        self.matricola = matricola
        self.nome = nome
        self.cognome = cognome
        self.grado = grado

    def to_dictionary(self):
        dictionary = {
            "matricola": self.matricola,
            "nome": self.nome,
            "cognome": self.cognome,
            "grado": self.grado
        }
        return dictionary


class Veicolo:
    def __init__(self, targa, marca, modello):
        self.targa = targa
        self.marca = marca
        self.modello = modello

    def to_dictionary(self):
        dictionary = {
            "targa": self.targa,
            "marca": self.marca,
            "modello": self.modello,
        }
        return dictionary


class Pattuglia:
    def __init__(self, primo_militare, secondo_militare, veicolo):
        self.veicolo = veicolo
        self.primo_militare = primo_militare
        self.secondo_militare = secondo_militare

    def to_dictionary(self):
        dictionary = {
            "veicolo": self.veicolo.to_dictiornary(),
            "primo_militare": self.primo_militare,
            "secondo_militare": self.secondo_militare
        }
        return dictionary


class TurnoDiPattuglia:
    def __init__(self, data, inizio_turno, fine_turno, pattuglia):
        self.inizio_turno = inizio_turno
        self.fine_turno = fine_turno
        self.data = data
        self.pattuglia = pattuglia

    def to_dictionary(self):
        dictionary = {
            "giorno": self.data,
            "inizio_turno": self.inizio_turno,
            "fine_turno": self.fine_turno,
            "pattuglia": self.pattuglia.to_dictiornary()
        }
        return dictionary
