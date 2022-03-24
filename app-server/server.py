import math
from flask import Flask, json, request, jsonify, make_response
import mysql.connector, sys
from mysql.connector import errorcode
from pyope.ope import OPE
import phe.encoding
from phe import paillier
import json
import requests

#Fonctions globales

#Connexion à la bdd
def db_connexion(user,pas,host,db):
    cnx = mysql.connector.connect(user=user, password=pas, host=host, database=db, autocommit=True)
    return cnx

#Fermeture de connexion à la bdd
def db_close(cnx):
    cnx.close()

#Fonction de mise à jour du ageHOM (ajout des attributs de l'objet chiffré) d'une personne
def updateHOMage(nom, HOM_age):
    connec = db_connexion(db_user,db_password,db_host,db_db)
    cur = connec.cursor()
    query = "UPDATE age SET HOM_age=(%s) WHERE nom=(%s)"
    cur.execute(query, (HOM_age, nom))
    cur.close
    db_close(connec)

#Fonction de calcul de la somme des HOM_age entre deux personnes
def calculsomme(nom1, nom2):
    connec = db_connexion(db_user,db_password,db_host,db_db)
    cur = connec.cursor()
    query = "SELECT HOM_age FROM age WHERE nom=(%s) OR nom=(%s)"
    cur.execute(query, (nom1, nom2))

    somme = 0
    for HOM_age in cur:
        #Chargement des attributs dans une variables
        recuperationHOM = json.loads(HOM_age[0])
        #Recuperation de la clé publique
        n = recuperationHOM['public_key']
        public_key = paillier.PaillierPublicKey(n=int(n))
        #Regénération de l'objet chiffré
        age = paillier.EncryptedNumber(public_key, int(recuperationHOM['ciphertext']), int(recuperationHOM['exponent']))
        #Somme des ages
        somme += age  
    cur.close
    db_close(connec)

    #Sérialisation de la somme
    serieSomme = {
        'public_key': public_key.n,
        'ciphertext': str(somme.ciphertext()),
        'exponent': somme.exponent
    }

    return serieSomme

#Définition des variables globales
db_user = 'lulutoto'
db_password = 'Ensibs2022!'
db_host = 'db'
db_db = 'TP2022_VIDELAINE-LUBISHTANI-BIZET'
app = Flask(__name__)

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

#Page servant au calcul de la somme
@app.route('/sumPost', methods=['GET', 'POST'])
def traitementSomme():
    #Récupération du contenu posté par le client
    data= request.get_json()
    nom1 = data.get('nom1')
    nom2 = data.get('nom2')
    #Calcul de la somme
    seriesomme = calculsomme(nom1,nom2)
    return seriesomme

#Listener constant
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

