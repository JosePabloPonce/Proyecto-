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
    seleccionar = "Select usuario, contrasena, suscripcion from  usuarios where usuario = %s"
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
    insertar =  " INSERT INTO canciones VALUES (%s,%s,%s,%s)"
    datos = (cancion, codigo, 0, today )
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

def insertarcancionaldia(usuario):
    cursor = engine.cursor()
    cancionAlDia = "select canciones_al_dia from usuarios where usuario = %s"
    cursor.execute(cancionAlDia, (usuario,))
    record = cursor.fetchall()
    if record[0][0] == 0 or None:
        insertar =  "update usuarios set canciones_al_dia = 1 WHERE usuario = (%s)"
        cursor.execute(insertar, [usuario])
        engine.commit()
        return True
    if record[0][0] == 1:
        insertar =  " update usuarios set canciones_al_dia =2 WHERE usuario = (%s)"
        cursor.execute(insertar, [usuario])
        engine.commit()
        return True
    if record[0][0] == 2:
        insertar =  " update usuarios set canciones_al_dia =3 WHERE usuario = (%s)"
        cursor.execute(insertar, [usuario])
        engine.commit()
        return True
    if record[0][0] == 3:
        return False

        
    

    
    
def menuprincipal():
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
            busqueda = "select t.nombre_artistico,(select c.cancion from canciones c where c.cancion = %s and c.codigo_cancion = t.codigo_cancion) from tiene_artista_cancion t"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()                       
            for i in range (0,len(record)):
                print(str(i+1)+". "+str(record[i]))
            
            cancion = int(input ("Ingrese el numero de opcion que desea:\n"))
            if(insertarcancionaldia(usuario)):
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
            if(insertarcancionaldia(usuario)):
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
            if(insertarcancionaldia(usuario)):
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
            if(insertarcancionaldia(usuario)):
                kit.playonyt(str(record[cancion-1]))
            else:
                print("Ya no puedes reproducir mas canciones")
            #abrir cancion youtube
        if opcion == '5':
            print("Adios")
            menu = False

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
            
            if(len(nombreartistico) == 0):
                if(informacion[0][2] == 'gratis'):
                    print('USUARIO GRATIS')
                    opcion = input(" 1.Buscar\n 2.Actualizar Suscripcion\n, 3.Darse de alta como Artista o Manager\n")
        
                    if opcion == "1":
                        menuprincipal()
                        
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
                        menuprincipal()
                    
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
                        menuprincipal()
                        
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
                        menuprincipal()
                        
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
                        
        else:
            print("Contrasena incorrecta")
    else:
        print("Usuario no existe")
