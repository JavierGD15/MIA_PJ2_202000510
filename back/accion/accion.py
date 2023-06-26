import base64
import os
import sys
import datetime
import shutil
from pathlib import Path
from datetime import datetime
from os import remove
from shutil import rmtree
from distutils.dir_util import copy_tree
import pyaes
import sys
sys.path.append(r'Archivos 2/back/accion')
from cloud.accion import Drive

# variables globales para guardar Configuracion de Archivos
tipoAlmacena = 0  # 1 = local , 2 = nube
encrypt_log = 0  # 1 = true , 2 = false
encrypt_read = 0  # 1 = true , 2 = false
llave = ''
# string llave para desencriptar.   Si se tiene los valores default , es porque no se ha ejecutado el comando configure

bitacora = []  # lista que lleva el registro de bitacora
_initPath = '/Archivos'  # carpeta donde se almacenaran localmente los archivos
drive = Drive()

# metodos estaticos (Comandos)-----------------------------------------------------------------------------------------
def variables_default():
    global tipoAlmacena
    global encrypt_log
    global encrypt_read
    global llave

    tipoAlmacena = 0
    encrypt_log = 0
    encrypt_read = 0
    llave = ''


def encriptar(_texto):
    global llave
    if _texto:
        if llave == '':
            raise Exception('No key ingresado o registrado')
        aes = pyaes.AESModeOfOperationCTR(llave.encode())
        return (base64.b64encode(aes.encrypt(_texto))).decode('utf-8')


def desencriptar(texto_encriptados):
    global llave
    if texto_encriptados:
        if llave == '':
            raise Exception('No key ingresado o registrado')
        aes = pyaes.AESModeOfOperationCTR(llave.encode())
        return (aes.decrypt(base64.b64decode(texto_encriptados))).decode('utf-8')


def guarda_registro(line, anio, mes, dia):  # metodo que registra log en archivo .txt

    global encrypt_log

    try:
        name = 'log_archivos.txt'
        ruta = '/logs/' + str(anio) + '/' + str(mes) + '/' + str(dia)
        # crea carpeta localmente
        home = Path.home()
        home = str(home) + _initPath + ruta
        home = home.replace('\\', '/')
        Path(home).mkdir(parents=True, exist_ok=True)

        # se crea el archivo localmente
        if encrypt_log == 1:
            # desencripta
            _texto = ''
            if Path(home + '/' + name).exists():  # hay que desencriptar
                file = open(home + '/' + name, "a")
                _texto = encriptar(line)
                file.write(_texto + '\n')
                file.close()
                # file = open(home + '/' + name, "r")
                # _texto = file.read()
                # _texto = desencriptar(_texto)
                # _texto = _texto + line + str('\n')
                # _texto = encriptar(_texto)
                # file = open(home + '/' + name, "w")
                # file.write(_texto)
                # file.close()

            else:
                file = open(home + '/' + name, "w")
                _texto = encriptar(line)
                file.write(_texto + '\n')
                file.close()

        else:  # en caso de que sea 2 o 0
            if Path(home + '/' + name).exists():
                file = open(home + '/' + name, "a")
            else:
                file = open(home + '/' + name, "w")

            file.write(line + '\n')
            file.close()

        return True

    except ValueError:
        print("Exception : Invalid key size")
        return False
    finally:
        return True


def inserta_bitacora_general(tipo, comando, parametros):
    global bitacora

    mes = str(datetime.now().strftime('%m'))
    dia = str(datetime.now().strftime('%d'))
    _now = datetime.now()

    hora_actual = '' + str(datetime.now())

    if tipo == "Input":
        tipo = tipo + ' '

    if len(comando) < 9:
        for i in range(len(comando), 9):
            comando += ' '

    hora_actual += '  --  ' + tipo + '  --  ' + comando + '  --  ' + parametros
    bitacora.append(hora_actual)
    guarda_registro(hora_actual, _now.year, mes, dia)
    return True


