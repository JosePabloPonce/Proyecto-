from psycopg2 import *
from datetime import date
import pywhatkit as kit


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

def agregaralbum(albumnombre, nombreartista):
    today =  date.today()
    cursor = engine.cursor()
    insertar =  " INSERT INTO albumes VALUES (%s,%s,%s)"
    datos = (albumnombre, today, nombreartista)
    cursor.execute(insertar, datos)
    engine.commit()

def chequearalbum(albumnombre):
    cursor = engine.cursor()
    seleccionar ="select * from albumes where album = %s"
    cursor.execute(seleccionar, (albumnombre,))
    record = cursor.fetchall()
    return record


opcion = input(" 1. Sign Up\n 2. Login\n")
if opcion == '1':
    nombre = input("Ingrese su nombre\n")
    usuarios = input("Ingrese un usuario\n")
    contrasena = input("Ingrese su contrasena\n")
    contrasenaConfirmacion = input("Ingrese nuevamente su contrasena\n")
    suscripcion = input("Seleccione el tipo de suscripcion\n1. Gratis \n2. Premium\n")
    if(suscripcion == '1'):
        suscripcion = 'gratis'
    elif(suscripcion =='2'):
        suscripcion = 'premium'
        
    if(len(comprobariniciosesion("'"+usuario+ "'")) == 0):
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
                        print("afag")
                        
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
                        print("afag")
                    
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
                        print("afag")
                        
                    elif(opcion == "2"):
                        actualizarSuscripcion(usuario)
                        print("Suscripcion Actualizada")
                        
                    elif(opcion =="3"):
                        nombrealbum = input("Ingresa del Album a registrar\n")
                        if(len(chequearalbum(albumnombre)) == 0):
                            agregaralbum(nombrealbum, nombreartistico[0][0])
                            print("Album Agregado Correctamente")
        
                        elif(len(chequearalbum(albumnombre)) != 0):
                            print("Album con dicho nombre ya existe")                        
                        
                elif(informacion[0][2] == 'premium'):
                    print('USUARIO PREMIUM')
                    print(nombreartistico[0][0])
                    opcion = input(" 1.Buscar\n 2.Registrar Album\n 3.Registrar Track\n")
                    if (opcion == "1"):
                        print("afag")
                    elif (opcion == "2"):
                        nombrealbum = input("Ingresa del Album a registrar\n")
                        if(len(chequearalbum(nombrealbum)) == 0):
                            agregaralbum(nombrealbum, nombreartistico[0][0])
                            print("Album Agregado Correctamente")
        
                        elif(len(chequearalbum(nombrealbum)) != 0):
                            print("Album con dicho nombre ya existe")
                            
                
        else:
            print("Contrasena incorrecta")
    else:
        print("Usuario no existe")


