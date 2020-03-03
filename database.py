import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
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
                'grado': row[3]
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

    def remove_veicolo(self, targa):
        self.cur.execute("DELETE FROM Veicolo WHERE targa=?", (targa,))
        self.conn.commit()

    #    def update(self, id, nome, cognome, grado):
    #        )

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
