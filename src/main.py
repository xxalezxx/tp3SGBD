from unittest import result
import psycopg2
import psycopg2.extras

hostname = 'localhost'
database ='postgresDB'
username = 'admin'
pwd = 'admin'
portId = '5455'

#Puntos de ejercicios!


def punto1():
    cursor.execute("SELECT code, population FROM country WHERE code = \'ARG\'")
    for item in cursor.fetchall():
        print("1) La cantidad de personas hasta la fecha son: ",format(item['population']))
    
def punto2():
    cursor.execute("SELECT DISTINCT continent FROM country")
    continents = ""
    for item in cursor.fetchall():
        continents = continents + " " +  item['continent']

    print("2) Los continentes registrados en la BD: ",format(continents))

def punto3():
    cursor.execute("""SELECT name, continent, population 
	FROM country 
	WHERE 
	continent = 'South America' 
	and population >= 15000;""")
    
    results = ""
    for item in cursor.fetchall():
        results = results + item['name'] + " con una cantidad de " + str(item['population']) + "\n"
        
    print("3) Resultado de paises con mas de 15.000 habitantes: \n",format(results))

def punto4():
    cursor.execute("""
    SELECT name, gnp 
	FROM country 
	ORDER BY gnp DESC
	LIMIT 10
    """)
    results = ""
    for item in cursor.fetchall():
        results = results + item['name'] + ' | ' + str(item['gnp']) + "\n"
    print("4) TOP 10 paises con mejor GNP: \n", format(results))
    
def punto5():
    cursor.execute("""
    SELECT governmentform, COUNT(*) cantidad
	FROM country
	GROUP BY governmentform
	ORDER BY cantidad DESC
    """)
    results = ""
    for item in cursor.fetchall():
        results = results + item['governmentform'] + " => " + str(item['cantidad']) +"\n"
    print("5) La cantidad de paises bajo regimen son:\n",format(results))
    
def punto6():
    cursor.execute("""
    SELECT continent, SUM(surfacearea) as area
	FROM country
	GROUP BY continent""")
    results = ""
    for item in cursor.fetchall():
        results = results + item["continent"] + " " + str(item['area']) + "\n"
    print("6) Tabla de area total de cada contienente segun BD:\n",format(results))

def punto7a():
    cursor.execute("""
    SELECT continent, COUNT(continent) 
	FROM country
	GROUP BY continent
	HAVING COUNT(continent)  >=15
	ORDER BY continent ASC
    """)
    results = ""
    for item in cursor.fetchall():
        results = results + item['continent'] + " total paises en el " + str(item['count']) + " paises" + '\n'
    print("7a) Continentes con mas de 15 paises en el segun BD: \n",format(results))
    
    
def puntoS2a():
    cursor.execute("""
        SELECT MAX(lifeexpectancy) as lifeexpectancy, name 
        FROM country 
        GROUP BY name 
        ORDER BY lifeexpectancy DESC 
        LIMIT 1
        """)
    results = cursor.fetchall()
    resultName = results[0]['name']
    resultValue = str(results[0]['lifeexpectancy'])
    print("S2a) el pais con mayor expectativa de vida es ",format(resultName))
    print("con un valor de", format(resultValue))

def puntoS2b():
    cursor.execute("""
        SELECT MIN(lifeexpectancy) as lifeexpectancy, name 
	    FROM country 
	    WHERE lifeexpectancy != -1 
	    GROUP BY name 
	    ORDER BY lifeexpectancy ASC 
	    LIMIT 1;
        """)
    results = cursor.fetchall()
    resultName = results[0]['name']
    resultValue = str(results[0]['lifeexpectancy'])
    print("S2b) el pais con menor expectativa de vida es ",format(resultName))
    print("con un valor de", format(resultValue))


def puntoS3():
    cursor.execute("""
        SELECT c.name, c.indepyear, c.continent 
        FROM country as c,
        (	
            SELECT continent 
	        FROM country 
	        GROUP BY continent, indepyear 
	        ORDER BY indepyear,continent ASC 
	        LIMIT 1) firstContinent
        WHERE c.continent = firstContinent.continent and c.indepyear != -1 
        ORDER BY c.indepyear
        """)
    results = ""
    
    dbResults = cursor.fetchall()
    for item in dbResults:
        results = results + item['name'] + " Anio Ind:  " + str(item['indepyear']) + "\n"
    print("S3) El contienente con el primer pais independiente es", format(dbResults[0]['continent']))
    print("lista de paises del continente con el primer pais independiente \n",format(results))
    
    
    
def puntoJ1():
    cursor.execute("""
        SELECT c.name AS country, l.language AS lenguage
        FROM country AS c 
        INNER JOIN countrylanguage AS l
        ON 	c.code = l.countryCode
        WHERE c.continent = 'Asia'
        """)
    dbResults = cursor.fetchall()
    
    results = ""
    for item in dbResults:
        results = results + item['country'] + "el idioma es " + item['lenguage'] + "\n"
        
    print("J1) Lista idiomas en continente asiatico\n",format(results))

