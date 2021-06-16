"""
Miguel Rivera miguel.rivera3@utp.ac.pa
Nabil Hernandez nabil.hernandez@utp.ac.pa
Samuel Valdelamar samuel.valdelamar@utp.ac.pa
Mark Tack marck.tack@utp.ac.pa
"""
from connect import connect
from tabulate import tabulate
import pandas as pd
#Conexion a la Base de Datos
conn=connect()
cur = conn.cursor()

#Importando Archivos
departamento = pd.read_csv("departamento.txt", sep=",")
informacion = pd.read_csv("informacion.txt", sep=",")

#Exportamos archivos as csv
departamento.to_csv('departamaento.csv', sep=',',index=False)
informacion.to_csv('informacion.csv', sep=',',index=False)

#Creando Tablas
query ='''CREATE TABLE IF NOT EXISTS informacion(
   ID INT,
   NOMBRE VARCHAR(50),
   EDAD INT,
   DIRECCION VARCHAR(50),
   SALARIO INT,
   PRIMARY KEY(ID) 
);
CREATE TABLE IF NOT EXISTS departamento(
   ID INT,
   DEP VARCHAR(50),
   EMP_ID INT,
   PRIMARY KEY(ID),
   FOREIGN KEY(EMP_ID) REFERENCES informacion(ID)
);
   '''
cur.execute(query)
print("Tablas creada exitosamente")
conn.commit()

#Insertando los Datos en las tablas
with open('informacion.csv','r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f,'informacion', sep=',')
print("Datos Insertados Correctamente")
conn.commit()
with open('departamaento.csv','r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f,'departamento', sep=',')
print("Datos Insertados Correctamente")
conn.commit()
#Realizando las Consultas
#Primera Consulta
print('Todos los salarios que son menos	de 20.000')
cur.execute("SELECT * FROM informacion WHERE salario < 20000")
query = cur.fetchall()
print(tabulate(query, headers=['ID', 'Nombre', 'Edad', 'Direccion', 'Salario'], tablefmt='psql'))
#Segunda Consulta
print('Todos	los	nombres	en	MAYÚSCULAS	a	través	de	SQL	')
cur.execute("SELECT UPPER(nombre) FROM informacion")
query = cur.fetchall()
print(tabulate(query, headers=['Nombre'], tablefmt='psql'))
#Tercera Consulta
print('La	edad	promedio	de	los	empleados')
cur.execute("SELECT AVG(edad) FROM informacion")
query = cur.fetchall()
print(tabulate(query, headers=['AVG'], tablefmt='psql'))
#Cuarta Consulta
print(' Realice	un	JOIN	entre	las	tablas	en	el	campo	employee_id y	id')
cur.execute("SELECT * FROM informacion INNER JOIN departamento ON informacion.id=departamento.emp_id")
query = cur.fetchall()
print(tabulate(query, headers=['ID', 'Nombre', 'Edad', 'Direccion', 'Salario','ID','Departamento','ID Empleado'], tablefmt='psql'))
#Quinta Consulta
print(' Realice	un	CROSS	JOIN	ambas	tablas')
print('Informacion x Departamento')
cur.execute("SELECT * FROM informacion CROSS JOIN departamento")
query = cur.fetchall()
print(tabulate(query, headers=['ID', 'Nombre', 'Edad', 'Direccion', 'Salario','ID','Departamento','ID Empleado'], tablefmt='psql'))
print('Departamento x Informacion')
cur.execute("SELECT * FROM departamento CROSS JOIN informacion")
query = cur.fetchall()
print(tabulate(query, headers=['ID','Departamento','ID Empleado','ID', 'Nombre', 'Edad', 'Direccion', 'Salario'], tablefmt='psql'))
#Sexta Consulta
print(' Realice un	LEFT	OUTER	JOIN	ambas	tablas')
print('Informacion x Departamento')
cur.execute("SELECT * FROM informacion LEFT OUTER JOIN departamento ON informacion.id=departamento.emp_id")
query = cur.fetchall()
print(tabulate(query, headers=['ID', 'Nombre', 'Edad', 'Direccion', 'Salario','ID','Departamento','ID Empleado'], tablefmt='psql'))
print('Departamento x Informacion')
cur.execute("SELECT * FROM departamento LEFT OUTER JOIN informacion ON departamento.emp_id=informacion.id")
query = cur.fetchall()
print(tabulate(query, headers=['ID','Departamento','ID Empleado','ID', 'Nombre', 'Edad', 'Direccion', 'Salario'], tablefmt='psql'))
#Cerrando Conexion
cur.close()
conn.commit()
conn.close()
print('Database connection closed.')
