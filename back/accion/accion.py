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
from cloud.accion import AWS

# variables globales para guardar Configuracion de Archivos
tipoAlmacena = 0  # 1 = local , 2 = nube
encrypt_log = 0  # 1 = true , 2 = false
encrypt_read = 0  # 1 = true , 2 = false
llave = ''
# string llave para desencriptar.   Si se tiene los valores default , es porque no se ha ejecutado el comando configure

bitacora = []  # lista que lleva el registro de bitacora
_initPath = '/Archivos'  # carpeta donde se almacenaran localmente los archivos
aws = AWS()

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


def create(_name, _body, _path, _tipo):
    global _initPath

    if _path == '':
        _path += '/'

    inserta_bitacora_general('Input', 'Create', 'name: ' + str(_name) + ' | body: ' + str(_body) +
                             ' | path: ' + str(_path))

    # para crear crea carpeta

    try:
        if _tipo == 'server':

            # crea carpeta localmente
            home = Path.home()
            home = str(home) + _initPath + _path
            home = home.replace("\\", "/")
            Path(home).mkdir(parents=True, exist_ok=True)

            # se crea el archivo localmente
            if Path(home + _name).exists():
                inserta_bitacora_general('Output', 'Create', 'Error : Archivo ya existe')
                return False

            files = open(home + _name, "w")
            files.write(_body)
            files.close()
            inserta_bitacora_general('Output', 'Create', 'Archivo Creado exitosamente')
            return True

        elif _tipo == 'bucket':
            msj = aws.create(_path, _name, _body)
            inserta_bitacora_general('Output', 'Create', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Create', 'Error : Comando Invalido')
            return False

    except Exception as e:
        
        print(f"Error al agregar contenido al archivosssss: {e}")
        inserta_bitacora_general('Output', 'Create', 'Error en metodo Create , error al crear Archivo ')
        return False


def delete(_path, _tipo, _name=''):
    global _initPath
    if _path == '':
        _path += '/'

    inserta_bitacora_general('Input', 'Delete', 'path: ' + str(_path) + ' | name: ' + str(_name))
    try:
        if _tipo == 'server':  # operacion local

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


        elif _tipo == 'bucket':
            # Elimina carpeta en la nube
            #aws = aws()
            msj = aws.delete(_path, _name)
            inserta_bitacora_general('Output', 'Create', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Delete', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Delete', 'Error en metodo Delete , error al eliminar Archivo ')
        return False


def copy(_from, _to, type_to,type_from):
    global _initPath

    try:

        inserta_bitacora_general('Input', 'Copy', 'from: ' + str(_from) + str(_name) + ' | to: ' + str(_to))
        
        if _tipo == 'server':  # operacion local
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

        elif _tipo == 'bucket':
            # mueve a la carpeta en la nube
            msj = aws.copy(_from+ _name, _to )
            inserta_bitacora_general('Output', 'Copy', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Copy', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Copy', 'Error en metodo Copy , error al copiar Archivo ')
        return False


def transfer(_from, _to, type_to,type_from):  # mode recibe 1 = local , 2 c= cloud
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
            msj = aws.transfer(_from+ _name, _to )
            inserta_bitacora_general('Output', 'Transfer', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Transfer', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Transfer', 'Error en metodo Transfer , error al mover Archivo ')
        return False


def rename(_path, _name, _new_name,_tipo):
    global _initPath

    try:
        if _path == '':
            _path += '/'

        inserta_bitacora_general('Input', 'Rename',
                                 'path: ' + str(_path) + str(_name) + ' | name: ' + str(_new_name))
        home = Path.home()
        _from = str(home) + _initPath + _path
        _from = _from.replace("\\", "/")

        if _tipo == 'server':  # operacion local
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

        elif _tipo == 'bucket':
            # realiza rename en la nube
            msj = aws.rename(_path + _name, _new_name)
            inserta_bitacora_general('Output', 'Rename', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Rename', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Rename', 'Error en metodo Rename , error al cambiar de nombre al Archivo ')
        return False


def modify(_path, _name, _body, _tipo):
    global _initPath

    try:
        if _path == '':
            _path += '/'

        inserta_bitacora_general('Input', 'Modify',
                                 'path: ' + str(_path) + str(_name) + ' | body: ' + str(_body))
        home = Path.home()
        _from = str(home) + _initPath + _path
        _from = _from.replace("\\", "/")

        if _tipo == 'server':  # operacion local
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

        elif _tipo == 'bucket':
            # realiza modify en la nube   , pendiente
            msj = aws.modify(_path + _name, _body)
            inserta_bitacora_general('Output', 'Modify', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Modify', 'Error : Comando Configure no ejecutado')
            return False
    except:
        inserta_bitacora_general('Output', 'Modify', 'Error en metodo Modify , error al insertar nueva linea de texto')
        return False

def backup(type_to,type_from,name ,_ip='', _port=''):
    try:
        home = Path.home()
        if _tipo == 'server':
            msj = aws.backup_local(str(home) + _initPath)
            inserta_bitacora_general('Output', 'Backup', msj)
            return True
        elif _tipo == 'bucket':
            msj = aws.backup_nube(str(home) + _initPath)
            inserta_bitacora_general('Output', 'Backup', msj)
            return True
        else:
            inserta_bitacora_general('Output', 'Add', 'Error : Comando backup no ejecutado')
            return False
        
    except Exception as e:
        print(f"Error al agregar contenido al archivosssss: {e}")
        inserta_bitacora_general('Output', 'Add', 'Error en metodo Add , error al agregar nuevo texto')
        return False


def recovery(type_to,type_from, _name,_ip='', _port=''):
    pass

def delete_all(_tipo):
    pass

def opens(type_to,type_from, _name,_ip='', _port=''):
    pass



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

