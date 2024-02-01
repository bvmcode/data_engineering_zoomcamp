--3
select count(*)
from public.yellow_taxi_data as td
where cast(lpep_pickup_datetime as date) = '2019-09-18'
and cast(lpep_dropoff_datetime as date) = '2019-09-18';

--4
SELECT lpep_pickup_datetime
FROM public.yellow_taxi_data as td
	 inner join
	 public.zones as p on p."LocationID" = td."PULocationID"
order by trip_distance desc
limit 1;

--5
SELECT p."Borough", sum(total_amount) as total_amount
FROM public.yellow_taxi_data as td
	 inner join
	 public.zones as p on p."LocationID" = td."PULocationID"
where cast(lpep_pickup_datetime as date) = '2019-09-18'
group by  p."Borough"
order by total_amount desc
limit 3;

--6
SELECT d."Zone"
FROM public.yellow_taxi_data as td
	 inner join
	 public.zones as p on p."LocationID" = td."PULocationID"
	 inner join
	 public.zones as d on d."LocationID" = td."DOLocationID"
where  p."Zone" = 'Astoria'
order by tip_amount desc
limit 1;