def configure(_tipo, encrypt, _encrypt_read, _llave=''):
    global tipoAlmacena
    global encrypt_log
    global encrypt_read
    global llave

    inserta_bitacora_general('Input', 'Configure', 'type: ' + str(_tipo) + ' | encrypt_log: ' + str(encrypt) +
                             ' | encrypt_read: ' + str(_encrypt_read) + ' | llave: ' + str(_llave))

    _tipo = _tipo.lower()
    encrypt = encrypt.lower()
    _encrypt_read = _encrypt_read.lower()

    if _tipo == 'local':
        tipoAlmacena = 1
    elif _tipo == 'cloud':
        tipoAlmacena = 2
    else:
        variables_default()
        inserta_bitacora_general('Output', 'Configure', 'Error : Tipo de Almacenamiento incorrecto')
        return False

    if encrypt == 'true':
        encrypt_log = 1
    elif encrypt == 'false':
        encrypt_log = 2
    else:
        variables_default()
        inserta_bitacora_general('Output', 'Configure', 'Error : Tipo de encriptación no valido')
        return False

    if _encrypt_read == 'true':
        encrypt_read = 1
    elif _encrypt_read == 'false':
        encrypt_read = 2
    else:
        variables_default()
        inserta_bitacora_general('Output', 'Configure', 'Error : Tipo de encriptación no valido')
        return False

    llave = _llave
    inserta_bitacora_general('Output', 'Configure', 'Configuración de sistema de archivos exitosa')
    return True


