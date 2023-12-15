#!/usr/bin/env python
# -*- coding: utf-8 -*
# librerias a utilizar
import mariadb
import time
from tqdm import tqdm
from tabulate import *
import datetime
import re
mydb = ""
mycursor = ""
# -----♦ Funcion para conectar al administrador ♦--------
def conectar_admin():
    mydb = mariadb.connect(
                 host =  "127.0.0.1",
                 user = "root",
                 autocommit = True
                 )
    return mydb

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

#--------------------------♦ Función CLEAR♦--------------------------
import os
def limpioPantalla():
	sisOper = os.name
	if sisOper == "posix":   
		os.system("clear")
	elif sisOper == "ce" or sisOper == "nt" or sisOper == "dos":  # windows
		os.system("cls")

# ----------------------♦Función validar dni♦-----------------------
def valido_dni():
   valido = 0
   while valido == 0:
      global dni
      dni = input('\nPor favor, ingrese DNI del cliente: ')
      if dni.isdigit() != True:
         print('\nError. DNI no admite valor alfanuméricos ni otro tipo de caracteres como "-, . , /" \n')
      else:
         if len(dni) <7 or len(dni)>8:
             print('Se debe ingresar un valor de 7 u 8 dígitos, según corresponda.\n')
         else:
            return dni
   valido = 1

# ---------------------♦ Funcion validar existencia dni ♦------------------
def existe_dni():
    valido = 0
    while valido == 0:
        mydb = connect_base()
        mycursor=mydb.cursor()
        sql = "SELECT dni from clientes where dni = '"+dni+"' "
        mycursor.execute(sql)
        myresultado=mycursor.fetchone()
        if myresultado == None:
            print(f'El cliente con dni {dni} no se encuentra registrado en la base.')
            valido = 1
            valido_dni()
        else:
            valido = 1
            return dni


# ----------------♦Función validar ISBN♦----------------------
def valido_isbn():
    valido = 0
    while valido == 0:
      global isbn
      isbn = input('Por favor, ingrese ISBN del libro: ')
      if isbn.isdigit() != True:
         print('Error. ISBN es un valor numérico, no admite letras ni otro tipo de caracteres')

      else:
        if len(isbn) < 13 or len(isbn) >13:
           print('Error. Se debe ingresar un valor de 13 dígitos')
        else:
           valido = 1
           return isbn
# ---------------------♦ Funcion validar existencia ISBN ♦------------------
def existe_isbn():
    valido = 0
    while valido == 0:
        mydb = connect_base()
        mycursor=mydb.cursor()
        sql = "SELECT ISBN from libros where isbn= '"+isbn+"' "
        mycursor.execute(sql)
        myresultado=mycursor.fetchone()
        if myresultado == None:
            print(f'El libro con ISBN {isbn} no se encuentra registrado en la base.')
            valido = 1
            valido_isbn()
        else:
            valido = 1
            return isbn

# -----------------♦ Función insertar fecha ♦-------------------------
def nueva_fecha():
        global fecha
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        return fecha

#♦-----------------------♦submenu 0-Disponibilidad♦---------------------------------♦
def submenudispo():
    valido = 0
    while valido == 0:
        try:
            info = [['Opciones', '¿Qué desea realizar?'],
                    ['1', 'Consultar nuevamente.'],
                    ['2', 'Ir al Menú Préstamos.'],
                    ['3', 'Volver al Menú Principal.'],
                    ]
            print(tabulate(info, headers='firstrow', tablefmt='fancy_grid'))
        except(Exception) as error:
            print(f'Ocurrió un problema... {error}')
        else:
            valido = 0
            while valido == 0:
                opcion = input('\nMarque 1, 2 o 3 según corresponda: ')
                if not opcion.isdigit():
                            print('Debe ingresar un valor numérico.')
                else:
                     if int(opcion) == 1:
                        limpioPantalla()
                        consultar_dispo()
                        valido = 1
                     elif int(opcion) == 2:
                        limpioPantalla()
                        submenu1()
                        valido = 1
                     elif int(opcion) == 3:
                        limpioPantalla()
                        menu_principal()
                        valido = 1
                     else:
                        print('Opción no válida. Reingrese por favor.')

