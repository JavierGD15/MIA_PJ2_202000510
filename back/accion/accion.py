import base64
import os
import sys
import datetime
import shutil
from pathlib import Path
from datetime import datetime
from os import remove
from shutil import rmtree
import shutil
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



#ya
def create(_name, _body, _path, _tipo):
    global _initPath

    if _path == '':
        _path += '/'


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
                return False

            files = open(home + _name, "w")
            files.write(_body)
            files.close()
            
            return True

        elif _tipo == 'bucket':
            msj = aws.create(_path, _name, _body)
            return True
        else:
            return False

    except Exception as e:
        
        print(f"Error al agregar contenido al archivosssss: {e}")
        return False

#ya
def delete(_path, _tipo, _name=''):
    global _initPath
    if _path == '':
        _path += '/'

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
                        return True
                    else:
                        return False
                else:
                    rmtree(home)
                    return True

            else:
                return False


        elif _tipo == 'bucket':
            # Elimina carpeta en la nube
            #aws = aws()
            msj = aws.delete(_path, _name)
            return True
        else:
            return False
    except:
        return False


def copy(_from, _to, type_to,type_from):
    global _initPath

    try:

        
        if type_to == 'server':  # operacion local
            if type_from == 'server':
                home = Path.home()
                _from = str(home) + _initPath + _from
                _from = _from.replace("\\", "/")
                _to = str(home) + _initPath + _to
                if Path(_from).exists():  # si la carpeta existe , procede a verificar que el archivo exista
                    if _name != '':
                        if Path(_from + _name).exists():  # si existe el archivo procede a copiar el archivo a la ruta
                            try:
                                shutil.copy(_from + _name, _to)
                                return True
                            except:
                                return False
                        else:
                            return False
                    else:  # procede a copiar el contenido de toda la carpeta
                        try:
                            copy_tree(_from, _to)
                            return True
                        except:
                            return False
                else:
                    return False
            else:
                _from += '/'
            
        elif type_to == 'bucket':
            if type_from == 'server':
                pass
            else:
                _from += '/'
            # mueve a la carpeta en la nube
            msj = aws.copy(_from+ _name, _to )
            return True
        else:
            return False
    except:
        return False


def transfer(_from, _to, type_to,type_from):  # mode recibe 1 = local , 2 c= cloud
    global _initPath

    try:
        
        

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
                            return True
                        except:
                             return False
                    else:
                       
                        return False
                else:  # procede a mover el contenido de toda la carpeta
                    try:
                        shutil.move(_from, _to) 
                        return True
                    except:
                        return False
            else:
                
                return False

        elif _mode == '2':
            # mueve a la carpeta en la nube
            msj = aws.transfer(_from+ _name, _to )
            return True
        else:
           
            return False
    except:
        return False

#ya
def rename(_path, _name, _new_name,_tipo):
    global _initPath
    print(_path)
    print(_name)
    print(_new_name)
    print(_tipo)
    try:
        if _path == '':
            _path += '/'
        home = Path.home()
        _from = str(home) + _initPath + _path
        _from = _from.replace("\\", "/")

        if _tipo == 'server':  # operacion local
            if Path(_from).exists():  # si la carpeta existe , procede a verificar que el archivo exista
                if _name != '':  # verifica que el archivo exista
                    if Path(_from + _name).exists():  # si existe el archivo procede a cambiar de nombre el archivo
                        try:
                            shutil.move(_from + _name, _from + _new_name)
                            return True
                        except Exception as e:
                            print(f"Error al agregar contenido al archivosssss: {e}")
                    else:
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
                        return True
                    except:
                        return False
            else:
                return False

        elif _tipo == 'bucket':
            # realiza rename en la nube
            msj = aws.rename(_path + _name, _new_name)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al renombrar : {e}")

#ya
def modify(_path, _name, _body, _tipo):
    global _initPath

    try:
        if _path == '':
            _path += '/'

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

                            return True
                        except:
                            return False
                    else:
                        return False
                else:  # procede a retornar error porque no ingresaron nombre de archivo

                    return False
            else:
                return False

        elif _tipo == 'bucket':
            # realiza modify en la nube   , pendiente
            msj = aws.modify(_path + _name, _body)
            return True
        else:
            return False
    except:
        return False

def backup(type_to,type_from,name ,_ip='', _port=''):
    try:
        home = Path.home()
        if _tipo == 'server':
            msj = aws.backup_local(str(home) + _initPath)
            return True
        elif _tipo == 'bucket':
            msj = aws.backup_nube(str(home) + _initPath)
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error al agregar contenido al archivosssss: {e}")
        return False

def recovery(type_to,type_from, _name,_ip='', _port=''):
    pass
#ya
def delete_all(_tipo):
    global _initPath
    try:
        if _tipo == 'server':
            # Crea la ruta completa
            home = Path.home()
            full_path = str(home) + _initPath
            full_path = full_path.replace("\\", "/")
            if not Path(full_path).exists():
                return False
            for filename in os.listdir(full_path):
                file_path = os.path.join(full_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            return True
        elif _tipo == 'bucket':
            pass
        else:
            return False
    except:
        return False

def opens(type_to,type_from, _name,_ip='', _port=''):
    pass

