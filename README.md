# Projet02
Hello !

Voici un petit script nous permettant de faire un scrap sur le site [Books to Scrape](http://books.toscrape.com/)

Pour exécuter ce code correctement merci de suivre ces quelques petites instructions :

- Cloner ce git
- Depuis le terminal : **python --version**

Si la version de Python est < 3.3, merci d'installer la dernière version

Depuis le terminal :
- pour créer l'environnement :
	+ **python -m venv env**
- pour l'activer :
	- Sur Unix et MacOS : 
		+ **source env/bon/activate**
	 - Sur Windows (Attention! pas de ".bat" sous Powershell) :		
		+ **env\Scripts\activate.bat**

Maintenant que l'environnement virtuel est crée et activé nous pouvons installer les packages requis:
- **pip install -r requirements.txt**

Pour executer le code :

- **python main.py**

Lorsque que le programme s'exécutera vous pourrez voir des messages indiquant le nombre de livres traités, le titre du livre quand l'image s'enregistre, ainsi que le nom de la catégorie et le nombre de livres enregistrés dans le CSV :smile:
