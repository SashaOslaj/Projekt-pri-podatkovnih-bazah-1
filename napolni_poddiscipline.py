import json
import sqlite3

# To datoteko pozeni potem, ko pozenes napolni_bazo.py


def dodaj_poddisciplino(conn, poddisciplina, disciplina):
    sql = '''
        INSERT INTO poddisciplina
        (ime, disciplina)
        VALUES
        ("{}",{})
    '''.format(poddisciplina, disciplina)
    conn.execute(sql)


def napolni_tabele_poddiscipline(conn, rezultati):
    ze_videne_poddisc = set()
    for rezultat in rezultati:
        if rezultat['poddisciplina'] not in ze_videne_poddisc:
            cur = conn.execute('SELECT id FROM disciplina WHERE ime="{}"'.format(rezultat['disciplina']))
            id_disc = cur.fetchall()
            if id_disc != []:
                ze_videne_poddisc.add(rezultat['poddisciplina'])
                dodaj_poddisciplino(conn, rezultat['poddisciplina'], id_disc[0][0])

    conn.commit()

def naredi_bazo():
    IME_DATOTEKE_Z_BAZO = 'zimskeOI.db'
    IME_DATOTEKE_Z_REZULTATI = 'rezultati.json'
    conn = sqlite3.connect(IME_DATOTEKE_Z_BAZO)
    # Naložimo podatke
    with open(IME_DATOTEKE_Z_REZULTATI) as datoteka_s_podatki:
        rezultati = json.load(datoteka_s_podatki)
    napolni_tabele_poddiscipline(conn, rezultati)

    conn.execute('VACUUM')


naredi_bazo()


