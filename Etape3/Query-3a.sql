-- Nombre de voitures vendues par modèle par pays -- 

select country,make,model, SUM(sales_volume) as total_sales 
from consumers 
group by country, make, model
order by country