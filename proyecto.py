from psycopg2 import *
from datetime import date
engine = connect(
    database="proyecto1datos",
    user="postgres",
    password="guidoraro",
    host="database-1.ciahoptmomix.us-east-2.rds.amazonaws.com",
    port='5432'
)




def comprobariniciosesion(usuario):
    cursor = engine.cursor()
    #seleccionar = """Select usuario, contrasena from  usuarios where usuario =%s"""
    cursor.execute("Select usuario, contrasena from  usuarios where usuario =" + usuario)
    record = cursor.fetchall()
    
    return record

def registrarse(usuario, contrasenaConfirmacion, nombre, suscripcion):
    today =  date.today()
    cursor = engine.cursor()
    insertar =  """ INSERT INTO usuarios(usuario, contrasena, nombre, suscripcion, fecha_inicio_suscripcion, tipo) VALUES (%s,%s,%s,%s,%s,%s)"""
    datos = (usuario, contrasenaConfirmacion, nombre, suscripcion, today, 'Usuario')
    cursor.execute(insertar, datos)
    engine.commit()

    

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
        
    if(len(comprobariniciosesion("'"+usuario+ "'")) == 0):
        registrarse(usuario, contrasenaConfirmacion, nombre, suscripcion)
    else:
        print("usuario ya existe")
    
        



if opcion =='2':
    usuario=input('Ingrese su usuario\n ')  
    if(len(comprobariniciosesion("'"+usuario+ "'")) != 0):
        contrasena= input('Ingrese su contraseña\n')
        if(comprobariniciosesion("'"+usuario+ "'")[0][1] == contrasena):
            print("Contrasena correcta")
        else:
            print("Contrasena incorrecta")
    else:
        print("Usuario no existe")



