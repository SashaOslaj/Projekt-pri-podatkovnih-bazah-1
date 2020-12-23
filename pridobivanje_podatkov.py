import orodja
import re
import unicodedata
import os
from pathlib import Path


leta = ["/pyeongchang-2018", "/sochi-2014", "/vancouver-2010", "/turin-2006", "/salt-lake-city-2002", "/nagano-1998", 
        "/lillehammer-1994", "/albertville-1992", "/calgary-1988", "/sarajevo-1984", "/lake-placid-1980", "/innsbruck-1976",
        "/sapporo-1972", "/grenoble-1968", "/innsbruck-1964", "/squaw-valley-1960", "/cortina-d-ampezzo-1956", "/oslo-1952", 
        "/st-moritz-1948", "/garmisch-partenkirchen-1936", "/lake-placid-1932", "/st-moritz-1928", "/chamonix-1924"]
disciplina1 = "/alpine-skiing"
poddiscipline1_1 = ["/mens-alpine-combined", "/mens-downhill", "/mens-giant-slalom", "/mens-slalom", "/mens-super-g",
            "/ladies-alpine-combined", "/ladies-downhill", "/ladies-giant-slalom", "/ladies-slalom", "/ladies-super-g"]
poddiscipline1_2 = ["/alpine-combined-men", "/downhill-men", "/giant-slalom-men", "/slalom-men", "/super-g-men",
            "/alpine-combined-women", "/downhill-women", "/giant-slalom-women", "/slalom-women", "/super-g-women"]
disciplina2 = "/biathlon"
poddiscipline2_1 = ["/mens-10km-sprint", "/mens-12-5km-pursuit", "/mens-15km-mass-start", "/mens-20km-individual", 
            "/womens-10km-pursuit", "/womens-12-5km-mass-start", "/womens-15km-individual", "/womens-7-5km-sprint"]
poddiscipline2_2 = ["/10km-men", "/12-5km-pursuit-men", "/15km-mass-start-men", "/20km-men", 
            "/10km-pursuit-women", "/12-5km-mass-start-women", "/15km-women", "/7-5km-women"]
disciplina3 = "/cross-country-skiing"
poddiscipline3_1 = ["/mens-15km-free", "/mens-15km-15km-skiathlon", "/mens-50km-mass-start-classic", "/mens-sprint-classic", 
            "/ladies-10km-free", "/ladies-30km-mass-start-classic", "/ladies-7-5km-7-5km-skiathlon", "/ladies-sprint-classic"]
poddiscipline3_2 = ["/15km-men", "/skiathlon-15km-15km-men", "/50km-men", "/sprint-15km-men", 
            "/10km-women", "/30km-women", "/skiathlon-7-5km-7-5km-women", "/sprint-15km-women"]
disciplina4 = "/figure-skating"
poddiscipline4_1 = ["/mens-single-skating", 
            "/ladies-single-skating"]
poddiscipline4_2 = ["/individual-men", 
            "/individual-women"]
disciplina5 = "/freestyle-skiing"
poddiscipline5_1 = ["/mens-aerials", "/mens-moguls", "/mens-ski-cross", "/mens-ski-halfpipe", "/mens-ski-slopestyle",
            "/ladies-aerials", "/ladies-moguls", "/ladies-ski-cross", "/ladies-ski-halfpipe", "/ladies-ski-slopestyle"]
poddiscipline5_2 = ["/aerials-men", "/moguls-women", "/ski-cross-men", "/ski-halfpipe-men", "/ski-slopestyle-men",
            "/aerials-women", "/moguls-women", "/ski-cross-women", "/ski-halfpipe-women", "/ski-slopestyle-women"]
disciplina6 = "/luge"
poddiscipline6_1 = ["/mens-singles",
            "/womens-singles"]
poddiscipline6_2 = ["/singles-men",
            "/singles-women"]
disciplina7 = "/nordic-combined"
poddiscipline7_1 = ["/mens-individual-gundersen-lh-10km", "/mens-individual-gundersen-nh-10km"]
poddiscipline7_2 = ["/individual-lh-men", "/individual-men"]
disciplina8_1 = "/short-track"
poddiscipline8_1 = ["/mens-1000m", "/mens-1500m", "/mens-500m",
                "/ladies-1000m", "/ladies-1500m", "/ladies-500m"]
disciplina8_2 = "/short-track-speed-skating"
poddiscipline8_2 = ["/1000m-men", "/1500m-men", "/500m-men",
                "/1000m-women", "/1500m-women", "/500m-women"]
