import csv
import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

url = 'https://books.toscrape.com/'

reponse = requests.get(url)

if reponse.ok:
    soup = BeautifulSoup(reponse.content, 'html.parser')

    if not os.path.exists("images"):
        os.mkdir("images")
    # Enregistrement des urls de categories
    url_category = []
    lk_cat = []
    ulcat = soup.find('ul', class_='nav')
    acat = ulcat.find_all('a')
    url_cat_next = []
    for a in acat:
        lk = a['href']
        urlcatcln = url + lk
        url_category.append(urlcatcln)
    # Suppression de la premiere information récolté (ici la page index.html)
    del url_category[0]
    # Pour chaque lien dans url_category, on visite la page
    for a in url_category:
        pagecat = requests.get(a)
        soup = BeautifulSoup(pagecat.content, 'html.parser')
        if pagecat.ok:
            url_livres = []
            liste_dico = []
            url_cat_next = a
            # Boucle qui permet de verifier les urls des livres ainsi que les pages next
            while True:
                title = soup.h1.string

                # Recherche et stock les urls des livres
                bouquins = soup.find_all('article', class_='product_pod')
                for bouquin in bouquins:
                    a = bouquin.find('a')
                    url_livre = a['href']
                    url_propre = url_livre.replace("../../../", "")
                    url_livres.append('http://books.toscrape.com/catalogue/' + url_propre)

                if (len(bouquins)) >= 20:
                    # Recherche de bouton next
                    elements = soup.find('li', class_='next')
                    if elements:
                        next_rep = url_cat_next.replace("index.html", "")
                        url_elm = elements.find("a")
                        link_next = url_elm['href']
                        next_url = next_rep + link_next
                        # Aller dans la page next
                        pagenext = requests.get(next_url)
                        soup = BeautifulSoup(pagenext.content, 'html.parser')
                else:
                    break

            # Pour chaque url de livre nous allons dans la page pour recupèrer les infos de celui ci
            for a in url_livres:
                page = requests.get(a)
                soup = BeautifulSoup(page.content, 'html.parser')

                if page.ok:
                    # Début d'extraction d'infos pour un livre
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
                    clean_numb_av = infos_tableau[5].strip("In stock() available hors stock")

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
                    # Creation des fichiers CSV
                    nom_category = str(links[3])
                    liste_dico.append(dico_livres)
                    en_tetes = ["product_page_url", "upc", "title", "price_including_tax",
                                "price_excluding_tax",
                                "number_available", "product_description", "product_category", "review_rating",
                                "image_url"]
                    nom_csv_rep = str(links[3]) + ".csv"
                    nom_csv = nom_csv_rep.replace(" ", "_")

                    try:
                        with open(nom_csv, 'w', encoding='utf-8') as f:
                            writer = csv.DictWriter(f, fieldnames=en_tetes)
                            writer.writeheader()
                            for elem in liste_dico:
                                writer.writerow(elem)
                            print("Création csv", len(liste_dico), " de la catégorie : ", nom_category, " Livre : ", title)
                    except:
                        print("échec de la creation du csv")

                    # Creation des dossiers
                    nom_cat_rep = nom_category.replace(" ", "_")
                    nom_dos_cat = "images/" + nom_cat_rep
                    if not os.path.exists(nom_dos_cat):
                        print("Création du dossier de la catégorie : ", nom_category)
                        os.mkdir(nom_dos_cat)

                    # Téléchargement des images
                    chem_cat_sl = nom_dos_cat + "/"
                    chem_cat = chem_cat_sl
                    name_url_img = str(title).replace(" ", "_")
                    x = ""
                    y = ""
                    z = "&é~\"#'’{([-|è`\\^à@)]=}$¤$¨^%ù*µ!§/:.;?,*€+äëüïöÿ"
                    mytable = str.maketrans(x, y, z)
                    nom_image = name_url_img.translate(mytable)
                    name_jpg = nom_image + ".jpg"
                    name_img = chem_cat + name_jpg
                    img_data = requests.get(clean_url_img).content
                    try:
                        with open(name_img, 'wb') as img_tel:
                            img_tel.write(img_data)
                        print("Image du livre ", title, "créé.")
                    except:
                        print("échec de la creation de l'image du livre ", title)