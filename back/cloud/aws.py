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

        # Aca evaluo si viene vacio valor2 es por que es un directorio el que voy a eliminar si viene es por es un archivo

        if ( len(valor2) == 0 ):
            eliminar_directorio()
        else:
            eliminar_archivo()

    def copy(self,valor1,valor2,valor3,valor4):
    
        patron = r'^\w+\/\w+\.\w+$'
        source_directory = valor1 + '/'

        destination_directory = valor2 + '/'
        #Valor3 Copy -from->/carpeta1/prueba1.txt -to->/”carpeta 2”/ -type_to->sever -type_from->bucket
        #Valor3 type_to
        #Valor4 type_from
        #To Server From Bucket
        if re.match(patron, valor1):

            print("Arhcivo")
            '''
            source_directory_2 = valor1
            try:
                #resultado = s3.head_object(Bucket=self.bucket_name, Key=source_directory_2)
                response = s3.list_objects_v2(Bucket=self.bucket_name, Prefix=destination_directory)
                objetos = response.get('Contents', [])
                if objetos :
                    print("No existe el directorio destino.")
                    print("Copy", "No se puede copiar. No existe el directorio destino.")
                    
                    Escribir_Consola(Fecha_Format + " " + " ERROR: No se puede copiar. No existe el directorio destino." + '\n')
                    
                else:

                    print("Existe el directorio destino")
                    #cadena = valor1
                    #resultado = cadena.split("/")[-1]
                    #destination_key = destination_directory + resultado



                    
                    try:
                        s3.copy_object(
                        Bucket=bucket_name,
                        CopySource={'Bucket': bucket_name, 'Key': source_directory_2},
                        Key=destination_key
                        )
                    
                        print(f"Se copió el archivo {source_directory_2} de {source_directory} a {destination_directory}.")

                        Escribir_Consola(Fecha_Format + " " + "Se copio el archivo del directorio origen al directorio destino." + '\n')

                        messagebox.showinfo("Copy", "Se copio el archivo del directorio origen al directorio destino.")
            
                    
                    except Exception as e:

                        print(f"Error al copiar el archivo: {e}")

                        messagebox.showerror("Error", "Error al copiar el archivo.")

                        Escribir_Consola(Fecha_Format + " " + "ERROR : No se copio el archivo del directorio origen al directorio destino." + '\n')
            
            except Exception as e:

                messagebox.showerror("Error", "El archivo no existe en S3.")

                Escribir_Consola(Fecha_Format + " " + " ERROR: No se puede copiar. No existe el archivo en S3." + '\n')
            '''
        else:
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

                for obj in objects:
                    s3_file_key = obj['Key']
                    patron = r'^\w+\/\w+\.\w+$'
                    if re.match(patron, s3_file_key):
                        s3_path = obj['Key']
                        local_path = os.path.join(local_folder_path, os.path.basename(s3_path))
                        self.s3.download_file(self.bucket_name, s3_path, local_path)
                    else:
                        print("Es un directorio")
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



