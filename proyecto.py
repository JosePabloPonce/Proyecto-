from psycopg2 import *
from datetime import date
import pywhatkit as kit
import random


engine = connect(
    database="proyecto1datos",
    user="postgres",
    password="guidoraro",
    host="database-1.ciahoptmomix.us-east-2.rds.amazonaws.com",
    port='5432'
)

def comprobariniciosesion(usuario):
    cursor = engine.cursor()
    seleccionar = "Select usuario, contrasena, suscripcion, tipo from  usuarios where usuario = %s"
    cursor.execute(seleccionar, (usuario,))
    record = cursor.fetchall()
    
    return record

def registrarse(usuario, contrasenaConfirmacion, nombre, suscripcion):
    today =  date.today()
    cursor = engine.cursor()
    insertar =  " INSERT INTO usuarios(usuario, contrasena, nombre, suscripcion, fecha_inicio_suscripcion, tipo) VALUES (%s,%s,%s,%s,%s,%s)"
    datos = (usuario, contrasenaConfirmacion, nombre, suscripcion, today, 'Usuario')
    cursor.execute(insertar, datos)
    engine.commit()

def actualizarSuscripcion(usuario):
    today =  date.today()
    cursor = engine.cursor()
    actualizar = "Update usuarios set suscripcion = %s where usuario = %s"
    cursor.execute(actualizar, ('premium',usuario))
    engine.commit()
    actualizarFecha = "Update usuarios set fecha_inicio_suscripcion = %s where usuario = %s"
    cursor.execute(actualizarFecha, (today,usuario))
    engine.commit()
    
def esartista(usuario):
    cursor = engine.cursor()
    seleccionar ="select a.nombre_artistico from artistas a where a.usuario = %s"
    cursor.execute(seleccionar, (usuario,))
    record = cursor.fetchall()
    return record

def chequearartista(nombreartistico):
    cursor = engine.cursor()
    seleccionar ="select a.nombre_artistico from artistas a where a.nombre_artistico = %s"
    cursor.execute(seleccionar, (nombreartistico,))
    record = cursor.fetchall()
    return record

def agregarartista(artista, usuario):
    cursor = engine.cursor()
    insertar =  " INSERT INTO artistas VALUES (%s,%s)"
    datos = (artista, usuario)
    cursor.execute(insertar, datos)
    engine.commit()

def agregaralbum(albumnombre, nombreartista, codigoalbum):
    today =  date.today()
    cursor = engine.cursor()
    insertar =  " INSERT INTO albumes VALUES (%s,%s,%s,%s)"
    datos = (albumnombre, today, nombreartista, codigoalbum)
    cursor.execute(insertar, datos)
    engine.commit()

#def chequearalbum(albumnombre):
#    cursor = engine.cursor()
#    seleccionar ="select * from albumes where album = %s"
#    cursor.execute(seleccionar, (albumnombre,))
#    record = cursor.fetchall()
#    return record

def mostrargeneros():
    cursor = engine.cursor()
    seleccionar ="select * from generos"
    cursor.execute(seleccionar)
    record = cursor.fetchall()
    return record

def agregarcancion(cancion, codigo):
    today =  date.today()
    cursor = engine.cursor()
    insertar =  " INSERT INTO canciones VALUES (%s,%s,%s,%s,%s )"
    datos = (cancion, codigo, 0, today, "activa" )
    cursor.execute(insertar, datos)
    engine.commit()
    
def agregarcanciongenero(codigo, genero):
    for i in genero:
        cursor = engine.cursor()
        insertar =  " INSERT INTO tiene_genero_cancion VALUES (%s,%s)"
        datos = (codigo, i )
        cursor.execute(insertar, datos)
        engine.commit()
        
def agregarcancionartista(codigo, artista):
        cursor = engine.cursor()
        insertar =  " INSERT INTO tiene_artista_cancion VALUES (%s,%s)"
        datos = (codigo, artista)
        cursor.execute(insertar, datos)
        engine.commit()
        
def seleccionaralbumdeartista(nombreartistico):
    cursor = engine.cursor()
    seleccionar ="select * from albumes where nombre_artistico = %s"
    cursor.execute(seleccionar, (nombreartistico,))
    record = cursor.fetchall()
    return record

def ingresaralbumcancion(codigocancion, codigoalbum):
        cursor = engine.cursor()
        insertar =  " INSERT INTO tiene_album_cancion VALUES (%s,%s)"
        datos = (codigocancion, codigoalbum)
        cursor.execute(insertar, datos)
        engine.commit()    

def insertarcanciondiaNoPremium(usuario,codigo_cancion):
    cursor = engine.cursor()
    con = "select count(h.codigo_escucha) from historial h where h.usuario = %s"
    cursor.execute(con,(usuario,))
    conteo = cursor.fetchall()
    if conteo[0][0] == 3:
        return False
    else:
        banderaCodigo = True
        while banderaCodigo:
            today =  date.today()
            codigoescucha = str((random.randint(3, 100000)))
            query = "select codigo_cancion from canciones"
            cursor.execute(query)
            lista = cursor.fetchall()
            if codigoescucha not in lista:
                insertar = "insert into historial values (%s,%s,%s,%s)"
                #cancionAlDia = "update historial set usuario = (%s), fecha_escuchada = (%s), codigo_escucha =(%s), codigo_cancion =(%s)"
                datos = (today,codigoescucha,codigo_cancion,usuario)
                cursor.execute(insertar,datos)
                engine.commit()
                banderaCodigo = False
                return True
            else:
                banderaCodigo = True
                
        
        
def insertarcanciondiaPremium(usuario,codigo_cancion):
    banderaCodigo = True
    while banderaCodigo:
        cursor = engine.cursor()
        today =  date.today()   
        codigoescucha = str((random.randint(3, 100000)))
        query = "select codigo_cancion from canciones"
        cursor.execute(query)
        lista = cursor.fetchall()
        if codigoescucha not in lista:
            insertar = "insert into historial values (%s,%s,%s,%s)"
            #cancionAlDia = "update historial set usuario = (%s), fecha_escuchada = (%s), codigo_escucha =(%s), codigo_cancion =(%s)"
            datos = (today,codigoescucha,codigo_cancion,usuario)
            cursor.execute(insertar,datos)
            engine.commit()
            banderaCodigo = False
        else:
            banderaCodigo = True
        
           

    
    
