import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'

reponse = requests.get(url)

if reponse.ok:
    soup = BeautifulSoup(reponse.content, 'html.parser')

    #   verification bouton next
    next_element = []
    elements = soup.find_all('li', class_='next')
    for element in elements:
        a = element.find('a')
        next_elt = a['href']
        next_element.append(next_elt)
    next_rep = url.replace("index.html", "")
    next_url = next_rep + next_element[0]

#   Début d'extraction d'infos pour un livre
    bouquins = soup.find_all('article', class_='product_pod')
    url_livres = []
    i = 0
    for bouquin in bouquins:
        a = bouquin.find('a')
        url_livre = a['href']
        url_propre = url_livre.replace("../../../", "")
        url_livres.append('http://books.toscrape.com/catalogue/' + url_propre)
        i += 1
        print("Dans boucle bouquins", i)
    len_url = len(url_livres)
    j = 0
    print("len avant boucle next", len(url_livres))
    if next_url is not None:
        next_page = requests.get(next_url)
        soup = BeautifulSoup(next_page.content, 'html.parser')
        if next_page.ok:
            print("Next ok")
            bouquins = soup.find_all('article', class_='product_pod')
            for bouquin in bouquins:
                a = bouquin.find('a')
                url_livre = a['href']
                url_propre = url_livre.replace("../../../", "")
                url_livres.append('http://books.toscrape.com/catalogue/' + url_propre)
                j += 1
                print("boucle next", j)

    print("len après les boucles", len(url_livres))
    """
    for a in url_livres:
        page = requests.get(a)
        soup = BeautifulSoup(page.content, 'html.parser')
        if page.ok:
            title = soup.h1.string
            print(title)

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

            images = soup.find_all("img")
            image_url = []
            for image in images:
                image_url.append(image)
            url_image = str(image_url[0])
            test_rep = url_image.replace('img alt', "")
            test_strip = test_rep.strip("<>=\"/ src" + title)

            dico_livres = {
                "product_page_url": page,
                "upc": infos_tableau[0],
                "title": soup.h1.string,
                "price_including_tax": infos_tableau[3],
                "price_excluding_tax": infos_tableau[2],
                "number_available": infos_tableau[5],
                "product_description": description_livres[3],
                "product_category": links[3],
                "review_rating": infos_tableau[6],
                "image_url": test_strip
            }
            print(dico_livres)
"""
            #   Fin d'extraction du livre
