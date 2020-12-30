import json
import os
import sqlite3

mesta_v_drzave = {
    "Pyeongchang": "ROK",
    "Sochi": "RUS",
    "Vancouver": "CAN",
    "Turin": "ITA",
    "Salt lake city": "USA",
    "Nagano": "JPN",
    "Lillehammer": "NOR",
    "Albertville": "FRA",
    "Calgary": "CAN",
    "Sarajevo": "SRB",
    "Lake placid": "USA",
    "Innsbruck": "AUT",
    "Sapporo": "JPN",
    "Grenoble": "FRA",
    "Squaw valley": "USA",
    "Cortina d ampezzo": "ITA",
    "Oslo": "NOR",
    "St moritz": "SUI",
    "Garmisch partenkirchen": "GER",
    "Chamonix": "FRA"
}


def dodaj_drzavo(conn, drzave):
    sql = '''
        INSERT INTO drzava
        (kratica, ime)
        VALUES
        (?,?)
    '''
    parametri = [
        drzave['kratica'],
        drzave['drzava'],
    ]
    conn.execute(sql, parametri)


def dodaj_oi(conn, oi):
    sql = '''
        INSERT INTO olimpijskeIgre
        (leto, drzava)
        VALUES
        (?,?)
    '''
    leto = int(oi[-4:])
    drzava = mesta_v_drzave[oi[:-5]]
    parametri = [
        leto,
        drzava,
    ]
    conn.execute(sql, parametri)


def dodaj_disciplino(conn, disciplina):
    sql = '''
        INSERT INTO disciplina
        (ime)
        VALUES
        (?)
    '''
    parametri = [
        disciplina,
    ]
    conn.execute(sql, parametri)


def dodaj_poddisciplino(conn, poddisciplina, disciplina):
    sql = '''
        INSERT INTO poddisciplina
        (ime, disciplina)
        VALUES
        (?,?)
    '''
    parametri = [
        poddisciplina,
        disciplina,
    ]
    conn.execute(sql, parametri)


def dodaj_tekmovalca(conn, tekmovalci):
    sql = '''
        INSERT INTO tekmovalec
        (ime, rojen, drzava)
        VALUES
        (?,?,?)'''
    parametri = [
        tekmovalci['ime'],
        tekmovalci['datum'],
        tekmovalci['drzava'],
    ]
    conn.execute(sql, parametri)


def napolni_tabele_drzav(conn, drzave):
    for drzava in drzave:
        dodaj_drzavo(conn, drzava)

    conn.commit()


def napolni_tabele_tekmovalcev(conn, tekmovalci):
    i = 0
    for tekmovalec in tekmovalci:
        i += 1
        print(tekmovalec, i)
        dodaj_tekmovalca(conn, tekmovalec)

    conn.commit()


def napolni_tabele_poddiscipline(conn, rezultati):
    ze_videne_poddisc = set()
    for rezultat in rezultati:
        if rezultat['poddisciplina'] not in ze_videne_poddisc:
            ze_videne_poddisc.add(rezultat['poddisciplina'])
            dodaj_poddisciplino(conn, rezultat['poddisciplina'], rezultat['disciplina'])

    conn.commit()


def napolni_tabele_preostale(conn, rezultati):
    ze_videne_oi = set()
    ze_videne_disc = set()
    for rezultat in rezultati:
        if rezultat['igre'][-4:] not in ze_videne_oi:
            ze_videne_oi.add(rezultat['igre'][-4:])
            dodaj_oi(conn, rezultat['igre'])
        if rezultat['disciplina'] not in ze_videne_disc:
            ze_videne_disc.add(rezultat['disciplina'])
            dodaj_disciplino(conn, rezultat['disciplina'])

    conn.commit()


def naredi_bazo(pobrisi_ce_obstaja=False):
    IME_DATOTEKE_Z_BAZO = 'zimskeOI.db'
    IME_DATOTEKE_S_SQL_UKAZI = 'zimske_oi.sql'
    IME_DATOTEKE_Z_REZULTATI = 'rezultati.json'
    IME_DATOTEKE_S_TEKMOVALCI = 'roj_dan_tekmovalcev.json'
    IME_DATOTEKE_Z_DRZAVAMI = 'drzave.json'
    # Naredimo prazno bazo
    if os.path.exists(IME_DATOTEKE_Z_BAZO):
        if pobrisi_ce_obstaja:
            os.remove(IME_DATOTEKE_Z_BAZO)
        else:
            print('Baza že obstaja in je ne bom spreminjal.')
            return
    conn = sqlite3.connect(IME_DATOTEKE_Z_BAZO)
    # Ustvarimo tabele iz DDL datoteke
    with open(IME_DATOTEKE_S_SQL_UKAZI) as datoteka_s_sql_ukazi:
        ddl = datoteka_s_sql_ukazi.read()
        conn.executescript(ddl)
    # Naložimo podatke
    with open(IME_DATOTEKE_Z_DRZAVAMI) as datoteka_s_podatki:
        drzave = json.load(datoteka_s_podatki)
    napolni_tabele_drzav(conn, drzave)
    with open(IME_DATOTEKE_Z_REZULTATI) as datoteka_s_podatki:
        rezultati = json.load(datoteka_s_podatki)
    napolni_tabele_preostale(conn, rezultati)
    napolni_tabele_poddiscipline(conn, rezultati)
    with open(IME_DATOTEKE_S_TEKMOVALCI) as datoteka_s_podatki:
        tekmovalci = json.load(datoteka_s_podatki)
    napolni_tabele_tekmovalcev(conn, tekmovalci)

    conn.execute('VACUUM')


naredi_bazo(pobrisi_ce_obstaja=True)

