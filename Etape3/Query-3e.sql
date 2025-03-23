-- notation moyenne par les consommateurs  des voitures électriques et thermiques -- 

select car.engine_type, avg(con.review_score) as avg_rate
from consumers con
join cars car on con.make = car.make and con.model = car.model and con.year = car.year 
group by car.engine_type 