def menuprincipalNoPremium():
    cursor = engine.cursor()
    saludo = "select nombre from usuarios where usuario = %s"
    cursor.execute(saludo,(usuario,))
    record = cursor.fetchall()
    print("Bienvenido "+ str(record[0][0]))
    menu = True
    while menu:
        opcion = input("Buscar:\n 1.Cancion \n 2.Artista \n 3.Genero \n 4.Album\n 5.Salir\n")
        if opcion == '1':
            banderaCancion = True
            while banderaCancion:
                buscar = input("Nombre de la cancion\n")
                busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion ilike %s and c.codigo_cancion = t.codigo_cancion and c.estado = 'activa') from tiene_artista_cancion t intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c where c.estado = 'activa')"
                formatear = '%{}%'.format(buscar)
                cursor.execute(busqueda,(formatear,))
                record = cursor.fetchall()
                if len(record) == 0:
                    print("No se encuentra la cancion :( ingresa otra\n")
                    op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                    if op == "2":
                        banderaCancion = False
                else:
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                    
                    cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                    codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.cancion = %s"
                    cursor.execute(codigoCancion,(record[cancion-1][1],))
                    histo = cursor.fetchall()
                    historial = histo[0][0]
                    if(insertarcanciondiaNoPremium(usuario,historial)):
                        kit.playonyt(str(record[cancion-1][0])+", "+str(record[cancion-1][1]))
                        banderaCancion = False
                    else:
                        print("Ya no puedes reproducir mas canciones")
                        banderaCancion = False
                    #abrir cancion youtube
        if opcion == '2':
            banderaArtista = True
            while banderaArtista:
                buscar = input("Nombre del Artista\n")
                busqueda = "select nombre_artistico from artistas where nombre_artistico ilike %s"
                formatear = '%{}%'.format(buscar)
                cursor.execute(busqueda,(formatear,))
                record = cursor.fetchall()
                if len(record) == 0:
                    print("No se encuentra el artista :( ingresa otro\n")
                    op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                    if op == "2":
                        banderaArtista = False
                else:
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0]))
                        
                    artista = int(input("Ingrese la opcion de artista:\n"))
                    eleccion = str(record[artista-1][0])
                    cancion = "select c.cancion from canciones c where c.estado = 'activa' and c.codigo_cancion in (select t.codigo_cancion from tiene_artista_cancion t where t.nombre_artistico = %s)"
                    cursor.execute(cancion,(eleccion,))
                    record = cursor.fetchall()
                    if len(record) == 0:
                        print("El artista no tiene canciones\n")
                        op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                        if op == "2":
                            banderaArtista = False
                    else:
                        for i in range (0,len(record)):
                            print(str(i+1)+". "+str(record[i][0]))
                        
                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                        codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.codigo_cancion in(select t.codigo_cancion from tiene_artista_cancion t where t.nombre_artistico = %s)"
                        cursor.execute(codigoCancion,(eleccion,))
                        histo = cursor.fetchall()
                        historial = histo[0][0]
                        if(insertarcanciondiaNoPremium(usuario,historial)):
                            kit.playonyt(eleccion+str(record[cancion-1]))
                            banderaArtista = False
                        else:
                            print("Ya no puedes reproducir mas canciones")
                            banderaArtista = False
                    #abrir cancion youtube
        if opcion == '3':
            banderaGenero = True
            while banderaGenero:
                busqueda = "select genero from generos"
                cursor.execute(busqueda)
                record = cursor.fetchall()
                if len(record)==0:
                    print("No se encuentra el genero :( ingresa otro\n")
                    op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                    if op == "2":
                        banderaGenero = False
                else:
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0]))
                        
                    artista = int(input("Ingrese la opcion de genero:\n"))
                    eleccion = str(record[artista-1][0])
                    cancion = "select tac.nombre_artistico, (select c2.cancion from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado = 'activa' and c2.codigo_cancion in (select tgc.codigo_cancion from tiene_genero_cancion tgc where tgc.genero=%s))from tiene_artista_cancion tac intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c where c.estado = 'activa')"
                    cursor.execute(cancion,(eleccion,))
                    record = cursor.fetchall()
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0])+', '+str(record[i][1]))
                        
                    cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                    codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.codigo_cancion in (select t.codigo_cancion from tiene_genero_cancion t where t.genero = %s)"
                    cursor.execute(codigoCancion,(eleccion,))
                    histo = cursor.fetchall()
                    historial = histo[0][0]
                    if(insertarcanciondiaNoPremium(usuario,historial)):
                        kit.playonyt(str(record[cancion-1][0])+", "+str(record[cancion-1][1]))
                        banderaGenero = False
                    else:
                        print("Ya no puedes reproducir mas canciones")
                        banderaGenero = False
                #abrir cancion youtube
        if opcion == '4':
            banderaAlbum = True
            while banderaAlbum:
                buscar = input("Nombre del Album\n")
                busqueda = "select nombre_artistico, album from albumes where album ilike %s"
                formatear = '%{}%'.format(buscar)
                cursor.execute(busqueda,(formatear,))
                record = cursor.fetchall()
                if len(record)==0:
                    print("No se encuentra el album :( ingresa otro\n")
                    op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                    if op == "2":
                        banderaAlbum = False
                else:
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                        
                    artista = int(input("Ingrese la opcion de album:\n"))
                    eleccion = str(record[artista-1][1])
                    print(eleccion)
                    cancion = "select t.nombre_artistico,(select c.cancion from canciones c where c.estado = 'activa' and c.codigo_cancion = t.codigo_cancion and c.codigo_cancion in (select t2.codigo_cancion from tiene_album_cancion t2 where t2.codigo_album in (select t3.codigo_album from albumes t3 where t3.album = %s))) from tiene_artista_cancion t intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c where c.estado = 'activa')"
                    cursor.execute(cancion,(eleccion,))
                    record = cursor.fetchall()
                    if len(record)==0:
                        print("El album no tiene canciones :( ingresa otro\n")
                        op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                        if op == "2":
                            banderaAlbum = False
                    else:
                        for i in range (0,len(record)):
                            print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                            
                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                        codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.codigo_cancion in (select t.codigo_cancion from tiene_album_cancion t where t.codigo_album in (select t2.codigo_album from albumes t2 where t2.album = %s)) "
                        cursor.execute(codigoCancion,(eleccion,))
                        histo = cursor.fetchall()
                        historial = histo[0][0]
                        if(insertarcanciondiaNoPremium(usuario,historial)):
                            kit.playonyt(str(record[cancion-1][0])+", "+ str(record[cancion-1][1]))
                            banderaAlbum = False
                        else:
                            print("Ya no puedes reproducir mas canciones")
                            banderaAlbum = False
                    #abrir cancion youtube
        if opcion == '5':
            print("Adios")
            menu = False
            
            
