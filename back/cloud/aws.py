import re
import boto3
import os
from botocore.exceptions import ClientError


class AWS:

    bucket_name = 'archivosvacasjunio2023'

    s3 = boto3.client('s3')

def __init__(self):
    
    print("Hola")

def create(self, valor1,valor2,valor3):
    # valor1 = name
    # valor2 = path
    # valor3 = body

    folder_name = valor2 + '/'
    response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=folder_name)

    if 'Contents' in response:
        print(f"La carpeta '{folder_name}' ya existe en el bucket '{self.bucket_name}'")
        print("Directorio", "La carpeta ya existe en el bucket.")

        if len(valor1) != 0:
            file_name = valor1
            file_content = valor3
            self.s3.put_object(Bucket=self.bucket_name, Key=folder_name + file_name, Body=file_content)
            print(f"Se agregó el archivo '{file_name}' a la carpeta '{folder_name}'")
            print("Archivo", "Se agregó el archivo al directorio")

    else:

        print(f"La carpeta '{folder_name}' no existe en el bucket '{self.bucket_name}'")
        # Crear un objeto vacío en la carpeta para simular su creación
        self.s3.put_object(Bucket=self.bucket_name, Key=(folder_name))
        print(f"Se creó la carpeta '{folder_name}' en el bucket '{self.bucket_name}'")
        print("Directorio", "Se creo el directorio")
            
        # Agregar un archivo a la carpeta
        
        if len(valor1) != 0:
            file_name = valor1
            file_content = valor3
            self.s3.put_object(Bucket=self.bucket_name, Key=folder_name + file_name, Body=file_content)
            print(f"Se agregó el archivo '{file_name}' a la carpeta '{folder_name}'")
            '''
            Escribir_Consola(Fecha_Format + " " + f"Se agregó el archivo '{file_name}' a la carpeta '{folder_name}'." + '\n')
            '''
            print("Archivo", "Se creo el archivo indicado")

def delete(self, valor1,valor2,eliminar):

    #valor1 = path
    #valor2 = name
    #eliminar = Mensaje de confirmacion si se elimina el directorio o archivo

    directory_path = valor1 + '/'

    folder_path = directory_path

    file_name = valor2

    file_key = folder_path + file_name

    #delete -path->/carpeta1/ -name->prueba1.txt -type->serve

    # Validar si un directorio existe en S3
    def validar_directorio():
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=directory_path)
        objetos = response.get('Contents', [])
        if objetos:
            return True
        else:
            print("Error", "El directorio no existe en S3.")
            '''
            Escribir_Consola(Fecha_Format + " " + f"ERROR : No se puede eliminar por que el directorio {directory_path} no existe en S3." + '\n')
            '''
            return False

    # Eliminar un directorio en S3
    def eliminar_directorio():

        if validar_directorio():
            #resultado = messagebox.askquestion("Eliminar", "¿ Está seguro que desea eliminar el directorio ?")
            if eliminar == "yes":
                print("Se procede con la eliminacion del directorio")
                response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=directory_path)
                objetos = response.get('Contents', [])
                if objetos:
                    objetos_a_borrar = [{'Key': objeto['Key']} for objeto in objetos]
                    self.s3.delete_objects(Bucket=self.bucket_name, Delete={'Objects': objetos_a_borrar})
                    '''
                    Escribir_Consola(Fecha_Format + " " + f"Se eliminó el directorio {directory_path} y todos sus archivos." + '\n')
                    '''
                    print("Delete", "Se eliminó el directorio y todos sus archivos.")
            else:
                print("Delete", "No se elimino el directorio")
                '''
                Escribir_Consola(Fecha_Format + " " + f"No eliminó el directorio {directory_path}." + '\n') 
                '''

    # Validar si un archivo existe en S3
    def validar_archivo():

        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=file_key)
            print(f"El archivo {file_key} existe en S3.")
            '''
            Escribir_Consola(Fecha_Format + " " + f"El archivo {file_key} existe en S3." + '\n')
            '''
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                print("Error", "El archivo no existe en S3.")
                '''
                Escribir_Consola(Fecha_Format + " " + "ERROR : No se puede eliminar por que el archivo no existe en S3." + '\n')
                '''                        
                return False
            else:
                print(f"Error al validar el archivo {file_key} en S3: {e}")
                '''
                Escribir_Consola(Fecha_Format + " " + f" Error al validar el archivo {file_key} en S3: {e} " + '\n')
                '''
                return False

    # Eliminar un archivo en S3
    def eliminar_archivo():

        if validar_archivo():
            #resultado = messagebox.askquestion("Eliminar", "¿ Está seguro que desea eliminar el archivo ?")
            if eliminar == "yes":
                self.s3.delete_object(Bucket=self.bucket_name, Key=file_key)
                '''
                Escribir_Consola(Fecha_Format + " " + f" Se elimino el archivo {file_key} ' . " + '\n')
                '''
                print(f"Se eliminó el archivo {file_key}.")
            else:

                print("No se elimino el archivo")
    # Aca evaluo si viene vacio valor2 es por que es un directorio el que voy a eliminar si viene es por es un archivo
    if ( len(valor2) == 0 ):
        eliminar_directorio()
    else:
        eliminar_archivo()

