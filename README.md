# LogReport - Internal Log Reporting Tool

logreport is an internal reporting tool to produce computed statistics from the news database on what readers like to read and a summary of errors encountered by users. 

The report produced includes the following three key result sets from the data in the news website servers logs:

* The Three Most Popular Articles of all time
* Author Popularity - ranked from most popular to least popular
* Website Error Statistics - days exceeding 1% errors

## Installation

Create the required views in the news database, byt executing the SQL below
```create or replace view v_ArticleViewStats as
select	a.title, count(l.id) view_count 
from articles a, log l 
where l.path = '/article/' || a.slug 
 and l.status = '200 OK' 
group by a.title 
order by view_count desc;

create or replace view v_ErrorStats as
select 	s.varDay as log_date, to_char(((e.varCount::float / (s.VarCount::float + e.varCount::float))*100::float), '0D00%') as error_ratio
from 	(select date_trunc('day', "time") varDay, count(*) varCount from log where status = '200 OK' group by date_trunc('day', "time")) s,
		(select	date_trunc('day', "time") varDay, count(*) varCount from log where status <> '200 OK' group by date_trunc('day', "time")) e 
where 	s.varDay = e.varDay and 
		((e.varCount::float / (s.VarCount::float + e.varCount::float))*100::float) >= 1.0
order by error_ratio desc;

create or replace view v_authorviewstats as
select	u."name", count(l.id) view_count
from	authors u, articles a, log l
where	l.path = '/article/' || a.slug
and 	l.status = '200 OK'
and 	u.id = a.author
group by u."name"
order by view_count desc ;
```

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install psycopg2 - the Postgres DB library.

```bash
pip install psycopg2
```

## Usage

```
$ python3 logreport.py
```

## Example Output
```
1. Three Most Popular Articles of all time

	* Candidate is jerk, alleges rival - 1234 views
	* Bears love berries, alleges bear - 567 views
	* Bad things gone, say good people - 89 views


2. Author Popularity - ranked from most popular to least popular

	* Ursula La Multa - 1234 views
	* Rudolf von Treppenwitz - 567 views
	* Anonymous Contributor - 89 views
	* Markoff Chaney - 12 views


3. Website Error Statistics - days exceeding 1% errors

	* January 01, 2000 -  1.23% error rate
```

## License
[MIT](https://choosealicense.com/licenses/mit/)