def menuprincipalPremium():
    cursor = engine.cursor()
    saludo = "select nombre from usuarios where usuario = %s"
    cursor.execute(saludo,(usuario,))
    record = cursor.fetchall()
    print("Bienvenido "+ str(record[0][0]))
    menu = True
    while menu:
        opcion = input("Buscar:\n 1.Cancion \n 2.Artista \n 3.Genero \n 4.Album\n 5.Salir\n")
        if opcion == '1':
            banderaCancion = True
            while banderaCancion:
                buscar = input("Nombre de la cancion\n")
                busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion ilike %s and c.codigo_cancion = t.codigo_cancion and c.estado = 'activa') from tiene_artista_cancion t intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c where c.estado = 'activa')"
                formatear = '%{}%'.format(buscar)
                cursor.execute(busqueda,(formatear,))
                record = cursor.fetchall()
                if len(record) == 0:
                    print("No se encuentra la cancion :( ingresa otra\n")
                    op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                    if op == "2":
                        banderaCancion = False
                else:
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
       
       
                    cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                    codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.cancion = %s"
                    cursor.execute(codigoCancion,(record[cancion-1][1],))
                    histo = cursor.fetchall()
                    historial = histo[0][0]
                    insertarcanciondiaPremium(usuario,historial)
                    kit.playonyt(str(record[cancion-1][0])+", "+str(record[cancion-1][1]))
                    banderaCancion = False
            
            #abrir cancion youtube
        if opcion == '2':
            banderaArtista = True
            while banderaArtista:
                buscar = input("Nombre del Artista\n")
                busqueda = "select nombre_artistico from artistas where nombre_artistico ilike %s"
                formatear = '%{}%'.format(buscar)
                cursor.execute(busqueda,(formatear,))
                record = cursor.fetchall()
                if len(record) == 0:
                    print("No se encuentra el artista :( ingresa otro")
                    op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                    if op == "2":
                        banderaArtista = False
                    
                else:
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0]))
                    
                    artista = int(input("Ingrese la opcion de artista:\n"))
                    eleccion = str(record[artista-1][0])
                    cancion = "select c.cancion from canciones c where c.estado = 'activa' and c.codigo_cancion in (select t.codigo_cancion from tiene_artista_cancion t where t.nombre_artistico = %s)"
                    cursor.execute(cancion,(eleccion,))
                    record = cursor.fetchall()
                    if len(record) == 0:
                        print("El artista no tiene canciones\n")
                        ope = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                        if ope == "2":
                            banderaArtista = False
                    else:
                        for i in range (0,len(record)):
                            print(str(i+1)+". "+str(record[i][0]))
          
                        
                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                        codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.codigo_cancion in(select t.codigo_cancion from tiene_artista_cancion t where t.nombre_artistico = %s)"
                        cursor.execute(codigoCancion,(eleccion,))
                        histo = cursor.fetchall()
                        historial = histo[0][0]
                        insertarcanciondiaPremium(usuario,historial)
                        kit.playonyt(eleccion+str(record[cancion-1]))
                        banderaArtista = False
        
                
            #abrir cancion youtube
        if opcion == '3':
            banderaGenero = True
            while banderaGenero:
                busqueda = "select genero from generos"
                cursor.execute(busqueda)
                record = cursor.fetchall()
                if len(record) == 0:
                    print("No se encuentra el genero :( ingresa otro")
                    op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                    if op == "2":
                        banderaGenero = False
                else:
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0]))
                        
                    artista = int(input("Ingrese la opcion de genero:\n"))
                    eleccion = str(record[artista-1][0])
                    cancion = "select tac.nombre_artistico, (select c2.cancion from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado = 'activa' and c2.codigo_cancion in (select tgc.codigo_cancion from tiene_genero_cancion tgc where tgc.genero=%s))from tiene_artista_cancion tac intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c where c.estado = 'activa')"
                    cursor.execute(cancion,(eleccion,))
                    record = cursor.fetchall()
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0])+", " + str(record[i][1]))
                        
                    cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                    codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.codigo_cancion in (select t.codigo_cancion from tiene_genero_cancion t where t.genero = %s)"
                    cursor.execute(codigoCancion,(eleccion,))
                    histo = cursor.fetchall()
                    historial = histo[0][0]
                    insertarcanciondiaPremium(usuario,historial)
                    kit.playonyt(str(record[cancion-1][0])+", "+str(record[cancion-1][1]))
                    banderaGenero = False
            #abrir cancion youtube
        if opcion == '4':
            banderaAlbum = True
            while banderaAlbum:
                buscar = input("Nombre del Album\n")
                busqueda = "select nombre_artistico, album from albumes where album ilike %s"
                formatear = '%{}%'.format(buscar)
                cursor.execute(busqueda,(formatear,))
                record = cursor.fetchall()
                if len(record)==0:
                    op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                    if op == "2":
                        banderaAlbum = False
                else:
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                        
                    artista = int(input("Ingrese la opcion de album:\n"))
                    eleccion = str(record[artista-1][1])
                    cancion = "select t.nombre_artistico,(select c.cancion from canciones c where c.estado = 'activa' and c.codigo_cancion = t.codigo_cancion and c.codigo_cancion in (select t2.codigo_cancion from tiene_album_cancion t2 where t2.codigo_album in (select t3.codigo_album from albumes t3 where t3.album = %s))) from tiene_artista_cancion t intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c where c.estado = 'activa')"
                    cursor.execute(cancion,(eleccion,))
                    record = cursor.fetchall()
                    if len(record)==0:
                        print("El album no tiene canciones :( ingresa otro\n")
                        op = input(" 1. Ingresar de nuevo\n 2. Regresar\n")
                        if op == "2":
                            banderaAlbum = False
                    else:
                        for i in range (0,len(record)):
                            print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                            
                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                        codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.codigo_cancion in (select t.codigo_cancion from tiene_album_cancion t where t.codigo_album in (select t2.codigo_album from albumes t2 where t2.album = %s))"
                        cursor.execute(codigoCancion,(eleccion,))
                        histo = cursor.fetchall()
                        historial = histo[0][0]
                        insertarcanciondiaPremium(usuario,historial)
                        kit.playonyt(str(record[cancion-1][0])+", "+str(record[cancion-1][1]))
                        banderaAlbum = False
                    #abrir cancion youtube
        if opcion == '5':
            print("Adios")
            menu = False
            
                    
            
 

def playlist(usuario):
    cursor = engine.cursor()
    bandera = True
    while bandera:
        opcion = input(" 1.Anadir Playlist \n 2.Ver Playlists \n 3. Salir\n")
        if opcion == '1':
            banderaCodigo = True
            nombre = input("Ingrese el nombre de la playlist:\n")
            while banderaCodigo:
                codigoplaylist = str((random.randint(3, 100000)))
                query = "select codigo_playlist from playlists"
                cursor.execute(query)
                lista = cursor.fetchall()
                if codigoplaylist not in lista:
                    insertar = "insert into playlists values(%s,%s,%s)"
                    datos = (nombre, codigoplaylist, usuario)
                    cursor.execute(insertar, datos)
                    engine.commit()
                    print("Playlist creada\n")
                    banderaCodigo = False
                else:
                    banderaCodigo = True
            
        if opcion == '2':
            verPlaylist = "select nombre from playlists where usuario = %s"
            cursor.execute(verPlaylist, (usuario,))
            record = cursor.fetchall()
            if len(record) == 0:
                print("No se encontraron playlists :(")
            else:
                for i in range (0,len(record)):
                    print(str(i+1)+". "+str(record[i][0]))
                    
                artista = int(input("Ingrese la opcion de playlist:\n"))
                eleccion = str(record[artista-1][0])
                query = "select t3.nombre_artistico,(select c.cancion from canciones c where c.estado = 'activa' and c.codigo_cancion = t3.codigo_cancion and c.codigo_cancion in (select t.codigo_cancion from tiene_playlist_cancion t where t.codigo_playlist in (select t2.codigo_playlist from playlists t2 where t2.nombre = %s)))from tiene_artista_cancion t3 intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac"
                cursor.execute(query,(eleccion,))
                record = cursor.fetchall()
                if len(record) == 0:
                    print("No tienes canciones en la playlist")
                else:
                    print("Canciones que tiene la playlist:\n")
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                        
                    cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                    codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.cancion = %s"
                    cursor.execute(codigoCancion,(record[cancion-1][1],))
                    histo = cursor.fetchall()
                    historial = histo[0][0]
                    insertarcanciondiaPremium(usuario,historial)
                    kit.playonyt(str(record[cancion-1][0])+", "+str(record[cancion-1][1]))
                    
                bandera2 = True
                while bandera2:
                    opcion = input("¿Desea añadir canciones?\n 1. Si\n 2. No\n")
                    if opcion == '1':
                        buscar = input("Nombre de la cancion\n")
                        busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion ilike %s and c.codigo_cancion = t.codigo_cancion and c.estado = 'activa') from tiene_artista_cancion t intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c where c.estado = 'activa')"
                        formatear = '%{}%'.format(buscar)
                        cursor.execute(busqueda,(formatear,))
                        record = cursor.fetchall()
                        if len(record) == 0:
                            print("No se encontraron canciones")
                        else:
                            for i in range (0,len(record)):
                                print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                            
                            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                            can = str(record[cancion-1][1])
                            codigoCancion = "select c.codigo_cancion from canciones c where c.estado = 'activa' and c.cancion = %s"
                            cursor.execute(codigoCancion,(can,))
                            recordCancion = cursor.fetchall()
                            codigoPlaylist = "select c.codigo_playlist from playlists c where c.nombre = %s"
                            cursor.execute(codigoPlaylist,(eleccion,))
                            recordPlaylist = cursor.fetchall()
                            insertar = "insert into tiene_playlist_cancion values(%s,%s)"
                            datos = (recordCancion[0][0],recordPlaylist[0][0])
                            cursor.execute(insertar, datos)
                            engine.commit()
                            print("Cancion agregada")
                    if opcion == '2':
                        bandera2 = False
            
        if opcion == '3':
            bandera = False
                

