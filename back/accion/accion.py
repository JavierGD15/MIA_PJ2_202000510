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



_initPath = '/Archivos'  # carpeta donde se almacenaran localmente los archivos
aws = AWS()


#ya ya
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
            
            msj = aws.create(_name,_path , _body)
            return msj
        else:
            return False

    except Exception as e:
        
        print(f"Error al agregar contenido al archivosssss: {e}")
        return False

#ya ya
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
            msj = aws.delete(_name, _path)
            return msj
        else:
            return False
    except:
        return False

#y
def copy(_from, _to, type_to,type_from):
    
    try:
        msj = aws.copy(_from,  _to, type_from, type_to,)
        return msj
    except:
        return False

#y
def transfer(_from, _to, type_to,type_from):  # mode recibe 1 = local , 2 c= cloud
    try:
        msj = aws.transfer(_from,  _to, type_from, type_to,)
        return msj
    except:
        return False

#ya ya
def rename(_path, _name, _new_name,_tipo):
    global _initPath
    _path = _path.replace('"', '')
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
            msj = aws.rename(_path, _name, _new_name)
            return msj
        else:
            return False
    except Exception as e:
        print(f"Error al renombrar : {e}")

#ya ya
def modify(_path, _name, _body, _tipo):
    global _initPath

    _path = _path.replace('"', '')
    _name = _name.replace('"', '')
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
            msj = aws.modify(_path, _name, _body,)
            return msj
        else:
            return False
    except:
        return False

#ya ya
def backup(type_to,type_from,name ,_ip='', _port=''):
    try:
        if type_from == 'server':
            if type_to == 'bucket':
                msj = aws.backup_server_bucket(name)
                return msj
            else:
                pass
            return True
        elif type_from == 'bucket':
            if type_to == 'server':
                print('entro')
                msj = aws.backup_bucket_server(name)
                return msj
            else:
                pass
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error al agregar contenido al archivosssss: {e}")
        return False
#ya ya
def recovery(type_to,type_from, _name,_ip='', _port=''):
    try:
        if type_from == 'server':
            if type_to == 'bucket':
                msj = aws.recovery_server_bucket(_name)
                return msj
            else:
                pass
            return True
        elif type_from == 'bucket':
            if type_to == 'server':
                print('entro')
                msj = aws.recovery_bucket_server(_name)
                return msj
            else:
                pass
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error al agregar contenido al archivosssss: {e}")
        return False
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
            msj = aws.delete_all()
            return msj
        else:
            return False
    except:
        return False
#ya ya
def opens(type, name,_ip='', _port=''):
    if type == 'server':
        if _ip != '' and _port != '':
            pass
        else:
            name = name.replace('"', '')
            
            # crea carpeta localmente
            home = Path.home()
            home = str(home) + _initPath + name
            home = home.replace("\\", "/")
            # Abrir y leer el archivo
            with open(home, 'r') as file:
                print("El contenido del archivo es:")
                print(file.read())
            return True
    elif type == 'bucket':
        if _ip != '' and _port != '':
            msj = aws.opens_grupal(name, _ip=_ip, _port=_port)
        else:
            msj = aws.opens_normal(name)
    else:
        return False
