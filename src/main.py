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
    
    connDb.commit()
    
    cursor.close()
    connDb.close()
except Exception as error:
    print(error)
    
    