def copy(self,valor1,valor2,valor3,valor4):

    patron = r'^\w+\/\w+\.\w+$'
    
    
    if re.match(patron, valor1):

        
        if valor3 == 'server' and valor4 == 'bucket':
            #valor1 = 'prueba1/prueba2.txt' EJEMPLOS
            #valor2 = 'carpeta   123' + '/' EJEMPLOS
            ruta_base = r'D:\USAC\Vacas Junio 2023\Archivos\Proyecto_1'
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
            ruta_base = r'D:\USAC\Vacas Junio 2023\Archivos\Proyecto_1'
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
                ruta_base = r'D:\USAC\Vacas Junio 2023\Archivos\Proyecto_1'
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
            ruta_base = r'D:\USAC\Vacas Junio 2023\Archivos\Proyecto_1'
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


#Rename

def verificar_existencia_carpeta(bucket,cliente_s3, nombre_carpeta):
        try:
            # Verificar si la carpeta existe en S3 utilizando la función head_object
            # Si la carpeta existe, la función no generará una excepción
            cliente_s3.head_object(Bucket=bucket, Key=nombre_carpeta+'/')
            return True
        except:
            # Si se produce una excepción, significa que la carpeta no existe
            return False
        
def verificar_existencia_archivo(bucket, cliente_s3, ruta_archivo):
        try:
            # Verificar si el archivo existe en S3 utilizando la función head_object
            # Si el archivo existe, la función no generará una excepción
            cliente_s3.head_object(Bucket=bucket, Key=ruta_archivo)
            return True
        except:
            # Si se produce una excepción, significa que el archivo no existe
            return False

def cambiar_nombre_archivo(bucket , cliente_s3, ruta_archivo, nuevo_nombre):
        # Construir la nueva ruta completa del archivo utilizando el nuevo nombre
        nuevo_nombre_archivo = os.path.dirname(ruta_archivo) + '/' + nuevo_nombre

        # Copiar el archivo con el nuevo nombre utilizando la función copy_object de S3
        cliente_s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': ruta_archivo}, Key=nuevo_nombre_archivo)

        # Eliminar el archivo original utilizando la función delete_object de S3
        cliente_s3.delete_object(Bucket=bucket, Key=ruta_archivo)

def check_folder_exists(bucket_name, folder_name):

    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucket_name)

    objects = list(bucket.objects.filter(Prefix=folder_name))

    return len(objects) > 0

