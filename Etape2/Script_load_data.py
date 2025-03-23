

"""
Objectif : Ce programme permet de télécharger deux fichiers csv ("car_data" et 
"consumer_data") sur la base de données test_db. 
Si le fichier existe déjà, il est mis à jour
S'il n'existe pas, il est créé. 

requirements : 
    Le fichier "create_tables.sql"  permettant la création des tables
    
Penser à adapter (si besoin): 
    les identifiants  
    les noms des bases de données 
    le codeSQL pour créer les tables      
    
""" 

#import des bibliothèques 
import pandas as pd #Pour la manipulation des données 
from sqlalchemy import create_engine, text #Pour interagir avec la base de données


#-------------------------------------------------------------------------------------------------------
#                                        Création des tables
#-------------------------------------------------------------------------------------------------------


#Identifiants pour la connexion à PostgreSQL
DB_USER = "admin" # identifiant
DB_PASSWORD = "admin" # mdp
DB_HOST = "localhost"  # ou l'IP du serveur
DB_PORT = "5432" #Port de connexion
DB_NAME = "test_db" #nom de la base de données

#Connexion à la base de données
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

#Ouverture du fichier SQL qui contient les requêtes  pour créer les tables dans la db
file = open("create_tables.sql", "r", encoding="utf-8")
sql_query = file.read()
file.close()
create_tables_query = text(sql_query) #create_tables_query = requêtes pour créer les tables 

# Connexion et envoi de la requête pour créer les 2 tables
conn = engine.connect()
conn.execute(create_tables_query)
conn.commit() #valide le changement
conn.close()

print("              Tables disponibles, connexion réussie !                 ")



#-------------------------------------------------------------------------------------------------------
#                                        Récupération des données de car_data
#-------------------------------------------------------------------------------------------------------


#Récupération du fichier csv 
cars_file = "car_data.csv"
car_data = pd.read_csv(cars_file)

#Nettoyage des données 
car_data.columns = ['make', 'model', 'year', 'price', 'engine_type'] #on donne des noms plus clairs aux colonnes
car_data.drop_duplicates(subset=['make', 'model','year'], keep='first', inplace=True) #suppression des doublons

""" Afin de pouvoir  ignorer les lignes déjà présentes dans la base de données
On crée une base de données temporaire """
#Envoi des données dans une table temporaire 
#cars = nom de la table à l'arrivée 
#engine = lien de connexion à la base 
#append = si la table existe déjà on ajoute les données 
car_data.to_sql('cars_temp', engine, if_exists='append', index=False)
#une table temporaire cars_temp a été créée


#Insertion des données de cars_temps dans cars en ignorant les données déjà présentes 

insert_query = text("""
    INSERT INTO cars (make, model, year, price, engine_type)
    SELECT make, model, year, price, engine_type FROM cars_temp
    ON CONFLICT (make, model, year) DO NOTHING;
""")

# Connexion et envoi de la requête pour créer les 2 tables
conn = engine.connect()
conn.execute(insert_query)
conn.commit() #valide le changement
conn.close()

print("              Données des voitures envoyées !                 ")



#-------------------------------------------------------------------------------------------------------
#                                        Récupération des données de consumer_data
#-------------------------------------------------------------------------------------------------------


#Récupération du fichier csv 
consumers_file = "consumer_data.csv"

"""Dans le fichier "consumer_data" la colonne 'Model' contient à la fois la 
marque et le modèle contrainrement au fichier car_data où elles sont séparées. 

Il faut donc corriger les noms des colonnes en deux. 
"""

#Nettoyage des données 
consumer_data = pd.read_csv("consumer_data.csv", header=None, names=['country', 'make', 'model', 'year', 'review_score', 'sales_volume'])
#suppresion de la première ligne avec les noms de colonnes
consumer_data= consumer_data.drop(index=0).reset_index(drop=True) 
#suppression des doublons
consumer_data.drop_duplicates(subset=['country','make', 'model','year'], keep='first', inplace=True) 
#Vérification que les colonnes ont bien le bon type 


""" Afin de pouvoir  ignorer les lignes déjà présentes dans la base de données
On crée une base de données temporaire """
#Export de la table dans la base de données
#consumers = nom de la table à l'arrivée 
#engine = lien de connexion à la base 
#append = si la table existe déjà on ajoute les données 
consumer_data.to_sql('consumers_temp', engine, if_exists='append', index=False)
#une table temporaire "consumers_temp" a été créée

#Insertion des données de consumers_temps dans consumers en ignorant les doublons
insert_query = text("""
    INSERT INTO consumers (country, make, model, year, review_score, sales_volume)
    SELECT country, make, model, CAST(year AS INTEGER), CAST(review_score as FLOAT), CAST(sales_volume as INTEGER) 
    FROM consumers_temp
    ON CONFLICT (country, make, model, year) DO NOTHING;
""")

  
    
# Connexion et envoi de la requête pour créer les 2 tables
conn = engine.connect()
conn.execute(insert_query)
conn.commit() #valide le changement
conn.close()

print("              Données des consommateurs envoyées !                 ")


#-------------------------------------------------------------------------------------------------------
#                                        Suppression des fichiers temporaires
#-------------------------------------------------------------------------------------------------------

#on supprime les tables cars_temp et consumers_temp qui sont désormais inutiles 

#requête SQL
drop_temp_tables_query = text("""
    DROP TABLE IF EXISTS cars_temp;
    DROP TABLE IF EXISTS consumers_temp;
""")

# Connexion et envoi de la requête pour créer les 2 tables
conn = engine.connect()
conn.execute(drop_temp_tables_query)
conn.commit() #valide le changement
conn.close()
  
    

"""" idées d'amélioration : 
    vérifier l'existence des fichiers csv avant de les charger
    vérifier les types des colonnes de chaque data frame avant de les envoyer à la base de données    
    """
