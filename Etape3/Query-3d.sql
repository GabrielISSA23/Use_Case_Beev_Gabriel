-- average car cost in every country by engine type -- 

select con.country, car.engine_type, avg(car.price) as average_price
from consumers con
join cars car
  on con.make = car.make and con.model = car.model and con.year = car.year
group by con.country, car.engine_type
order by con.country, car.engine_type;