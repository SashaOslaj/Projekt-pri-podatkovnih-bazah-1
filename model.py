import sqlite3

conn = sqlite3.connect('zimskeOI.db')

iz_star_v_novo = {
    "Federal Republic Of Germany 1950 1990 Ger Since": "Germany",
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
        self.drzava = iz_star_v_novo.get(drzava, drzava)
        self.id = id

    def __str__(self):
        if self.letnica==None and self.drzava==None:
            return self.ime
        return self.ime + ' born ' + self.letnica + ' from ' + str(self.drzava)

    @staticmethod
    def poisci_sql(sql, podatki=None):
        for poizvedba in conn.execute(sql, podatki):
            yield Tekmovalec(*poizvedba)

    @staticmethod
    def poisci_vse_tekmovalce():
        sql = '''
        SELECT tekmovalec.ime, tekmovalec.rojen, drzava.ime, tekmovalec.id FROM tekmovalec
        JOIN drzava ON tekmovalec.drzava = drzava.kratica
        ORDER BY ime'''
        yield from Tekmovalec.poisci_sql(sql)

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
        yield from Tekmovalec.poisci_sql(sql, podatki)

    @staticmethod
    def poisci_po_id(id):
        sql = '''
            SELECT tekmovalec.ime, drzava.ime FROM tekmovalec
            JOIN drzava ON tekmovalec.drzava = drzava.kratica
            WHERE tekmovalec.id=?'''
        podatki = [id]
        tekm = conn.execute(sql, podatki).fetchone()
        return tekm

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
        yield from Tekmovalec.poisci_sql(sql, podatki)

    @staticmethod
    def poisci_po_drzavi(drzava):
        k = drzava
        if k in iz_star_v_novo_krat:
            k = iz_star_v_novo_krat[k]
        sql = '''
        SELECT tekmovalec.ime, tekmovalec.rojen, drzava.ime, tekmovalec.id FROM tekmovalec
        JOIN drzava ON tekmovalec.drzava = drzava.kratica
        WHERE tekmovalec.drzava LIKE ?'''.format(k)
        yield from Tekmovalec.poisci_sql(sql, ['%' + k + '%'])

    @staticmethod
    def poisci_po_letnici(leto):
        sql = '''
        SELECT tekmovalec.ime, tekmovalec.rojen, drzava.ime, tekmovalec.id FROM tekmovalec
        JOIN drzava ON tekmovalec.drzava = drzava.kratica
        WHERE tekmovalec.rojen LIKE ?'''
        yield from Tekmovalec.poisci_sql(sql, [str(leto) + '-%'])


class Leta:

    def __init__(self, leto=None):
        self.leto = leto

    def __str__(self):
        return str(self.leto)

    @staticmethod
    def pridobi_vsa_leta():
        sql = '''
        SELECT leto FROM olimpijskeIgre
        ORDER BY leto DESC'''
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield poizvedba[0]


class Discipline:

    def __init__(self, disciplina=None):
        self.disciplina = disciplina

    def __str__(self):
        return self.disciplina

    @staticmethod
    def pridobi_vse_discipline():
        sql = '''
                SELECT ime FROM disciplina
                ORDER BY ime'''
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield Discipline(poizvedba[0])


class Poddiscipline:

    def __init__(self, disciplina=None, poddisciplina=None):
        self.disciplina = disciplina
        self.poddisciplina = poddisciplina

    def __str__(self):
        return self.poddisciplina

    @staticmethod
    def pridobi_vse_poddiscipline():
        sql = '''
                SELECT DISTINCT id, ime FROM poddisciplina
                ORDER BY ime'''
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield poizvedba

    @staticmethod
    def pridobi_poddisciplino(id):
        sql = '''
        SELECT ime FROM poddisciplina
        WHERE id={}'''.format(id)
        poizvedbe = conn.execute(sql).fetchall()
        return poizvedbe[0][0]

class Rezultati:

    def __init__(self, ime=None, leto=None, poddisciplina=None, drzava=None, mesto=None, rezultat=None):
        self.ime = ime
        self.leto = leto
        self.poddisciplina = poddisciplina
        self.drzava = drzava
        self.mesto = mesto
        self.rezultat = rezultat

    def __str__(self):
        return self.drzava, self.ime, self.mesto, self.rezultat, self.leto, self.poddisciplina

    @staticmethod
    def pridobi_rezultate(leto, poddisciplina):
        sql = '''
        SELECT tekmovalec.ime, rezultat.leto, poddisciplina.ime, drzava.ime, rezultat.mesto, rezultat.rezultat
        FROM rezultat
        JOIN tekmovalec ON tekmovalec.id = rezultat.tekmovalec
        JOIN poddisciplina ON poddisciplina.id = rezultat.disciplina
        JOIN drzava ON drzava.kratica = rezultat.drzava
        WHERE rezultat.leto={} AND rezultat.disciplina={}'''.format(leto, poddisciplina)
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield poizvedba

    @staticmethod
    def pridobi_rezultate_iz_id(id):
        sql = '''
        SELECT tekmovalec.ime, rezultat.leto, poddisciplina.ime, drzava.ime, rezultat.mesto, rezultat.rezultat
        FROM rezultat
        JOIN tekmovalec ON tekmovalec.id = rezultat.tekmovalec
        JOIN poddisciplina ON poddisciplina.id = rezultat.disciplina
        JOIN drzava ON drzava.kratica = rezultat.drzava
        WHERE rezultat.tekmovalec={}'''.format(id)
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield poizvedba


class Uporabnik:

    def __init__(self, uporabniskoIme, geslo=None):
        self.uporabniskoIme = uporabniskoIme
        self.geslo = geslo

    def __str__(self):
        return self.uporabniskoIme

    def jeUporabnik(self):
        if self.geslo is None:
            sql = '''
                    SELECT * FROM uporabnik
                    WHERE uporabniskoIme="{}"'''.format(self.uporabniskoIme)
        else:
            sql = '''
            SELECT * FROM uporabnik
            WHERE uporabniskoIme="{}" AND geslo="{}"'''.format(self.uporabniskoIme, self.geslo)
        poizvedba = conn.execute(sql)
        if poizvedba.fetchone():
            return poizvedba
        return None

    def vstaviUporabnika(self):
        sql = '''
        INSERT INTO uporabnik (uporabniskoIme, geslo) VALUES ("{}","{}")'''.format(self.uporabniskoIme, self.geslo)
        conn.execute(sql)
        conn.commit()

