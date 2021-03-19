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
    
def menuprincipal():
    cursor = engine.cursor()
    saludo = "select nombre from usuarios where usuario = %s"
    cursor.execute(saludo,(usuario,))
    record = cursor.fetchall()
    print("Bienvenido "+ str(record))
    opcion = input("Buscar:\n 1.Cancion \n 2.Artista \n 3.Genero \n 4.Album\n 5.Salir\n")
    while (True):
        if opcion = '1':
            buscar = input("Nombre de la cancion\n")
            busqueda = "select cancion from canciones where cancion = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            print("Resultado:\n"+str(record))
            #abrir cancion youtube
        if opcion = '2':
            buscar = input("Nombre del Artista\n")
            busqueda = "select nombre_artistico from artistas where nombre_artistico = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            print("Resultado:\n"+str(record))
            #abrir cancion youtube
        if opcion = '3':
            buscar = input("Nombre del Genero\n")
            busqueda = "select genero from generos where genero = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            print("Resultado:\n"+str(record))
            #abrir cancion youtube
        if opcion = '4':
            buscar = input("Nombre del Album\n")
            busqueda = "select album from albumes where album = %s"
            cursor.execute(busqueda,(buscar,))
            record = cursor.fetchall()
            print("Resultado:\n"+str(record))
            #abrir cancion youtube
        if opcion = '5':
            False

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
            
            if(informacion[0][2] == 'gratis'):
                print('USUARIO GRATIS')
                opcion = input(" 1.Buscar\n 2.Actualizar Suscripcion\n ")
                
                if opcion == "1":
                    menuprincipal()
                    
                elif(opcion == "2"):
                    actualizarSuscripcion(usuario)
                    print("Suscripcion Actualizada")
                    
                
            elif(informacion[0][2] == 'premium'):
                print('USUARIO PREMIUM')            
                opcion = input(" 1.Buscar\n ")
                if opcion == "1":
                    menuprincipal()
        else:
            print("Contrasena incorrecta")
    else:
        print("Usuario no existe")
