import sqlite3

from oggetti import *


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Militare (matricola integer primary key, nome string, cognome string,  "
            "grado string)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Veicolo (marca string, modello string, targa string);")
        self.cur.execute("CREATE TABLE  if not exists Riposo (matricola_militare integer, giorno date)")
        self.cur.execute("CREATE TABLE if not exists Licenza (matricola_militare integer, giorno date);")
        self.cur.execute("CREATE TABLE if not exists Altro (matricola_militare integer, note text, giorno date);")
        self.cur.execute("CREATE TABLE if not exists Giornata (giorno date PRIMARY KEY);")
        self.cur.execute(
            "CREATE TABLE if not exists TurnoDiPattuglia (id_pattuglia INTEGER PRIMARY KEY AUTOINCREMENT, matricola_militare integer, "
            "inizio_turno time, fine_turno time, giorno date, targa_veicolo string);")
        self.conn.commit()

    def fetch_disponibili(self, data):
        self.cur.execute(
            "SELECT * FROM Militare WHERE matricola NOT IN (SELECT matricola FROM TurnoDiPattuglia as tdp WHERE "
            "tdp.giorno=?)", (data,))
        rows = self.cur.fetchall()
        lista_disponibili = []
        for row in rows:
            militare = {
                'matricola': row[0],
                'nome': row[1],
                'cognome': row[2],
                'grado': row[3],
                "busy": "no"
            }
            lista_disponibili.append(militare)
        return lista_disponibili

    def insert_turno_pattuglia(self, inizioTurno, fineTurno, data, targa, primoMilitare, secondoMilitare):
        self.cur.execute("INSERT INTO TurnoDiPattuglia VALUES (null,?,?,?,?,?)",
                         (primoMilitare, inizioTurno, fineTurno, data, targa))
        self.cur.execute("INSERT INTO TurnoDiPattuglia VALUES (null,?,?,?,?,?)",
                         (secondoMilitare, inizioTurno, fineTurno, data, targa))
        self.conn.commit()

    # def update_turno_pattuglia(self):
    #     self.cur.execute("UPDATE parts SET nome = ?, cognome = ?, grado = ? WHERE id = ?",(nome, cognome, grado, id))
    #     self.conn.commit()

    def insert_licenza(self, data, matricola):
        self.cur.execute("INSERT INTO Licenza VALUES (?,?)", (matricola, data))
        self.conn.commit()

    def insert_riposo(self, data, matricola):
        self.cur.execute("INSERT INTO Riposo VALUES (?,?)", (matricola, data))
        self.conn.commit()

    def insert_altro(self, data, matricola, note):
        self.cur.execute("INSERT INTO Altro VALUES (?,?, ?)", (matricola, data, note))
        self.conn.commit()

    def insert_militare(self, matricola, nome, cognome, grado):
        self.cur.execute("INSERT INTO Militare VALUES (?, ?, ?, ?)",
                         (matricola, nome, cognome, grado))
        self.conn.commit()

    def remove_militare(self, matricola):
        self.cur.execute("DELETE FROM Militare WHERE matricola=?", (matricola,))
        self.conn.commit()

    def insert_veicolo(self, targa, marca, modello):
        self.cur.execute("INSERT INTO Veicolo VALUES (?, ?, ?)", (targa, marca, modello))
        self.conn.commit()

    def fetch_veicolo(self, targa):
        self.cur.execute("select * from Veicolo where targa=?", (targa,))
        row = self.cur.fetchone()
        veicolo = Veicolo(row[0], row[1], row[1])
        return veicolo

    def remove_veicolo(self, targa):
        self.cur.execute("DELETE FROM Veicolo WHERE targa=?", (targa,))
        self.conn.commit()

    #    def update(self, id, nome, cognome, grado):
    #        )

    def fetch_pattuglie_turno(self, giorno, ora_inizio):
        self.cur.execute(
            "SELECT targa_veicolo from TurnoDiPattuglia where giorno=? and inizio_turno=?",
            (giorno, ora_inizio,))
        rows = self.cur.fetchall()
        lista_pattuglie_turno = []

        for row in rows:
            targa = row[0]
            self.cur.execute(
                "SELECT matricola, nome, cognome, grado from  Militare as M join TurnoDiPattuglia as TDP on "
                "M.matricola=TDP.matricola_militare where TDP.giorno=? and inizio_turno=? and targa_veicolo=?",
                (giorno, ora_inizio, targa))
            pattuglia_result = self.cur.fetchall()
            militari_pattuglia = []
            for militare in pattuglia_result:
                militare = Militare(militare[0], militare[1], militare[2], militare[3])
                militari_pattuglia.append(militare)
            pattuglia = Pattuglia(militari_pattuglia[0], militari_pattuglia[1],
                                  self.fetch_veicolo(targa)).to_dictionary()
            lista_pattuglie_turno.append(pattuglia)
        return lista_pattuglie_turno

    def fetch_personale(self):
        self.cur.execute("SELECT * FROM Militare")
        rows = self.cur.fetchall()
        lista_militari = []
        for row in rows:
            militare = Militare(row[0], row[1], row[2], row[3]).to_dictionary()
            lista_militari.append(militare)
        return lista_militari

    def fetch_info_giorno(self, giorno):
        self.cur.execute("select matricola_militare from Riposo where giorno=? union SELECT matricola_militare from "
                         "TurnoDiPattuglia where giorno=? union select matricola_militare from Licenza where "
                         "giorno=? union select matricola_militare from Altro where giorno=? group by "
                         "matricola_militare", (giorno, giorno, giorno, giorno,))
        rows = self.cur.fetchall()
        militari_impegnati = []
        for row in rows:
            militare = Militare(row[0], row[1], row[2], row[3]).to_dictionary()
            militare["busy"] = "yes"
            militari_impegnati.append(militare)
        return militari_impegnati.append(self.fetch_disponibili(giorno))

    def __del__(self):
        self.conn.close()

# db = Database('store.db')
# db.insert_militare("12345678", "John Doe", "Microcenter", "pfc")
# db.insert("Asus Mobo", "Mike Henry", "Microcenter", "360")
# db.insert("500w PSU", "Karen Johnson", "Newegg", "80")
# db.insert("2GB DDR4 Ram", "Karen Johnson", "Newegg", "70")
# db.insert("24 inch Samsung Monitor", "Sam Smith", "Best Buy", "180")
# db.insert("NVIDIA RTX 2080", "Albert Kingston", "Newegg", "679")
# db.insert("600w Corsair PSU", "Karen Johnson", "Newegg", "130")
