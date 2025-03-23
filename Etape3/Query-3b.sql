-- Les pays avec le plus de vente pour chaque modèle et combien il y en a -- 

with model_sales_per_country as ( -- requête de la question 4a
    select country, make, model, SUM(sales_volume) as total_sales
    from consumers
    group by  country, make, model
)
select make, model, country, total_sales
from model_sales_per_country
where (make, model, total_sales) in (
    select make, model, MAX(total_sales)
    from model_sales_per_country
    group by make, model
)
order by make, model;