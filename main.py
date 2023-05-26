import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/the-guilty-will-robie-4_750/index.html'

reponse = requests.get(url)

if reponse.ok:
    soup = BeautifulSoup(reponse.content, 'html.parser')

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
 #   test_rep = url_image.replace('<img alt="' + title + '" src="', "")
    test_strip = url_image.strip("<>img alt =\"/ src" + title)
    print(test_strip)

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
#        "image_url" : image_url[0]
    }
#    print(dico_livres)
 #   print(upc, " \n", price_exclud_tax, " \n", price_includ_tax, " \n", number_available, " \n", title, " \n", product_category, " \n", product_description)

""""
    upc = infos_tableau[0]
    price_exclud_tax = infos_tableau[2]
    price_includ_tax = infos_tableau[3]
    number_available = infos_tableau[5]
    title = soup.h1.string
"""
#   reste à trouver l'url du produit et l'url de l'image :
#    image_url = soup.find('div', class_="item active")
#    print(image_url)
