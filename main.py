import csv

import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

url = 'https://books.toscrape.com/'

reponse = requests.get(url)
d = 1
n = 1
e = 0
u = 0
if reponse.ok:
    soup = BeautifulSoup(reponse.content, 'html.parser')



    if not os.path.exists("images"):
        os.mkdir("images")
    # DEBUT BON CODE
    #   Enregistrement des urls de categories
    url_category = []
    lk_cat = []
    ulcat = soup.find('ul', class_='nav')
    acat = ulcat.find_all('a')
    print(len(acat))
    url_cat_next = []
    for a in acat:
        lk = a['href']
        urlcatcln = url + lk
        url_category.append(urlcatcln)
    print("Len de url_category AVANT del: ", len(url_category))
    del url_category[0]
    print("Len de url_category APRES del: ", len(url_category))
   #    print(url_category)
    for a in url_category:
        pagecat = requests.get(a)
        soup = BeautifulSoup(pagecat.content, 'html.parser')
        if pagecat.ok:
            url_livres = []
            liste_dico = []
            print("\n", "IIIIICCCIIII", a, "\n")
            url_cat_next = a
            print("\n", "HUPHUHP", url_cat_next, "\n")
            #           Boucle qui permet de verifier les urls des livres ainsi que les pages next
            while True:
                d -= 1
                title = soup.h1.string
                print("le titre de la page :", title, "n =", n, " d = ", d)

                # recherche et stock les urls des livres
                bouquins = soup.find_all('article', class_='product_pod')
                i = 0
                for bouquin in bouquins:
                    a = bouquin.find('a')
                    url_livre = a['href']
                    url_propre = url_livre.replace("../../../", "")
                    url_livres.append('http://books.toscrape.com/catalogue/' + url_propre)
                    i += 1
                    print("Dans boucle bouquins", i)
                if (len(bouquins)) >= 20:
                    # recherche de bouton next
                    elements = soup.find('li', class_='next')
                    print("PRINT elements PAGE ACCUEIL = ", elements)
                    if elements:
                        n += 1
                        next_rep = url_cat_next.replace("index.html", "")
                        url_elm = elements.find("a")
                        link_next = url_elm['href']
                        next_url = next_rep + link_next
                        print("Bouton next ok", next_url, "LEN url_livres dans boucle next", len(url_livres))
                        # aller dans la page next
                        pagenext = requests.get(next_url)
                        soup = BeautifulSoup(pagenext.content, 'html.parser')
                else:
                    print("PAS DE NEXT\n", len(url_livres))
                    break
                b = 0
                e += 1
            #           Pour chaque url de livre nous allons dans la page pour recupèrer les infos de celui ci
            for a in url_livres:
                page = requests.get(a)
                soup = BeautifulSoup(page.content, 'html.parser')
                b = + 1
                if page.ok:
                    #   Début d'extraction d'infos pour un livre
                    infos_tableau = []
                    tds = soup.find_all('td')
                    for td in tds:
                        infos_tableau.append(td.string)

                    descriptions = soup.find_all('p')
                    description_livres = []
                    for description in descriptions:
                        description_livres.append(description.string)
                    product_description = description_livres[3]

                    categories = soup.find_all('a')
                    links = []
                    for categorie in categories:
                        links.append(categorie.string)
                    product_category = links[3]

                    title = soup.h1.string
                    images = soup.find_all("img")
                    image_url = []
                    for image in images:
                        image_url.append(image)
                    url_image = str(image_url[0])
                    url_img = url_image[-63:-3]
                    img_rep = url_img.replace("../../", "")
                    clean_url_img = "http://books.toscrape.com/" + img_rep

                    clean_price_icl = infos_tableau[3].strip("€$£")
                    clean_price_excl = infos_tableau[2].strip("€$£")
                    clean_numb_av = infos_tableau[5].strip("In stock() available hors")

                    dico_livres = {
                        "product_page_url": a,
                        "upc": infos_tableau[0],
                        "title": title,
                        "price_including_tax": clean_price_icl,
                        "price_excluding_tax": clean_price_excl,
                        "number_available": clean_numb_av,
                        "product_description": description_livres[3],
                        "product_category": links[3],
                        "review_rating": infos_tableau[6],
                        "image_url": clean_url_img
                    }
                    nom_category = str(links[3])



                    #            print(b, e, len(dico_livres), len(url_livres), "\n")
                    liste_dico.append(dico_livres)
                    #            print(liste_dico, "\n\n")
                    en_tetes = ["product_page_url", "upc", "title", "price_including_tax",
                                "price_excluding_tax",
                                "number_available", "product_description", "product_category", "review_rating",
                                "image_url"]
                    nom_csv = str(links[3]) + ".csv"
                    # FIN BON CODE

                    print("len de liste_dico", len(liste_dico))

            # Telechargement des images et creation des dossiers

                    u += 1
                    nom_cat_rep = nom_category.replace(" ", "_")
                    nom_dos_cat = "images/" + nom_cat_rep
                    if not os.path.exists(nom_dos_cat):
                        print("Dossier de cat n'existe pas, creation", )
                        os.mkdir(nom_dos_cat)
                    chem_cat_sl = nom_dos_cat + "/"
                    chem_cat = chem_cat_sl

                    name_url_img = url_image[-39:-3]
                    name_img = chem_cat + name_url_img
                    print(name_img)
                    img_data = requests.get(clean_url_img).content
                    with open(name_img, 'wb') as img_tel:
                        img_tel.write(img_data)