def eliminarcancion():
        
        cursor = engine.cursor()
        buscar = input("Ingresa el Nombre del Artista de la Cancion\n")
        busqueda = "select nombre_artistico from artistas where nombre_artistico ilike %s"
        formatear = '%{}%'.format(buscar)
        cursor.execute(busqueda,(formatear,))
        record = cursor.fetchall()
        
        for i in range (0,len(record)):
            print(str(i+1)+". "+str(record[i][0]))
            
        artista = int(input("Ingresa el numero del artista correspondiente:\n"))
        eleccion = str(record[artista-1][0])
        cancion = "select c.cancion, c.codigo_cancion from canciones c where c.codigo_cancion in (select t.codigo_cancion from tiene_artista_cancion t where t.nombre_artistico = %s)"
        cursor.execute(cancion,(eleccion,))
        record = cursor.fetchall()
        for i in range (0,len(record)):
            print(str(i+1)+". "+eleccion+" "+str(record[i][0]))
            
        cancion = int(input ("Ingrese el numero de cancion que deseas eliminar:\n"))
        eliminargenero = ("delete from tiene_genero_cancion where codigo_cancion =%s")
        cursor.execute(eliminargenero, [record[cancion-1][1]])
        engine.commit()
        
        eliminarhistorial = ("delete from historial where codigo_cancion =%s")
        cursor.execute(eliminarhistorial, [record[cancion-1][1]])
        engine.commit()
        
        eliminaralbum = ("delete from tiene_album_cancion where codigo_cancion =%s")
        cursor.execute(eliminaralbum, [record[cancion-1][1]])
        engine.commit()
        
        eliminarartista = ("delete from tiene_artista_cancion where codigo_cancion =%s")
        cursor.execute(eliminarartista, [record[cancion-1][1]])
        engine.commit()
        
        eliminarplaylist = ("delete from tiene_playlist_cancion where codigo_cancion =%s")
        cursor.execute(eliminarplaylist, [record[cancion-1][1]])
        engine.commit()
        
        eliminarcancion = ("delete from canciones where codigo_cancion =%s")
        cursor.execute(eliminarcancion, [record[cancion-1][1]])
        engine.commit()
        

        print("cancion eliminada")

def eliminaralbum():
        cursor = engine.cursor()
        buscar = input("Nombre del Album\n")
        busqueda = "select album, codigo_album from albumes where album ilike %s"
        formatear = '%{}%'.format(buscar)
        cursor.execute(busqueda,(formatear,))
        record = cursor.fetchall()
        for i in range (0,len(record)):
            print(str(i+1)+". "+str(record[i][0]))
            
        artista = int(input("Ingrese la opcion de album:\n"))
        eleccion = str(record[artista-1][1])

        cancion = "select * from tiene_album_cancion where codigo_album =%s"
        cursor.execute(cancion,(eleccion,))
        record = cursor.fetchall()
        for i in range (0,len(record)):            
            eliminargenero = ("delete from tiene_genero_cancion where codigo_cancion =%s")
            cursor.execute(eliminargenero, [record[i][0]])
            engine.commit()
            
            eliminarhistorial = ("delete from historial where codigo_cancion =%s")
            cursor.execute(eliminarhistorial, [record[i][0]])
            engine.commit()
            
            eliminaralbum = ("delete from tiene_album_cancion where codigo_cancion =%s")
            cursor.execute(eliminaralbum, [record[i][0]])
            engine.commit()
            
            eliminarartista = ("delete from tiene_artista_cancion where codigo_cancion =%s")
            cursor.execute(eliminarartista, [record[i][0]])
            engine.commit()
            
            eliminarplaylist = ("delete from tiene_playlist_cancion where codigo_cancion =%s")
            cursor.execute(eliminarplaylist, [record[i][0]])
            engine.commit()
            
            eliminarcancion = ("delete from canciones where codigo_cancion =%s")
            cursor.execute(eliminarcancion, [record[i][0]])
            engine.commit()
        
        eliminarnombrealbum = ("delete from albumes where codigo_album =%s")
        cursor.execute(eliminarnombrealbum, [eleccion])
        engine.commit()
            
        print("Album y sus canciones eliminadas")
            
            
def eliminarartista():
        cursor = engine.cursor()
        buscar = input("Ingresa el Nombre del Artista a eliminar\n")
        busqueda = "select nombre_artistico from artistas where nombre_artistico ilike %s"
        formatear = '%{}%'.format(buscar)
        cursor.execute(busqueda,(formatear,))
        record = cursor.fetchall()
        
        for i in range (0,len(record)):
            print(str(i+1)+". "+str(record[i][0]))
            
        artista = int(input("Ingresa el numero del artista correspondiente:\n"))
        eleccion = str(record[artista-1][0])

        busqueda = "select codigo_album from albumes where nombre_artistico = %s"
        cursor.execute(busqueda,(eleccion,))
        record = cursor.fetchall()
        for i in range (0,len(record)):            
            cancion = "select * from tiene_album_cancion where codigo_album =%s"
            cursor.execute(cancion,(record[i][0],))
            record2 = cursor.fetchall()
            for i in range (0,len(record2)):            
                eliminargenero = ("delete from tiene_genero_cancion where codigo_cancion =%s")
                cursor.execute(eliminargenero, [record2[i][0]])
                engine.commit()
                
                eliminarhistorial = ("delete from historial where codigo_cancion =%s")
                cursor.execute(eliminarhistorial, [record2[i][0]])
                engine.commit()
                
                eliminaralbum = ("delete from tiene_album_cancion where codigo_cancion =%s")
                cursor.execute(eliminaralbum, [record2[i][0]])
                engine.commit()
                
                eliminarartista = ("delete from tiene_artista_cancion where codigo_cancion =%s")
                cursor.execute(eliminarartista, [record2[i][0]])
                engine.commit()
                
                eliminarplaylist = ("delete from tiene_playlist_cancion where codigo_cancion =%s")
                cursor.execute(eliminarplaylist, [record2[i][0]])
                engine.commit()
                
                eliminarcancion = ("delete from canciones where codigo_cancion =%s")
                cursor.execute(eliminarcancion, [record2[i][0]])
                engine.commit()
            
            eliminarnombrealbum = ("delete from albumes where codigo_album =%s")
            cursor.execute(eliminarnombrealbum, [record[i][0]])
            engine.commit()
        
        eliminarnombreartista = ("delete from artistas where nombre_artistico =%s")
        cursor.execute(eliminarnombreartista, [eleccion])
        engine.commit()
        
        print("Artista eliminado con albumes y canciones")

def albumesmasrecientesultimasemana():
    cursor = engine.cursor()
    seleccionar ="select a.album, a.nombre_artistico from albumes a where a.fecha_agregado between (now() -'1 week'::interval) and   now()"
    cursor.execute(seleccionar)
    record = cursor.fetchall()
    for i in range (0,len(record)):
        print(str(i+1)+". "+str(record[i][0])+", " + str(record[i][1]))
        
def aumentopopularidad3meses():
    cursor = engine.cursor()
    seleccionar ="select a2.nombre_artistico, (select count(h2.codigo_cancion) as reproducciones from historial h2 where h2.fecha_escuchada between (now() - '3 month'::interval) and now() and h2.codigo_cancion in(select tac.codigo_cancion  from tiene_artista_cancion tac where tac.nombre_artistico= a2.nombre_artistico))  from artistas a2  order by reproducciones desc limit 10"
    cursor.execute(seleccionar)
    record = cursor.fetchall()
    print("Top 10 Artistas con mayor cantidad de reproducciones en los ultimos 3 meses")
    for i in range (0,len(record)):
        print(str(i+1)+". "+str(record[i][0])+", " + str(record[i][1]) + " reproducciones")
        
def cantidaddesuscripciones():
    cursor = engine.cursor()
    seleccionar ="select to_char(u.fecha_inicio_suscripcion, 'YYYY-MM') as mes, count(u.suscripcion)as cantidad from usuarios u where u.suscripcion = 'premium' AND u.fecha_inicio_suscripcion between (now() - '6 month'::interval) and now()group by mes order by mes asc"
    cursor.execute(seleccionar)
    record = cursor.fetchall()
    print("Cantidad de suscripciones premium por mes en los ultimos 6 meses")
    for i in range (0,len(record)):
        print(str(i+1)+". "+str(record[i][0])+", " + str(record[i][1]) + " Suscripciones Nuevas")
    
    
    
    
    
def artistasmayorproduccion():
    cursor = engine.cursor()
    seleccionar ="select  a.nombre_artistico, (select count(tac.codigo_cancion) as cantidad_canciones from tiene_artista_cancion tac where tac.nombre_artistico=a.nombre_artistico) from artistas a  order by cantidad_canciones desc limit 10"
    cursor.execute(seleccionar)
    record = cursor.fetchall()
    print("Top 10 Artistas con mayor cantidad de canciones en la plataforma")
    for i in range (0,len(record)):
        print(str(i+1)+". "+str(record[i][0])+", " + str(record[i][1]) + " canciones")
        
