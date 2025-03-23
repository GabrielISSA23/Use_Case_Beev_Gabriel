""" Objectif : Création de deux graphiques d'analyse des données 
                disponibles sur la data base test_db 
                
                -Un graphique qui décrit le nombre de voitures 
                électriques et thermiques  vendues par an 
                
                - Un graphique qui décrit la valeur des ventes
                des voitures éléctriques et thermiques chaque année 

Penser à adapter :  les identifiants de connexion
"""

#Import des librairies
import pandas as pd 
import matplotlib.pyplot as plt 
from sqlalchemy import create_engine, text


#Identiants pour récupérer les données dans test_db 
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "test_db"

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

#Requête pour récupérer le volume et la valeur des ventes de voitures thermiques par année
thermal_query = text("""
select car.year, sum(con.sales_volume) as thermal_sales, sum(con.sales_volume * car.price) as total_value
from consumers con 
join cars car on con.make = car.make and con.model = car.model and con.year = car.year
where car.engine_type = 'Thermal'
group by car.year 
order by car.year
""")

#Requête pour récupérer le volume et la valeur des ventes de voitures électriques par année
electric_query = text("""
select car.year, sum(con.sales_volume) as electric_sales, sum(con.sales_volume * car.price) as total_value
from consumers con 
join cars car on con.make = car.make and con.model = car.model and con.year = car.year
where car.engine_type = 'Electric'
group by car.year 
order by car.year
""")

#Envoi des requêtes et récupération des données 
sales_per_year_thermal = pd.read_sql_query(thermal_query, engine)
sales_per_year_electric = pd.read_sql_query(electric_query, engine)

#-------------------------------------------------------------------------------------------------------
#                                        Graphique Volume
#-------------------------------------------------------------------------------------------------------

#Tracé du graphique de volume 
plt.figure(figsize=(12, 5))
plt.plot(sales_per_year_thermal['year'],sales_per_year_thermal['thermal_sales'])
plt.plot(sales_per_year_electric['year'],sales_per_year_electric['electric_sales'])

plt.xlabel("Année")
plt.ylabel("Volume de voiture vendu")
plt.title("Evolution du nombre de voiture électriques et thermiques vendues par année (2010 - 2022)")
plt.grid(True)

plt.show()


#-------------------------------------------------------------------------------------------------------
#                                        Graphique Valeur
#-------------------------------------------------------------------------------------------------------


#Division par 1 milliard pour lecture graphique
sales_per_year_thermal['total_value'] = sales_per_year_thermal['total_value']/1000000000
sales_per_year_electric['total_value'] = sales_per_year_electric['total_value']/1000000000

#Tracé du graphique de valeur  
plt.figure(figsize=(12, 5))
plt.plot(sales_per_year_thermal['year'],sales_per_year_thermal['total_value'])
plt.plot(sales_per_year_electric['year'],sales_per_year_electric['total_value'])

plt.xlabel("Année")
plt.ylabel("Valeur des voitures vendu (en Mds $)")
plt.title("Evolution de la valeur des voitures électriques et thermiques vendues par année (2010 - 2022)")
plt.grid(True)

plt.show()




print( "                        Les graphiques sont apparus !")