disciplina9 = "/skeleton"
poddiscipline9_1 = ["/men", 
            "/women"]
poddiscipline9_2 = ["/individual-men", 
            "/individual-women"]
disciplina10 = "/ski-jumping"
poddiscipline10_1 = ["/mens-large-hill-individual", "/mens-normal-hill-individual",
            "/ladies-normal-hill-individual"]
poddiscipline10_2 = ["/large-hill-individual-men", "/normal-hill-individual-men",
            "/normal-hill-individualwomen"]
disciplina11 = "/snowboard"
poddiscipline11_1 = ["/mens-big-air", "/mens-halfpipe", "/mens-parallel-giant-slalom", "/mens-slopestyle", "/mens-snowboard-cross",
            "/ladies-big-air", "/ladies-halfpipe", "/ladies-parallel-giant-slalom", "/ladies-slopestyle", "/ladies-snowboard-cross"]
poddiscipline11_2 = ["/parallel-slalom-men", "/half-pipe-men", "/giant-parallel-slalom-men", "/slopestyle-men", "/snowboard-cross-men",
            "/parallel-slalom-women", "/half-pipe-women", "/giant-parallel-slalom-women", "/slopestyle-women", "/snowboard-cross-women"]
disciplina12 = "/speed-skating"
poddiscipline12_1 = ["/mens-10000m", "/mens-1000m", "/mens-1500m", "/mens-5000m", "/mens-500m", "/mens-mass-start",
            "/ladies-1000m", "/ladies-1500m", "/ladies-3000m", "/ladies-5000m", "/ladies-500m", "/ladies-mass-start"]
poddiscipline12_2 = ["/10000m-men", "/1000m-men", "/1500m-men", "/5000m-men", "/2x500m-men",
            "/1000m-women", "/1500m-women", "/3000m-women", "/5000m-women", "/2x500m-women"]


osnovni_naslov = "https://www.olympic.org"


def podatki_posameznik(datoteka, olimpijske, disciplina, poddisciplina):
    '''
    Funkcija sprejme ime datoteke, olimpijske igre in disciplino in naredi seznam
    slovarjev v katerih so rezultati tekmovalca.
    '''
    print(datoteka)
    with open(str(datoteka), encoding='utf-8') as f:
        vsebina = f.read()

        stevec = 0
        for tekmovalec in re.finditer(
            r'<tr>.+?<td class="col1">(?P<mesto>.*?)</td>.+?<td class="col2">'
            r'.+?<a href="/(?P<ime>.+?)">.+?<span class="picture">'
            r'.+?<span>(?P<drzava>\D{3})</span>'
            r'.+?<td class="col3">(?P<rezultat>.*?)</td>.+?</tr>'
        ,vsebina, flags=re.DOTALL):

                
            mesto = tekmovalec.group('mesto')
            x = re.search(r'\d+', mesto)
            if x:
                mesto = x.group()
            else:
                if re.search('G', mesto):
                    mesto = '1'
                elif re.search('S', mesto):
                    mesto = '2'
                elif re.search('B', mesto):
                    mesto = '3'
                else:
                    mesto = ''
            
            stevec += 1
            if str(stevec) != mesto or mesto == '':
                continue

            ime = tekmovalec.group('ime')
            if ime not in tekmovalci:
                    tekmovalci.add(ime)
            ime = ime.replace("-", " ")
            ime = ime.title()

            drzava = tekmovalec.group('drzava')

            rezultat = tekmovalec.group('rezultat')
            rezultat = rezultat.strip()
            rezultat = rezultat.replace("\n", "")

            igre = olimpijske[1:]
            igre = igre.replace("-", " ")
            igre = igre.capitalize()

            # za vsakega nastopajočega ustvarimo slovar
            nastop = {}
            nastop['igre'] = igre
            nastop['disciplina'] = disciplina
            nastop['poddisciplina'] = poddisciplina
            nastop['mesto'] = mesto
            nastop['ime'] = ime
            nastop['drzava'] = drzava
            nastop['rezultat'] = rezultat
            rezultati.append(nastop)
            sez.add(tekmovalec.group('ime'))


