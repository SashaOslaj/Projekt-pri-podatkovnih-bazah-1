from bottle import *
import model

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/')
def osnovna_stran():
    return template('home.html')

@get('/athletes')
def poisci():
    return template('izberi_tekmovalca.html', tekmovalci=model.Tekmovalec().poisci_vse_tekmovalce())

@get('/name/<name>')
def poisci(name):
    return template('tekmovalci.html', name=name, poizvedbe=model.Tekmovalec(ime=name).poisci_po_imenu())

@get('/country/<drzava>')
def poisci(drzava):
    return template('tekmovalci.html', name=drzava, poizvedbe=model.Tekmovalec(drzava=drzava).poisci_po_drzavi())

@get('/year/<letnica>')
def poisci(letnica):
    return template('tekmovalci.html', name=letnica, poizvedbe=model.Tekmovalec(letnica=letnica).poisci_po_letnici())

run(host='localhost', port=8080, reloader=True, debug=True)
