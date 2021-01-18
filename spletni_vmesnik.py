from bottle import *
import json
import hashlib
import model

#-----------------------------------------------------------------------------------------------------------------------
# Pomozne funkcije
def password_md5(s):
    """Vrni MD5 hash danega UTF-8 niza. Gesla vedno spravimo v bazo
       kodirana s to funkcijo."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

secret = "to skrivnost je zelo tezko uganiti 1094107c907cw982982c42"

def get_user():
    """Poglej cookie in ugotovi, kdo je prijavljeni uporabnik,
       vrni njegov username in ime. Če ni prijavljen, presumeri
       na stran za prijavo ali vrni None (advisno od auto_login).
    """
    # Dobimo username iz piškotka
    uporabniskoIme = request.get_cookie('uporabniskoIme', secret=secret)
    # Preverimo, ali ta uporabnik obstaja
    if uporabniskoIme is not None:
        r = model.Uporabnik(uporabniskoIme).jeUporabnik()
        if r is not None:
            # uporabnik obstaja, vrnemo njegove podatke
            return uporabniskoIme
    # Če pridemo do sem, uporabnik ni prijavljen, naredimo redirect
    else:
        return None

# Pomozne funkcije
#-----------------------------------------------------------------------------------------------------------------------

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/')
def osnovna_stran():
    return template('home.html', user=get_user())

@get('/login')
def login():
    return template('login.html', napaka=None)

@post('/login')
def login_post():
    '''Obdelaj izpolnjeno formo za prijavo'''
    # Uporabniško ime, ki ga je uporabnik vpisal v formo
    uporabniskoIme = request.forms.uporabniskoIme
    # Izračunamo MD5 has gesla, ki ga bomo spravili
    geslo = password_md5(request.forms.geslo)
    # Preverimo, ali se je uporabnik pravilno prijavil
    poizvedba = model.Uporabnik(uporabniskoIme, geslo).jeUporabnik()
    if poizvedba is None:
        # Uporabnisko ime in geslo se ne ujemata
        return template('login.html', napaka='Uporabnik ne obstaja.')
    else:
        # Vse je vredu, nastavimo
        response.set_cookie('uporabniskoIme', uporabniskoIme, path='/', secret=secret)
        redirect('/')

@get('/logout')
def logout():
    '''Pobrisi cookie in preusmeri na login.'''
    response.delete_cookie('uporabniskoIme')
    redirect('/')

@get('/register')
def register():
    return template('register.html', uporabniskoIme=None, napaka=None)

@post('/register')
def register_post():
    print('trying to register')
    '''Registriraj novega uporabnika.'''
    uporabniskoIme = request.forms.uporabniskoIme
    licencna_st = request.forms.licenca
    geslo1 = request.forms.geslo1
    geslo2 = request.forms.geslo2
    licenca = model.Uporabnik().jePravaLicenca(licencna_st)
    poizvedba1 = model.Uporabnik(uporabniskoIme=uporabniskoIme).jeUporabnik()
    poizvedba2 = model.Uporabnik(licenca=licencna_st).jeUporabljenaLicenca()
    if poizvedba1:
        print('Uporabnisko ime ze obstaja')
        # Uporabnisko ime ze obstaja
        return template('register.html', uporabniskoIme=uporabniskoIme, napaka='To uporabnisko ime ze obstaja.')
    elif poizvedba2:
        print('Licenca je ze uporabljena.')
        # Licenca je ze uporabljena
        return template('register.html', uporabniskoIme=uporabniskoIme, napaka='Ta licenca je ze uporabljena.')
    elif licenca:
        if not geslo1 == geslo2:
            print('gesli se ne ujemata')
            # Gesli se ne ujemata
            return template('register.html', uporabniskoIme=uporabniskoIme, napaka='Gesli se ne ujemata.')
        else:
            # Vse je vredu, vstavi novega uporabnika v bazo
            print('ustvarjamo novega uporabnika')

            geslo = password_md5(geslo1)
            model.Uporabnik(uporabniskoIme, geslo, licenca).vstaviUporabnika()

            # Dodaj uporabniku cookie
            response.set_cookie('uporabniskoIme', uporabniskoIme, path='/', secret=secret)
            redirect('/')
    else:
        return template('register.html', uporabniskoIme=uporabniskoIme, napaka='Ta licenca ne obstaja.')

@get('/athletes')
def poisci_tekmovalca():
    return template('izberi_tekmovalca.html', user=get_user())

@get('/athlete/<id>')
def vrni_po_id(id):
    print()
    ime, drzava = model.Tekmovalec.poisci_po_id(id)
    return template('tekmovalci.html', user=get_user(), name=ime, drzava=drzava, poizvedbe=model.Rezultati.pridobi_rezultate_iz_id(id))

@get('/country/<drzava>')
def vrni_po_drzavi(drzava):
    return template('tekmovalci.html', user=get_user(), name=drzava, poizvedbe=model.Tekmovalec.poisci_po_drzavi(drzava))

@get('/year/<letnica:int>')
def vrni_po_letnici(letnica):
    return template('tekmovalci.html', user=get_user(), name=letnica, poizvedbe=model.Tekmovalec.poisci_po_letnici(letnica))

@get('/results')
def poisci_rezultat():
    return template('rezultati.html', user=get_user(),
                    leta=model.Leta.pridobi_vsa_leta(),
                    discipline=list(model.Discipline.pridobi_vse_discipline()),
                    poddiscipline=model.Poddiscipline.pridobi_vse_poddiscipline())

@get('/results/<letnica:int>/<poddisciplina:int>')
def vrni_rezultate(letnica, poddisciplina):
    return template('izpis_rezultatov.html', user=get_user(), l=letnica, pd=model.Poddiscipline.pridobi_poddisciplino(poddisciplina),
                    poizvedbe=model.Rezultati.pridobi_rezultate(letnica, poddisciplina))

@get('/uredi')
def uredi():
    return template('uredi.html', user=get_user())

@post('/uredi')
def uredi_post():

    uporabnik=get_user()

    imeTekmovalca = request.forms.imeTekmovalca
    rojDan = request.forms.rojDan
    drzava = request.forms.drzava
    leto = request.forms.leto
    disciplina = request.forms.disciplina
    poddisciplina = request.forms.poddisciplina
    mesto = request.forms.mesto
    rezultat = request.forms.rezultat

    idTekmovalca = request.forms.idTekmovalca
    letoTekmovanja = request.forms.letoTekmovanja
    razlog = request.forms.razlog

    if imeTekmovalca:
        print("dodaj")
        model.Uredi.dodaj_tekmovalca(imeTekmovalca, rojDan, drzava, leto, disciplina, poddisciplina, mesto, rezultat)
        model.Uredi.zabelezi_dodajanje(uporabnik, imeTekmovalca, rojDan, drzava)
    else:
        print("odstrani")
        model.Uredi.odstraniRezultat(idTekmovalca, letoTekmovanja)
        model.Uredi.zabelezi_odstranitev(uporabnik, idTekmovalca, razlog)

    redirect('/uredi')


@get('/autocomplete/athletes')
def autocomplete_athletes():
    query = request.query.get("query", "")
    return json.dumps({"suggestions": [{"value": tekmovalec.ime, "data": tekmovalec.id}
                                       for tekmovalec in model.Tekmovalec.poisci_po_imenu(query, limit=20)]})

run(host='localhost', port=8080, reloader=True, debug=True)
