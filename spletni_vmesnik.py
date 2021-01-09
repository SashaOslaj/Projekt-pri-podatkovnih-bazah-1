from bottle import *
import json
import model

def password_md5(s):
    """Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
       kodirana s to funkcijo."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/')
def osnovna_stran():
    return template('home.html')

@get('/login')
def login():
    return template('login.html', napaka=None)

@post('/login')
def login_post():
    '''Obdelaj izpolnjeno formo za prijavo'''
    # Uporabniško ime, ki ga je uporabnik vpisal v formo
    uporabniskoIme = request.forms.username
    # Izračunamo MD5 has gesla, ki ga bomo spravili
    geslo = password_md5(request.forms.password)
    # Preverimo, ali se je uporabnik pravilno prijavil
    poizvedba = model.Uporabnik(uporabniskoIme, geslo).jeUporabnik()
    if poizvedba is None:
        # Uporabnisko ime in geslo se ne ujemata
        return  template('login.html', napaka='Uporabnik ne obstaja.')
    else:
        # Vse je vredu, nastavimo
        response.set_cookie('uporabniskoIme', uporabniskoIme, path='/')
        redirect('/')

@get('/logout')
def logout():
    '''Pobrisi cookie in preusmeri na login.'''
    response.delete_cookie('uporabniskoIme')
    redirect('/')

@get('/register')
def register():
    return template('register.html', username=None, napaka=None)

@post('/register')
def register_post():
    print('trying to register')
    '''Registriraj novega uporabnika.'''
    uporabniskoIme = request.forms.username
    geslo1 = request.forms.password1
    geslo2 = request.forms.password2
    poizvedba = model.Uporabnik(uporabniskoIme=uporabniskoIme).jeUporabnik()
    if poizvedba:
        print('Uporabnisko ime ze obstaja')
        # Uporabnisko ime ze obstaja
        return template('register.html', username=uporabniskoIme, napaka='To uporabnisko ime ze obstaja.')
    elif not geslo1 == geslo2:
        print('gesli se ne ujemata')
        # Gesli se ne ujemata
        return template('register.html', username=uporabniskoIme, napaka='Gesli se ne ujemata.')
    else:
        # Vse je vredu, vstavi novega uporabnika v bazo
        print('ustvarjamo novega uporabnika')

        geslo = password_md5(geslo1)
        model.Uporabnik(uporabniskoIme, geslo).vstaviUporabnika()
        
        # Dodaj uporabniku cookie
        response.set_cookie('uporabniskoIme', uporabniskoIme, path='/')
        redirect('/')

@get('/athletes')
def poisci():
    return template('izberi_tekmovalca.html')

@get('/name/<name>')
def poisci(name):
    return template('tekmovalci.html', name=name, poizvedbe=model.Tekmovalec.poisci_po_imenu(name))

@get('/country/<drzava>')
def poisci(drzava):
    return template('tekmovalci.html', name=drzava, poizvedbe=model.Tekmovalec.poisci_po_drzavi(drzava))

@get('/year/<letnica:int>')
def poisci(letnica):
    return template('tekmovalci.html', name=letnica, poizvedbe=model.Tekmovalec.poisci_po_letnici(letnica))

@get('/autocomplete/athletes')
def autocomplete_athletes():
    query = request.query.get("query", "")
    return json.dumps({"suggestions": [{"value": tekmovalec.ime, "data": tekmovalec.id}
                                       for tekmovalec in model.Tekmovalec.poisci_po_imenu(query, limit=20)]})

run(host='localhost', port=8080, reloader=True, debug=True)