#♦--------------------------♦submenu Registrar♦---------------------------------♦
def submenuregistrar():
    valido = 0
    while valido == 0:
        try:
            info = [['Opciones', '¿Qué desea realizar?'],
                    ['1', 'Realizar otro registro.'],
                    ['2', 'Volver al Menú Préstamos.'],
                    ['3', 'Volver al Menú Principal.'],
                    ]
            print(tabulate(info, headers='firstrow',tablefmt='fancy_grid'))
        except(Exception) as error:
            print(f'Ocurrió un problema...{error}')
        else:
            valido = 0
            while valido == 0:
                opcion = input('\nMarque 1, 2 o 3 según corresponda: ')
                if not opcion.isdigit():
                            print('Debe ingresar un valor numérico.')
                else:
                     if int(opcion) == 1:
                        limpioPantalla()
                        registrar_prestamo(mydb)
                        valido = 1
                     elif int(opcion) == 2:
                        limpioPantalla()
                        print('Volviendo al Menú anterior ←\n')
                        submenu1()
                        valido = 1
                     elif int(opcion) == 3:
                        limpioPantalla()
                        menu_principal()
                        valido = 1
                     else:
                        print('Opción no válida. Reingrese por favor.')

# ---------------------------submenu Devoluciones----------------
def submenudev():
    valido = 0
    while valido == 0:
        try:
            info = [['Opciones', '¿Qué desea realizar?'],
                    ['1', 'Registrar nueva devolución.'],
                    ['2', 'Volver al Menú Préstamos.'],
                    ['3', 'Volver al Menú Principal.'],
                    ]
            print(tabulate(info, headers='firstrow',tablefmt='fancy_grid'))
        except(Exception) as error:
            print(f'Ocurrió un problema...{error}')
        else:
            valido = 0
            while valido == 0:
                opcion = input('\nMarque 1, 2 o 3 según corresponda: ')
                if not opcion.isdigit():
                            print('\nDebe ingresar un valor numérico.')
                else:
                     if int(opcion) == 1:
                        registrar_devolucion(mydb)
                        valido = 1
                     elif int(opcion) == 2:
                        submenu1()
                        valido = 1
                     elif int(opcion) == 3:
                        menu_principal()
                        valido = 1
                     else:
                        print('Opción no válida. Reingrese por favor')


#----------------♦0 - Consulta de disponibilidad ♦--------------------------
def consultar_dispo():
  valido = False
  while valido == False:
      mydb = connect_base()
      valido_isbn()
      existe_isbn()
      mycursor= mydb.cursor()
      sql = "SELECT estado FROM prestamos WHERE ISBN ='"+isbn+"' "
      mycursor.execute(sql)
      myresultado = mycursor.fetchone()
      if myresultado == None:
          print('No se encuentra dentro de Préstamos el libro ingresado. Intente de nuevo por favor')
          consultar_dispo()
      else:
          for ind in myresultado:
           if ind == 'D':
                print('Libro Disponible')
                valido = True
           else:
                mycursor=mydb.cursor()
                sql = "SELECT clientes.NombreCompleto from clientes INNER JOIN prestamos ON clientes.dni = prestamos.dni INNER JOIN libros ON prestamos.ISBN= libros.ISBN WHERE prestamos.estado = 'P' AND libros.isbn LIKE '%"+isbn+"%'"
                mycursor.execute(sql)
                myresult=mycursor.fetchone()
                print(f'\n▬Libro en préstamo a: {myresult[0]}.\n')
                valido = True
           if valido:
                    close_connect(mycursor, mydb)
                    print('\n')
                    submenudispo()

# ------------- Función -1.A-Consultar todos los títulos disponibles-------------------

def consultar_titulos(mydb):
  mydb = connect_base()
  sql = "SELECT libros.titulo, libros.autor FROM libros WHERE libros.estado = 'D' ORDER BY libros.titulo ASC "
  mycursor=mydb.cursor()
  mycursor.execute(sql)
  myresultado= mycursor.fetchall()
  if len(myresultado) == 0:
      print('\nNo se encontraron registros disponibles.')
  else:
      txt = "Titulos Disponibles"
      x = txt.center(70)
      print(x)
      titulos =['TITULOS', 'AUTORES']
      print(tabulate(myresultado, headers=titulos,tablefmt='simple_outline')) 
  print('\n')
  close_connect(mycursor,mydb)
  print('\n ← Volviendo al Menú de Préstamos...\n')
  print('\n')
  submenu1()

