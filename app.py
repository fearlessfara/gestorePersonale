import json

from flask import Flask, render_template, request
import database

db = database.Database("store.db")
db.fetch_disponibili("02-03-2020")
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/inserisciPattuglia', methods=['POST'])
def inserisci_pattuglia():
    # read the posted values from the UI
    content = request.get_json()
    inizioTurno = content['inizioTurno']
    fineTurno = content['fineTurno']
    data = content['dataTurno']
    primoMilitare = content['primoMilitare']
    secondoMilitare = content['secondoMilitare']
    targa = content['targaVeicolo']
    db.insert_turno_pattuglia(inizioTurno, fineTurno, data, targa, primoMilitare, secondoMilitare)
    return json.dumps({'status': 'executed'})


@app.route('/inserisciMilitare', methods=['POST'])
def inserisci_militare():
    content = request.get_json()
    matricola = content['matricola']
    nome = request['nome']
    cognome = request['cognome']
    grado = request['grado']
    db.insert_militare(matricola, nome, cognome, grado)
    return json.dumps({'status': 'executed'})


@app.route('/getListaDisponibili', methods=['GET', 'POST'])
def get_lista_disponibili():
    content = request.get_json()
    print(content)
    giorno = content['giorno']
    try:
        lista_disponibili = db.fetch_disponibili(giorno)
        return json.dumps(lista_disponibili)
    except:
        return json.dumps({'status': 'error'})


if __name__ == '__main__':
    app.run()