def rename(self,valor1,valor2):
    source_directory = valor1
    #extension = os.path.splitext(source_directory)[1]
    nuevo_nombre = valor2 #+ extension
    cliente_s3 = boto3.client('s3')
    if not verificar_existencia_carpeta(self.bucket_name,cliente_s3, source_directory):
        if verificar_existencia_archivo(self.bucket_name,cliente_s3, source_directory):
            while verificar_existencia_archivo(self.bucket_name,cliente_s3, os.path.dirname(source_directory) + '/' + nuevo_nombre):
                #Escribir_Consola(Fecha_Format + " " + f"ERROR : El archivo con nombre {nuevo_nombre} ya existe en {source_directory}." + '\n')
                #messagebox.showerror("Error", "El archivo con ese nombre ya existe'. En el directorio destino")
                return
            cambiar_nombre_archivo(self.bucket_name,cliente_s3, source_directory, nuevo_nombre)
            #Escribir_Consola(Fecha_Format + " " + f" El nombre del archivo se ha cambiado exitosamente a  {nuevo_nombre} ." + '\n')
            #messagebox.showinfo("Rename", "El nombre del archivo se ha cambiado exitosamente.")
        else:
            print("No existe la carpeta y tampoco existe el archivo. Debe dar eror.")
            #Escribir_Consola(Fecha_Format + " " + f"ERROR : No existe la carpeta o archivo {source_directory}." + '\n')
            #messagebox.showerror("Error", "No existe la carpeta y tampoco existe el archivo. Debe dar error.")
    else :
        print('La carpeta existe')
        current_folder_name = valor1 + '/'
        s3 = boto3.client('s3')
        new_folder_name = valor2 + '/'
        if check_folder_exists(self.bucket_name, new_folder_name):
            print("El nuevo nombre de carpeta ya existe en el bucket.")

            return
        
        # Obtener la lista de archivos dentro de la carpeta actual
        s3_resource = boto3.resource('s3')

        bucket = s3_resource.Bucket(self.bucket_name)
        
        objects = list(bucket.objects.filter(Prefix=current_folder_name))
        
        # Renombrar la carpeta
        for obj in objects:

            new_key = obj.key.replace(current_folder_name, new_folder_name, 1)
            
            s3.copy_object(
            
                Bucket=self.bucket_name,
            
                CopySource={'Bucket': self.bucket_name, 'Key': obj.key},
            
                Key=new_key
            
            )
            
            s3.delete_object(Bucket=self.bucket_name, Key=obj.key)
        
        print("Carpeta renombrada con éxito.")
        
        print("carpeta renombrada")

#Modify

def modify(self,valor1,valor2):
    
    directorio = valor1

    contenido = valor2
    
    print("Comando: modify")
    print("Argumentos:")
    print(f"  directorio: {directorio}")
    print(f"  contenido: {contenido}")

    # Separar el directorio y el nombre del archivo
    directorio, nombre_archivo = directorio.rsplit('/', 1)

    # Validar la existencia de la carpeta en S3

    s3 = boto3.client('s3')

    try:
        
        s3.head_object(Bucket= self.bucket_name, Key=directorio+'/')

    except Exception as e:

        print("Error: La carpeta especificada no existe en S3.")

        #Escribir_Consola(Fecha_Format + " " + f" ERROR: El directorio {directorio} no existe." + '\n')

        print("Modify", "Error: La carpeta especificada no existe en S3.")

        
        return

    # Verificar si el archivo existe en S3
    try:

        s3.head_object(Bucket=self.bucket_name, Key=directorio+'/'+nombre_archivo)
    
    except Exception as e:
    
        print("Error: El archivo especificado no existe en S3.")

        #Escribir_Consola(Fecha_Format + " " + f" ERROR: El archivo {directorio} +'/'+ {nombre_archivo} no existe en S3." + '\n')

        print("Modify", "Error: La carpeta especificada no existe en S3.")

    
        return

    # Subir el archivo actualizado a S3
    try:
        
        s3.put_object(Body=contenido.encode('utf-8'), Bucket=self.bucket_name, Key=directorio+'/'+nombre_archivo)

        #Escribir_Consola(Fecha_Format + " " + f" Archivo {directorio} +'/'+ {nombre_archivo} modificado correctamente en S3." + '\n')

        print("Modify", "Archivo modificado correctamente en S3.")

    except Exception as e:

        #Escribir_Consola(Fecha_Format + " " + f" Error {directorio} +'/'+ {nombre_archivo} al modificar en S3." + '\n')

        print("Modify", "Error al modificar el archivo en S3.")

    
#Transfer

def transfer(self,valor1,valor2,valor3,valor4):
    patron = r'^[\w\s]+\/[\w\s]+\.\w+$'
    # valor1 = 'carpeta prueba transfer/05122021.txt' EJEMPLO ESTRUCTURA
    # valor2 = 'carpeta prueba transfer 4' EJEMPLO ESTRUCTURAy
    if re.match(patron, valor1):

        if valor3 == 'bucket' and valor4 == 'bucket':
            source_directory = valor1
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
            ruta_base = r'D:\USAC\Vacas Junio 2023\Archivos\Proyecto_1'
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
