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

![SCHEMA_LOGIQUE_CLIENT](https://user-images.githubusercontent.com/26573507/160190215-cde179f9-c84a-4674-85b8-16eab4b211d6.png)

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

![WEBUI](https://user-images.githubusercontent.com/26573507/160178105-665354a4-1b55-4604-924a-707bff54049e.png)

L’implémentation finale confirme le fonctionnement de la relation d’ordre lors de requêtes de comparaison, voici un aperçu de l'exécution des fonctions présentent :

- Afficher la table Age chiffrée

![FUNCTION_1](https://user-images.githubusercontent.com/26573507/160178136-5102c92b-45c9-4333-be35-d3065d7ba1c2.png)

- Afficher la table Age déchiffrée

![FUNCTION_2](https://user-images.githubusercontent.com/26573507/160178166-6967b97a-c194-4de8-bd39-2584e4962d68.png)

- Insérer une nouvelle personne

![FUNCTION_3](https://user-images.githubusercontent.com/26573507/160178193-653c1aae-c36f-4af4-9ec4-586b38c2d259.png)

- Mettre à jour une personne

![FUNCTION_4](https://user-images.githubusercontent.com/26573507/160178214-45a17e30-220b-465d-b8c6-17298b4d412d.png)

- Supprimer une personne

![FUNCTION_5](https://user-images.githubusercontent.com/26573507/160178230-766aa7ba-c1fc-4459-b948-17fab9c9f434.png)

- Comparer les âges de deux personnes 

![FUNCTION_6](https://user-images.githubusercontent.com/26573507/160178284-a09cdbb2-ba21-4a42-80d5-da79d0490c72.png)

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

![SCHEMA_LOGIQUE_SERVEUR](https://user-images.githubusercontent.com/26573507/160190248-ab708706-7a4d-48fc-b02c-99e3ad42d7a8.png)

L'ensemble des données seront chiffrées côté client. Le chiffrement homomorphique des données permettra au serveur d'effectuer des opérations mathématiques et également de stocker et traiter des informations vers la base de données MysQL distante.

L'environnement Docker reprend celui présenté lors du chiffrement ORE, avec maintenant une brique serveur supplémentaire et une colonne supplémentaire dans la base de données. Pour cela, nous utilisons un container Python Flask où le programme *server.py* écoutera sur le port 5000.

Le chiffrement homomorphique commence par l’établissement de la paire de clés, une nouvelle fois pour faciliter la preuve de concept, nous générerons une paire de clés avec nos propres valeurs de p et q inscrites en dur dans le code de l'application.
```python
# Paire de clés pour le chiffrement homomorphique
public_key = paillier.PaillierPublicKey(2161831391)
private_key = paillier.PaillierPrivateKey(public_key, 47147,45853)
```
La librairie du cryptosystème de Paillier retourne lors de la génération de clés des objets sur lesquels des attributs et méthodes sont disponibles. C'est justement certaines de ces méthodes propres à la libraire que nous allons exploiter par la suite : *encrypt* et *decrypt*\
La première méthode est *encrypt* :
```python
ageHOM = public_key.encrypt(age)
```
Elle permet le chiffrement de l'âge en clair saisi par l'utilisateur, grâce à la clé publique. Un objet est retourné en sortie de cette méthode, et est composé de 3 attributs distincts : la *public_key*, la donnée chiffrée *ciphertext*, et un exposant *exponent*. Ces informations sont essentielles au bon fonctionnement de notre middleware serveur, et ce sont elles que nous irons stocker dans notre base de données à la fin des traitements par le middleware serveur.\
Notre middleware client doit donc transmettre ces informations au middleware serveur, nous utilisons pour cela Flask afin d'envoyer des requêtes contenants des données JSON entre les deux programmes à l'aide du réseau. 
```python
ageHOM = public_key.encrypt(age)
# Decomposition de la serie composant l'objet ageHOM
serieHOM = {'public_key': public_key.n, 'ciphertext': str(ageHOM.ciphertext()), 'exponent': ageHOM.exponent}
# Dump de la serie pour exploitation par le serveur distant
serialized = json.dumps(serieHOM)
# Envoi vers l'app serveur
payload = {'nom':str(nom), 'HOM_age':serialized}
# Envoi du payload vers l'app serveur
r = requests.post("http://"+server_host+":5000/encrypted", json=payload)
```
Il nous suffit alors de récupérer les informations qui nous intéressent dans l'objet généré par *encrypt* afin de les sérialiser au format JSON. Ainsi, nous pouvons transmettre les données à l'aide du requête POST vers le middleware serveur.\
Sur le serveur, nous récupérons la requête reçue sur la route */encrypted* prévue et avec la méthode POST attendue. Une fois cela fait, il nous suffit de transmettre les informations à une fonction permettant la mise à jour de la donnée dans la table *age*.
```python
#Page servant à l'ajout du HOM_age à la base de données
@app.route('/encrypted', methods=['POST'])
def transfertEncryptedNumber():
    print(request.is_json)
    data= request.get_json()
    print(data)
    receivedEncrypted = data.get('HOM_age')
    print(receivedEncrypted)
    updateHOMage(data.get('nom'), receivedEncrypted)
    return "JSON received & HOM updated"
```
Pour résumé, étant donné que la clé privée est stockée côté client, les données en base de données sont sécurisées. En revanche, ce type de chiffrement devient intéressant puisque la clé publique est directement stockée dans la base de données. Comme observé, par définition, l’addition homomorphique n’ayant besoin que de la clé publique pour additionner deux données chiffrées, toutes les données stockées en base peuvent être manipulées en garantissant la confidentialité du calcul.
En effet, comme nous allons le voir dans les prochaines requêtes, lors de la demande d’un calcul par le client, les requêtes viendront directement récupérer l’intégralité de l’objet requêté pour pouvoir effectuer une somme du côté du serveur. Cette fonctionnalité permet alors une protection optimale des données côté base de données car seul le middleware client, disposant de la clé privée, sera capable de déchiffrer le contenu de l’objet.

![FONCTIONNEMENT_SOMME](https://user-images.githubusercontent.com/26573507/160289495-a62bfccd-da64-420a-a6b9-875c16cfc63c.png)

