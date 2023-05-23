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

    upc = infos_tableau[0]
    price_exclud_tax = infos_tableau[2]
    price_includ_tax = infos_tableau[3]
    number_available = infos_tableau[5]
    title = soup.h1.string

#   reste à trouver l'url du produit et l'url de l'image :
#    image_url = soup.find('div', class_="item active")
#    print(image_url)

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

    print(upc, price_exclud_tax, price_includ_tax, number_available, title, product_category)