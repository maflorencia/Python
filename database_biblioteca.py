#!/usr/bin/env python
# -*- coding: utf-8 -*
import mariadb
from tqdm import tqdm
import time
# -----♦ Funcion para conectar al administrador ♦--------
def conectar_admin():
    mydb = mariadb.connect(
                 host =  "127.0.0.1",
                 user = "root",
                 autocommit = True
                 )
    return mydb
# ---------♦ Funcion para crear la base de datos BIBLIOTECA ♦----------
def crear_base(mydb):
    valido = 0
    while valido == 0:
        try:
            mycursor = mydb.cursor()
            mycursor.execute("CREATE DATABASE IF NOT EXISTS BIBLIOTECA")
            mycursor = mydb.cursor()
            mycursor.execute("SHOW DATABASES")
        except mariadb.ProgrammingError:
            print('Error. Database ya existe')
        else:
            valido = 1
# -----♦ Función para generar la conexión al database BIBLIOTECA ♦--------------
def connect_base():
    valido = 0
    while valido == 0:
        try:
            mydb = mariadb.connect(host = "127.0.0.1",
                       user ="root",
                       database = "BIBLIOTECA")
        except mariadb.ProgrammingError:
            print('Error. Database inexistente')
        else:
            mycursor=mydb.cursor()
            valido = 1
    return mydb
# ------ Función para generar la desconexión del database BIBLIOTECA ---------------
def close_connect(mycursor, mydb):
    mycursor.close()
    mydb.close()
# --------♦ Función para crear las tablas 'clientes', 'libros' y 'prestamos'♦------------
def crear_tablas(mydb):
     valido = 0
     while valido == 0:
          try:
               mycursor = mydb.cursor()
               mycursor.execute("CREATE TABLE IF NOT EXISTS clientes(dni VARCHAR(8) PRIMARY KEY NOT NULL, NombreCompleto VARCHAR(256) NOT NULL,  telefono VARCHAR(30)NOT NULL, direccion VARCHAR(256)NOT NULL, estado CHAR(1)NOT NULL)")
               mycursor.execute("CREATE TABLE IF NOT EXISTS libros (ISBN VARCHAR(13) PRIMARY KEY NOT NULL, titulo VARCHAR(256)NOT NULL, autor VARCHAR(256)NOT NULL, estado CHAR (1)NOT NULL)")
               mycursor.execute("CREATE TABLE IF NOT EXISTS prestamos (ID_prestamo INT AUTO_INCREMENT PRIMARY KEY NOT NULL, dni VARCHAR(8) NOT NULL, ISBN VARCHAR(13)NOT NULL, estado CHAR(1)NOT NULL, fecha_prestamos DATE NOT NULL, fecha_devolucion DATE)")
          except mariadb.OperationalError:
               print('Error. Las tablas ya existen.')
          else:
               valido = 1
# ----------♦  Volcado de datos para la tabla 'clientes'♦-----------
def registros_usuarios(mydb):
     valido = 0
     while valido == 0:
          try:
               mycursor=mydb.cursor()
               sql = "INSERT INTO clientes(dni, NombreCompleto, telefono, direccion, estado) VALUES(%d, %s, %d, %s, %s)"
               val= [
                    (10100100, 'Jose Perez', 1510001000, 'Avenida Rivadavia 5100', 'P'),
                    (20200200, 'Maria Gonzalez', 1520002000, 'Avenida Independencia 7200', 'P'),
                    (30300300, 'Ana Godoy', 1530003000, 'Valles 4141', 'D'),
                    
                    ]
               mycursor.executemany(sql, val)
               mydb.commit()
               
          except mariadb.ProgrammingError:
               print('Error. Registros existentes.')
          else:
               valido = 1

# ----------♦ Volcado de datos para la tabla 'libros'♦-----------
def registros_libros(mydb):
     valido = 0
     while valido == 0:
          try:
               mycursor=mydb.cursor()
               sql= "INSERT INTO libros (ISBN, titulo, autor, estado) VALUES(%d,%s,%s,%s)"
               val= [
  ('9789500000450', 'Cartas a Theo', 'Vincent Van Gogh', 'P'),
  ('9786070000100', 'Rayuela','Julio Cortazar','D'),
  ('9780100000403', 'El Aleph', 'Jorge Luis Borges','D')
  

      ]
               mycursor.executemany(sql, val)
               mydb.commit()
               
          except mariadb.ProgrammingError:
               print('Error. Registros existentes.')
          else:
               valido = 1
# ----------♦ Volcado de datos para la tabla 'prestamos' ♦-----------
def registros_prestamos(mydb):
     valido = 0
     while valido == 0:
          try:
               mycursor=mydb.cursor()
               sql = "INSERT INTO prestamos (dni, ISBN, estado, fecha_prestamos, fecha_devolucion) VALUES(%d,%s,%s,%s,%s)"
               val = [
                    (10100100,'9789500000450','P',"2023-10-03", None),
                    (20200200,'9786070000100','P',"2023-11-30", None)

                     ]
               mycursor.executemany(sql, val)
               mydb.commit()

          except mariadb.ProgrammingError:
               print('Error. Registros existentes.')
          else:
               valido = 1


# -----♦ Indices de la tabla prestamos ♦------
def fk_prestamos(mydb):
     mycursor = mydb.cursor()
     mycursor.execute("ALTER TABLE prestamos ADD FOREIGN KEY(dni) REFERENCES clientes(dni) ON UPDATE CASCADE")
     mydb.commit()
     mycursor=mydb.cursor()
     mycursor.execute("ALTER TABLE prestamos ADD FOREIGN KEY(ISBN) REFERENCES libros(ISBN) ON UPDATE CASCADE")
     mydb.commit()
# -------------------------------- Bienvenida al programa --------------------------------------------------

def bienvenida():
    valido = False
    while valido == False:
        try:
            bienv = '''
  ♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦
  ||                                                     ||
  ||    ¡Bienvenidos a nuestro programa BIBLIOTECA!      ||
  || ---♦-----♦----♦-----♦-----♦----♦-----♦-----♦---♦--- ||
  || ▬ Alumnos: E. Leandro,                              ||
  ||            G. Juan,                                 ||
  ||            López Florencia.                         ||
  ||                                                     ||
  || ▬ Profesora: Anabella Hidalgo.                      ||
  ||                                                     ||
  ||                                                     ||
  ||      ~ 1° Cuatrimestre 2023 - IFTS N°24 ~           ||
  ♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦---♦
                   '''

            print(bienv)
            time.sleep(2)
        except (Exception, mariadb.Error) as error:
            print(f'Ocurrió un problema: {error}')
        else:
            print('INICIANDO...\n')
            mydb = conectar_admin()
            crear_base(mydb)
            mydb = connect_base()
            crear_tablas(mydb)
            registros_usuarios(mydb)
            registros_libros(mydb)
            registros_prestamos(mydb)
            fk_prestamos(mydb)
            for i in tqdm(range(10000)):
                        print(' ', end='\r')
            print('\nDatabase y tablas generadas con éxito.\n')
            valido = True
# --------♦ Inicio ♦--------------------------
bienvenida()