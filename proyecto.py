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
    cursor = engine.cursor()
    actualizar = "Update usuarios set suscripcion = %s where usuario = %s"
    cursor.execute(actualizar, ('premium',usuario))
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
    print(conteo[0][0])
    if conteo[0][0] == 3:
        return False
    else:
        today =  date.today()   
        codigoescucha = str((random.randint(3, 100000)))
        insertar = "insert into historial values (%s,%s,%s,%s)"
        #cancionAlDia = "update historial set usuario = (%s), fecha_escuchada = (%s), codigo_escucha =(%s), codigo_cancion =(%s)"
        datos = (today,codigoescucha,codigo_cancion,usuario)
        cursor.execute(insertar,datos)
        engine.commit()
        return True
        
def insertarcanciondiaPremium(usuario,codigo_cancion):
    cursor = engine.cursor()
    today =  date.today()   
    codigoescucha = str((random.randint(3, 100000)))
    insertar = "insert into historial values (%s,%s,%s,%s)"
    #cancionAlDia = "update historial set usuario = (%s), fecha_escuchada = (%s), codigo_escucha =(%s), codigo_cancion =(%s)"
    datos = (today,codigoescucha,codigo_cancion,usuario)
    cursor.execute(insertar,datos)
    engine.commit()
        
           

    
    
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
            buscar = input("Nombre de la cancion\n")
            busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion = %s and c.codigo_cancion = t.codigo_cancion) from tiene_artista_cancion t where t.codigo_cancion in (select c.codigo_cancion from canciones c where c.cancion = %s)"
            cursor.execute(busqueda,(buscar,buscar,))
            record = cursor.fetchall()                       
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i]))
            
            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
            codigoCancion = "select c.codigo_cancion from canciones c where c.cancion = %s"
            cursor.execute(codigoCancion,(buscar,))
            histo = cursor.fetchall()
            historial = histo[0][0]
            if(insertarcanciondiaNoPremium(usuario,historial)):
                kit.playonyt(str(record[cancion-1]))
            else:
                print("Ya no puedes reproducir mas canciones")
            #abrir cancion youtube
        if opcion == '2':
            buscar = input("Nombre del Artista\n")
            busqueda = "select nombre_artistico from artistas where nombre_artistico = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i][0]))
                
            artista = int(input("Ingrese la opcion de artista:\n"))
            eleccion = str(record[artista-1][0])
            cancion = "select c.cancion from canciones c where c.codigo_cancion in (select t.codigo_cancion from tiene_artista_cancion t where t.nombre_artistico = %s)"
            cursor.execute(cancion,(eleccion,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+eleccion+" "+str(record[i][0]))
                
            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
            codigoCancion = "select c.codigo_cancion from canciones c where c.codigo_cancion in(select t.codigo_cancion from tiene_artista_cancion t where t.nombre_artistico = %s)"
            cursor.execute(codigoCancion,(buscar,))
            histo = cursor.fetchall()
            historial = histo[0][0]
            if(insertarcanciondiaNoPremium(usuario,historial)):
                kit.playonyt(str(record[cancion-1]))
            else:
                print("Ya no puedes reproducir mas canciones")
            #abrir cancion youtube
        if opcion == '3':
            buscar = input("Nombre del Genero\n")
            busqueda = "select genero from generos where genero = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i][0]))
                
            artista = int(input("Ingrese la opcion de genero:\n"))
            eleccion = str(record[artista-1][0])
            cancion = "select t.nombre_artistico,(select c.cancion from canciones c where c.codigo_cancion in (select t2.codigo_cancion from tiene_genero_cancion t2 where t2.genero = %s)limit 1) from tiene_artista_cancion t"
            cursor.execute(cancion,(eleccion,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i]))
                
            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
            codigoCancion = "select c.codigo_cancion from canciones c where c.codigo_cancion in (select t.codigo_cancion from tiene_genero_cancion t where t.genero = %s)"
            cursor.execute(codigoCancion,(buscar,))
            histo = cursor.fetchall()
            historial = histo[0][0]
            if(insertarcanciondiaNoPremium(usuario,historial)):
                kit.playonyt(str(record[cancion-1]))
            else:
                print("Ya no puedes reproducir mas canciones")
            #abrir cancion youtube
        if opcion == '4':
            buscar = input("Nombre del Album\n")
            busqueda = "select album from albumes where album = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i][0]))
                
            artista = int(input("Ingrese la opcion de album:\n"))
            eleccion = str(record[artista-1][0])
            print(eleccion)
            cancion = "select t.nombre_artistico,(select c.cancion from canciones c where c.codigo_cancion in (select t2.codigo_cancion from tiene_album_cancion t2 where t2.codigo_album in (select t3.codigo_album from albumes t3 where t3.album = %s))) from tiene_artista_cancion t where t.codigo_cancion in (select c.codigo_cancion from canciones c where c.codigo_cancion in (select t2.codigo_cancion from tiene_album_cancion t2 where t2.codigo_album in (select t3.codigo_album from albumes t3 where t3.album = %s)))"
            cursor.execute(cancion,(eleccion,eleccion,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i]))
                
            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
            codigoCancion = "select c.codigo_cancion from canciones c where c.codigo_cancion in (select t.codigo_cancion from tiene_album_cancion t where t.codigo_album in (select t2.codigo_album from albumes t2 where t2.album = %s)) "
            cursor.execute(codigoCancion,(buscar,))
            histo = cursor.fetchall()
            historial = histo[0][0]
            if(insertarcanciondiaNoPremium(usuario,historial)):
                kit.playonyt(str(record[cancion-1]))
            else:
                print("Ya no puedes reproducir mas canciones")
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
    bandera = True
    bandera2 = True
    while menu:
        opcion = input("Buscar:\n 1.Cancion \n 2.Artista \n 3.Genero \n 4.Album\n 5.Anadir Playlist\n 6.Salir\n")
        if opcion == '1':
            buscar = input("Nombre de la cancion\n")
            busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion = %s and c.codigo_cancion = t.codigo_cancion) from tiene_artista_cancion t where t.codigo_cancion in (select c.codigo_cancion from canciones c where c.cancion = %s)"
            cursor.execute(busqueda,(buscar,buscar,))
            record = cursor.fetchall()                       
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i]))
            
            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
            codigoCancion = "select c.codigo_cancion from canciones c where c.cancion = %s"
            cursor.execute(codigoCancion,(buscar,))
            histo = cursor.fetchall()
            historial = histo[0][0]
            insertarcanciondiaPremium(usuario,historial)
            kit.playonyt(str(record[cancion-1]))
            
            #abrir cancion youtube
        if opcion == '2':
            buscar = input("Nombre del Artista\n")
            busqueda = "select nombre_artistico from artistas where nombre_artistico = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i][0]))
                
            artista = int(input("Ingrese la opcion de artista:\n"))
            eleccion = str(record[artista-1][0])
            cancion = "select c.cancion from canciones c where c.codigo_cancion in (select t.codigo_cancion from tiene_artista_cancion t where t.nombre_artistico = %s)"
            cursor.execute(cancion,(eleccion,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+eleccion+" "+str(record[i][0]))
                
            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
            codigoCancion = "select c.codigo_cancion from canciones c where c.codigo_cancion in(select t.codigo_cancion from tiene_artista_cancion t where t.nombre_artistico = %s)"
            cursor.execute(codigoCancion,(buscar,))
            histo = cursor.fetchall()
            historial = histo[0][0]
            insertarcanciondiaPremium(usuario,historial)
            kit.playonyt(str(record[cancion-1]))
            #abrir cancion youtube
        if opcion == '3':
            buscar = input("Nombre del Genero\n")
            busqueda = "select genero from generos where genero = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i][0]))
                
            artista = int(input("Ingrese la opcion de genero:\n"))
            eleccion = str(record[artista-1][0])
            cancion = "select t.nombre_artistico,(select c.cancion from canciones c where c.codigo_cancion in (select t2.codigo_cancion from tiene_genero_cancion t2 where t2.genero = %s)limit 1) from tiene_artista_cancion t"
            cursor.execute(cancion,(eleccion,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i]))
                
            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
            codigoCancion = "select c.codigo_cancion from canciones c where c.codigo_cancion in (select t.codigo_cancion from tiene_genero_cancion t where t.genero = %s)"
            cursor.execute(codigoCancion,(buscar,))
            histo = cursor.fetchall()
            historial = histo[0][0]
            insertarcanciondiaPremium(usuario,historial)
            kit.playonyt(str(record[cancion-1]))
            #abrir cancion youtube
        if opcion == '4':
            buscar = input("Nombre del Album\n")
            busqueda = "select album from albumes where album = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i][0]))
                
            artista = int(input("Ingrese la opcion de album:\n"))
            eleccion = str(record[artista-1][0])
            print(eleccion)
            cancion = "select t.nombre_artistico,(select c.cancion from canciones c where c.codigo_cancion in (select t2.codigo_cancion from tiene_album_cancion t2 where t2.codigo_album in (select t3.codigo_album from albumes t3 where t3.album = %s))) from tiene_artista_cancion t where t.codigo_cancion in (select c.codigo_cancion from canciones c where c.codigo_cancion in (select t2.codigo_cancion from tiene_album_cancion t2 where t2.codigo_album in (select t3.codigo_album from albumes t3 where t3.album = %s)))"
            cursor.execute(cancion,(eleccion,eleccion,))
            record = cursor.fetchall()
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i]))
                
            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
            codigoCancion = "select c.codigo_cancion from canciones c where c.codigo_cancion in (select t.codigo_cancion from tiene_album_cancion t where t.codigo_album in (select t2.codigo_album from albumes t2 where t2.album = %s))"
            cursor.execute(codigoCancion,(buscar,))
            histo = cursor.fetchall()
            historial = histo[0][0]
            insertarcanciondiaPremium(usuario,historial)
            kit.playonyt(str(record[cancion-1]))
            #abrir cancion youtube
        if opcion == '5':
            while bandera:
                opcion = input("1.Anadir Playlist \n 2.Ver Playlists \n 3. Salir\n")
                if opcion == '1':
                    nombre = input("Ingrese el nombre de la playlist:\n")
                    codigoplaylist = str((random.randint(3, 100000)))
                    insertar = "insert into playlists values(%s,%s,%s)"
                    datos = (nombre, codigoplaylist, usuario)
                    cursor.execute(insertar, datos)
                    engine.commit()
                    
                if opcion == '2':
                    verPlaylist = "select nombre from playlists"
                    cursor.execute(verPlaylist)
                    record = cursor.fetchall()
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0]))
                        
                    artista = int(input("Ingrese la opcion de playlist:\n"))
                    eleccion = str(record[artista-1][0])
                    print(eleccion)
                    query = "select c.cancion from canciones c where c.codigo_cancion in (select t.codigo_cancion from tiene_playlist_cancion t where t.codigo_playlist in (select t2.codigo_playlist from playlists t2 where t2.nombre = %s))"
                    cursor.execute(query,(eleccion,))
                    record = cursor.fetchall()
                    print("Canciones que tiene la playlist:\n")
                    for i in range (0,len(record)):
                        print(str(i+1)+". "+str(record[i][0]))
                        
                    cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                    codigoCancion = "select c.codigo_cancion from canciones c where c.cancion = %s"
                    cursor.execute(codigoCancion,(record[cancion-1],))
                    histo = cursor.fetchall()
                    historial = histo[0][0]
                    insertarcanciondiaPremium(usuario,historial)
                    kit.playonyt(str(record[cancion-1]))
                    
                    while bandera2:
                        opcion = input("¿Desea añadir mas canciones?\n 1. Si\n 2. No\n")
                        if opcion == '1':
                            buscar = input("Nombre de la cancion\n")
                            busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion = %s and c.codigo_cancion = t.codigo_cancion) from tiene_artista_cancion t where t.codigo_cancion in (select c.codigo_cancion from canciones c where c.cancion = %s)"
                            cursor.execute(busqueda,(buscar,buscar,))
                            record = cursor.fetchall()                       
                            for i in range (0,len(record)):
                                print(str(i+1)+". "+str(record[i]))
                            
                            print(eleccion)
                            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
                            can = str(record[cancion-1][1])
                            print(can)
                            codigoCancion = "select c.codigo_cancion from canciones c where c.cancion = %s"
                            cursor.execute(codigoCancion,(can,))
                            recordCancion = cursor.fetchall()
                            codigoPlaylist = "select c.codigo_playlist from playlists c where c.nombre = %s"
                            cursor.execute(codigoPlaylist,(eleccion,))
                            recordPlaylist = cursor.fetchall()
                            insertar = "insert into tiene_playlist_cancion values(%s,%s)"
                            datos = (recordCancion[0][0],recordPlaylist[0][0])
                            cursor.execute(insertar, datos)
                            engine.commit()
                        if opcion == '2':
                            bandera2 = False
                    
                if opcion == '3':
                    bandera = False
                    
                
            
            
        if opcion == '6':
            print("Adios")
            menu = False
 
    
