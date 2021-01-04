from bottle import *
import json
import model

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/')
def osnovna_stran():
    return template('home.html')

@get('/athletes')
def poisci():
    return template('izberi_tekmovalca.html')

@get('/name/<name>')
def poisci(name):
    return template('tekmovalci.html', name=name, poizvedbe=model.Tekmovalec.poisci_po_imenu(ime))

@get('/country/<drzava>')
def poisci(drzava):
    return template('tekmovalci.html', name=drzava, poizvedbe=model.Tekmovalec.poisci_po_drzavi(drzava))

@get('/year/<letnica>')
def poisci(letnica):
    return template('tekmovalci.html', name=letnica, poizvedbe=model.Tekmovalec.poisci_po_letnici(letnica))

@get('/autocomplete/athletes')
def autocomplete_athletes():
    query = request.query.get("query", "")
    return json.dumps({"suggestions": [{"value": tekmovalec.ime, "data": tekmovalec.id}
                                       for tekmovalec in model.Tekmovalec.poisci_po_imenu(query, limit=20)]})

run(host='localhost', port=8080, reloader=True, debug=True)
