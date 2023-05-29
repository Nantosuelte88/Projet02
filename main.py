import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/the-guilty-will-robie-4_750/index.html'

reponse = requests.get(url)

if reponse.ok:
    soup = BeautifulSoup(reponse.content, 'html.parser')

#    next_element = soup.find()


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
    test_rep = url_image.replace('img alt', "")
    test_strip = test_rep.strip("<>=\"/ src" + title)

    dico_livres = {
        "product_page_url" : "En cours...",
        "upc": infos_tableau[0],
        "title": soup.h1.string,
        "price_including_tax": infos_tableau[3],
        "price_excluding_tax": infos_tableau[2],
        "number_available": infos_tableau[5],
        "product_description": description_livres[3],
        "product_category": links[3],
        "review_rating" : infos_tableau[6],
        "image_url" : test_strip
    }
    print(dico_livres)

#   Fin d'extraction