def eliminarcancion():

        cursor = engine.cursor()
        buscar = input("Ingresa el Nombre del Artista de la Cancion\n")
        busqueda = "select nombre_artistico from artistas where nombre_artistico = %s"
        cursor.execute(busqueda,(buscar,))
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
        busqueda = "select album, codigo_album from albumes where album = %s"
        cursor.execute(busqueda,(buscar,))
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
        busqueda = "select nombre_artistico from artistas where nombre_artistico = %s"
        cursor.execute(busqueda,(buscar,))
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



opcion = input(" 1. Sign Up\n 2. Login\n")
if opcion == '1':
    nombre = input("Ingrese su nombre\n")
    usuario = input("Ingrese un usuario\n")
    contrasena = input("Ingrese su contrasena\n")
    contrasenaConfirmacion = input("Ingrese nuevamente su contrasena\n")
    suscripcion = input("Seleccione el tipo de suscripcion\n1. Gratis \n2. Premium\n")
    if(suscripcion == '1'):
        suscripcion = 'gratis'
    elif(suscripcion =='2'):
        suscripcion = 'premium'
        
    if(len(comprobariniciosesion(usuario)) == 0):
        registrarse(usuario, contrasenaConfirmacion, nombre, suscripcion)
    else:
        print("usuario ya existe")
    
        
