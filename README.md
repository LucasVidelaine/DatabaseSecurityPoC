# DatabaseSecurityPoC

Projet réalisé dans le cadre du module de "Sécurité des bases de données", dispensé en 4ème année de formation Ingénieur Cyberdéfense à l'ENSIBS.

## Contexte

Définissez une nouvelle base mysql avec une table dont une colonne contenant des entiers est chiffrée à l'aide d'un algorithme préservant la relation d'ordre — aka. Order Revealing Encryption — (afin que les requêtes sur intervalles soient permises), puis donnez l'implémentation (en python, c, ou java) du middleware et d'une application cliente de cette base illustrant la récupération et le déchiffrement des informations de la base ainsi que le bon fonctionnement de la relation d'ordre.

Focalisez-vous sur la preuve de fonctionnement, on n'attend pas ici un produit fini avec parseur de requête, une application cliente effectuant une requête sur intervalle, vérifiant la réponse, et terminant, est suffisant.

### Explications

Notre architecture est une nouvelle fois basée sur Docker. Elle est composée d'un serveur MySQL, d'un container exécutant le Middleware client, et d'un container exécutant le Middleware serveur.
Voici le fichier docker-compose.yml qui permet de démarrer les services.

```yaml
version: '3'

services:
    db:
      image: mysql:latest
      environment:
        MYSQL_DATABASE: 'TP2022_VIDELAINE-LUBISHTANI-BIZET'
        MYSQL_USER: 'lulutoto'
        MYSQL_PASSWORD: 'Ensibs2022!'
        MYSQL_ROOT_PASSWORD: 'Ensibs2022!'
      ports:
        - '3306:3306'
      volumes:
        - ./db:/var/lib/mysql

    server:
      build:
        context: .
        dockerfile: Dockerfile-server
      ports:
        - 5000:5000
      volumes:
        - ./app-server:/app
      links:
        - db
      tty: true
      command: bash -c "python server.py"
    
    client:
      build:
        context: .
        dockerfile: Dockerfile-client
      ports:
        - 8000:8000
      volumes:
        - ./app-client:/app
      links:
        - db
        - server
      tty: true
      command: bash -c "python client.py"
```
Commande à exécuter pour démarrer les applications : 

```
sudo docker-compose up --build
```

Commande à exécuter pour stopper les applications : 

```
sudo docker-compose down
```

*Bon à savoir : Pour s'assurer du bon fonctionnement du Docker-compose, il est conseillé de remplacer les chemins relatifs des volumes par les chemins absolus en rapport avec votre environnement d'exécution.*

**URL de l'interface web :** http://localhost:8000 

Nos Middlewares sont entièrements développés en Python, avec le framework Flask afin de pouvoir fonctionner comme une sorte d'API simplifié, et desservant un interface web utilisateur "WebUI". *L'ensemble des applications sont fonctionnelles, mais le code n'est pas optimal et gagnerait à être largement renforcé, faute de temps.*

L'application Middleware client est donc une preuve de concept répondant au principe de fonctionnant suivant : 
- Un utilisateur intéragit, à l'aide de la WebUI et au travers du middleware, avec la base de données (ici permettant de stocker des personnes et leurs âges au sein de la table "age").
- La base de données stocke donc le nom de la personne (varchar(30)), et son âge (int) de façon chiffrée.

Nous souhaitons montrer l’implémentation d’un chiffrement de type ORE (Order Revealing Encryption) permettant l’insertion de valeurs chiffrées au sein d’une table "age" contenant des âges. Ces âges seront donc stockés chiffrés. L’avantage d’un chiffrement ORE est qu’il conserve la relation d’ordre, ainsi, le SGBD pourra parfaitement répondre à des requêtes de comparaison sur ce type de données, tout en garantissant leur confidentialité lors des requêtes.
Afin de fonctionner, l'algorithme nécessite l'usage d'un clé. Dans notre cas, et par soucis de facilité, nous avons inscrit cette clé en dur dans le code client du middleware.
D'un point de vue utilisation, l’utilisateur précise le nom ainsi que la valeur de l'âge à modifier en clair vers le middleware et ce dernier retourne la valeur chiffrée du salaire qu’il renseigne directement dans la base de données en fonction de la personne choisie. A ce stade, nous avons donc plusieurs fonctionnalités en place : 
-  Afficher la table Age chiffrée
- Afficher la table Age déchiffrée
- Insérer une nouvelle personne
- Mettre à jour une personne
- Supprimer une personne
- Comparer les âges de deux personnes 



## Question 31 (Bis)

On souhaite effectuer une opération à distance sur des données qui nous appartiennent, sans pour autant révéler à la machine distante le contenu de ces données. Implémentez un middleware côté serveur, capable d'effectuer une somme sur des données chiffrées par un client (le client est en mesure de déchiffrer cette somme).
Combinez les deux middlewares afin que :
- il soit possible de comparer des entiers chiffrées (cf. relation d'ordre)
- il soit possible d'additionner des entiers chiffrées

### Requêtes

### Réponses du SGBD

### Explications