#------------1.B-Registrar préstamo --------------------------------------------------
def registrar_prestamo(mydb):
     valido = False
     while valido == False:
         try:
             mydb = connect_base()
             mycursor = mydb.cursor()
             nuevo_prestamo= []
             valido_dni()
             existe_dni()
             sql = "SELECT estado from prestamos where dni = '"+dni+"' "
             mycursor.execute(sql)
             resultado = mycursor.fetchone()
             print(resultado)
             if resultado[0] == 'D':
                nuevo_prestamo.append(dni)
                valido_isbn()
                existe_isbn()
                sql = "SELECT estado from prestamos where ISBN = '"+isbn+"' "
                mycursor.execute(sql)
                myresultado = mycursor.fetchone()
                if myresultado[0] == 'D':
                    nuevo_prestamo.append(isbn)
                    nuevo_estado = 'P'
                    nuevo_prestamo.append(nuevo_estado)
                    nueva_fecha()
                    nuevo_prestamo.append(fecha)
                    mycursor=mydb.cursor()
                    sql = "INSERT INTO prestamos (dni, ISBN, estado, fecha_prestamos) VALUES (%d, %s, %s,%s)"
                    val = nuevo_prestamo
                    mycursor.execute(sql, val)
                    mydb.commit()
                    mycursor=mydb.cursor()
                  # Actualizar el estado en las tablas 'clientes' y 'libros'
                    sql_1= "UPDATE libros SET estado = 'P' where ISBN = '"+isbn+"' "
                    mycursor.execute(sql_1)
                    sql_2 = "UPDATE clientes SET estado = 'P' where dni = '"+dni+"' "
                    mycursor.execute(sql_2)
                    mydb.commit()
                    print('\nSe registró el préstamo exitosamente\n')
                    valido = True
                    print(f'\nEstado de libro con n° ISBN {isbn} y Cliente con DNI {dni} actualizados exitosamente.\n')
                else:
                    print('¡Advertencia! El libro ya se encuentra en préstamo')
                    print('\n')
                    valido = True
             else:
                 print('\n ¡Advertencia! El cliente ya tiene un préstamo.\n')
                 print('\n')
                 valido = True
                 
         except(Exception, mariadb.ProgrammingError) as error:
             print(f'Ocurrió un problema...{error}')
         finally:
             valido = True             
             if valido:
                 print('\n')
                 close_connect(mycursor,mydb)
                 print('\n')
                 submenuregistrar()


#-----------♦1.C-Registrar Devolución ♦-------------------------------------
def registrar_devolucion(mydb):
    valido = 0
    while valido == 0:
        try:
            mydb = connect_base()
            valido_dni()
            existe_dni()
            mycursor= mydb.cursor()
            sql = "SELECT NombreCompleto, prestamos.ISBN, clientes.estado from clientes INNER JOIN prestamos ON clientes.dni = prestamos.dni WHERE prestamos.estado = 'P' AND clientes.dni = '"+dni+"'"
            mycursor.execute(sql)
            myresultado= mycursor.fetchone()
            if (myresultado) == None:
                print('Cliente no se encuentra con préstamo vigente. Por favor intente de nuevo')
                registrar_devolucion(mydb)
            else:
                print('\nDatos del cliente ingresado:')
                data = [[myresultado[0], myresultado[1], myresultado[2]]]
                titulos = ['Nombre', 'ISBN del libro', 'Estado']
                print(tabulate(data, headers=titulos, tablefmt='simple_outline'))
            print('\n')
            isbn = myresultado[1]
            sql2="SELECT libros.titulo, libros.autor,libros.estado FROM libros INNER JOIN prestamos ON libros.ISBN=prestamos.ISBN WHERE prestamos.estado = 'P' AND libros.ISBN = '"+isbn+"'"
            mycursor.execute(sql2)
            myresult= mycursor.fetchone()
            if (myresult) == None:
                print('\nEl libro ingresado no se encuentra con prestamo vigente. Por favor intente de nuevo.\n')
                valido_isbn()
            else:
                print('\nDatos del libro ingresado:')
                info = [[myresult[0], myresult[1], myresult[2]]]
                titulos = ['Titulo', 'Autor', 'Estado']
                print(tabulate(info, headers=titulos, tablefmt='simple_outline'))
        except(Exception, mariadb.ProgrammingError) as error:
            print(f'Ocurrió un problema... {error}')
        else:
             print('\n')
             nueva_fecha()
             mycursor=mydb.cursor()
             sql3= "UPDATE libros SET estado = 'D' where ISBN = '"+isbn+"' "
             mycursor.execute(sql3)
             sql4 = "UPDATE clientes SET estado = 'D' where dni = '"+dni+"' "
             mycursor.execute(sql4)
             sql4 = "UPDATE prestamos SET estado = 'D' where ISBN= '"+isbn+"' "
             mycursor.execute(sql4)
             sql5= f"UPDATE prestamos SET fecha_devolucion = '"+fecha+"' WHERE dni = '"+dni+"'"
             mycursor.execute(sql5)
             mydb.commit()
        finally:
            valido = True
            print(f'\nSe actualizó exitosamente la devolución del libro con ISBN {isbn} del Cliente con DNI {dni}')
            if valido:
                close_connect(mycursor,mydb)
                print('\n')
                submenudev()

