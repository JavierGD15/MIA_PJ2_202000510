import boto3

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
