import json
import os
import sqlite3


def dodaj_rezultat(conn, id_tekmovalec, rezultati):
    leto = int(rezultati['igre'][-4:])
    mesto = int(rezultati['mesto'])
    parametri = [
        leto,
        rezultati['poddisciplina'],
        id_tekmovalec,
        rezultati['drzava'],
        mesto,
        rezultati['rezultat'],
    ]
    sql = '''
        INSERT INTO rezultat
        (leto, disciplina, tekmovalec, drzava, mesto, rezultat)
        VALUES
        ({},'{}',{},'{}',{},'{}')'''.format(parametri[0],parametri[1],parametri[2],parametri[3],parametri[4],parametri[5])
    conn.execute(sql)


def napolni_tabele_rezultati(conn, rezultati):
    for rezultat in rezultati:
        cur = conn.execute('SELECT id FROM tekmovalec WHERE ime="{}"'.format(rezultat['ime']))
        id_tek = cur.fetchall()
        if id_tek != []:
            dodaj_rezultat(conn, id_tek[0][0], rezultat)

    conn.commit()


def naredi_bazo():
    IME_DATOTEKE_Z_BAZO = 'zimskeOI.db'
    IME_DATOTEKE_Z_REZULTATI = 'rezultati.json'
    conn = sqlite3.connect(IME_DATOTEKE_Z_BAZO)
    # Naložimo podatke
    with open(IME_DATOTEKE_Z_REZULTATI) as datoteka_s_podatki:
        rezultati = json.load(datoteka_s_podatki)
    napolni_tabele_rezultati(conn, rezultati)

    conn.execute('VACUUM')


naredi_bazo()
