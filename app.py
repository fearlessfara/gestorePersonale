import json

from flask import Flask, request, Response, render_template
from flask_cors import CORS

import database

db = database.Database("store.db")

app = Flask(__name__)

CORS(app)

# definizione delle costanti

STATUS = "STATUS"


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/get', methods=['GET'])
def get():
    response_dict = {}
    content = request.get_json()
    response_dict[STATUS] = "true"
    response_dict["content"] = content
    js_dump = json.dumps(response_dict)
    resp = Response(js_dump, status=200, mimetype='application/json')
    return resp


@app.route('/post', methods=['POST'])
def post():
    response_dict = {}
    content = request.get_json()
    response_dict[STATUS] = "true"
    response_dict["content"] = content
    js_dump = json.dumps(response_dict)
    resp = Response(js_dump, status=200, mimetype='application/json')
    return resp


@app.route('/inserisciPattuglia', methods=['POST'])
def inserisci_pattuglia():
    # la pattuglia è composta da due militari ed un veicolo, per comodità passiamo le matricole dei 2 mlitari
    # è una soluzione molto hard coded ma attualmente va bene così com'è

    response_dict = {}
    content = request.get_json()
    inizio_turno = content['inizio_turno']
    fine_turno = content['fineTurno']
    data = content['dataTurno']
    primo_militare = content['primo_militare']
    secondo_militare = content['secondo_militare']
    targa = content['targa_veicolo']
    try:
        db.insert_turno_pattuglia(inizio_turno, fine_turno, data, targa, primo_militare, secondo_militare)
        response_dict[STATUS] = "true"
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=200, mimetype='application/json')
    except Exception as e:
        response_dict = {'error': 'error occured on server side. Please try again', "stacktrace": str(e)}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=500,
                        mimetype='application/json')

    return resp


@app.route('/inserisciMilitare', methods=['POST'])
def inserisci_militare():
    # endpoint per l'inserimento di un militare nel db
    # i parametri necessari sono matricola, nome, cognome e grado

    response_dict = {}
    content = request.get_json()
    matricola = content['matricola']
    nome = content['nome']
    cognome = content['cognome']
    grado = content['grado']
    print(content)
    try:
        db.insert_militare(matricola, nome, cognome, grado)
        response_dict[STATUS] = "true"
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=200, mimetype='application/json')
    except Exception as e:
        response_dict = {'error': 'error occured on server side. Please try again',
                         "stacktrace": str(e)}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=500,
                        mimetype='application/json')

    return resp


@app.route("/getListaPersonale", methods=["GET"])
def get_lista_personale():
    # ritorna la lista con tutti i militari presenti nel database
    response_dict = {}
    try:
        lista_personale = db.fetch_personale()
        response_dict[STATUS] = "true"
        response_dict["lista_personale"] = lista_personale
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=200, mimetype='application/json')
    except Exception as e:
        response_dict = {'error': 'error occured on server side. Please try again', "stacktrace": str(e)}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=500,
                        mimetype='application/json')

    return resp


@app.route('/getListaDisponibili', methods=['GET', 'POST'])
def get_lista_disponibili():
    # passando il giorno come parametro viene restituita la lista dei militari disponibili, cioè non impegnati in
    # servizi, licenze, risposi o altro

    response_dict = {}
    content = request.get_json()
    print(content)
    giorno = content['giorno']
    try:
        lista_disponibili = db.fetch_disponibili(giorno)
        response_dict[STATUS] = "true"
        response_dict["lista_disponibili"] = lista_disponibili
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=200, mimetype='application/json')
    except Exception as e:
        response_dict = {'error': 'error occured on server side. Please try again', "stacktrace": str(e)}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=500,
                        mimetype='application/json')

    return resp


@app.route("/getPattuglieTurno", methods=["GET"])
def get_pattuglie_turno():
    response_dict = {}
    content = request.get_json()
    giorno = content["giorno"]
    ora_inizio = content["ora_inizio"]
    try:
        pattuglie_turno = db.fetch_pattuglie_turno(giorno, ora_inizio)
        response_dict[STATUS] = "true"
        response_dict["pattuglie_turno"] = pattuglie_turno
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=200, mimetype='application/json')
    except Exception as e:
        response_dict = {'error': 'error occured on server side. Please try again', "stacktrace": str(e)}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=500,
                        mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