def create(_name, _body, _path):
    global _initPath

    if _path == '':
        _path += '/'

    inserta_bitacora_general('Input', 'Create', 'name: ' + str(_name) + ' | body: ' + str(_body) +
                             ' | path: ' + str(_path))

    # para crear crea carpeta

    try:
        if tipoAlmacena == 1:

            # crea carpeta localmente
            home = Path.home()
            home = str(home) + _initPath + _path
            home = home.replace("\\", "/")
            Path(home).mkdir(parents=True, exist_ok=True)

            # se crea el archivo localmente
            if Path(home + _name).exists():
                inserta_bitacora_general('Output', 'Create', 'Error : Archivo ya existe')
                return False

            file = open(home + _name, "w")
            file.write(_body)
            file.close()
            inserta_bitacora_general('Output', 'Create', 'Archivo Creado exitosamente')
            return True

        elif tipoAlmacena == 2:
            msj = drive.create(_path, _name, _body)
            inserta_bitacora_general('Output', 'Create', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Create', 'Error : Comando Configure no ejecutado')
            return False

    except Exception as e:
        
        print(f"Error al agregar contenido al archivosssss: {e}")
        inserta_bitacora_general('Output', 'Create', 'Error en metodo Create , error al crear Archivo ')
        return False


def delete(_path, _name=''):
    global _initPath
    if _path == '':
        _path += '/'

    inserta_bitacora_general('Input', 'Delete', 'path: ' + str(_path) + ' | name: ' + str(_name))
    try:
        if tipoAlmacena == 1:  # operacion local

            # crea carpeta localmente
            home = Path.home()
            home = str(home) + _initPath + _path
            home = home.replace("\\", "/")  # ruta path completa (solo carpetas)

            if Path(home).exists():  # si la carpeta existe , procede a verificar que el archivo exista
                if _name != '':
                    if Path(home + _name).exists():  # si existe el archivo procede a eliminar el archivo
                        remove(home + _name)
                        inserta_bitacora_general('Output', 'Delete', 'Archivo Eliminado Satisfactoriamente')
                        return True
                    else:
                        inserta_bitacora_general('Output', 'Delete', 'Error en metodo Delete , Archivo no existe')
                        return False
                else:
                    rmtree(home)
                    inserta_bitacora_general('Output', 'Delete', 'Carpeta Eliminada Satisfactoriamente')
                    return True

            else:
                inserta_bitacora_general('Output', 'Delete', 'Error en metodo Delete , ruta no existe')
                return False


        elif tipoAlmacena == 2:
            # Elimina carpeta en la nube
            #drive = Drive()
            msj = drive.delete(_path, _name)
            inserta_bitacora_general('Output', 'Create', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Delete', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Delete', 'Error en metodo Delete , error al eliminar Archivo ')
        return False


def copy(_from, _to, _name=''):
    global _initPath

    try:

        inserta_bitacora_general('Input', 'Copy', 'from: ' + str(_from) + str(_name) + ' | to: ' + str(_to))
        
        if tipoAlmacena == 1:  # operacion local
            home = Path.home()
            _from = str(home) + _initPath + _from
            _from = _from.replace("\\", "/")
            _to = str(home) + _initPath + _to
            if Path(_from).exists():  # si la carpeta existe , procede a verificar que el archivo exista
                if _name != '':
                    if Path(_from + _name).exists():  # si existe el archivo procede a copiar el archivo a la ruta
                        try:
                            shutil.copy(_from + _name, _to)
                            inserta_bitacora_general('Output', 'Copy', 'Archivo copiado exitosamente')
                            return True
                        except:
                            inserta_bitacora_general('Output', 'Copy', 'Error al copiar Archivo en ruta especificada')
                            return False
                    else:
                        inserta_bitacora_general('Output', 'Copy', 'Error Archivo no existe')
                        return False
                else:  # procede a copiar el contenido de toda la carpeta
                    try:
                        copy_tree(_from, _to)
                        inserta_bitacora_general('Output', 'Copy', 'Carpeta copiada exitosamente')
                        return True
                    except:
                        inserta_bitacora_general('Output', 'Delete', 'Error al copiar Carpeta en ruta especificada')
                        return False
            else:
                inserta_bitacora_general('Output', 'Copy', 'Error  ruta no existe')
                return False

        elif tipoAlmacena == 2:
            # mueve a la carpeta en la nube
            msj = drive.copy(_from+ _name, _to )
            inserta_bitacora_general('Output', 'Copy', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Copy', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Copy', 'Error en metodo Copy , error al copiar Archivo ')
        return False


def transfer(_from, _to, _mode, _name=''):  # mode recibe 1 = local , 2 c= cloud
    global _initPath

    try:
        inserta_bitacora_general('Input', 'Transfer',
                                 'from: ' + str(_from) + str(_name) + ' | to: ' + str(_to) + ' | mode: ' + str(_mode))
        

        if _mode == '1':  # operacion local
            home = Path.home()
            _from = str(home) + _initPath + _from
            _from = _from.replace("\\", "/")
            _to = str(home) + _initPath + _to
            print(_from)
            if Path(_from).exists():  # si la carpeta existe , procede a verificar que el archivo exista
                if _name != '':
                    if Path(_from + _name).exists():  # si existe el archivo procede a mover el archivo a la ruta
                        try:
                            shutil.move(_from + _name, _to)
                            inserta_bitacora_general('Output', 'Transfer', 'Archivo movido exitosamente')
                            return True
                        except:
                            inserta_bitacora_general('Output', 'Transfer',
                                                     'Error al mover Archivo en ruta especificada')
                            return False
                    else:
                        inserta_bitacora_general('Output', 'Transfer', 'Error Archivo no existe')
                        return False
                else:  # procede a mover el contenido de toda la carpeta
                    try:
                        shutil.move(_from, _to)
                        inserta_bitacora_general('Output', 'Transfer', 'Carpeta movida exitosamente')
                        return True
                    except:
                        inserta_bitacora_general('Output', 'Transfer', 'Error al mover Carpeta en ruta especificada')
                        return False
            else:
                inserta_bitacora_general('Output', 'Transfer', 'Error  ruta no existe')
                return False

        elif _mode == '2':
            # mueve a la carpeta en la nube
            msj = drive.transfer(_from+ _name, _to )
            inserta_bitacora_general('Output', 'Transfer', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Transfer', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Transfer', 'Error en metodo Transfer , error al mover Archivo ')
        return False


def rename(_path, _name, _new_name):
    global _initPath

    try:
        if _path == '':
            _path += '/'

        inserta_bitacora_general('Input', 'Rename',
                                 'path: ' + str(_path) + str(_name) + ' | name: ' + str(_new_name))
        home = Path.home()
        _from = str(home) + _initPath + _path
        _from = _from.replace("\\", "/")

        if tipoAlmacena == 1:  # operacion local
            if Path(_from).exists():  # si la carpeta existe , procede a verificar que el archivo exista
                if _name != '':  # verifica que el archivo exista
                    if Path(_from + _name).exists():  # si existe el archivo procede a cambiar de nombre el archivo
                        try:
                            shutil.move(_from + _name, _from + _new_name)
                            inserta_bitacora_general('Output', 'Rename', 'Se cambia el nombre de Archivo exitosamente')
                            return True
                        except:
                            inserta_bitacora_general('Output', 'Rename',
                                                     'Error al cambiar de nombre al Archivo en ruta especificada')
                            return False
                    else:
                        inserta_bitacora_general('Output', 'Rename', 'Error Archivo no existe')
                        return False
                else:  # procede a cambiar de nombre la  carpeta
                    try:
                        # Creo carpeta con nuevo nombre
                        home = Path.home()
                        _from = str(home) + _initPath + _path

                        _from = _from.replace("\\", "/")

                        _from = _from.split('/')

                        _pos = str(_from[-1])

                        _path_ant = ''
                        for i in _from[:-1]:
                            _path_ant += str(i) + '/'

                        if _pos == '':
                            _pos = str(_from[-2])
                            _path_ant = ''
                            for i in _from[:-2]:
                                _path_ant += str(i) + '/'

                        os.chdir(str(_path_ant))
                        os.rename(str(_pos), _new_name)
                        inserta_bitacora_general('Output', 'Rename', 'Carpeta movida exitosamente')
                        return True
                    except:
                        inserta_bitacora_general('Output', 'Rename', 'Error al mover Carpeta en ruta especificada')
                        return False
            else:
                inserta_bitacora_general('Output', 'Rename', 'Error  ruta no existe')
                return False

        elif tipoAlmacena == 2:
            # realiza rename en la nube
            msj = drive.rename(_path + _name, _new_name)
            inserta_bitacora_general('Output', 'Rename', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Rename', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Rename', 'Error en metodo Rename , error al cambiar de nombre al Archivo ')
        return False


def modify(_path, _name, _body):
    global _initPath

    try:
        if _path == '':
            _path += '/'

        inserta_bitacora_general('Input', 'Modify',
                                 'path: ' + str(_path) + str(_name) + ' | body: ' + str(_body))
        home = Path.home()
        _from = str(home) + _initPath + _path
        _from = _from.replace("\\", "/")

        if tipoAlmacena == 1:  # operacion local
            if Path(_from).exists():  # si la carpeta existe , procede a verificar que el archivo exista
                if _name != '':  # verifica que el archivo exista

                    if Path(_from + _name).exists():  # si existe el archivo procede a insertar linea
                        try:

                            file = open(_from + _name, "w")
                            file.write(_body)
                            file.close()

                            inserta_bitacora_general('Output', 'Modify',
                                                     'Se cambia el contenido del Archivo exitosamente')
                            return True
                        except:
                            inserta_bitacora_general('Output', 'Modify',
                                                     'Error al insertar contenido en el archivo')
                            return False
                    else:
                        inserta_bitacora_general('Output', 'Modify', 'Error Archivo no existe')
                        return False
                else:  # procede a retornar error porque no ingresaron nombre de archivo

                    inserta_bitacora_general('Output', 'Modify', 'Error archivo no existe')
                    return False
            else:
                inserta_bitacora_general('Output', 'Modify', 'Error  ruta no existe')
                return False

        elif tipoAlmacena == 2:
            # realiza modify en la nube   , pendiente
            msj = drive.modify(_path + _name, _body)
            inserta_bitacora_general('Output', 'Modify', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Modify', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Modify', 'Error en metodo Modify , error al insertar nueva linea de texto')
        return False


def add(_path, _name, _body):
    global _initPath

    try:
        if _path == '':
            _path += '/'

        inserta_bitacora_general('Input', 'Add',
                                 'path: ' + str(_path) + str(_name) + ' | body: ' + str(_body))
        home = Path.home()
        _from = str(home) + _initPath + _path
        _from = _from.replace("\\", "/")

        if tipoAlmacena == 1:  # operacion local
            if Path(_from).exists():  # si la carpeta existe , procede a verificar que el archivo exista
                if _name != '':  # verifica que el archivo exista

                    if Path(_from + _name).exists():  # si existe el archivo procede a insertar linea
                        try:

                            file = open(_from + _name, "a")
                            file.write('\n' + _body)
                            file.close()

                            inserta_bitacora_general('Output', 'Add',
                                                     'Se agrega contenido al Archivo exitosamente')
                            return True
                        except:
                            inserta_bitacora_general('Output', 'Add',
                                                     'Error al agregar contenido en el archivo')
                            return False
                    else:
                        inserta_bitacora_general('Output', 'Add', 'Error Archivo no existe')
                        return False
                else:  # procede a retornar error porque no ingresaron nombre de archivo

                    inserta_bitacora_general('Output', 'Add', 'Error archivo no existe')
                    return False
            else:
                inserta_bitacora_general('Output', 'Add', 'Error  ruta no existe')
                return False

        elif tipoAlmacena == 2:
            # realiza modify en la nube   , pendiente
            
            msj = drive.add(_path, _name,_body)
            inserta_bitacora_general('Output', 'Add', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Add', 'Error : Comando Configure no ejecutado')
            return False
    except Exception as e:
        print(f"Error al agregar contenido al archivosssss: {e}")
        inserta_bitacora_general('Output', 'Add', 'Error en metodo Add , error al agregar nuevo texto')
        return False

def backup():
    try:
        home = Path.home()
        if tipoAlmacena == 1:
            msj = drive.backup_local(str(home) + _initPath)
            inserta_bitacora_general('Output', 'Backup', msj)
            return True
        elif tipoAlmacena == 2:
            msj = drive.backup_nube(str(home) + _initPath)
            inserta_bitacora_general('Output', 'Backup', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Add', 'Error : Comando backup no ejecutado')
            return False
        
    except Exception as e:
        print(f"Error al agregar contenido al archivosssss: {e}")
        inserta_bitacora_general('Output', 'Add', 'Error en metodo Add , error al agregar nuevo texto')
        return False

def salir():
    print("\n FIN DE LA APLICACIÓN  ")
    sys.exit(0)

def devolver_ecrypt_read():
    return encrypt_read

def cambiar_ecrypt_read():
    global encrypt_read
    encrypt_read = 0
    
def devolver_llave():
    return llave

# FIN metodos estaticos (Comandos)-------------------------------------------------------------------------------------


# metodos para similar las entradas en consola

def mostrar_menu():
    print("""
    ########################      Menu Principal      ########################

                1)  Comando  Configure   
                2)  Comando Create
                3)  Comando Delete
                4)  Comando Copy
                5)  Comando Transfer
                6)  Comando Rename
                7)  Comando Modify
                8)  Comando Add
                9)  Comando Backup
                10)  Salir
    """)


class Menu:
    def __init__(self):
        self.acciones = {
            "1": self.configure,
            "2": self.create,
            "3": self.delete,
            "4": self.copy,
            "5": self.transfer,
            "6": self.rename,
            "7": self.modify,
            "8": self.add,
            # "9": self.backup,
            "10": self.salir
        }

        while True:
            mostrar_menu()
            eleccion = input("\n   Seleccione una opción: ")
            accion = self.acciones.get(eleccion)
            if accion:
                accion()
            else:
                os.system("cls")
                print("\n{0} no es una elección válida".format(eleccion))

    def configure(self):
        _tipo = input("\n   Ingrese tipo: ")
        encrypt = input("\n   Ingrese encrypt: ")
        _encrypt_read = input("\n   Ingrese _encrypt_read: ")
        _llave = input("\n   Ingrese _llave: ")
        configure(_tipo, encrypt, _encrypt_read, _llave)
        Menu()

    def create(self):
        _name = input("\n   Ingrese name: ")
        _body = input("\n   Ingrese body: ")
        _path = input("\n   Ingrese path: ")
        create(_name, _body, _path)
        Menu()

    def delete(self):

        _path = input("\n   Ingrese path: ")
        _name = input("\n   Ingrese name: ")
        delete(_path, _name)
        Menu()

    def copy(self):

        _from = input("\n   Ingrese from: ")
        _name = input("\n   Ingrese name:")
        _to = input("\n   Ingrese to: ")
        copy(_from, _to, _name)
        Menu()

    def transfer(self):

        _from = input("\n   Ingrese from: ")
        _name = input("\n   Ingrese name:")
        _to = input("\n   Ingrese to: ")
        _modo = input("\n   Ingrese modo:")
        transfer(_from, _to, _modo, _name)
        Menu()

    def rename(self):

        _from = input("\n   Ingrese path: ")
        _name = input("\n   Ingrese name:")
        _new_name = input("\n   Ingrese new name: ")
        rename(_from, _name, _new_name)
        Menu()

    def modify(self):

        _path = input("\n   Ingrese path: ")
        _name = input("\n   Ingrese name:")
        _body = input("\n   Ingrese body: ")
        modify(_path, _name, _body)
        Menu()

    def add(self):

        _path = input("\n   Ingrese path: ")
        _name = input("\n   Ingrese name:")
        _body = input("\n   Ingrese body: ")
        add(_path, _name, _body)
        Menu()

    """def backup(self):

        _path = input("\n   Ingrese path: ")
        _name = input("\n   Ingrese name:")
        _body = input("\n   Ingrese body: ")
        backup(_path, _name, _body)
        Menu()
    """

    def salir(self):
        print("Inicio bitacora --------------------------------")
        for i in bitacora:
            print(i)
        print("Fin  bitacora --------------------------------")
        print("\n FIN DE LA APLICACIÓN  ")

        sys.exit(0)

