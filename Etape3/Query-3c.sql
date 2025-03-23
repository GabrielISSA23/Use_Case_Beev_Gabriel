-- Liste des modèles vendues aux USA mais pas en France  -- 

select distinct make, model
from consumers 
where country = 'USA' and (make, model) not in ( select make, model from consumers where country ='France' )
order by make, model 