def posameznik_rojstni_dan(datoteka, sportnik):
    '''
    Funkcija sprejme ime datotekein ime tekmovalca in naredi dva seznama.
    V enem so slovarji z imenom tekmovalca in njegovim rojstnim dnem. V drugem
    so slovarji z kratico in polnim imenom drzave.
    '''
    print(datoteka)
    with open(str(datoteka), encoding='utf-8') as f:
        vsebina = f.read()
        
        for tekmovalec in re.finditer(
            r'<div class="flag-image">'
            r'.+?<span>(?P<kratica>\D\D\D)</span>'
            r'.+?<div class="frame">'
            r'.+?<strong class="title">Country </strong>.+?'
            r'<a (itemprop="url" )?href="/(?P<drzava>.+?)">.+?</a>'
            r'.+?<strong class="title">(Born|Lived)</strong>(?P<datum>.+?)</div>'
        , vsebina, flags=re.DOTALL):

            ime = sportnik
            ime = ime.replace("-", " ")
            ime = ime.title()

            datum = tekmovalec.group('datum')
            datum = datum.replace("\n", "")
            
            meseci = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 
                      'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 
                      'Nov':'11', 'Dec':'12'}
            

            nastopajoci = {}
            nastopajoci['ime'] = ime
            if '01 Jan 0001' == datum[:11]:
                nastopajoci['datum'] = ''
            else:
                datum = datum[:11] # nekateri imajo naveden še datum smrti
                st = meseci[datum[3:6]]
                nastopajoci['datum'] = datum[:2] + '.' + st + '.' + datum[-4:]
            roj_dan_tekmovalcev.append(nastopajoci)

            kratica = tekmovalec.group('kratica')
            drzava = tekmovalec.group('drzava')
            drzava = drzava.replace("-", " ")
            drzava = drzava.title()

            if kratica not in drz:
                drz.add(kratica)
                drzave_s_kratico = {}
                drzave_s_kratico['kratica'] = kratica
                drzave_s_kratico['drzava'] = drzava
                drzave.append(drzave_s_kratico)


