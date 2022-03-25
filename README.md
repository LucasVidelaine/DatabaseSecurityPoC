# DatabaseSecurityPoC

Projet réalisé dans le cadre du module de "Sécurité des bases de données", dispensé en 4ème année de formation Ingénieur Cyberdéfense à l'ENSIBS.

## Enoncé du projet

### Consigne n°1

Définissez une nouvelle base MySQL avec une table dont une colonne contenant des entiers est chiffrée à l'aide d'un algorithme préservant la relation d'ordre — aka. Order Revealing Encryption — (afin que les requêtes sur intervalles soient permises), puis donnez l'implémentation (en Python, C, ou Java) du middleware et d'une application cliente de cette base illustrant la récupération et le déchiffrement des informations de la base ainsi que le bon fonctionnement de la relation d'ordre.
Focalisez-vous sur la preuve de fonctionnement, nous n'attendons pas ici un produit fini avec parseur de requête, mais une application cliente effectuant une requête sur intervalle, vérifiant la réponse, et terminant.

### Consigne n°2

Nous souhaitons effectuer une opération à distance sur des données qui nous appartiennent, sans pour autant révéler à la machine distante le contenu de ces données. Implémentez un middleware côté serveur, capable d'effectuer une somme sur des données chiffrées par un client (le client est en mesure de déchiffrer cette somme).
Combinez les deux middlewares afin que :
- il soit possible de comparer des entiers chiffrées (cf. relation d'ordre)
- il soit possible d'additionner des entiers chiffrées

## Rapport

### Architecture choisie

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

### Chiffrement ORE - Order Revealing Encryption

L'application Middleware client est donc une preuve de concept répondant au principe de fonctionnant suivant : 
- Un utilisateur intéragit, à l'aide de la WebUI et au travers du middleware, avec la base de données (ici permettant de stocker des personnes et leurs âges au sein de la table "age").
- La base de données stocke donc le nom de la personne (varchar(30)), et son âge (int) de façon chiffrée.

!!SCHEMA LOGIQUE CLIENT!!

Nous souhaitons montrer l’implémentation d’un chiffrement de type ORE (Order Revealing Encryption) permettant l’insertion de valeurs chiffrées au sein d’une table "age" contenant des âges. Ces âges seront donc stockés chiffrés. L’avantage d’un chiffrement ORE est qu’il conserve la relation d’ordre, ainsi, le SGBD pourra parfaitement répondre à des requêtes de comparaison sur ce type de données, tout en garantissant leur confidentialité lors des requêtes.
Afin de fonctionner, l'algorithme nécessite l'usage d'un clé. Dans notre cas, et par soucis de facilité, nous avons inscrit cette clé en dur dans le code client du middleware.
D'un point de vue utilisation, l’utilisateur précise le nom ainsi que la valeur de l'âge à modifier en clair vers le middleware et ce dernier retourne la valeur chiffrée du salaire qu’il renseigne directement dans la base de données en fonction de la personne choisie. A ce stade, nous avons donc plusieurs fonctionnalités en place : 
- Afficher la table Age chiffrée
- Afficher la table Age déchiffrée
- Insérer une nouvelle personne
- Mettre à jour une personne
- Supprimer une personne
- Additionner les âges de deux personnes
- Comparer les âges de deux personnes 

!!SCREEN WEBUI!!

L’implémentation finale reprend le principe logique suivant, qui confirme le fonctionnement de la relation d’ordre lors de requêtes de comparaison :

!!SCHEMA IMPLEMENTATION!!

Voici maintenant un aperçu de l'exécution des fonctions présentent :

- Afficher la table Age chiffrée

!!SCREEN!!

- Afficher la table Age déchiffrée

!!SCREEN!!

- Insérer une nouvelle personne

!!SCREEN!!

- Mettre à jour une personne

!!SCREEN!!

- Supprimer une personne

!!SCREEN!!

- Comparer les âges de deux personnes 

!!SCREEN!!

Pour conclure cette implémentation d'algorithme ORE, nous pouvons dire qu'il permet de garantir la confidentialité des données, mais les comparaisons permettent tout de même de récupérer des informations importantes de notre table. En effet, nous pouvons connaître les relations d'ordre qui sont en vigueur dans notre jeu de données (telle personne est plus vieille que telle autre personne par exemple).
La conservation de ce genre d’informations sous cette forme n’est donc pas recommandée pour garantir pleinement la confidentialité d’une donnée. Les valeurs stockées dans la base de données ne doivent pas rendre possible ce problème d’inférence.

Le problème de ce type de chiffrement se pose sur les opérations mathématiques : il ne supporte pas les opérations mathématiques telles que l’addition et la multiplication.
Il est donc nécessaire de trouver un autre moyen d’effectuer ce genre d’opérations à travers le serveur MySQL tout en garantissant de bout en bout la confidentialité des données. Pour cela, nous allons utiliser le chiffrement homomorphique permettant ce genre d’actions.

### Chiffrement Homomorphique - Cryptosystème de Paillier

Pour cette dernière partie, nous avons décidé d'implémenter l'algorithme de chiffrement homomorphique du cryptosystème de Paillier. Le principe de cet algorithme reprend la logique de l'algorithme de cryptographie asymétrique RSA, en impliquant la génération d'une paire de clé (respectivement publique et privée).

Formule de calcul de la clé publique : *pk = N = p . q*\
Formule de calcul de la clé privée : *sk = $\varphi$ (N) = (p - 1) . (q . -1)*\
Formule de chiffrement d'un message : Soit *m* un message que l'on souhaite chiffrer avec 0 $\le$ *m* $<$ N. Soit *r*, un entier aléatoire tel que 0 $<$ *r* $<$ N (appelé aléa). Le chiffré est alors : *c = $(1 + N)^n$ . $r^N$ mod $N^2$*.\
Formule de déchiffrement d'un message : *m = $\frac{(c . r^{-N} mod N^2) - 1}{N}$*\
Le principal avantage du cryptosystème de Paillier est qu'il fait parti des modèles de chiffrement homomorphique conservant leurs capacités additives. De ce fait, à l'aide de la clé publique, nous sommes en capacité d'additionner *c1 = cipher(m1)* et *c2 = cipher(m2)* tel que *c3 = cipher(m1 + m2)* et cela sans nécessité de déchiffrer *c1* et *c2*. Nous déclinons cette relation mathématique telle que : *c1 . c2 = $(1 + N)^{m1}r_2^N mod N^2 = (1 + N)^{m1+m2}(r1 . r2)^N mod N^2$*. Ce qui correspond à un chiffré *m1 + m2* sous l'aléa *r1 . r2*.

Maintenant, concernant le middleware mis en place pour répondre à notre besoin, nous avons adapté notre middleware client afin qu'il puisse s'interfacer avec un middleware serveur. D'un point de vue fonctionnement, le chiffrement des données est réalisé par le middleware client (une nouvelle fois la paire de clé est stocké en dur dans le programme client pour plus de simplicité) puis envoyé au middleware serveur afin qu'il effectue les opérations et interactions avec le serveur MySQL. Le serveur reçoit alors des demandes de stockage, mise à jour, ou encore d'addition, qu'il traite avant de répondre au client. C'est finalement le client qui déchiffre les réponses au besoin.

!!SCHEMA LOGIQUE SERVEUR!!

L'ensemble des données seront chiffrées côté client. Le chiffrement homomorphique des données permettra au serveur d'effectuer des opérations mathématiques et également de stocker et traiter des informations vers la base de données MysQL distante.

L'environnement Docker reprend celui présenté lors du chiffrement ORE, avec maintenant une brique serveur supplémentaire. Pour cela, nous utilisons un container Python Flask où le programme *server.py* écoutera sur le port 5000.