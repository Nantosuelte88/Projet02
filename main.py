import csv
import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

reponse = requests.get(url)
d = 1
n = 1

if reponse.ok:
    soup = BeautifulSoup(reponse.content, 'html.parser')

    url_livres = []
    liste_dico = []
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

            #recherche de bouton next
            elements = soup.find('li', class_='next')
            print("PRINT elements PAGE ACCUEIL = ", elements)
            if elements:
                n += 1
                next_rep = url.replace("index.html", "")
                url_elm = elements.find("a")
                link_next = url_elm['href']
                next_url = next_rep + link_next
                print("Bouton next ok", next_url, "LEN url_livres dans boucle next", len(url_livres))
                # aller dans la page next
                page = requests.get(next_url)
                soup = BeautifulSoup(page.content, 'html.parser')

        else:
            print("PAS DE NEXT", len(url_livres))

            break

    for a in url_livres:
        page = requests.get(a)
        soup = BeautifulSoup(page.content, 'html.parser')
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
#            test_rep = url_image.replace('img alt', "")
 #           test_strip = test_rep.strip("<>=\"/ src &amp ;," + title)
            img_rep = url_img.replace("../../", "")

            clean_url_img = "http://books.toscrape.com/" + img_rep
 #           print(clean_url_img, url_image)

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
            # telecharger l'image
            name_url_img = url_image[-39:-3]
            name_img = name_url_img
            img_data = requests.get(clean_url_img).content
            with open(name_img, 'wb') as img_tel:
                img_tel.write(img_data)

    """            
                for it in dico_livres.fromkeys('title'):
                    liste_dico.append(it)
                    print(it)
                print("liste dico = ", liste_dico)
    
    
    
    
                en_tetes = ["product_page_url", "upc", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "product_category", "review_rating", "image_url"]
    
                with open('test.csv', 'w', encoding='utf-8') as fichier_csv:
                    writer = csv.DictWriter(fichier_csv, fieldnames=en_tetes)
                    writer.writeheader()
                    writer.writerows(liste_dico.fromkeys())
    """