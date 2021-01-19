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
    def poisci_po_drzavi(drzava):
        k = drzava
        if k in iz_star_v_novo_krat:
            k = iz_star_v_novo_krat[k]
        sql = '''
        SELECT tekmovalec.ime, tekmovalec.rojen, drzava.ime, tekmovalec.id FROM tekmovalec
        JOIN drzava ON tekmovalec.drzava = drzava.kratica
        WHERE tekmovalec.drzava LIKE ?'''
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
        ORDER BY leto DESC;'''
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield poizvedba[0]


class Discipline:

    def __init__(self, disciplina=None, id=None):
        self.disciplina = disciplina
        self.id = id

    def __str__(self):
        return self.disciplina

    @staticmethod
    def poisci_sql(sql, podatki=None):
        for poizvedba in conn.execute(sql, podatki):
            yield Discipline(*poizvedba)

    @staticmethod
    def pridobi_vse_discipline():
        sql = '''
                SELECT id, ime FROM disciplina
                ORDER BY ime;'''
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield poizvedba

    @staticmethod
    def poisci_po_imenu(ime, limit=None):
        sql = '''
            SELECT ime FROM disciplina
            WHERE ime LIKE ?'''
        podatki = ['%' + ime + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Discipline.poisci_sql(sql, podatki)


class Poddiscipline:

    def __init__(self, poddisciplina=None, disciplina=None):
        self.disciplina = disciplina
        self.poddisciplina = poddisciplina

    def __str__(self):
        return self.poddisciplina

    @staticmethod
    def poisci_sql(sql, podatki=None):
        for poizvedba in conn.execute(sql, podatki):
            yield Poddiscipline(*poizvedba)

    @staticmethod
    def poisci_po_imenu(ime, limit=None):
        sql = '''
                SELECT ime FROM poddisciplina
                WHERE ime LIKE ?'''
        podatki = ['%' + ime + '%']
        if limit:
            sql += ' LIMIT ?'
            podatki.append(limit)
        yield from Poddiscipline.poisci_sql(sql, podatki)

    @staticmethod
    def pridobi_vse_poddiscipline():
        sql = '''
                SELECT DISTINCT id, ime, disciplina FROM poddisciplina
                ORDER BY ime;'''
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield poizvedba

    @staticmethod
    def pridobi_poddisciplino_id_disc(id_disc):
        sql = '''
            SELECT id, ime FROM poddisciplina
            WHERE disciplina={};'''.format(id_disc)
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield poizvedba

    @staticmethod
    def pridobi_poddisciplino(id):
        sql = '''
        SELECT ime FROM poddisciplina
        WHERE id={};'''.format(id)
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
        WHERE rezultat.leto={} AND rezultat.disciplina={};'''.format(leto, poddisciplina)
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
        WHERE rezultat.tekmovalec={}
        ORDER BY rezultat.leto DESC, rezultat.mesto ASC;'''.format(id)
        poizvedbe = conn.execute(sql).fetchall()
        for poizvedba in poizvedbe:
            yield poizvedba


class Uporabnik:

    def __init__(self, uporabniskoIme=None, geslo=None, licenca=None):
        self.uporabniskoIme = uporabniskoIme
        self.geslo = geslo
        self.licenca = licenca

    def __str__(self):
        return self.uporabniskoIme

    def jeUporabnik(self):
        sql = '''
        SELECT * FROM uporabnik
        WHERE uporabniskoIme="{}";'''.format(self.uporabniskoIme)
        poizvedba = conn.execute(sql)
        if poizvedba.fetchone():
            return poizvedba
        return None

    def jeUporabljenaLicenca(self):
        sql = '''
        SELECT * FROM uporabnik
        WHERE licenca="{}";'''.format(self.licenca)
        poizvedba = conn.execute(sql)
        if poizvedba.fetchone():
            return poizvedba
        return None

    def vstaviUporabnika(self):
        sql = '''
        INSERT INTO uporabnik (uporabniskoIme, geslo, licenca) VALUES ("{}","{}", "{}");'''.format(self.uporabniskoIme, self.geslo, self.licenca)
        conn.execute(sql)
        conn.commit()

    @staticmethod
    def jePravaLicenca(licencna_st):
        sql = '''
        SELECT id FROM licenca
        WHERE id="{}"'''.format(licencna_st)
        poizvedba = conn.execute(sql).fetchone()
        print(poizvedba)
        if poizvedba:
            return poizvedba[0]
        return None

class Uredi:

    def __init__(self, uporabnik=None):
        self.uporabnik = uporabnik

    def __str__(self):
        return self.uporabnik

    @staticmethod
    def zabelezi_dodajanje(uporabnik, ime, rojDan, drzava):
        rojDan = rojDan.replace(".", "-")
        tekmovalec_drzava, tekmovalec_kratica = tuple(drzava.split(","))
        tekmovalec_kratica = tekmovalec_kratica[1:]
        id_tekmovalca = Uredi.idTekmovalca(ime, rojDan, tekmovalec_drzava, tekmovalec_kratica)
        kajNaredil = "Dodal"
        razlog = "Je tekmoval in prišel do konca."
        sql = '''
        INSERT INTO popravi (uporabnik, tekmovalec, kajNaredi, razlog)
        VALUES ("{}",{},"{}","{}")'''.format(uporabnik, id_tekmovalca, kajNaredil, razlog)
        conn.execute(sql)
        conn.commit()

    @staticmethod
    def dodaj_tekmovalca(ime, rojDan, drzava, leto, disciplina, poddisciplina, mesto, rezultat):
        rojDan = rojDan.replace(".", "-")
        tekmovalec_drzava, tekmovalec_kratica = tuple(drzava.split(","))
        tekmovalec_kratica = tekmovalec_kratica[1:]
        oi_leto, oi_drzava, oi_kratica = tuple(leto.split(','))
        oi_drzava = oi_drzava[1:]
        oi_kratica = oi_kratica[1:]
        Uredi.dodajLeto(oi_leto, oi_drzava, oi_kratica)
        id_poddiscipline = Uredi.idPoddisciplina(disciplina, poddisciplina)
        id_tekmovalca = Uredi.idTekmovalca(ime, rojDan, tekmovalec_drzava, tekmovalec_kratica)
        sql = '''
        INSERT INTO rezultat (leto, disciplina, tekmovalec, drzava, mesto, rezultat) 
        VALUES ({}, {}, {}, "{}", {}, "{}")'''.format(int(oi_leto), id_poddiscipline, id_tekmovalca, tekmovalec_kratica, int(mesto), rezultat)
        conn.execute(sql)
        conn.commit()

    @staticmethod
    def idPoddisciplina(disciplina,poddisciplina):
        sql1 = '''
        SELECT ime 
        FROM poddisciplina;'''
        poddiscipline = conn.execute(sql1).fetchall()
        if (poddisciplina,) not in poddiscipline:
            id_discipline = Uredi.idDisciplina(disciplina)
            sql2 = '''
            INSERT INTO poddisciplina (ime, disciplina) 
            VALUES ("{}",{})'''.format(poddisciplina, id_discipline)
            conn.execute(sql2)
            conn.commit()
        sql3 = '''
        SELECT id FROM poddisciplina
        WHERE ime="{}"'''.format(poddisciplina)
        id = conn.execute(sql3).fetchone()
        return id[0]


    @staticmethod
    def idDisciplina(disciplina):
        sql1 = '''
        SELECT ime 
        FROM disciplina;'''
        discipline = conn.execute(sql1).fetchall()
        if (disciplina,) not in discipline:
            sql2 = '''
            INSERT INTO disciplina (ime) 
            VALUES ("{}")'''.format(disciplina)
            conn.execute(sql2)
            conn.commit()
        sql3 = '''
        SELECT id FROM disciplina
        WHERE ime="{}"'''.format(disciplina)
        id = conn.execute(sql3).fetchone()
        return id[0]

    @staticmethod
    def idTekmovalca(ime, rojDan, drzava, kratica):
        sql1 = '''
        SELECT ime 
        FROM tekmovalec;'''
        tekmovalci = conn.execute(sql1).fetchall()
        if (ime,) not in tekmovalci:
            Uredi.dodajDrzavo(drzava, kratica)
            sql2 = '''
            INSERT INTO tekmovalec (ime, rojen, drzava) 
            VALUES ("{}","{}","{}")'''.format(ime, rojDan, kratica)
            print(sql2)
            conn.execute(sql2)
            conn.commit()
        sql3 = '''
        SELECT id FROM tekmovalec
        WHERE ime="{}" AND rojen="{}"'''.format(ime, rojDan)
        id = conn.execute(sql3).fetchone()
        return id[0]

    @staticmethod
    def dodajDrzavo(drzava, kratica):
        sql1 = '''
        SELECT kratica 
        FROM drzava;'''
        kratice = conn.execute(sql1).fetchall()
        if (kratica,) not in kratice:
            sql2 = '''
            INSERT INTO drzava (kratica, ime) 
            VALUES ("{}", "{}")'''.format(kratica, drzava)
            conn.execute(sql2)
            conn.commit()

    @staticmethod
    def dodajLeto(leto, drzava, kratica):
        leto = int(leto)
        sql1 = '''
        SELECT leto 
        FROM olimpijskeIgre;'''
        leta = conn.execute(sql1).fetchall()
        sql2 = '''
        SELECT kratica 
        FROM drzava;'''
        kratice = conn.execute(sql2).fetchall()
        if (leto,) not in leta:
            if (kratica,) not in kratice:
                Uredi.dodajDrzavo(drzava, kratica)
            sql3 = '''
            INSERT INTO olimpijskeIgre (leto, drzava) 
            VALUES ({}, "{}")'''.format(leto, kratica)
            conn.execute(sql3)
            conn.commit()

    @staticmethod
    def odstraniRezultat(id_tekmovalca, leto):
        leto = int(leto)
        id_tekmovalca = int(id_tekmovalca)
        sql1 = '''
        SELECT disciplina, mesto FROM rezultat
        WHERE tekmovalec={} AND leto={};'''.format(id_tekmovalca, leto)
        discipline = conn.execute(sql1).fetchall()
        for disciplina, mesto1 in discipline:
            sql2 = '''
            SELECT id, mesto FROM rezultat
            WHERE leto={} AND disciplina="{}" AND mesto>{}'''.format(leto, disciplina, mesto1)
            poizvedbe = conn.execute(sql2).fetchall()
            for id, mesto2 in poizvedbe:
                mesto2 = mesto2 - 1
                sql3 = '''
                UPDATE rezultat
                SET mesto={}
                WHERE id={};'''.format(mesto2, id)
                conn.execute(sql3)
                conn.commit()
        sql4 = '''
        DELETE FROM rezultat 
        WHERE tekmovalec={} AND leto={}'''.format(id_tekmovalca, leto)
        conn.execute(sql4)
        conn.commit()


    @staticmethod
    def zabelezi_odstranitev(uporabnik, id_tekmovalca, razlog):
        id_tekmovalca = int(id_tekmovalca)
        kajNaredil = "Odstranil"
        sql = '''
        INSERT INTO popravi (uporabnik, tekmovalec, kajNaredi, razlog)
        VALUES ("{}",{},"{}","{}")'''.format(uporabnik, id_tekmovalca, kajNaredil, razlog)
        conn.execute(sql)
        conn.commit()







