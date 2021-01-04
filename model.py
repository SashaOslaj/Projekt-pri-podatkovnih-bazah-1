import sqlite3

conn = sqlite3.connect('zimskeOI.db')

iz_star_v_novo = {
    "Federal Republic Of Germany 1950 1990 Ger Since" : "Germany",
    "Russian Federation": "Russia",
    "United Team Of Germany 1956 1960 1964": "Germany",
    "Olympic Athlete From Russia": "Russia",
    "Democratic People S Republic Of Korea": "Republic Of Korea",
    "Unified Team Ex Ussr In 1992": "Ussr",
    "People S Republic Of China": "China",
    "Hong Kong China": "China",
    "Chinese Taipei": "Taipei",
    "German Democratic Republic": "Germany"
}

iz_star_v_novo_krat = {
    "EUA": "GER",
    "FRG": "GER",
    "EUN": "URS",
    "OAR": "RUS",
    "PRK": "KOR",
    "GDR": "GER",
    "HKG": "CHN"
}

# Tu bova naredili poizvedbe, do katerih bi lahko prišli na spletnem vmesniku

class Tekmovalec:
    
    def __init__(self, ime=None, letnica=None, drzava=None, id=None):
        self.ime = ime
        self.letnica = letnica
        self.drzava = drzava
        self.id = id

    def __str__(self):
        if self.letnica==None and self.drzava==None:
            return self.ime
        return self.ime + ' born ' + self.letnica + ' from ' + str(self.drzava)

    @staticmethod
    def poisci_vse_tekmovalce():
        sql = '''
        SELECT ime FROM tekmovalec
        ORDER BY ime'''
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield Tekmovalec(poizvedba[0])

    @staticmethod
    def poisci_po_imenu(ime, limit=None):
        sql = '''
        SELECT tekmovalec.ime, tekmovalec.rojen, drzava.ime, tekmovalec.id FROM tekmovalec
        JOIN drzava ON tekmovalec.drzava = drzava.kratica
        WHERE tekmovalec.ime LIKE ?'''
        podatki = ['%' + ime + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        poizvedbe = conn.execute(sql, podatki)
        for poizvedba in poizvedbe:
            d = poizvedba[2]
            if poizvedba[2] in iz_star_v_novo:
                d = iz_star_v_novo[poizvedba[2]]
            yield Tekmovalec(poizvedba[0], poizvedba[1], d, poizvedba[3])

    @staticmethod
    def poisci_po_drzavi(drzava):
        k = drzava
        if k in iz_star_v_novo_krat:
            k = iz_star_v_novo_krat[k]
        sql = '''
        SELECT tekmovalec.ime, tekmovalec.rojen, drzava.ime, tekmovalec.id FROM tekmovalec
        JOIN drzava ON tekmovalec.drzava = drzava.kratica
        WHERE tekmovalec.drzava LIKE ?'''.format(k)
        poizvedbe = conn.execute(sql, ['%' + k + '%'])
        for poizvedba in poizvedbe:
            d = poizvedba[2]
            if poizvedba[2] in iz_star_v_novo:
                d = iz_star_v_novo[poizvedba[2]]
            yield Tekmovalec(poizvedba[0], poizvedba[1], d, poizvedba[3])

    @staticmethod
    def poisci_po_letnici(leto):
        sql = '''
        SELECT tekmovalec.ime, tekmovalec.rojen, drzava.ime, tekmovalec.id FROM tekmovalec
        JOIN drzava ON tekmovalec.drzava = drzava.kratica
        WHERE tekmovalec.rojen LIKE ?'''
        poizvedbe = conn.execute(sql, ['%' + leto + '%'])
        for poizvedba in poizvedbe:
            d = poizvedba[2]
            if poizvedba[2] in iz_star_v_novo:
                d = iz_star_v_novo[poizvedba[2]]
            yield Tekmovalec(poizvedba[0], poizvedba[1], d, poizvedba[3])


class Leta:

    def __init__(self, leto=None):
        self.leto = leto

    def __str__(self):
        return str(self.leto)

    def pridobi_vsa_leta(self):
        sql = '''
        SELECT leto FROM olimpijskeIgre
        ORDER BY leto DESC'''
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield Leta(poizvedba[0])