def generosmaspopulares():
    cursor = engine.cursor()
    seleccionar ="select g.genero, (select count(h2.codigo_cancion) as reproducciones from historial h2 where h2.fecha_escuchada between (now() - '1 month'::interval) and now() and h2.codigo_cancion in (select tgc.codigo_cancion from tiene_genero_cancion tgc where tgc.genero=g.genero)) from generos g order by reproducciones desc limit 5"
    cursor.execute(seleccionar)
    record = cursor.fetchall()
    print("Top 5 Generos mas escuchados del ultimo mes")
    for i in range (0,len(record)):
        print(str(i+1)+". "+str(record[i][0])+", " + str(record[i][1]) + " reproducciones")
        
def usuariosmasactivos():
    cursor = engine.cursor()
    seleccionar ="select u.usuario, (select count(h2.usuario) as cantidad_canciones_escuchadas from historial h2 where h2.usuario= u.usuario and h2.fecha_escuchada  between (now() - '1 month'::interval) and now()) from usuarios u order by cantidad_canciones_escuchadas desc limit 5"
    cursor.execute(seleccionar)
    record = cursor.fetchall()
    print("Top 5 Usuarios con mas canciones escuchadas del ultimo mes")
    for i in range (0,len(record)):
        print(str(i+1)+". "+str(record[i][0])+", " + str(record[i][1]) + " canciones escuchadas")
        
