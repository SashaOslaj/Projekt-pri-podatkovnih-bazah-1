import random
import string
import sqlite3

def dodaj_licencno_st(conn, licenca):
    sql = '''
        INSERT INTO licenca
        (id)
        VALUES
        ("{}")
    '''.format(licenca)
    conn.execute(sql)
    conn.commit()

def naredi_bazo():
    IME_DATOTEKE_Z_BAZO = 'zimskeOI.db'
    conn = sqlite3.connect(IME_DATOTEKE_Z_BAZO)
    ze_dodani = set()
    stevec = 0
    # Generiramo podatke
    while stevec < 100:
        licencna_st = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        if licencna_st not in ze_dodani:
            ze_dodani.add(licencna_st)
            stevec += 1
            dodaj_licencno_st(conn, licencna_st)
        
    #conn.execute('VACUUM')


naredi_bazo()