"""

                
                
                    test = os.path.exists(bon_doss)
                    if test:
                        path_name = d
                        print("OUII le dossier existe deja", path_name)
                        s = 0

                        for i in listeuh:
                            s += 1
                            nom_f = listdeux[s] + ".txt"
                            chem_img_cat = "images/" + path_name
                            sl_chm_cat = chem_img_cat + "/"
                            chem = sl_chm_cat + nom_f
                            print(chem)
                            with open(chem, 'w') as f:
                                print("fichier ok", s)
                                print("u = ", u)
                                print(nom_f)

                        print("Break de while verif dossiers")
                        break
                    else:
                        print("NOOON il ,n'existe pas, creation du dossier")
                        os.mkdir(bon_doss)
            print("Break de while verif dossier images ")
            break



    



  #  os.path.abspath(test_chemin)

   # open('images/new_file.txt', 'w')

    #    test_chemin = "test/truc"
    #    test_nom = "images/Cat"

    #    print(test)  # imprime le nom d'utilisateur

    #    myDirectory = "RRRR"
    #    p = Path(myDirectory)
    #    print(p.is_dir())  # affiche True
    #    print(p.is_file())  # affiche False

    #   nom_fichier = 'Koeufkdj'



# DEBUT BON CODE
#   Enregistrement des urls de categories
    url_category = []
    lk_cat = []
    ulcat = soup.find('ul', class_='nav')
    acat = ulcat.find_all('a')
    print(len(acat))
    url_cat_next = []
    for a in acat:
        lk = a['href']
        urlcatcln = url + lk
        url_category.append(urlcatcln)
    print("Len de url_category AVANT del: ",len(url_category))
    del url_category[0]
    print("Len de url_category APRES del: ",len(url_category))

#    print(url_category)
    for a in url_category:
        pagecat = requests.get(a)
        soup = BeautifulSoup(pagecat.content, 'html.parser')
        if pagecat.ok:
            url_livres = []
            liste_dico = []
            print("\n", "IIIIICCCIIII", a, "\n")
            url_cat_next = a
            print("\n", "HUPHUHP", url_cat_next, "\n")
#           Boucle qui permet de verifier les urls des livres ainsi que les pages next
            while True:
                d -= 1
                title = soup.h1.string
                print("le titre de la page :", title, "n =", n, " d = ", d)

                # recherche et stock les urls des livres
                bouquins = soup.find_all('article', class_='product_pod')
                i = 0
                for bouquin in bouquins:
                    a = bouquin.find('a')
                    url_livre = a['href']
                    url_propre = url_livre.replace("../../../", "")
                    url_livres.append('http://books.toscrape.com/catalogue/' + url_propre)
                    i += 1
                    print("Dans boucle bouquins", i)
                if (len(bouquins)) >= 20:
                    # recherche de bouton next
                    elements = soup.find('li', class_='next')
                    print("PRINT elements PAGE ACCUEIL = ", elements)
                    if elements:
                        n += 1
                        next_rep = url_cat_next.replace("index.html", "")
                        url_elm = elements.find("a")
                        link_next = url_elm['href']
                        next_url = next_rep + link_next
                        print("Bouton next ok", next_url, "LEN url_livres dans boucle next", len(url_livres))
                        # aller dans la page next
                        pagenext = requests.get(next_url)
                        soup = BeautifulSoup(pagenext.content, 'html.parser')
                else:
                    print("PAS DE NEXT\n", len(url_livres))
                    break
                b = 0
                e += 1
#           Pour chaque url de livre nous allons dans la page pour recupèrer les infos de celui ci
            for a in url_livres:
                page = requests.get(a)
                soup = BeautifulSoup(page.content, 'html.parser')
                b = + 1
                if page.ok:
                    #   Début d'extraction d'infos pour un livre
                    infos_tableau = []
                    tds = soup.find_all('td')
                    for td in tds:
                        infos_tableau.append(td.string)

                    descriptions = soup.find_all('p')
                    description_livres = []
                    for description in descriptions:
                        description_livres.append(description.string)
                    product_description = description_livres[3]

                    categories = soup.find_all('a')
                    links = []
                    for categorie in categories:
                        links.append(categorie.string)
                    product_category = links[3]

                    title = soup.h1.string
                    images = soup.find_all("img")
                    image_url = []
                    for image in images:
                        image_url.append(image)
                    url_image = str(image_url[0])
                    url_img = url_image[-63:-3]
                    img_rep = url_img.replace("../../", "")
                    clean_url_img = "http://books.toscrape.com/" + img_rep

                    clean_price_icl = infos_tableau[3].strip("€$£")
                    clean_price_excl = infos_tableau[2].strip("€$£")
                    clean_numb_av = infos_tableau[5].strip("In stock() available hors")

                    dico_livres = {
                        "product_page_url": a,
                        "upc": infos_tableau[0],
                        "title": title,
                        "price_including_tax": clean_price_icl,
                        "price_excluding_tax": clean_price_excl,
                        "number_available": clean_numb_av,
                        "product_description": description_livres[3],
                        "product_category": links[3],
                        "review_rating": infos_tableau[6],
                        "image_url": clean_url_img
                    }
                    #            print(b, e, len(dico_livres), len(url_livres), "\n")
                    liste_dico.append(dico_livres)
                    #            print(liste_dico, "\n\n")
                    en_tetes = ["product_page_url", "upc", "title", "price_including_tax", "price_excluding_tax",
                                "number_available", "product_description", "product_category", "review_rating",
                                "image_url"]
                    nom_csv = str(links[3]) + ".csv"
# FIN BON CODE











#                   Creation fichier

    user = os.getlogin()
    print(user)  # imprime le nom d'utilisateur


                    # Creation fichier CSV
#                    print("LEN de liste_dico dans page ", title, len(liste_dico))





  #      print(url_category)




                    exists(path)              →   Test si un chemin existe







                    try:
                        with open(nom_csv, 'w', encoding='utf-8') as f:
                            writer = csv.DictWriter(f, fieldnames=en_tetes)
                            writer.writeheader()
                            for elem in liste_dico:
                                writer.writerow(elem)
                            print("CSV OK", len(liste_dico))
                    except:
                        print("NOPE")





            # telechargement de l'image
            name_url_img = url_image[-39:-3]
            name_img = name_url_img
            img_data = requests.get(clean_url_img).content
            with open(name_img, 'wb') as img_tel:
                img_tel.write(img_data)
















    while True:
        verif_dir_img = os.path.exists("images")
        if verif_dir_img:
            print("dossier img existe")
            listeuh = [
                "A0", "A1", "A2", "A3"
            ]
            listdeux = [
                "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15",
            ]
            doss = [
                "dossier1", "dossier2", "dossier3"
            ]

            print("Len de listeuh", len(listeuh), "\n", "Len de listdeux", len(listdeux), "\n", "len de doss",
                  len(doss))

            u = 0


            for d in doss:

                bon_doss = "images/" + doss[u]


                u += 1
                print(bon_doss)
                while True:
                    test = os.path.exists(bon_doss)
                    if test:
                        path_name = d
                        print("OUII le dossier existe deja", path_name)
                        s = 0

                        for i in listeuh:
                            s += 1
                            nom_f = listdeux[s] + ".txt"
                            chem_img_cat = "images/" + path_name
                            sl_chm_cat = chem_img_cat + "/"
                            chem = sl_chm_cat + nom_f
                            print(chem)
                            with open(chem, 'w') as f:
                                print("fichier ok", s)
                                print("u = ", u)
                                print(nom_f)

                        print("Break de while verif dossiers")
                        break
                    else:
                        print("NOOON il ,n'existe pas, creation du dossier")
                        os.mkdir(bon_doss)
            print("Break de while verif dossier images ")
            break
        else:
            print("Dossier images n'existe pas")
            os.mkdir("images")
            print("-> creation en cours")













    while True:
        verif_dir_img = os.path.exists("images")
        if verif_dir_img:

            





            break
        else:
            print("Dossier images n'existe pas")
            os.mkdir("images")
            print("-> creation en cours")


  """