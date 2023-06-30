import re
import boto3
import os
from botocore.exceptions import ClientError
from pathlib import Path

class AWS:
    bucket_name = 'archivosvacasjunio2023'
    _initPath = '/Archivos'
    s3 = boto3.client('s3')
    def __init__(self):
        print("Hola")
    
    def create(self, valor1, valor2, valor3):
        # valor1 = name
        # valor2 = path
        # valor3 = body
        valor2 = str(valor2).lstrip('/')
        print(valor1) 
        print(valor2)
        print(valor3)
        
        # Dividir la ruta en partes
        path_parts = valor2.split('/')
        print(path_parts)
        current_path = ''
        # Verificar/crear cada carpeta en la jerarquía
        for part in path_parts:
            if part:
                current_path += part + '/'
                response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=current_path)
                if 'Contents' not in response:
                    self.s3.put_object(Bucket=self.bucket_name, Key=(current_path))
                    print(f"Se creó la carpeta '{current_path}' en el bucket '{self.bucket_name}'")
                    print("Directorio", "Se creo el directorio")

        # Agregar un archivo a la carpeta
        if len(valor1) != 0:
            file_name = valor1
            file_content = valor3
            self.s3.put_object(Bucket=self.bucket_name, Key=current_path + file_name, Body=file_content)
            print(f"Se agregó el archivo '{file_name}' a la carpeta '{current_path}'")
            print("Archivo", "Se creo el archivo indicado")
            return True
        else:
            return False

    def delete(self, valor1, valor2):
        # valor1 = name
        # valor2 = path
        valor2 = str(valor2).lstrip('/')
        print(valor1)
        print(valor2)

        # Dividir la ruta en partes
        path_parts = valor2.split('/')
        
        current_path = ''
        # Verificar cada carpeta en la jerarquía
        for part in path_parts:
            if part:
                current_path += part + '/'

        if len(valor1) != 0:
            # Si se proporciona un nombre de archivo, se elimina el archivo
            file_name = valor1
            self.s3.delete_object(Bucket=self.bucket_name, Key=current_path + file_name)
            print(f"Se eliminó el archivo '{file_name}' de la carpeta '{current_path}'")
            print("Archivo", "Se eliminó el archivo indicado")
            return True
        
        else:
            # Si no se proporciona un nombre de archivo, se eliminan todos los archivos en la carpeta
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=current_path)
            if 'Contents' in response:
                for obj in response['Contents']:
                    self.s3.delete_object(Bucket=self.bucket_name, Key=obj['Key'])
                print(f"Se eliminaron todos los archivos en la carpeta '{current_path}'")
                print("Directorio", "Se eliminaron todos los archivos en el directorio")
                # Intentar eliminar el objeto vacío que representa la "carpeta"
                self.s3.delete_object(Bucket=self.bucket_name, Key=current_path)
                print(f"Se eliminó la carpeta '{current_path}'")
                return True
            else:
                print(f"La carpeta '{current_path}' no existe en el bucket '{self.bucket_name}'")
                print("Directorio", "El directorio no existe")
                return False

    # def copy(self, from_path, type_from, type_to, to_path):
    #     # Configurar las rutas base
    #     home = Path.home()
    #     _initPath = '/Archivos'
    #     base_local_path = str(home) + _initPath
    #     patron = r'^[\w\s]+\/[\w\s]+\.\w+$'
    #     print(from_path)
        
    #     if re.match(patron, from_path):
    #         print("Es un archivo")
    #         if type_from == 'server' and type_to == 'bucket':
                
    #             from_path = base_local_path + from_path.lstrip('/')
    #             to_path = to_path.lstrip('/')

    #             if not os.path.isfile(from_path):
    #                 print(f"El archivo '{from_path}' no existe en el servidor local.")
    #                 return True

    #             new_s3_file = os.path.join(to_path, os.path.basename(from_path)).replace("\\", "/")  # Asegurar que se use el separador correcto

    #             self.s3.upload_file(from_path, self.bucket_name, new_s3_file)
    #             print(f"Se subió el archivo '{from_path}' a '{new_s3_file}' en el bucket '{self.bucket_name}'.")

    #             os.remove(from_path)
    #             print(f"Se eliminó el archivo original '{from_path}' del servidor local.")
    #             print("Archivo", "Se movió el archivo")
   
    #         elif type_from == 'bucket' and type_to == 'server':
    #             from_path = base_local_path + from_path.lstrip('/')
    #             to_path = to_path.lstrip('/')

    #             if not os.path.isfile(from_path):
    #                 print(f"El archivo '{from_path}' no existe en el servidor local.")
    #                 return False

    #             new_s3_file = os.path.join(to_path, os.path.basename(from_path)).replace("\\", "/")  # Asegurar que se use el separador correcto

    #             self.s3.upload_file(from_path, self.bucket_name, new_s3_file)
    #             print(f"Se subió el archivo '{from_path}' a '{new_s3_file}' en el bucket '{self.bucket_name}'.")

    #             os.remove(from_path)
    #             print(f"Se eliminó el archivo original '{from_path}' del servidor local.")
    #             print("Archivo", "Se movió el archivo")
                        
    #         elif type_from == 'bucket' and type_to == 'bucket':

    #             from_path = from_path.lstrip('/')
    #             to_path = to_path.lstrip('/')
                
    #             # Verificar si la carpeta origen existe en el bucket
    #             response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=from_path)
    #             if 'Contents' not in response:
    #                 print(f"La carpeta origen '{from_path}' no existe en el bucket '{self.bucket_name}'.")
    #                 return True

    #             # Verificar si la carpeta de destino existe en el bucket
    #             response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=to_path)
    #             if 'Contents' not in response:
    #                 print(f"La carpeta destino '{to_path}' no existe en el bucket '{self.bucket_name}'.")
    #                 return True

    #             # Copiar cada archivo en la carpeta origen al nuevo destino dentro del mismo bucket
    #             for item in response['Contents']:
    #                 s3_file = item['Key']
    #                 if s3_file.startswith(from_path + '/'):
    #                     # Construir la ruta completa del archivo en el destino
    #                     relative_path = s3_file[len(from_path):]
    #                     new_s3_file = to_path + relative_path.replace("\\", "/")  # Asegurar que se use el separador correcto

    #                     # Copiar el objeto
    #                     self.s3.copy_object(Bucket=self.bucket_name, CopySource={'Bucket': self.bucket_name, 'Key': s3_file}, Key=new_s3_file)
    #                     print(f"Se copió el archivo '{s3_file}' a '{new_s3_file}' en el bucket '{self.bucket_name}'.")
    #                     print("Archivo", "Se copió el archivo")  

    #     else:
    #         print("Es una carpeta")
    #         if type_from == 'server' and type_to == 'bucket':
    #             from_path = base_local_path + from_path.lstrip('/')
    #             to_path = to_path.lstrip('/')
                
    #             # Verificar si la carpeta origen existe
    #             if not os.path.exists(from_path):
    #                 print(f"La carpeta origen '{from_path}' no existe.")
    #                 return True

    #             # Verificar si cada carpeta en la ruta de destino existe en el bucket S3
    #             path_parts = to_path.split('/')
    #             current_path = ''
    #             for part in path_parts:
    #                 if part:
    #                     current_path += part + '/'
    #                     response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=current_path)
    #                     if 'Contents' not in response:
    #                         print(f"La carpeta destino '{current_path}' no existe en el bucket '{self.bucket_name}'.")
    #                         return True

    #             # Copiar cada archivo en la carpeta origen al bucket
    #             for root, dirs, files in os.walk(from_path):
    #                 for file_name in files:
    #                     # Construir la ruta completa del archivo en el sistema local
    #                     local_file = os.path.join(root, file_name)
                        
    #                     # Construir la ruta completa del archivo en el bucket S3
    #                     relative_path = os.path.relpath(local_file, from_path)
    #                     s3_file = to_path + '/' + relative_path.replace("\\", "/")  # Asegurar que se use el separador correcto
                        
    #                     self.s3.upload_file(local_file, self.bucket_name, s3_file)
    #                     print(f"Se copió el archivo '{local_file}' a '{s3_file}' en el bucket '{self.bucket_name}'.")
    #                     print("Archivo", "Se copió el archivo")
                        
    #         elif type_from == 'bucket' and type_to == 'server':
    #             from_path = from_path.lstrip('/')
    #             to_path = base_local_path + to_path.lstrip('/')
                
    #             # Verificar si la carpeta origen existe en el bucket
    #             response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=from_path)
    #             if 'Contents' not in response:
    #                 print(f"La carpeta origen '{from_path}' no existe en el bucket '{self.bucket_name}'.")
    #                 return True

    #             # Verificar si la carpeta de destino existe en el servidor local
    #             if not os.path.exists(to_path):
    #                 print(f"La carpeta destino '{to_path}' no existe.")
    #                 return True

    #             # Copiar cada archivo en la carpeta origen del bucket al servidor local
    #             for item in response['Contents']:
    #                 s3_file = item['Key']
    #                 if s3_file.startswith(from_path + '/'):
    #                     # Construir la ruta completa del archivo en el servidor local
    #                     relative_path = s3_file[len(from_path):]
    #                     local_file = to_path + relative_path.replace("/", os.path.sep)  # Asegurar que se use el separador correcto

    #                     # Crear cualquier subcarpeta necesaria
    #                     os.makedirs(os.path.dirname(local_file), exist_ok=True)

    #                     self.s3.download_file(self.bucket_name, s3_file, local_file)
    #                     print(f"Se copió el archivo '{s3_file}' a '{local_file}'.")
    #                     print("Archivo", "Se copió el archivo")
                        
    #         elif type_from == 'bucket' and type_to == 'bucket':

    #             from_path = from_path.lstrip('/')
    #             to_path = to_path.lstrip('/')
                
    #             # Verificar si la carpeta origen existe en el bucket
    #             response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=from_path)
    #             if 'Contents' not in response:
    #                 print(f"La carpeta origen '{from_path}' no existe en el bucket '{self.bucket_name}'.")
    #                 return True

    #             # Verificar si la carpeta de destino existe en el bucket
    #             response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=to_path)
    #             if 'Contents' not in response:
    #                 print(f"La carpeta destino '{to_path}' no existe en el bucket '{self.bucket_name}'.")
    #                 return True

    #             # Copiar cada archivo en la carpeta origen al nuevo destino dentro del mismo bucket
    #             for item in response['Contents']:
    #                 s3_file = item['Key']
    #                 if s3_file.startswith(from_path + '/'):
    #                     # Construir la ruta completa del archivo en el destino
    #                     relative_path = s3_file[len(from_path):]
    #                     new_s3_file = to_path + relative_path.replace("\\", "/")  # Asegurar que se use el separador correcto

    #                     # Copiar el objeto
    #                     self.s3.copy_object(Bucket=self.bucket_name, CopySource={'Bucket': self.bucket_name, 'Key': s3_file}, Key=new_s3_file)
    #                     print(f"Se copió el archivo '{s3_file}' a '{new_s3_file}' en el bucket '{self.bucket_name}'.")
    #                     print("Archivo", "Se copió el archivo")

    def rename(self, _path, _name, _new_name):
        _path = _path.lstrip('/')
        s3_old_file = os.path.join(_path, _name).replace("\\", "/")  # Asegurar que se use el separador correcto
        s3_new_file = os.path.join(_path, _new_name).replace("\\", "/")  # Asegurar que se use el separador correcto

        # Verificar si el archivo existe en el bucket
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_old_file)
        if 'Contents' not in response:
            print(f"El archivo '{s3_old_file}' no existe en el bucket '{self.bucket_name}'.")
            return False

        # Verificar si el nuevo nombre ya existe en el bucket
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_new_file)
        if 'Contents' in response:
            print(f"Ya existe un archivo con el nombre '{s3_new_file}' en el bucket '{self.bucket_name}'.")
            return False

        # Copiar el archivo con el nuevo nombre
        self.s3.copy_object(Bucket=self.bucket_name, CopySource={'Bucket': self.bucket_name, 'Key': s3_old_file}, Key=s3_new_file)
        print(f"Se copió el archivo '{s3_old_file}' a '{s3_new_file}' en el bucket '{self.bucket_name}'.")

        # Eliminar el archivo original
        self.s3.delete_object(Bucket=self.bucket_name, Key=s3_old_file)
        print("Archivo", "Se renombró el archivo")
        return True

    def modify(self, _path, _name, _body):
        _path = _path.lstrip('/')
        s3_file = os.path.join(_path, _name).replace("\\", "/")  # Asegurar que se use el separador correcto

        # Verificar si el archivo existe en el bucket
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_file)
        if 'Contents' not in response:
            print(f"El archivo '{s3_file}' no existe en el bucket '{self.bucket_name}'.")
            return False

        # Sobrescribir el archivo con el nuevo contenido
        self.s3.put_object(Bucket=self.bucket_name, Key=s3_file, Body=_body)
        print(f"Se modificó el archivo '{s3_file}' en el bucket '{self.bucket_name}'.")
        print("Archivo", "Se modificó el archivo")
        return True

    def delete_all(self):
        # Obtener una lista de todos los objetos en el bucket
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)

        if 'Contents' in response:
            # Eliminar cada objeto
            for item in response['Contents']:
                self.s3.delete_object(Bucket=self.bucket_name, Key=item['Key'])
                print(f"Se eliminó '{item['Key']}' del bucket '{self.bucket_name}'.")
            print("Se eliminaron todos los objetos del bucket.")
            return True
        else:
            print("No hay objetos en el bucket para eliminar.")
            return False

    def opens_grupal(self,name, _name,_ip='', _port=''):
        pass
    
    def opens_normal(self,name):
        # crea carpeta localmente
        _initPath = '/Archivos'
        name = name.replace('"', '')
        home = Path.home()
        home = str(home) + _initPath
        name = name.lstrip('/')
        found = False
        # Listar todos los objetos en el bucket
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        if 'Contents' in response:
            # Revisar cada objeto
            for item in response['Contents']:
                if item['Key'].endswith(name):
                    # Descargar el archivo si el nombre coincide
                    self.s3.download_file(self.bucket_name, item['Key'], name)
                    print(f"Se descargó '{item['Key']}' del bucket '{self.bucket_name}' a tu máquina local.")

                    # Abrir y leer el archivo
                    with open(name, 'r') as file:
                        print("El contenido del archivo es:")
                        print(file.read())
                    found = True
                    break  # Si se encuentra el archivo, no se necesitan más iteraciones

        if not found:
            print(f"El archivo '{name}' no existe en el bucket '{self.bucket_name}'.")

    def backup_bucket_server(self, name):
        # crea carpeta localmente
        _initPath = '/Archivos'
        name = name.replace('"', '')
        home = Path.home()
        home = str(home) + _initPath + '/' + name
        home = home.replace("\\", "/")
        # Crear la carpeta de respaldo si no existe
        if not os.path.exists(home):
            os.makedirs(home)
        
        # Listar todos los objetos en el bucket
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        
        if 'Contents' in response:
            # Descargar cada objeto en la carpeta de respaldo
            for item in response['Contents']:
                # Comprobar si el objeto es un archivo y no una carpeta
                if not item['Key'].endswith("/"):
                    # Crear una estructura de directorios que coincida con la del bucket
                    local_path = os.path.join(home, item['Key'])
                    local_directory = os.path.dirname(local_path)
                    if not os.path.exists(local_directory):
                        os.makedirs(local_directory)
                    
                    self.s3.download_file(self.bucket_name, item['Key'], local_path)
            print(f"Se ha respaldado el bucket '{self.bucket_name}' en la carpeta local '{home}'")
            return True
        else:
            print(f"No hay objetos en el bucket '{self.bucket_name}' para respaldar")
            return False

            
    def backup_server_bucket(self, name):
        # Configurar la ruta del directorio local
        _initPath = '/Archivos'
        name = name.replace('"', '')
        home = Path.home()
        home = str(home) + _initPath
        
        # Crear la carpeta en el bucket si no existe
        folder_name = name + "/"
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=folder_name)
        if 'Contents' not in response:
            # Crear un objeto vacío en la carpeta para simular su creación
            self.s3.put_object(Bucket=self.bucket_name, Key=folder_name)
            print(f"Se creó la carpeta '{folder_name}' en el bucket '{self.bucket_name}'")
        
        # Recorrer todos los archivos en el directorio local
        for root, dirs, files in os.walk(home):
            for file in files:
                local_path = os.path.join(root, file)
                s3_key = os.path.join(folder_name, file)
                # Cargar el archivo en el bucket
                self.s3.upload_file(local_path, self.bucket_name, s3_key)
                
        print(f"Se ha respaldado la carpeta local '{home}' en el bucket '{self.bucket_name}'")
        return True
    def recovery_bucket_server(self, name):
        # Configurar la ruta del directorio local
        _initPath = '/Archivos'
        name = name.replace('"', '')
        home = Path.home() / _initPath / name

        # Crear la carpeta de respaldo localmente si no existe
        home.mkdir(parents=True, exist_ok=True)

        # Comprobar si la carpeta de respaldo existe en el bucket
        folder_name = f"{name}/"
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=folder_name)
        
        if 'Contents' in response:
            # Descargar cada objeto en la carpeta de respaldo
            for item in response['Contents']:
                # Comprobar si el objeto es un archivo y no una carpeta
                if not item['Key'].endswith("/"):
                    # Crear una estructura de directorios que coincida con la del bucket
                    s3_key = item['Key']
                    relative_path = Path(s3_key[len(folder_name):])  # Eliminar el prefijo de la carpeta del nombre de la clave
                    local_path = home / relative_path
                    local_path.parent.mkdir(parents=True, exist_ok=True)  # Crear subdirectorios si no existen

                    self.s3.download_file(self.bucket_name, s3_key, str(local_path))

            print(f"Se ha recuperado la carpeta de respaldo '{name}' del bucket '{self.bucket_name}' en la carpeta local '{home}'")
            return True
        else:
            print(f"No hay una carpeta de respaldo con el nombre '{name}' en el bucket '{self.bucket_name}'")
            return False
        
    def recovery_server_bucket(self, name):
        # Configura la ruta del directorio local
        _initPath = '/Archivos'
        name = name.replace('"', '')
        home = Path.home() / _initPath / name

        # Verifica si la carpeta de respaldo existe en el directorio local
        if home.is_dir():
            for root, dirs, files in os.walk(home):
                for filename in files:
                    # Crea la estructura de directorios que coincida con la del bucket
                    local_path = Path(root) / filename
                    relative_path = local_path.relative_to(home)
                    s3_key = f"{name}/{relative_path}"

                    # Sube cada archivo a la carpeta de respaldo en el bucket
                    self.s3.upload_file(str(local_path), self.bucket_name, s3_key)

            print(f"Se ha recuperado la carpeta de respaldo '{name}' del directorio local '{home}' en el bucket '{self.bucket_name}'")
            return True
        else:
            
            print(f"No hay una carpeta de respaldo con el nombre '{name}' en el directorio local")
            return False
        
    def copy(self,valor1,valor2,valor3,valor4):

        patron = r'^\w+\/\w+\.\w+$'
        _initPath = '/Archivos'
        home = Path.home()
        home = str(home) + _initPath + '/'
        home = home.replace("\\", "/")
        
        if re.match(patron, valor1):

            
            if valor3 == 'server' and valor4 == 'bucket':
                #valor1 = 'prueba1/prueba2.txt' EJEMPLOS
                #valor2 = 'carpeta   123' + '/' EJEMPLOS
                ruta_base = home
                folder_file_name = valor1
                local_folder_path = os.path.join(ruta_base, folder_file_name)
                nombre_archivo = valor1.split('/')[-2]
                s3_file_key = os.path.join(valor2, nombre_archivo)
                try:
                    self.s3.upload_file(local_folder_path, self.bucket_name, s3_file_key)
                    print("El archivo se ha subido correctamente a S3.")
                except Exception as e:
                    print("Ocurrió un error al subir el archivo a S3:", e)
            elif valor3 == 'bucket' and valor4 == 'server':
                s3_folder = valor1
                ruta_base = home
                folder_name = valor2
                local_folder_path = os.path.join(ruta_base, folder_name)
                objects = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_folder)['Contents']

                for obj in objects:
                    #s3_file_key = obj['Key']
                    #patron = r'^\w+\/\w+\.\w+$'
                    #if re.match(patron, s3_file_key):
                    s3_path = obj['Key']
                    local_path = os.path.join(local_folder_path, os.path.basename(s3_path))
                    self.s3.download_file(self.bucket_name, s3_path, local_path)
                    #else:
                        #print("Es un directorio")
            elif valor3 == 'bucket' and valor4 == 'bucket':

                source_directory = valor1 #'carpeta1/prueba1.txt' # valor 1
                destination_directory = valor2 + '/' #'carpeta   123/' #  valor2
                try:
                    #Validar la existencia del archivo a copiar
                    self.s3.head_object(Bucket=self.bucket_name, Key=source_directory)
                    response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=destination_directory)
                    objetos = response.get('Contents', [])
                    if objetos :
                        print("Existe el directorio.")
                        '''
                        Escribir_Consola(Fecha_Format + " " + " ERROR: No se puede copiar. No existe el directorio destino." + '\n')
                        '''
                        #Copy -from->/carpeta1/prueba1.txt -to->/”carpeta 2”/ -type_to->sever -type_from->bucket

                        #source_directory_2 = valor1
                        cadena = valor1 #'carpeta1/prueba1.txt'
                        resultado = cadena.split("/")[-1]
                        destination_key = destination_directory + resultado
                        try:
                            self.s3.copy_object(
                            Bucket=self.bucket_name,
                            CopySource={'Bucket': self.bucket_name, 'Key': source_directory},
                            Key=destination_key
                            )
                            print(f"Se copió el archivo {source_directory} de {source_directory} a {destination_directory}.")
                            #Escribir_Consola(Fecha_Format + " " + "Se copio el archivo del directorio origen al directorio destino." + '\n')
                            #messagebox.showinfo("Copy", "Se copio el archivo del directorio origen al directorio destino.")
                        except Exception as e:
                            print(f"Error al copiar el archivo: {e}")
                            #messagebox.showerror("Error", "Error al copiar el archivo.")
                            #Escribir_Consola(Fecha_Format + " " + "ERROR : No se copio el archivo del directorio origen al directorio destino." + '\n')
                    else:
                        print(" No Existe el directorio")
                        print("Copy", "No se puede copiar. No existe el directorio destino.")
                except Exception as e:
                    print("Error", "El archivo no existe en S3.")

        else:
            source_directory = valor1 + '/'
            destination_directory = valor2 + '/'
            if valor3 == 'server' and valor4 == 'bucket':
                #To Server From Bucket Directorio entero hacia una carpeta de un bucket
            
                response_2 = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=destination_directory)
                objetos_2 = response_2.get('Contents', [])
                if len(objetos_2) == 0 :
                    print("Copy", "No se puede copiar. No existe el directorio destino.")
                    print(" No existe el direcotiro destino")
                else:
                    ruta_base = home
                    folder_name = valor1
                    local_folder_path = os.path.join(ruta_base, folder_name)
                    
                    for root, dirs, files in os.walk(local_folder_path):
                            for file in files:
                                local_file_path = os.path.join(root, file)
                                relative_path = os.path.relpath(local_file_path, local_folder_path)
                                s3_file_key = os.path.join(destination_directory, relative_path).replace("\\", "/")
                                self.s3.upload_file(local_file_path, self.bucket_name, s3_file_key)
            
            elif valor3 == 'bucket' and valor4 == 'server':
            
                s3_folder = valor1
                ruta_base = home
                folder_name = valor2
                local_folder_path = os.path.join(ruta_base, folder_name)
                objects = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_folder)['Contents']

                #for obj in objects:
                #    s3_path = obj['Key']
                #    local_path = os.path.join(local_folder_path, os.path.basename(s3_path))
                #    self.s3.download_file(self.bucket_name, s3_path, local_path)


        


                for obj in objects:
                    s3_path = obj['Key']
                    local_filename = os.path.basename(s3_path)
                    local_path = os.path.join(local_folder_path, local_filename)

                    # Validar si el archivo ya existe en el directorio local
                    if os.path.isfile(local_path):
                        # Generar un nuevo nombre para el archivo agregando un sufijo
                        name, extension = os.path.splitext(local_filename)
                        new_local_filename = f"{name}_renamed{extension}"
                        local_path = os.path.join(local_folder_path, new_local_filename)
                        print(f"El archivo {local_filename} ya existe. Se renombrará como {new_local_filename}.")

                        self.s3.download_file(self.bucket_name, s3_path, local_path)

            elif valor3 == 'bucket' and valor4 == 'bucket':

                response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=source_directory)

                objetos = response.get('Contents', [])


                for objeto in objetos:

                    source_key = objeto['Key']

                    destination_key = source_key.replace(source_directory, destination_directory)

                    self.s3.copy_object(

                        Bucket=self.bucket_name,

                        CopySource={'Bucket': self.bucket_name, 'Key': source_key},

                        Key=destination_key

                    )

                    print(f"Se copió el archivo de {source_key} a {destination_key}.")

                    #Escribir_Consola(Fecha_Format + " " + f"Se copió el archivo de {source_key} a {destination_key}." + '\n')

                print("Copy", "Se copiaron los archivos del directorio origen al directorio destino.")
                
                #Escribir_Consola(Fecha_Format + " " + "Se copiaron los archivos del directorio origen al directorio destino." + '\n')

    def transfer(self,valor1,valor2,valor3,valor4):
        _initPath = '/Archivos'
        home = Path.home()
        home = str(home) + _initPath + '/'
        home = home.replace("\\", "/")
        patron = r'^[\w\s]+\/[\w\s]+\.\w+$'
        source_directory = valor1
        # valor1 = 'carpeta prueba transfer/05122021.txt' EJEMPLO ESTRUCTURA
        # valor2 = 'carpeta prueba transfer 4' EJEMPLO ESTRUCTURAy
        if re.match(patron, valor1):

            if valor3 == 'bucket' and valor4 == 'bucket':
                
                destination_directory = valor2 + '/'
                exists_file = True
                try:
                    self.s3.head_object(Bucket=self.bucket_name, Key=valor1)
                except ClientError as e:
                    if e.response['Error']['Code'] == '404':
                        exists_file = False
                if exists_file :
                    response_a2 = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=destination_directory)
                    objetos_a2 = response_a2.get('Contents', [])
                    if objetos_a2:
                        nombre_archivo = source_directory.split('/')[-1]
                        ruta_archivo_destino = destination_directory + nombre_archivo
                        exists_destino_file = True
                        try:
                            self.s3.head_object(Bucket=self.bucket_name, Key=ruta_archivo_destino)
                        except ClientError as e:
                            if e.response['Error']['Code'] == '404':
                                exists_destino_file = False
                        if exists_destino_file:
                            extension = os.path.splitext(nombre_archivo)[1]
                            nuevo_nombre = input('Por favor, ingresa un nuevo nombre (sin extensión): ')
                            nombre_nuevo_archivo = os.path.splitext(nuevo_nombre)[0]  # Obtener el nuevo nombre sin la extensión del archivo
                            ruta_archivo_destino = destination_directory + nombre_nuevo_archivo + extension
                            print("El archivo fue renombrado ya que existia en Amazon S3.")
                        else:
                            print("El archivo no existe en Amazon S3.")
                        self.s3.copy_object(
                        Bucket=self.bucket_name,
                        CopySource={'Bucket': self.bucket_name, 'Key': source_directory},
                        Key=ruta_archivo_destino
                        )
                    
                        self.s3.delete_object(Bucket=self.bucket_name, Key=source_directory)

                        print(f'El archivo "{nombre_archivo}" se ha movido correctamente a "{ruta_archivo_destino}"')
                        #Escribir_Consola(f'El archivo "{nombre_archivo}" se ha movido correctamente a "{ruta_archivo_destino}"' + '\n')
                        print("exist el directorio")
                    else:
                        print("directorio destino no existe")
                        print(f"La ruta de destino '{self.bucket_name}/{destination_directory}' no existe.")
                        #Escribir_Consola(Fecha_Format + " " + f"La ruta de destino '{str(bucket_name)}/{str(destination_directory)}' no existe." + '\n')
                        print("Tranfer",  "La ruta de destino no existe.")
                        self.s3.put_object(Bucket=self.bucket_name , Key=destination_directory)
                        print("Tranfer",  " Se creo la ruta de destino.")
                        #Escribir_Consola(Fecha_Format + " " + f"La ruta de destino '{str(bucket_name)}/{str(destination_directory)}' fue creada." + '\n')
                        nombre_archivo = source_directory.split('/')[-1]
                        print("nombre de archivo" + nombre_archivo)
                        ruta_archivo_destino = destination_directory + nombre_archivo
                        print(ruta_archivo_destino + "ruta archivo destino") 
                        print("valido existencia destino")
                        
                        self.s3.copy_object(
                        Bucket=self.bucket_name,
                        CopySource={'Bucket': self.bucket_name, 'Key': source_directory},
                        Key=ruta_archivo_destino
                        )
                        self.s3.delete_object(Bucket=self.bucket_name, Key=source_directory)
                        print(f'El archivo "{nombre_archivo}" se ha movido correctamente a "{ruta_archivo_destino}"')
                        #Escribir_Consola(f'El archivo "{nombre_archivo}" se ha movido correctamente a "{ruta_archivo_destino}"' + '\n')
                else:

                    print("Transfer", "El archivo que desea transferir no existe en S3.")
            elif valor3 == 'bucket' and valor4 == 'server':
                s3_folder = valor1
                ruta_base = home
                folder_name = valor2
                local_folder_path = os.path.join(ruta_base, folder_name)
                
                objects = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_folder)['Contents']

                for obj in objects:
                    s3_file_key = obj['Key']
                    patron = r'^\w+\/\w+\.\w+$'
                    if re.match(patron, s3_file_key):
                        s3_path = obj['Key']
                        local_path = os.path.join(local_folder_path, os.path.basename(s3_path))
                        self.s3.download_file(self.bucket_name, s3_path, local_path)
                        self.s3.delete_object(Bucket=self.bucket_name, Key=source_directory)
                    else:
                        print("Es un directorio")

            elif valor3 == 'server' and valor4 == 'bucket':
                    print("lo que viene")

        else:

            if valor3 == 'bucket' and valor4 == 'bucket':

                #valor1 = 'carpeta_calificacion1/carpeta ejemplo/ejemplo3' EJEMPLO DE LA RUTA
                #valor2 = 'carpeta_transfer_2' # EJEMPLO DE LA RUTA
                source_directory = valor1
                destination_directory = valor2 + '/'

                #transfer -from->/”carpeta 2”/ -to->/carpeta1/ -type_to->sever -type_from->bucket

                response_1 = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=source_directory)
                objetos_1 = response_1.get('Contents', [])
    
                if len(objetos_1) == 0:
                    print(f"La ruta de origen '{self.bucket_name}/{source_directory}' no existe.")
                    #Escribir_Consola(Fecha_Format + " " + f"ERROR :La ruta de origen '{bucket_name}/{source_directory}' no existe." + '\n')
                    print("Error",  "ERROR :La ruta de origen no existe.")

                elif len(objetos_1) > 1:
                    response_2 = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=destination_directory)
                    objetos_2 = response_2.get('Contents', [])
                    if len(objetos_2) == 0:
                        print("directorio destino no existe")
                        print(source_directory)
                        print(f"La ruta de destino '{self.bucket_name}/{destination_directory}' no existe.")
                        #Escribir_Consola(Fecha_Format + " " + f"La ruta de destino '{str(bucket_name)}/{str(destination_directory)}' no existe." + '\n')
                        print("Tranfers",  "La ruta de destino no existe.")
                        self.s3.put_object(Bucket=self.bucket_name , Key=destination_directory)
                        print("Tranfers",  " Se creo la ruta de destino.")
                        #Escribir_Consola(Fecha_Format + " " + f"La ruta de destino '{str(bucket_name)}/{str(destination_directory)}' fue creada." + '\n')
                        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=source_directory)
                        archivos_origen = response['Contents'] if 'Contents' in response else []
                        for archivo_origen in archivos_origen:
                            if 'Key' in archivo_origen and archivo_origen['Key'].split('/')[-1]:
                                nombre_archivo = archivo_origen['Key'].split('/')[-1]
                                ruta_archivo_destino = destination_directory + nombre_archivo
                                try:
                                    self.s3.head_object(Bucket=self.bucket_name, Key=ruta_archivo_destino)
                                    print(f'El archivo "{nombre_archivo}" ya existe en el directorio de destino.')
                                    extension = os.path.splitext(nombre_archivo)[1]
                                    nuevo_nombre = input('Por favor, ingresa un nuevo nombre (sin extensión): ')
                                    #nuevo_nombre = simpledialog.askstring("Nuevo Nombre", f"Ingrese el nuevo nombre para el archivo {nombre_archivo}:")
                                    nombre_nuevo_archivo = os.path.splitext(nuevo_nombre)[0]  # Obtener el nuevo nombre sin la extensión del archivo
                                    ruta_archivo_destino = destination_directory + nombre_nuevo_archivo + extension
                                except:
                                    pass
                                self.s3.copy_object(Bucket=self.bucket_name, CopySource={'Bucket': self.bucket_name, 'Key': archivo_origen['Key']}, Key=ruta_archivo_destino)
                                self.s3.delete_object(Bucket=self.bucket_name, Key=archivo_origen['Key'])
                                print(f'El archivo "{nombre_archivo}" se ha movido correctamente a "{ruta_archivo_destino}"')
                                #Escribir_Consola(f'El archivo "{nombre_archivo}" se ha movido correctamente a "{ruta_archivo_destino}"' + '\n')
                    else:
                        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=source_directory)
                        archivos_origen = response['Contents'] if 'Contents' in response else []
                        for archivo_origen in archivos_origen:
                            print("entro aca al for")
                            if 'Key' in archivo_origen and archivo_origen['Key'].split('/')[-1]:
                                print("entro aca al KEY")
                                nombre_archivo = archivo_origen['Key'].split('/')[-1]
                                print("valor nombre archivo")
                                print(nombre_archivo)
                                print(" ruta inicial de archivo destion")
                                ruta_archivo_destino = destination_directory + nombre_archivo
                                print(ruta_archivo_destino)
                                try:
                                    self.s3.head_object(Bucket=self.bucket_name, Key=ruta_archivo_destino)
                                    print(f'El archivo "{nombre_archivo}" ya existe en el directorio de destino.')
                                    print("Extension Archivo Original")
                                    extension = os.path.splitext(nombre_archivo)[1]
                                    print(extension)
                                    nuevo_nombre = input('Por favor, ingresa un nuevo nombre (sin extensión): ')
                                    print("Nuevo nombre")
                                    #nuevo_nombre = simpledialog.askstring("Nuevo Nombre", f"Ingrese el nuevo nombre para el archivo {nombre_archivo}:")
                                    print(nuevo_nombre)
                                    print("nombre_nuevo_archivo")
                                    nombre_nuevo_archivo = os.path.splitext(nuevo_nombre)[0]  # Obtener el nuevo nombre sin la extensión del archivo
                                    print(nombre_nuevo_archivo)
                                    print("ruta destion")
                                    ruta_archivo_destino = destination_directory + nombre_nuevo_archivo + extension
                                    print(ruta_archivo_destino)
                                    print("carpeta destion con nombre modificado")
                                except:
                                    pass
                                print("que llega aqui")
                                print(ruta_archivo_destino)
                                self.s3.copy_object(Bucket=self.bucket_name, CopySource={'Bucket': self.bucket_name, 'Key': archivo_origen['Key']}, Key=ruta_archivo_destino)
                                self.s3.delete_object(Bucket=self.bucket_name, Key=archivo_origen['Key'])
                                print(f'El archivo "{nombre_archivo}" se ha movido correctamente a "{ruta_archivo_destino}"')
                                #Escribir_Consola(f'El archivo "{nombre_archivo}" se ha movido correctamente a "{ruta_archivo_destino}"' + '\n')
                                print("si existe")
                elif len(objetos_1) == 1:
                    print("Error", "No se puede mover. No hay archivos en el directorio origen.")
                    #Escribir_Consola(Fecha_Format + " " + f"ERROR: No se puede mover. No hay archivos en el directorio' + { str(bucket_name)}/{str(source_directory)} 'origen." + '\n')
                    print(" No Existen archivos en el directorio")