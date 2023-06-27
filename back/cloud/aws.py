import boto3
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