if opcion =='2':
    usuario=input('Ingrese su usuario\n ')
    informacion = comprobariniciosesion(usuario)
    if(len(informacion) != 0):
        contrasena= input('Ingrese su contraseña\n')
        if(informacion[0][1] == contrasena):
            print("Contrasena correcta\n")
            nombreartistico = esartista(usuario)
            if(informacion[0][3] == 'Usuario'):
                if(len(nombreartistico) == 0):
                    if(informacion[0][2] == 'gratis'):
                        print('USUARIO GRATIS')
                        opcion = input(" 1.Buscar\n 2.Actualizar Suscripcion\n, 3.Darse de alta como Artista o Manager\n")
            
                        if opcion == "1":
                            menuprincipalNoPremium()
                            
                        elif(opcion == "2"):
                            actualizarSuscripcion(usuario)
                            print("Suscripcion Actualizada")
                            
                        elif(opcion =="3"):
                            nombreartistico = input("Ingresa tu nombre Artistico\n")
                            if(len(chequearartista(nombreartistico)) != 0):
                                print("Nombre artistico en uso")
                                
                            elif(len(chequearartista(nombreartistico)) == 0):
                                agregarartista(nombreartistico, usuario)
                                print("Nombre Artistico Agregado")
                            
                            
                    elif(informacion[0][2] == 'premium'):
                        print('USUARIO PREMIUM')            
                        opcion = input(" 1.Buscar\n 2.Darse de alta como Artista o Manager\n")
                        if opcion == "1":
                            menuprincipalPremium()
                        
                        elif(opcion =="2"):
                            nombreartistico = input("Ingresa tu nombre Artistico\n")
                            if(len(chequearartista(nombreartistico)) != 0):
                                print("Nombre artistico en uso")
                                
                            elif(len(chequearartista(nombreartistico)) == 0):
                                agregarartista(nombreartistico, usuario)
                                print("Nombre Artistico Agregado")                    
                            
                elif(len(nombreartistico) != 0):
                    if(informacion[0][2] == 'gratis'):
                        print('USUARIO GRATIS')
                        print(nombreartistico[0][0])
                        opcion = input(" 1.Buscar\n 2.Actualizar Suscripcion\n 3.Registrar Album\n 4.Registrar Track\n")
                        if opcion == "1":
                            menuprincipalNoPremium()
                            
                        elif(opcion == "2"):
                            actualizarSuscripcion(usuario)
                            print("Suscripcion Actualizada")
                            
                        elif(opcion =="3"):
                            nombrealbum = input("Ingresa el nombre del Album a registrar\n")
                            codigoalbum = str((random.randint(3, 100000)))
                            agregaralbum(nombrealbum, nombreartistico[0][0], codigoalbum)
                            print("Album Agregado Correctamente")
                        
                        elif(opcion =="4"):
                            cancion = input('Ingresa el nombre de la cancion a registrar\n')
                            codigocancion = (random.randint(3, 100000))
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
                                codigoalbum = str((random.randint(3, 100000)))
                                agregaralbum(cancion, nombreartistico[0][0], codigoalbum)
                                ingresaralbumcancion(codigocancion, codigoalbum)
                                print("Cancion Agregada Correctamente")  
                            
            
                           
                            
                    elif(informacion[0][2] == 'premium'):
                        print('USUARIO PREMIUM')
                        print(nombreartistico[0][0])
                        opcion = input(" 1.Buscar\n 2.Registrar Album\n 3.Registrar Track\n")
                        
                        if (opcion == "1"):
                            menuprincipalPremium()
                            
                        elif (opcion == "2"):
                            nombrealbum = input("Ingresa el nombre del Album a registrar\n")
                            codigoalbum = str((random.randint(3, 100000)))
                            agregaralbum(nombrealbum, nombreartistico[0][0],codigoalbum)
                            print("Album Agregado Correctamente")

                                
                        elif (opcion == "3"):
                            cancion = input('Ingresa el nombre de la cancion a registrar\n')
                            codigocancion = (random.randint(3, 100000))
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
                                codigoalbum = str((random.randint(3, 100000)))
                                agregaralbum(cancion, nombreartistico[0][0], codigoalbum)
                                ingresaralbumcancion(codigocancion, codigoalbum)
                                print("Cancion Agregada Correctamente")
                                
            elif(informacion[0][3] == 'Administrador'):
                if(len(nombreartistico) == 0):      
                    if(informacion[0][2] == 'premium'):
                        print('ADMINISTRADOR')
                        print('USUARIO PREMIUM')            
                        opcion = input(" 1.Buscar\n 2.Darse de alta como Artista o Manager\n 3.Inactivar cancion del catalogo\n 4.Modificar cancion\n 5.Modificar Artista\n 6.Eliminar una cancion\n 7.Eliminar album\n 8.Eliminar artista\n")
                        if opcion == "1":
                            menuprincipalPremium()
                        
                        elif(opcion =="2"):
                            nombreartistico = input("Ingresa tu nombre Artistico\n")
                            if(len(chequearartista(nombreartistico)) != 0):
                                print("Nombre artistico en uso")
                                
                            elif(len(chequearartista(nombreartistico)) == 0):
                                agregarartista(nombreartistico, usuario)
                                print("Nombre Artistico Agregado")
                                
                            
                        elif(opcion =="6"):
                            eliminarcancion()
                            
                        elif(opcion =="7"):
                            eliminaralbum()
                            
                        elif(opcion =="8"):
                            eliminarartista()
                            
                            
                elif(len(nombreartistico) != 0):
                                         
                            
                    if(informacion[0][2] == 'premium'):
                        print('ADMINISTRADOR')
                        print('USUARIO PREMIUM')
                        print(nombreartistico[0][0])
                        opcion = input(" 1.Buscar\n 2.Registrar Album\n 3.Registrar Track\n 4.Inactivar cancion del catalogo\n 5.Modificar cancion\n 6.Modificar Artista\n 7.Eliminar una cancion\n 8.Eliminar album\n 9.Eliminar artista\n")
                        
                        if (opcion == "1"):
                            menuprincipalPremium()
                            
                        elif (opcion == "2"):
                            nombrealbum = input("Ingresa el nombre del Album a registrar\n")
                            codigoalbum = str((random.randint(3, 100000)))
                            agregaralbum(nombrealbum, nombreartistico[0][0],codigoalbum)
                            print("Album Agregado Correctamente")

                                
                        elif (opcion == "3"):
                            cancion = input('Ingresa el nombre de la cancion a registrar\n')
                            codigocancion = (random.randint(3, 100000))
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
                                codigoalbum = str((random.randint(3, 100000)))
                                agregaralbum(cancion, nombreartistico[0][0], codigoalbum)
                                ingresaralbumcancion(codigocancion, codigoalbum)
                                print("Cancion Agregada Correctamente")
                        
                                
                        elif(opcion =="7"):
                            eliminarcancion()
                            
                        elif(opcion =="8"):
                            eliminaralbum()
                            
                        elif(opcion =="9"):
                            eliminarartista()
                                                    
                        
        else:
            print("Contrasena incorrecta")
    else:
        print("Usuario no existe")