def puntoJ2():
    cursor.execute("""
        SELECT COUNT(DISTINCT language) qty, name AS country 
        FROM (
            SELECT * FROM country INNER JOIN countrylanguage 
            ON country.code = countrylanguage.countrycode
            ) languageInner
        WHERE code = countrycode
        GROUP BY name
        HAVING COUNT(DISTINCT language) >= 2
        ORDER BY qty DESC
        """)
    dbResults = cursor.fetchall()
    results = ""
    for item in dbResults:
        results = results + item['country'] + " con una cantidad de idiomas " + str(item['qty']) + "\n"
    print("J2) La lista de paises con mas de 2 idiomas son: ", format(results))
    
def puntoJ3():
    cursor.execute("""
        SELECT DISTINCT language 
        FROM (
            SELECT DISTINCT code 
            FROM (
                SELECT SUM(gnp) gnpTotal, continent 
                FROM (
	                SELECT * 
	                FROM (
		                SELECT * 
		                FROM country 
		                INNER JOIN countrylanguage 
		                ON country.code = countrylanguage.countrycode
		            ) languageInner
	                WHERE 
		                code = countrycode 
	                AND 
		                continent != 'Antartic'
	                ) t 
                GROUP BY continent 
                ORDER BY SUM(gnp) ASC
                LIMIT 1) finalTable 
                INNER JOIN country 
                ON finalTable.continent = country.continent 
                ) ft
        INNER JOIN countrylanguage 
        ON ft.code = countrylanguage.countrycode
        """)
    dbResults = cursor.fetchall()
    results = ""
    
    for item in dbResults:
        results = results + item['language'] + "\n"
        
    print("J3) El continente mas pobre es Oceania donde se habla los sigiente idiomas \n",format(results))

def puntoJ4():

    cursor.execute("""
        SELECT country, (populationPartial * 100) / populationTotal as percentage 
        FROM
        (
            SELECT tablaTotal.country, populationPartial, populationTotal 
            FROM 
	        (
		        SELECT population as populationTotal, name AS country 
                FROM country ORDER BY population DESC

	        ) tablaTotal
	        INNER JOIN 
		    (
		        SELECT population as populationPartial, name AS country
		        FROM (
			        SELECT SUM(city.population) as population, country.code, country.name FROM city INNER JOIN country ON city.countrycode = country.code GROUP BY country.code, 	country.name
	                ) finaltable
                ORDER BY population DESC
		    ) tablaParcial 
            ON tablaTotal.country = tablaParcial.country
            ORDER BY populationTotal DESC) totalTable
            ORDER BY percentage DESC
        """)
    
    dbResults = cursor.fetchall()
    
    results = ""

    for item in dbResults:       
        results = results + item['country'] + " => " + str(item['percentage']) + "%\n" 
        
    print("J4) % en poblacion de cada pais: \n", format(results))
    
    
    
try:
    connDb = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = portId
    )
    
    cursor = connDb.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #1)
    punto1()
    #2)
    punto2()
    #3)
    punto3()
    #4)
    punto4()    
    #5)
    punto5()
    #6)
    punto6()
    #7)
    punto7a()
    #Subqueries
    #s2)
    puntoS2a()
    puntoS2b()
    #s3)
    puntoS3()
    #J1)
    puntoJ1()
    #J2
    puntoJ2()
    #J3
    puntoJ3()
    #J4
    puntoJ4()
    #punto 3 ejercicio
    """

ALTER TABLE country ADD CONSTRAINT pkCode PRIMARY KEY (code);

CREATE TABLE IF NOT EXISTS stats (
	countrycode char(3) PRIMARY KEY,
	cant_lenguas int not null,
	pop_urbana int,
	CONSTRAINT fkCc FOREIGN KEY (countrycode) REFERENCES country(code)
);


INSERT INTO stats 
	(SELECT c.code AS codigoPais, count(c2.countrycode) AS cantLenguas 
	FROM country c 
	INNER JOIN countrylanguage c2 
	ON c.code = c2.countrycode 
	GROUP BY c.code 
	ORDER BY c.code);


UPDATE stats SET pop_urbana = tablaFinal.poblacion 
FROM (
	SELECT c.code, sum(c2.population) AS poblacion 
	FROM city c2, country c 
	WHERE c.code = c2.countrycode 
	GROUP BY c.code 
	ORDER BY c.code) AS tablaFinal 
WHERE stats.countrycode = tablaFinal.code;


select * from stats;

    """
    
    
    
    #punto 4 ejercicio
    
    """CREATE TABLE IF NOT EXISTS sitio (
	id int primary key, 
	entidad varchar not null, 
	tipo_entidad varchar not null, 
	pais varchar not null, 
	countrycode char(3) not null,
	CONSTRAINT fkCc FOREIGN KEY (countrycode) REFERENCES country(code)
);
"""

    
    connDb.commit()
    
    cursor.close()
    connDb.close()
except Exception as error:
    print(error)
    
    