banderaTotal = True
cursor = engine.cursor()
while banderaTotal:
    opcionTotal = input(" 1. Sign Up\n 2. Login\n 3. Salir \n")
    if opcionTotal == '1':
        banderaSignUp = True
        while banderaSignUp:
            nombre = input("Ingrese su nombre\n")
            usuario = input("Ingrese un usuario\n")
            contrasenaConfirmacion = input("Ingrese su contrasena\n")
            suscripcion = input("Seleccione el tipo de suscripcion\n1. Gratis \n2. Premium\n")
            if(suscripcion == '1'):
                suscripcion = 'gratis'
            elif(suscripcion =='2'):
                suscripcion = 'premium'
                
            if(len(comprobariniciosesion(usuario)) == 0):
                registrarse(usuario, contrasenaConfirmacion, nombre, suscripcion)
                banderaSignUp = False
            else:
                print("usuario ya existe")
        

        

    if opcionTotal =='2':
        banderaLogIn = True
        while banderaLogIn:
            usuario=input('Ingrese su usuario\n ')
            informacion = comprobariniciosesion(usuario)
            if(len(informacion) != 0):
                contrasena= input('Ingrese su contraseña\n')
                if(informacion[0][1] == contrasena):
                    print("Contrasena correcta\n")
                    banderaLogIn = False
                    nombreartistico = esartista(usuario)
                    if(informacion[0][3] == 'Usuario'):
                        if(len(nombreartistico) == 0):
                            if(informacion[0][2] == 'gratis'):
                                print('USUARIO GRATIS')
                                banderafree = True
                                while banderafree:
                                    opcion = input(" 1.Buscar\n 2.Actualizar Suscripcion\n 3.Darse de alta como Artista o Manager\n 4. Salir\n")
                        
                                    if opcion == "1":
                                        menuprincipalNoPremium()
                                        
                                    elif(opcion == "2"):
                                        actualizarSuscripcion(usuario)
                                        print("Suscripcion Actualizada, inicia sesion nuevamente")
                                        banderafree = False
                                        
                                    elif(opcion =="3"):
                                        banderaart = True
                                        while banderaart:
                                            nombreartistico = input("Ingresa tu nombre Artistico\n")
                                            if(len(chequearartista(nombreartistico)) != 0):
                                                print("Nombre artistico en uso")
                                        
                                            
                                            elif(len(chequearartista(nombreartistico)) == 0):
                                                agregarartista(nombreartistico, usuario)
                                                print("Nombre Artistico Agregado, inicia sesion nuevamente")
                                                banderaart = False
                                                banderafree = False
                                    elif opcion == "4":
                                        banderafree = False
                                    
                            elif(informacion[0][2] == 'premium'):
                                print('USUARIO PREMIUM')
                                banderapre = True
                                while banderapre:
                                    opcion = input(" 1.Buscar\n 2.Darse de alta como Artista o Manager\n 3.Playlist\n 4.Salir\n")
                                    if opcion == "1":
                                        menuprincipalPremium()
                                    
                                    elif(opcion =="2"):
                                        banderra = True
                                        while banderra:
                                            nombreartistico = input("Ingresa tu nombre Artistico\n")
                                            if(len(chequearartista(nombreartistico)) != 0):
                                                print("Nombre artistico en uso")
                                    
                                            elif(len(chequearartista(nombreartistico)) == 0):
                                                agregarartista(nombreartistico, usuario)
                                                print("Nombre Artistico Agregado, inicia sesion nuevamente")
                                                banderra = False
                                                banderapre = False
                                    elif opcion == "3":
                                        playlist(usuario)
                                    elif opcion == "4":
                                        banderapre = False
                                        
                        elif(len(nombreartistico) != 0):
                            if(informacion[0][2] == 'gratis'):
                                print('USUARIO GRATIS')
                                print(nombreartistico[0][0])
                                banderagra = True
                                while banderagra:
                                    opcion = input(" 1.Buscar\n 2.Actualizar Suscripcion\n 3.Registrar Album\n 4.Registrar Track\n 5. Salir \n")
                                    if opcion == "1":
                                        menuprincipalNoPremium()
                                        
                                    elif(opcion == "2"):
                                        actualizarSuscripcion(usuario)
                                        print("Suscripcion Actualizada, inicia sesion nuevamente")
                                        banderagra = False
                                        
                                    elif(opcion =="3"):
                                        banderaAlbum = True
                                        nombrealbum = input("Ingresa el nombre del Album a registrar\n")
                                        while banderaAlbum:
                                            codigoalbum = str((random.randint(3, 100000)))
                                            query = "select codigo_album from albumes"
                                            cursor.execute(query)
                                            lista = cursor.fetchall()
                                            if codigoalbum not in lista:
                                                agregaralbum(nombrealbum, nombreartistico[0][0], codigoalbum)
                                                print("Album Agregado Correctamente")
                                                banderaAlbum = False
                                            else:
                                                banderaAlbum = True
                                    
                                    elif(opcion =="4"):
                                        banderaCancion = True
                                        cancion = input('Ingresa el nombre de la cancion a registrar\n')
                                        while banderaCancion:
                                            codigocancion = (random.randint(3, 100000))
                                            query = "select codigo_cancion from canciones"
                                            cursor.execute(query)
                                            lista = cursor.fetchall()
                                            if codigocancion not in lista:
                                                banderaCancion = False
                                                generos = []
                                                while True:
                                                    print("Ingresa el numero del genero o generos a elegir o ingresa '0' para concluir con los generos\n")
                                                    for x in range (len(mostrargeneros())):
                                                        print(str(x+1) + ". " + mostrargeneros()[x][0])
                                                    generoelegido = int(input())
                                                    

                                                    if(len(generos) != 0 and generoelegido == 0 ):                                
                                                        break
                                                    
                                                    elif (mostrargeneros()[generoelegido-1][0] not in generos and generoelegido != 0):
                                                        generos.append(mostrargeneros()[generoelegido-1][0])
                                                        print("Genero agregado")
                                                    else:
                                                        print("Genero ya habia sido agregado anteriormente")
                                                opcion = input(" 1.Agregar en album existente\n 2.Agregar como sencillo\n ")
                                                if(opcion == "1"):
                                                    if(len(seleccionaralbumdeartista(nombreartistico[0][0])) !=0):       
                                                        for x in range (len(seleccionaralbumdeartista(nombreartistico[0][0]))):
                                                            print(str(x+1) + ". " + seleccionaralbumdeartista(nombreartistico[0][0])[x][0] + ", " +seleccionaralbumdeartista(nombreartistico[0][0])[x][2])
                                                            
                                                        albumelegido = int(input("Ingresa el numero del album en el que la agregaras\n"))
                                                        agregarcancion(cancion, codigocancion)
                                                        agregarcanciongenero(codigocancion, generos)
                                                        agregarcancionartista(codigocancion, nombreartistico[0][0])
                                                        ingresaralbumcancion(codigocancion, seleccionaralbumdeartista(nombreartistico[0][0])[albumelegido-1][3])
                                                        print("Cancion Agregada Correctamente")
                                                    else:
                                                        print("No tienes ningun album creado, primero crea uno o agrega cancion como sencillo")
                                                    
                                                if(opcion == "2"):
                                                    agregarcancion(cancion, codigocancion)
                                                    agregarcanciongenero(codigocancion, generos)
                                                    agregarcancionartista(codigocancion, nombreartistico[0][0])
                                                    banderaCodigo = True
                                                    while banderaCodigo:
                                                        codigoalbum = str((random.randint(3, 100000)))
                                                        query = "select codigo_album from albumes"
                                                        cursor.execute(query)
                                                        lista = cursor.fetchall()
                                                        if codigoalbum not in lista:
                                                            agregaralbum(cancion, nombreartistico[0][0], codigoalbum)
                                                            ingresaralbumcancion(codigocancion, codigoalbum)
                                                            print("Cancion Agregada Correctamente")
                                                            banderaCodigo = False
                                                        else:
                                                            banderaCodigo = True
                                            else:
                                                banderaCancion = True
                                                
                                    elif opcion == "5":
                                        bannderaCancion = False
                                        
                                        
                    
                                   
                                    
                            elif(informacion[0][2] == 'premium'):
                                print('USUARIO PREMIUM')
                                print(nombreartistico[0][0])
                                banderaaa = True
                                while banderaaa:
                                    opcion = input(" 1.Buscar\n 2.Registrar Album\n 3.Registrar Track\n 4.Playlist \n 5.Salir \n")
                                    
                                    if (opcion == "1"):
                                        menuprincipalPremium()
                                        
                                    elif (opcion == "2"):
                                        banderaAlbum = True
                                        nombrealbum = input("Ingresa el nombre del Album a registrar\n")
                                        while banderaAlbum:
                                            codigoalbum = str((random.randint(3, 100000)))
                                            query = "select codigo_album from albumes"
                                            cursor.execute(query)
                                            lista = cursor.fetchall()
                                            if codigoalbum not in lista:
                                                agregaralbum(nombrealbum, nombreartistico[0][0],codigoalbum)
                                                print("Album Agregado Correctamente")
                                                banderaAlbum = False
                                            else:
                                                banderaAlbum = True

                                            
                                    elif (opcion == "3"):
                                        banderaCancion = True
                                        cancion = input('Ingresa el nombre de la cancion a registrar\n')
                                        while banderaCancion:
                                            codigocancion = (random.randint(3, 100000))
                                            query = "select codigo_cancion from canciones"
                                            cursor.execute(query)
                                            lista = cursor.fetchall()
                                            if codigocancion not in lista:
                                                generos = []
                                                banderaCancion = False
                                                while True:
                                                    print("Ingresa el numero del genero o generos a elegir o ingresa '0' para concluir con los generos\n")
                                                    for x in range (len(mostrargeneros())):
                                                        print(str(x+1) + ". " + mostrargeneros()[x][0])
                                                    generoelegido = int(input())
                                                    

                                                    if(len(generos) != 0 and generoelegido == 0 ):                                
                                                        break
                                                    
                                                    elif (mostrargeneros()[generoelegido-1][0] not in generos and generoelegido != 0):
                                                        generos.append(mostrargeneros()[generoelegido-1][0])
                                                        print("Genero agregado")
                                                    else:
                                                        print("Genero ya habia sido agregado anteriormente")
                                                opcion = input(" 1.Agregar en album existente\n 2.Agregar como sencillo\n ")
                                                if(opcion == "1"):
                                                    if(len(seleccionaralbumdeartista(nombreartistico[0][0])) !=0):       
                                                        for x in range (len(seleccionaralbumdeartista(nombreartistico[0][0]))):
                                                            print(str(x+1) + ". " + seleccionaralbumdeartista(nombreartistico[0][0])[x][0] + ", " +seleccionaralbumdeartista(nombreartistico[0][0])[x][2])
                                                            
                                                        albumelegido = int(input("Ingresa el numero del album en el que la agregaras\n"))
                                                        agregarcancion(cancion, codigocancion)
                                                        agregarcanciongenero(codigocancion, generos)
                                                        agregarcancionartista(codigocancion, nombreartistico[0][0])
                                                        ingresaralbumcancion(codigocancion, seleccionaralbumdeartista(nombreartistico[0][0])[albumelegido-1][3])
                                                        print("Cancion Agregada Correctamente")
                                                        
                                                    else:
                                                        print("No tienes ningun album creado, primero crea uno o agrega cancion como sencillo")
                                                        
                                                if(opcion == "2"):
                                                    agregarcancion(cancion, codigocancion)
                                                    agregarcanciongenero(codigocancion, generos)
                                                    agregarcancionartista(codigocancion, nombreartistico[0][0])
                                                    banderaAlbum = True
                                                    while banderaAlbum:
                                                        codigoalbum = str((random.randint(3, 100000)))
                                                        query = "select codigo_album from albumes"
                                                        cursor.execute(query)
                                                        lista = cursor.fetchall()
                                                        if codigoalbum not in lista:
                                                            agregaralbum(cancion, nombreartistico[0][0], codigoalbum)
                                                            ingresaralbumcancion(codigocancion, codigoalbum)
                                                            print("Cancion Agregada Correctamente")
                                                            codigoalbum = False
                                                        else:
                                                            codigoalbum = True
                                        else:
                                            banderaCancion = True
                                    elif opcion == "4":
                                        playlist(usuario)
                                    elif opcion == "5":
                                        banderaaa = False
                                    
                    elif(informacion[0][3] == 'Administrador'):
                        if(len(nombreartistico) == 0):      
                            if(informacion[0][2] == 'premium'):
                                print('ADMINISTRADOR')
                                print('USUARIO PREMIUM')
                                banderaAdmin = True
                                while banderaAdmin:
                                    opcion = input(" 1.Buscar\n 2.Darse de alta como Artista o Manager\n 3.Inactivar cancion del catalogo\n 4.Modificar cancion\n 5.Modificar Artista\n 6.Modificar Album\n 7.Eliminar una cancion\n 8.Eliminar album\n 9.Eliminar artista\n 10.Reporteria\n 11. Playlist\n 12. Salir\n")
                                    if opcion == "1":
                                        menuprincipalPremium()
                                    
                                    elif(opcion =="2"):
                                        banddera = True
                                        while banddera:
                                            nombreartistico = input("Ingresa tu nombre Artistico\n")
                                            if(len(chequearartista(nombreartistico)) != 0):
                                                print("Nombre artistico en uso")
                                                
                                            elif(len(chequearartista(nombreartistico)) == 0):
                                                agregarartista(nombreartistico, usuario)
                                                print("Nombre Artistico Agregado, inicia sesion nuevamente")
                                                banddera = False
                                                banderaAdmin = False
                                            
                                    if opcion =="3":
                                        cursor = engine.cursor()
                                        buscar = input("Nombre de la cancion\n")
                                        busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion ilike %s and c.codigo_cancion = t.codigo_cancion and c.estado = 'activa') from tiene_artista_cancion t intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c where c.estado = 'activa')"
                                        formatear = '%{}%'.format(buscar)
                                        cursor.execute(busqueda,(formatear,))
                                        record = cursor.fetchall()                       
                                        for i in range (0,len(record)):
                                            print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                                        
                                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                                        codigoCancion = "select c.codigo_cancion from canciones c where c.cancion = %s"
                                        cursor.execute(codigoCancion,(record[cancion-1][1],))
                                        histo = cursor.fetchall()
                                        historial = histo[0][0]
                                        cambiarEstado = "update canciones set estado = 'inactiva' where codigo_cancion = %s"
                                        cursor.execute(cambiarEstado,(historial,))
                                        engine.commit()
                                        cursor.close()
                                        print("Cancion desactivada")
                                    if opcion == "4":
                                        bandera = True
                                        cursor = engine.cursor()
                                        buscar = input("Nombre de la cancion\n")
                                        busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion ilike %s and c.codigo_cancion = t.codigo_cancion) from tiene_artista_cancion t intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion) as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c)"
                                        formatear = '%{}%'.format(buscar)
                                        cursor.execute(busqueda,(formatear,))
                                        record = cursor.fetchall()                       
                                        for i in range (0,len(record)):
                                            print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                                        
                                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                                        codigoCancion = "select c.codigo_cancion from canciones c where c.cancion = %s"
                                        cursor.execute(codigoCancion,(record[cancion-1][1],))
                                        histo = cursor.fetchall()
                                        historial = histo[0][0]
                                        while bandera:
                                            opcion = input("¿Desea cambiar el nombre de la cancion?\n 1.Si\n 2.No\n")
                                            if opcion == '1':
                                                nombre = input("Ingrese el nuevo nombre de la cancion: \n")
                                                cambiarEstado = "update canciones set cancion = %s where codigo_cancion = %s"
                                                cursor.execute(cambiarEstado,(nombre,historial,))
                                                engine.commit()
                                                cursor.close()
                                                print("Cancion Modificada")
                                                bandera = False
                                            if opcion == '2':
                                                bandera = False
                                                
                                        
                                    if opcion == "5":
                                        bandera = True
                                        cursor = engine.cursor()
                                        buscar = input("Nombre del artista\n")
                                        busqueda = "select nombre_artistico from artistas where nombre_artistico ilike %s"
                                        formatear = '%{}%'.format(buscar)
                                        cursor.execute(busqueda,(formatear,))
                                        record = cursor.fetchall()                       
                                        for i in range (0,len(record)):
                                            print(str(i+1)+". "+str(record[i][0]))
                                        
                                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                                        codigoCancion = "select a.usuario from artistas a where a.nombre_artistico = %s"
                                        cursor.execute(codigoCancion,(str(record[cancion-1][0]),))
                                        histo = cursor.fetchall()
                                        historial = histo[0][0]
                        
                                        while bandera:
                                            opcion = input("¿Desea cambiar el nombre del artista?\n 1.Si\n 2.No\n")
                                            if opcion == '1':
                                                nombre = input("Ingrese el nuevo nombre del artista: \n")
                                                cambiarEstado = "update artistas set nombre_artistico = %s where usuario = %s"
                                                cursor.execute(cambiarEstado,(nombre,historial,))
                                                engine.commit()
                                                cursor.close()
                                                print("Artista Modificado")
                                                bandera = False
                                            if opcion == '2':
                                                bandera = False
                                    
                                    elif opcion == "6":
                                        bandera = True
                                        cursor = engine.cursor()
                                        buscar = input("Nombre del album\n")
                                        busqueda = "select nombre_artistico, album from albumes where album ilike %s"
                                        formatear = '%{}%'.format(buscar)
                                        cursor.execute(busqueda,(formatear,))
                                        record = cursor.fetchall()                       
                                        for i in range (0,len(record)):
                                            print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                                        
                                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                                        codigoCancion = "select codigo_album from albumes where album = %s"
                                        cursor.execute(codigoCancion,(buscar,))
                                        histo = cursor.fetchall()
                                        historial = histo[0][0]
                                        while bandera:
                                            opcion = input("¿Desea cambiar el nombre del album?\n 1.Si\n 2.No\n")
                                            if opcion == '1':
                                                nombre = input("Ingrese el nuevo nombre del album: \n")
                                                cambiarEstado = "update albumes set album = %s where codigo_album = %s"
                                                cursor.execute(cambiarEstado,(nombre,historial,))
                                                engine.commit()
                                                cursor.close()
                                                print("Album Modificado")
                                                bandera = False
                                            if opcion == '2':
                                                bandera = False
                                                
                                    elif(opcion =="7"):
                                        eliminarcancion()
                                        
                                    elif(opcion =="8"):
                                        eliminaralbum()
                                        
                                    elif(opcion =="9"):
                                        eliminarartista()
                                        
                                    elif(opcion == "10"):
                                        opcion = input(" 1.Albumes mas recientes de la ultima semana\n 2.Artistas con popularidad creciente en los ultimos tres meses\n 3.Cantidad de nuevas suscripciones mensuales durante los ultimos seis meses\n 4.Artistas con mayor producción musical\n 5.Generos mas populares\n 6.Usuarios mas activos en la plataforma\n")
                                        if(opcion == "1"):
                                            albumesmasrecientesultimasemana()
                                            
                                        elif(opcion =="2"):
                                            aumentopopularidad3meses()
                                        elif opcion == "3":
                                            cantidaddesuscripciones()
                                            
                                        elif(opcion =="4"):
                                            artistasmayorproduccion()
                                            
                                        elif(opcion == "5"):
                                            generosmaspopulares()
                                            
                                        elif(opcion =="6"):
                                            usuariosmasactivos()
                                        
                                    elif opcion == "11":
                                        playlist(usuario)
                                    elif opcion == "12":
                                        banderaAdmin = False
                                    
                        elif(len(nombreartistico) != 0):
                                                 
                                    
                            if(informacion[0][2] == 'premium'):
                                print('ADMINISTRADOR')
                                print('USUARIO PREMIUM')
                                print(nombreartistico[0][0])
                                bandera12 = True
                                while bandera12:
                                    opcion = input(" 1.Buscar\n 2.Registrar Album\n 3.Registrar Track\n 4.Inactivar cancion del catalogo\n 5.Modificar cancion\n 6.Modificar Artista\n 7.Modificar Album \n 8.Eliminar una cancion\n 9.Eliminar album\n 10.Eliminar artista\n 11.Reporteria\n 12.Playlist\n 13.Salir\n")
                                    
                                    if (opcion == "1"):
                                        menuprincipalPremium()
                                        
                                    elif (opcion == "2"):
                                        banderaAlbum = True
                                        nombrealbum = input("Ingresa el nombre del Album a registrar\n")
                                        while banderaAlbum:
                                            codigoalbum = str((random.randint(3, 100000)))
                                            query = "select codigo_album from albumes"
                                            cursor.execute(query)
                                            lista = cursor.fetchall()
                                            if codigoalbum not in lista:
                                                agregaralbum(nombrealbum, nombreartistico[0][0],codigoalbum)
                                                print("Album Agregado Correctamente")
                                                banderaAlbum = False
                                            else:
                                                banderaAlbum = True

                                            
                                    elif (opcion == "3"):
                                        banderaCancion = True
                                        cancion = input('Ingresa el nombre de la cancion a registrar\n')
                                        while banderaCancion:
                                            codigocancion = (random.randint(3, 100000))
                                            query = "select codigo_cancion from canciones"
                                            cursor.execute(query)
                                            lista = cursor.fetchall()
                                            if codigocancion not in lista:
                                                banderaCancion = False
                                                generos = []
                                                while True:
                                                    print("Ingresa el numero del genero o generos a elegir o ingresa '0' para concluir con los generos\n")
                                                    for x in range (len(mostrargeneros())):
                                                        print(str(x+1) + ". " + mostrargeneros()[x][0])
                                                    generoelegido = int(input())
                                                    

                                                    if(len(generos) != 0 and generoelegido == 0 ):                                
                                                        break
                                                    
                                                    elif (mostrargeneros()[generoelegido-1][0] not in generos and generoelegido != 0):
                                                        generos.append(mostrargeneros()[generoelegido-1][0])
                                                        print("Genero agregado")
                                                    else:
                                                        print("Genero ya habia sido agregado anteriormente")
                                                opcion = input(" 1.Agregar en album existente\n 2.Agregar como sencillo\n ")
                                                if(opcion == "1"):
                                                    if(len(seleccionaralbumdeartista(nombreartistico[0][0])) !=0):       
                                                        for x in range (len(seleccionaralbumdeartista(nombreartistico[0][0]))):
                                                            print(str(x+1) + ". " + seleccionaralbumdeartista(nombreartistico[0][0])[x][0] + ", " +seleccionaralbumdeartista(nombreartistico[0][0])[x][2])
                                                            
                                                        albumelegido = int(input("Ingresa el numero del album en el que la agregaras\n"))
                                                        agregarcancion(cancion, codigocancion)
                                                        agregarcanciongenero(codigocancion, generos)
                                                        agregarcancionartista(codigocancion, nombreartistico[0][0])
                                                        ingresaralbumcancion(codigocancion, seleccionaralbumdeartista(nombreartistico[0][0])[albumelegido-1][3])
                                                        print("Cancion Agregada Correctamente")
                                                        
                                                    else:
                                                        print("No tienes ningun album creado, primero crea uno o agrega cancion como sencillo")
                                                        
                                                if(opcion == "2"):
                                                    agregarcancion(cancion, codigocancion)
                                                    agregarcanciongenero(codigocancion, generos)
                                                    agregarcancionartista(codigocancion, nombreartistico[0][0])
                                                    banderaAlbum = True
                                                    while banderaAlbum:
                                                        codigoalbum = str((random.randint(3, 100000)))
                                                        query = "select codigo_album from albumes"
                                                        cursor.execute(query)
                                                        lista = cursor.fetchall()
                                                        if codigoalbum not in lista:
                                                            agregaralbum(cancion, nombreartistico[0][0], codigoalbum)
                                                            ingresaralbumcancion(codigocancion, codigoalbum)
                                                            print("Cancion Agregada Correctamente")
                                                            banderaAlbum = False
                                                        else:
                                                            banderaAlbum = True
                                            else:
                                                banderaCancion = True
                                            
                                    
                                    if opcion =="4":
                                        cursor = engine.cursor()
                                        buscar = input("Nombre de la cancion\n")
                                        busqueda ="select t.nombre_artistico,(select c.cancion from canciones c where c.cancion ilike %s and c.codigo_cancion = t.codigo_cancion and c.estado = 'activa') from tiene_artista_cancion t intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion and c2.estado ='activa') as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c where c.estado = 'activa')"
                                        formatear = '%{}%'.format(buscar)
                                        cursor.execute(busqueda,(formatear,))
                                        record = cursor.fetchall()                       
                                        for i in range (0,len(record)):
                                            print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                                        
                                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                                        codigoCancion = "select c.codigo_cancion from canciones c where c.cancion = %s"
                                        cursor.execute(codigoCancion,(record[cancion-1][1],))
                                        histo = cursor.fetchall()
                                        historial = histo[0][0]
                                        cambiarEstado = "update canciones set estado = 'inactiva' where codigo_cancion = %s"
                                        cursor.execute(cambiarEstado,(historial,))
                                        engine.commit()
                                        cursor.close()
                                        print("Cancion desactivada")
                                        
                                    if opcion =="5":
                                        bandera = True
                                        cursor = engine.cursor()
                                        buscar = input("Nombre de la cancion\n")
                                        busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion ilike %s and c.codigo_cancion = t.codigo_cancion) from tiene_artista_cancion t intersect select tac.nombre_artistico, (select c2.cancion  from canciones c2 where c2.codigo_cancion=tac.codigo_cancion ) as canciones from tiene_artista_cancion tac where tac.codigo_cancion in(select c.codigo_cancion from canciones c)"
                                        formatear = '%{}%'.format(buscar)
                                        cursor.execute(busqueda,(formatear,))
                                        record = cursor.fetchall()                       
                                        for i in range (0,len(record)):
                                            print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                                        
                                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                                        codigoCancion = "select c.codigo_cancion from canciones c where c.cancion = %s"
                                        cursor.execute(codigoCancion,(record[cancion-1][1],))
                                        histo = cursor.fetchall()
                                        historial = histo[0][0]
                                        while bandera:
                                            opcion = input("¿Desea cambiar el nombre de la cancion?\n 1.Si\n 2.No\n")
                                            if opcion == '1':
                                                nombre = input("Ingrese el nuevo nombre de la cancion: \n")
                                                cambiarEstado = "update canciones set cancion = %s where codigo_cancion = %s"
                                                cursor.execute(cambiarEstado,(nombre,historial,))
                                                engine.commit()
                                                cursor.close()
                                                print("Cancion Modificada")
                                                bandera = False
                                            if opcion == '2':
                                                bandera = False
                                    
                                    if opcion =="7":
                                        bandera = True
                                        cursor = engine.cursor()
                                        buscar = input("Nombre del album\n")
                                        busqueda = "select nombre_artistico, album from albumes where album ilike %s"
                                        formatear = '%{}%'.format(buscar)
                                        cursor.execute(busqueda,(formatear,))
                                        record = cursor.fetchall()                       
                                        for i in range (0,len(record)):
                                            print(str(i+1)+". "+str(record[i][0])+", "+str(record[i][1]))
                                        
                                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                                        codigoCancion = "select codigo_album from albumes where album = %s"
                                        cursor.execute(codigoCancion,(record[cancion-1][1],))
                                        histo = cursor.fetchall()
                                        historial = histo[0][0]
                                        while bandera:
                                            opcion = input("¿Desea cambiar el nombre del album?\n 1.Si\n 2.No\n")
                                            if opcion == '1':
                                                nombre = input("Ingrese el nuevo nombre del album: \n")
                                                cambiarEstado = "update albumes set album = %s where codigo_album = %s"
                                                cursor.execute(cambiarEstado,(nombre,historial,))
                                                engine.commit()
                                                cursor.close()
                                                print("Album Modificado")
                                                bandera = False
                                            if opcion == '2':
                                                bandera = False
                                         
                                            
                                        
                                    if opcion == "6":
                                        bandera = True
                                        cursor = engine.cursor()
                                        buscar = input("Nombre del artista\n")
                                        busqueda = "select nombre_artistico from artistas where nombre_artistico ilike %s"
                                        formatear = '%{}%'.format(buscar)
                                        cursor.execute(busqueda,(formatear,))
                                        record = cursor.fetchall()                       
                                        for i in range (0,len(record)):
                                            print(str(i+1)+". "+str(record[i][0]))
                                        
                                        cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                                        codigoCancion = "select a.usuario from artistas a where a.nombre_artistico = %s"
                                        cursor.execute(codigoCancion,(record[cancion-1][0],))
                                        histo = cursor.fetchall()
                                        historial = histo[0][0]
                                        
                                        while bandera:
                                            opcion = input("¿Desea cambiar el nombre del artista?\n 1.Si\n 2.No\n")
                                            if opcion == '1':
                                                nombre = input("Ingrese el nuevo nombre del artista: \n")
                                                cambiarEstado = "update artistas set nombre_artistico = %s where usuario = %s"
                                                cursor.execute(cambiarEstado,(nombre,historial,))
                                                engine.commit()
                                                cursor.close()
                                                bandera = False
                                                print("Artista Modificado")
                                            if opcion == '2':
                                                bandera = False
                                            
                                    elif(opcion =="8"):
                                        eliminarcancion()
                                        
                                    elif(opcion =="9"):
                                        eliminaralbum()
                                        
                                    elif(opcion =="10"):
                                        eliminarartista()
                                        
                                    elif(opcion == "11"):
                                        opcion = input(" 1.Albumes mas recientes de la ultima semana\n 2.Artistas con popularidad creciente en los ultimos tres meses\n 3.Cantidad de nuevas suscripciones mensuales durante los ultimos seis meses\n 4.Artistas con mayor producción musical\n 5.Generos mas populares\n 6.Usuarios mas activos en la plataforma\n")
                                        if(opcion == "1"):
                                            albumesmasrecientesultimasemana()
                                            
                                        elif(opcion =="2"):
                                            aumentopopularidad3meses()
                                            
                                        elif opcion == "3":
                                            cantidaddesuscripciones()
                                            
                                        elif(opcion =="4"):
                                            artistasmayorproduccion()
                                            
                                        elif(opcion == "5"):
                                            generosmaspopulares()
                                            
                                        elif(opcion =="6"):
                                            usuariosmasactivos()
                                    elif opcion == "12":
                                        playlist(usuario)
                                    elif opcion == "13":
                                        bandera12 = False
                                                                                            
                                
                else:
                    print("Contrasena incorrecta")
            else:
                print("Usuario no existe")
    if opcionTotal == "3":
        banderaTotal = False
        print("Vuelve pronto")

                                   