#♦--------------------------♦Submenu 1♦----------------------------------♦
def submenu1():
    valido = 0
    while valido == 0:
        try:
            info = [['Opciones', '¿Qué desea realizar?'],
                    ['A', 'Consultar todos los títulos disponibles'],
                    ['B', 'Registrar Préstamo'],
                    ['C', 'Registrar Devolución'],
                    ['D', 'Volver al menú principal']
                    ]
            print(tabulate(info, headers='firstrow', tablefmt='fancy_grid'))
        except(Exception) as error:
            print(f'Ocurrió un problema... {error}')
        else:
            opciones = input('Ingrese la opción deseada (A/B/C/D):').upper()
            print('\n')
            try:
                if opciones.isalpha():
                    if opciones == 'A':
                        consultar_titulos(mydb)
                        valido = 1
                    elif opciones == 'B':
                        registrar_prestamo(mydb)
                        valido = 1
                    elif opciones== 'C':
                        registrar_devolucion(mydb)
                        valido = 1
                    elif opciones == 'D':
                        menu_principal()
                        valido = 1
                    else:
                        print('Debe ingresar una opción válida: A, B, C o D')
            except ValueError as error:
                print(f'Ocurrió un problema...{error}')
            else: 
                if not valido:
                    print('\nError. Reingrese:\n ')
       


# -----------------------♦ Menú Principal ♦-----------------------------------
def menu_principal():
    valido = 0
    while valido == 0:
        try:
           print('\n')
           info = [['Opciones', '¿Qué desea realizar?'],
                    ['0', 'Consultar disponibilidad'],
                    ['1', 'Menú Préstamo'],
                    ['2', 'Menú Gestión del Cliente'],
                    ['3', 'Menú Gestión del Libro'],
                    ['4', 'Salir del programa']
                    ]
           print(tabulate(info, headers='firstrow', tablefmt='fancy_grid'))
        except (Exception) as error:
            print(f'Ocurrió un problema...{error}')
        else:
            valido = 0
            while valido == 0:
                opcion = input('\nIngrese la opción deseada: ')
                if not opcion.isdigit():
                            print('\nDebe ingresar un valor numérico.')
                else:
                     if int(opcion) == 0:
                        limpioPantalla()
                        consultar_dispo()
                        valido = 1
                     elif int(opcion) == 1:
                        limpioPantalla()
                        submenu1()
                        valido = 1
                     elif int(opcion) == 2:
                        limpioPantalla()
                        mydb=connect_base()
                        mycursor = mydb.cursor()
                        #menu_gestion_cliente()
                        close_connect(mycursor,mydb)
                        valido = 1
                     elif int(opcion) == 3:
                         limpioPantalla()
                         mydb=connect_base()
                         mycursor = mydb.cursor()
                         #gestion_libro_submenu()
                         close_connect(mycursor,mydb)
                         valido = 1
                     elif int(opcion) == 4:
                         limpioPantalla()
                         print('¡Gracias por utilizar Biblioteca!', end='')
                         time.sleep(1)
                         for t in range (5):
                             print('.', end = '')
                         print('Programa terminado.')
                         valido = 1
                     else:
                        print('Opción no válida. Reingrese por favor.\n')
# ----------------♦ Inicio del programa ♦-------------------  
menu_principal()
                    