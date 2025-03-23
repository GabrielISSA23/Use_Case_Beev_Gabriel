select car.year, sum(con.sales_volume) as electric_sales, sum(con.sales_volume * car.price) as total_value
from consumers con 
join cars car on con.make = car.make and con.model = car.model and con.year = car.year
where car.engine_type = 'Electric'
group by car.year 
order by car.year