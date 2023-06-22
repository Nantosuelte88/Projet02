import csv
import requests
from bs4 import BeautifulSoup
import os

url = 'https://books.toscrape.com/'

reponse = requests.get(url)

if reponse.ok:
    soup = BeautifulSoup(reponse.content, 'html.parser')

    # Si le dossier "images" n'éxiste pas nous le créons
    if not os.path.exists("images"):
        os.mkdir("images")
    # Enregistrement des urls de categories
    url_category = []
    ulcat = soup.find('ul', class_='nav')
    acat = ulcat.find_all('a')
    url_cat_next = []
    # Pour chaque balise a nous extrayons le href puis l'ajoutons à la liste url_category
    for a in acat:
        lk = a['href']
        urlcatcln = url + lk
        url_category.append(urlcatcln)

    # Suppression de la premiere information récoltée (ici la page index.html)
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

                # Si la page contient 20 livres ou plus nous cherchons la presence d'un bouton next
                if (len(bouquins)) >= 20:
                    # Recherche de bouton next
                    elements = soup.find('li', class_='next')
                    # Si le bouton next existe nous extrayons le href puis le concatenons dans l'url de la page, en prenant soin d'enlever le index.html
                    if elements:
                        next_rep = url_cat_next.replace("index.html", "")
                        url_elm = elements.find("a")
                        link_next = url_elm['href']
                        next_url = next_rep + link_next
                        # Nous allons dans la page next
                        pagenext = requests.get(next_url)
                        soup = BeautifulSoup(pagenext.content, 'html.parser')
                # Fin de la boucle
                else:
                    break

            # Pour chaque url de livre nous allons dans la page pour recupèrer les infos de celui ci
            for urlb in url_livres:
                page = requests.get(urlb)
                soup = BeautifulSoup(page.content, 'html.parser')

                if page.ok:
                    # Début d'extraction d'infos pour un livre
                    title = soup.h1.string

                    infos_tableau = []
                    tds = soup.find_all('td')
                    for td in tds:
                        infos_tableau.append(td.string)

                    # Extraction de la description du livre
                    descriptions = soup.find_all('p')
                    description_livres = []
                    for description in descriptions:
                        description_livres.append(description.string)
                    product_description = description_livres[3]

                    # Extraction du nom de la categorie
                    categories = soup.find_all('a')
                    links = []
                    for categorie in categories:
                        links.append(categorie.string)
                    product_category = links[3]

                    # Extraction de la balise href des images, nettoyage des urls, concatenation pour avoir une url valide
                    images = soup.find_all("img")
                    image_url = []
                    for image in images:
                        image_url.append(image)
                    url_image = str(image_url[0])
                    url_img = url_image[-63:-3]
                    img_rep = url_img.replace("../../", "")
                    clean_url_img = "http://books.toscrape.com/" + img_rep

                    # Nettoyage de certaines informations de livres
                    clean_price_icl = infos_tableau[3].strip("€$£")
                    clean_price_excl = infos_tableau[2].strip("€$£")
                    clean_numb_av = infos_tableau[5].strip("In stock() available hors stock")

                    # Engistrement des informations récupérées dans un dictionnaire
                    dico_livres = {
                        "product_page_url": urlb,
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
                    liste_dico.append(dico_livres)
                    print("Livre n°", len(liste_dico), "ajouté à la liste ")

                    # Creation des dossiers
                    nom_cat_rep = nom_category.replace(" ", "_")
                    nom_dos_cat = "images/" + nom_cat_rep
                    # Si le dossier n'existe pas, il est créé
                    if not os.path.exists(nom_dos_cat):
                        print("Création du dossier de la catégorie  ", nom_category)
                        os.mkdir(nom_dos_cat)

                    # Téléchargement des images, mise en place du chemin de dossier
                    chem_cat_sl = nom_dos_cat + "/"
                    chem_cat = chem_cat_sl
                    name_url_img = str(title).replace(" ", "_")
                    # Vefication et effacement des caracteres speciaux si besoin, pour avoir un nom valide pour les images
                    x = ""
                    y = ""
                    z = "&é~\"#'’{([-|è`\\^à@)]=}$¤$¨^%ù*µ!§/:.;?,*€+äëüïöÿ“á”"
                    mytable = str.maketrans(x, y, z)
                    nom_image = name_url_img.translate(mytable)
                    name_jpg = nom_image + ".jpg"
                    name_img = chem_cat + name_jpg
                    img_data = requests.get(clean_url_img).content
                    try:
                        with open(name_img, 'wb') as img_tel:
                            img_tel.write(img_data)
                        print("Image du livre", title, "créé.")
                    except:
                        print("échec de la creation de l'image du livre ", title)

            # Creation des fichiers CSV, initialisation des noms d'en-tetes
            en_tetes = ["product_page_url", "upc", "title", "price_including_tax",
                        "price_excluding_tax",
                        "number_available", "product_description", "product_category", "review_rating",
                        "image_url"]
            nom_csv_rep = str(links[3]) + ".csv"
            nom_csv = nom_csv_rep.replace(" ", "_")

            try:
                with open(nom_csv, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=en_tetes)
                    writer.writeheader()
                    writer.writerows(liste_dico)
                    print("\nCréation du CSV de la catégorie :", nom_csv_rep.replace(".csv", ""), ". Nombre de livre.s traité.s :", len(liste_dico), "\n\n")
            except:
                print("échec de la creation du csv")