def prenesi_html():
    '''
    Funcija za shranitev html datoteke za tekme. Sklicuje se na funkcijo
    shrani iz datoteke orodja.
    '''

    for poddisciplina in poddiscipline1_1:
        naslov = osnovni_naslov + leta[0] + disciplina1 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina1[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline2_1:
        naslov = osnovni_naslov + leta[0] + disciplina2 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina2[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline3_1:
        naslov = osnovni_naslov + leta[0] + disciplina3 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina3[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline4_1:
        naslov = osnovni_naslov + leta[0] + disciplina4 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina4[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline5_1:
        naslov = osnovni_naslov + leta[0] + disciplina5 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina5[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline6_1:
        naslov = osnovni_naslov + leta[0] + disciplina6 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina6[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline7_1:
        naslov = osnovni_naslov + leta[0] + disciplina7 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina7[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline8_1:
        naslov = osnovni_naslov + leta[0] + disciplina8_1 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina8_1[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline9_1:
        naslov = osnovni_naslov + leta[0] + disciplina9 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina9[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline10_1:
        naslov = osnovni_naslov + leta[0] + disciplina10 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina10[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline11_1:
        naslov = osnovni_naslov + leta[0] + disciplina11 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina11[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)
    for poddisciplina in poddiscipline12_1:
        naslov = osnovni_naslov + leta[0] + disciplina12 + poddisciplina
        datoteka = "rezultati_{}_{}_{}.html".format(leta[0], disciplina12[1:], poddisciplina[1:])
        orodja.shrani(naslov, datoteka)

    for olimpijske in leta[1:]: 
        for poddisciplina in poddiscipline1_2:
            naslov = osnovni_naslov + olimpijske + disciplina1 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina1[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline2_2:
            naslov = osnovni_naslov + olimpijske + disciplina2 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina2[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline3_2:
            naslov = osnovni_naslov + olimpijske + disciplina3 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina3[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline4_2:
            naslov = osnovni_naslov + olimpijske + disciplina4 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina4[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline5_2:
            naslov = osnovni_naslov + olimpijske + disciplina5 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina5[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline6_2:
            naslov = osnovni_naslov + olimpijske + disciplina6 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina6[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline7_2:
            naslov = osnovni_naslov + olimpijske + disciplina7 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina7[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline8_2:
            naslov = osnovni_naslov + olimpijske + disciplina8_2 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina8_2[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline9_2:
            naslov = osnovni_naslov + olimpijske + disciplina9 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina9[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline10_2:
            naslov = osnovni_naslov + olimpijske + disciplina10 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina10[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline11_2:
            naslov = osnovni_naslov + olimpijske + disciplina11 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina11[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)
        for poddisciplina in poddiscipline12_2:
            naslov = osnovni_naslov + olimpijske + disciplina12 + poddisciplina
            datoteka = "rezultati_{}_{}_{}.html".format(olimpijske, disciplina12[1:], poddisciplina[1:])
            orodja.shrani(naslov, datoteka)


def prenesi_html_tekmovalca():
    '''
    Funcija za shranitev html datoteke za vsakega tekmovalca. Sklicuje se
    na funkcijo shrani iz datoteke orodja.
    '''
    
    for tekmovalec in tekmovalci:
        tekmovalec.replace('\n', '')
        naslov = osnovni_naslov + "/" + tekmovalec
        datoteka = "{}.html".format(tekmovalec)
        pot = os.path.join("tekmovalci", datoteka)
        orodja.shrani(naslov, pot)


def preberi_podatke():
    '''
    Funkcija shrani rezultate tekmovalcev v seznam s pomocjo zgornjih dveh
    funkcij: podatki_posameznik in podatki_skupine.
    '''

    
    for poddisc in poddiscipline1_1:
        disc = disciplina1.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline2_1:
        disc = disciplina2.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline3_1:
        disc = disciplina3.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline4_1:
        disc = disciplina4.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline5_1:
        disc = disciplina5.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline6_1:
        disc = disciplina6.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline7_1:
        disc = disciplina7.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline8_1:
        disc = disciplina8_1.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline9_1:
        disc = disciplina9.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline10_1:
        disc = disciplina10.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline11_1:
        disc = disciplina11.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)
    for poddisc in poddiscipline12_1:
        disc = disciplina12.replace("/", "")
        poddisc = poddisc.replace("/", "")
        dat = Path("rezultati_{}_{}_{}.html".format(leta[0], disc, poddisc))
        #print(dat)
        disc = disc.replace('-',' ')
        poddisc = poddisc.replace('-', ' ')
        podatki_posameznik(dat, leta[0], disc, poddisc)

    for olimpijske in leta[1:]:
        for poddisc in poddiscipline1_2:
            disc = disciplina1.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline2_2:
            disc = disciplina2.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline3_2:
            disc = disciplina3.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline4_2:
            disc = disciplina4.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline5_2:
            disc = disciplina5.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline6_2:
            disc = disciplina6.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline7_2:
            disc = disciplina7.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline8_2:
            disc = disciplina8_2.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline9_2:
            disc = disciplina9.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline10_2:
            disc = disciplina10.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline11_2:
            disc = disciplina11.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        for poddisc in poddiscipline12_2:
            disc = disciplina12.replace("/", "")
            poddisc = poddisc.replace("/", "")
            dat = Path("rezultati_{}_{}_{}.html".format(olimpijske, disc, poddisc))
            #print(dat)
            disc = disc.replace('-',' ')
            poddisc = poddisc.replace('-', ' ')
            podatki_posameznik(dat, olimpijske, disc, poddisc)
        

def preberi_podatke_tekmovalcev():
    '''
    Funkcija shrani rojstne dneve tekmovalcev in kratice in polna imena drzav v
    seznam s pomocjo zgornje funkcije posameznik_rojstni_dan.
    '''

    tekm = set()
    f = open('tekmovalci.txt', 'r')
    for line in f:
        tekm.add(line)
    f.close()

    mnozica_tekmovalcev = [tekmovalec[:-1] for tekmovalec in tekm]

    for tekmovalec in mnozica_tekmovalcev:
        dat = Path("tekmovalci")
        pot = dat / "{}.html".format(tekmovalec)
        posameznik_rojstni_dan(pot, tekmovalec)


def zapisi_tekmovalce(tekmovalci):
    '''
    Funkcija v datoteko tekmovalci.txt zapise vsa imena tekmovalcev iz seznama.
    '''

    f = open("tekmovalci.txt", "w+", encoding='utf-8')
    for tekmovalec in tekmovalci:
        f.write(tekmovalec + "\n")
    f.close()


rezultati = []
tekmovalci = set()
roj_dan_tekmovalcev = []
sez = set()
drz = set()
drzave = []


#prenesi_html()
preberi_podatke()
print(len(tekmovalci))
#prenesi_html_tekmovalca()


zapisi_tekmovalce(tekmovalci)
preberi_podatke_tekmovalcev()

orodja.zapisi_tabelo(rezultati, ['igre', 'disciplina', 'poddisciplina', 'mesto', 'ime', 'drzava', 'rezultat'], 'rezultati.csv')
orodja.zapisi_tabelo(roj_dan_tekmovalcev, ['ime', 'datum'], 'roj_dan_tekmovalcev.csv')
orodja.zapisi_tabelo(drzave, ['kratica', 'drzava'], 'seznam_drzav.csv')
