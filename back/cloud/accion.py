import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError
import os
import mimetypes

directorio_credenciales = 'credentials_modules.json'
id_folder_base = '1UtnT-_UsMEnCO9pdltTUoxEe9wNptPii'


class AWS:
    def __init__(self):
        # self.s3 = self.authenticate(aws_access_key_id, aws_secret_access_key, aws_session_token)
        print("AWS")

    def authenticate(self, aws_access_key_id, aws_secret_access_key, aws_session_token):
        s3 = boto3.client(
            's3', 
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token  # Puede ser None
        )
        return s3

    def crear_subFolder(self, nombre, id_parents):
        archivo = self.drive.CreateFile({'title': '' + nombre + '', 'parents': [{'id': id_parents}],
                                         "mimeType": "application/vnd.google-apps.folder"})
        archivo.Upload()

    def crear_folder(self, nombre):
        folder = self.drive.CreateFile({'title': '' + nombre + '', "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()

    def buscar(self, nombre, parent_id=None):
        if parent_id:
            query = f"'{parent_id}' in parents and trashed=false"
            try:
                archivos = self.drive.ListFile({'q': query}).GetList()
                for archivo in archivos:
                    if archivo['title'].strip() == nombre.strip():
                        return archivo['id']
                    
            except Exception as e:
                print(f"Hubo un error al listar los archivos: {str(e)}")
        else:
            query = f"title = '{nombre}' and trashed=false"    
            try:
                print(query)
                listaArchivos = self.drive.ListFile({'q': query}).GetList()
                if listaArchivos:
                    id_carpeta = listaArchivos[0]['id']
                    return id_carpeta
                else:
                    print(f"No se encontró ninguna carpeta o archivo con el nombre {nombre}.")
                    return None
            except Exception as e:
                print(f"Hubo un error al buscar el nombre {nombre}: {str(e)}")
                return None

    def crear_Archivo(self, nombre, body, id_parents):
        archivo = self.drive.CreateFile({'title': '' + nombre + '', 'parents': [{'id': id_parents}]})
        archivo.SetContentString(body)
        archivo.Upload()

    def create(self, path, name, body) -> str:
        carpeta_principal_id = '1UtnT-_UsMEnCO9pdltTUoxEe9wNptPii'  # el ID de la carpeta principal

        # Eliminar los slashes al principio y al final del path
        path = path.strip('/')
        # Dividir el path en subcarpetas
        subcarpetas = path.split('/')

        # Verificar si la carpeta principal existe
        carpeta_principal = None
        try:
            carpeta_principal = self.drive.CreateFile({'id': carpeta_principal_id})
        except Exception as e:
            print(f"No se pudo obtener la carpeta principal con el ID {carpeta_principal_id}: {str(e)}")
            return "Error al obtener la carpeta principal"

        # Intentar buscar y/o crear las subcarpetas en la carpeta principal
        id_carpeta_actual = carpeta_principal_id
        for subcarpeta in subcarpetas:
            id_subcarpeta = self.buscar(subcarpeta)
            if not id_subcarpeta:
                try:
                    self.crear_subFolder(subcarpeta, id_carpeta_actual)
                    id_subcarpeta = self.buscar(subcarpeta)  # Actualizar el ID de la subcarpeta después de crearla
                except Exception as e:
                    print(f"No se pudo crear la subcarpeta {subcarpeta} en la carpeta con ID {id_carpeta_actual}: {str(e)}")
                    return "Error al crear subcarpeta"
            id_carpeta_actual = id_subcarpeta  # La subcarpeta actual se convertirá en la carpeta principal para la próxima iteración

        # Crear el archivo en la última subcarpeta
        try:
            if self.buscar(name):
                return "Archivo ya existe"
            else:
                self.crear_Archivo(name, body, id_carpeta_actual)
                return "Archivo Creado con Exito"
        except Exception as e:
            print(f"No se pudo crear el archivo {name} en la carpeta con ID {id_carpeta_actual}: {str(e)}")
            return "Error al crear archivo"

    def delete(self, path, name=None) -> str:
        
        path = path.strip('/')
        subcarpetas = path.split('/')

        carpeta_principal_id = '1UtnT-_UsMEnCO9pdltTUoxEe9wNptPii'
        carpeta_principal = None
        try:
            carpeta_principal = self.drive.CreateFile({'id': carpeta_principal_id})
        except Exception as e:
            print(f"No se pudo obtener la carpeta principal con el ID {carpeta_principal_id}: {str(e)}")
            return "Error al obtener la carpeta principal"

        
        id_carpeta_actual = carpeta_principal_id
        for subcarpeta in subcarpetas:
            
            id_subcarpeta = self.buscar(subcarpeta)
            if not id_subcarpeta:
                print(f"No se encontró la subcarpeta {subcarpeta} en la carpeta con ID {id_carpeta_actual}")
                return "Error al buscar subcarpeta"
            id_carpeta_actual = id_subcarpeta 
        
        if name:
            try:
                if self.buscar(name, id_carpeta_actual):
                    eliminarArchivo = self.drive.CreateFile({'id': self.buscar(name, id_carpeta_actual)})
                    eliminarArchivo.Delete()
                    return "Archivo Eliminado con Exito"
                else:
                    print(f"No se encontró el archivo {name} en la carpeta con ID {id_carpeta_actual}")
                    return "Error al buscar archivo"
            except Exception as e:
                print(f"No se pudo eliminar el archivo {name} en la carpeta con ID {id_carpeta_actual}: {str(e)}")
                return "Error al eliminar archivo"
        
        else:
            try:
                eliminarFolder = self.drive.CreateFile({'id': id_carpeta_actual})
                eliminarFolder.Delete()
                return "Carpeta Eliminada con Exito"
            except Exception as e:
                print(f"No se pudo eliminar la carpeta con ID {id_carpeta_actual}: {str(e)}")
                return "Error al eliminar carpeta"

    def rename(self, path: str, name: str) -> str:
        path = path.strip('/')
        subcarpetas = path.split('/')
        carpeta_principal_id = '1UtnT-_UsMEnCO9pdltTUoxEe9wNptPii'
        carpeta_principal = None
        try:
            carpeta_principal = self.drive.CreateFile({'id': carpeta_principal_id})
        except Exception as e:
            print(f"No se pudo obtener la carpeta principal con el ID {carpeta_principal_id}: {str(e)}")
            return "Error al obtener la carpeta principal"
        id_carpeta_actual = carpeta_principal_id
        for subcarpeta in subcarpetas:
            id_subcarpeta = self.buscar(subcarpeta, id_carpeta_actual)
            if not id_subcarpeta:
                print(f"No se encontró la subcarpeta {subcarpeta} en la carpeta con ID {id_carpeta_actual}")
                return "Error al buscar subcarpeta"
            id_carpeta_actual = id_subcarpeta
        if self.buscar(name, id_carpeta_actual):
            print(f"Ya existe un archivo o carpeta con el nombre {name} en la carpeta con ID {id_carpeta_actual}")
            return "Error el archivo o carpeta ya existe"
        else:
            try:
                print(f"Renombrando archivo o carpeta en la carpeta con ID {id_carpeta_actual}")
                file = self.drive.CreateFile({'id': id_carpeta_actual})
                file['title'] = name
                file.Upload()
                return "Archivo renombrado con Exito"
            except Exception as e:
                print(f"No se pudo renombrar el archivo o carpeta en la carpeta con ID {id_carpeta_actual}: {str(e)}")
                return "Error al renombrar archivo o carpeta"

    def modify(self, path: str, body: str) -> str:
       
        path = path.strip('/')
        subcarpetas = path.split('/')

        carpeta_principal_id = '1UtnT-_UsMEnCO9pdltTUoxEe9wNptPii' 
        carpeta_principal = None
        try:
            carpeta_principal = self.drive.CreateFile({'id': carpeta_principal_id})
        except Exception as e:
            print(f"No se pudo obtener la carpeta principal con el ID {carpeta_principal_id}: {str(e)}")
            return "Error al obtener la carpeta principal"

        id_carpeta_actual = carpeta_principal_id
        for subcarpeta in subcarpetas:
            id_subcarpeta = self.buscar(subcarpeta, id_carpeta_actual)
            if not id_subcarpeta:
                print(f"No se encontró la subcarpeta {subcarpeta} en la carpeta con ID {id_carpeta_actual}")
                return "Error al buscar subcarpeta"
            id_carpeta_actual = id_subcarpeta  
        try:
            file = self.drive.CreateFile({'id': id_carpeta_actual})
            file.SetContentString(body)
            file.Upload()
            return "Contenido del Archivo modificado exitosamente"
        except Exception as e:
            print(f"No se pudo modificar el contenido del archivo en la carpeta con ID {id_carpeta_actual}: {str(e)}")
            return "Error al modificar el contenido del archivo"

    def copiarArchivo(self, id_archivo, id_folder, nombre):
        print(f"Copiando archivo con ID {id_archivo} a la carpeta con ID {id_folder}")
        archivo_para_copiar = {'title': nombre, 'parents': [{'id': id_folder}]}
        self.drive.auth.service.files().copy(fileId=id_archivo, body=archivo_para_copiar).execute()

    def copy(self, source: str, dest: str) -> str:
        
        source = source.strip('/')
        dest = dest.strip('/')
        subcarpetas_source = source.split('/')
        subcarpetas_dest = dest.split('/')

        carpeta_principal_id = '1UtnT-_UsMEnCO9pdltTUoxEe9wNptPii' 
        carpeta_principal = None
        try:
            carpeta_principal = self.drive.CreateFile({'id': carpeta_principal_id})
        except Exception as e:
            print(f"No se pudo obtener la carpeta principal con el ID {carpeta_principal_id}: {str(e)}")
            return "Error al obtener la carpeta principal"

        
        id_carpeta_source = carpeta_principal_id
        for subcarpeta in subcarpetas_source:
            id_subcarpeta = self.buscar(subcarpeta, id_carpeta_source)
            if not id_subcarpeta:
                print(f"No se encontró la subcarpeta {subcarpeta} en la carpeta con ID {id_carpeta_source}")
                return "Error al buscar subcarpeta"
            id_carpeta_source = id_subcarpeta  
        id_carpeta_dest = carpeta_principal_id
        for subcarpeta in subcarpetas_dest:
            id_subcarpeta = self.buscar(subcarpeta, id_carpeta_dest)
            if not id_subcarpeta:
                print(f"No se encontró la subcarpeta {subcarpeta} en la carpeta con ID {id_carpeta_dest}")
                return "Error al buscar subcarpeta"
            id_carpeta_dest = id_subcarpeta  
        try:
            archivo_o_carpeta = self.drive.CreateFile({'id': id_carpeta_source})
            if archivo_o_carpeta['mimeType'] == "application/vnd.google-apps.folder":
                archivos_en_carpeta = self.drive.ListFile({'q': f"'{id_carpeta_source}' in parents and trashed=false"}).GetList()
                for archivo in archivos_en_carpeta:
                    self.copiarArchivo(archivo['id'], id_carpeta_dest, archivo['title'])
            else:
                self.copiarArchivo(id_carpeta_source, id_carpeta_dest, archivo_o_carpeta['title'])
            return "Copia realizada con éxito"
        except Exception as e:
            print(f"No se pudo copiar el archivo o carpeta con ID {id_carpeta_source}: {str(e)}")
            return "Error al copiar archivo o carpeta"

    def transferirArchivo(self, id_archivo, id_folder):
        archivo = self.drive.CreateFile({'id': id_archivo})
        archivo['parents'] = [{'id': id_folder}]
        archivo.Upload(param={'supportsAllDrives': True})

    def transfer(self, source: str, dest: str) -> str:
        source = source.strip('/')
        dest = dest.strip('/')
        subcarpetas_source = source.split('/')
        subcarpetas_dest = dest.split('/')

        id_carpeta_source = None
        for subcarpeta in subcarpetas_source:
            if id_carpeta_source is None:
                id_carpeta_source = self.buscar(subcarpeta)
            else:
                id_carpeta_source = self.buscar(subcarpeta, id_carpeta_source)
            if not id_carpeta_source:
                print(f"No se encontró la subcarpeta {subcarpeta}")
                return "Error al buscar subcarpeta en la ruta de origen"

        id_carpeta_dest = None
        for subcarpeta in subcarpetas_dest:
            if id_carpeta_dest is None:
                id_carpeta_dest = self.buscar(subcarpeta)
            else:
                id_carpeta_dest = self.buscar(subcarpeta, id_carpeta_dest)
            if not id_carpeta_dest:
                print(f"No se encontró la subcarpeta {subcarpeta}")
                return "Error al buscar subcarpeta en la ruta de destino"

        try:
            archivo_o_carpeta = self.drive.CreateFile({'id': id_carpeta_source})
            if archivo_o_carpeta['mimeType'] == "application/vnd.google-apps.folder":
                archivos_en_carpeta = self.drive.ListFile({'q': f"'{id_carpeta_source}' in parents and trashed=false"}).GetList()
                for archivo in archivos_en_carpeta:
                    self.transferirArchivo(archivo['id'], id_carpeta_dest)
            else:
                self.transferirArchivo(id_carpeta_source, id_carpeta_dest)
            return "Transferencia realizada con éxito"
        except Exception as e:
            print(f"No se pudo transferir el archivo o carpeta con ID {id_carpeta_source}: {str(e)}")
            return "Error al transferir archivo o carpeta"

    def add(self, path, name ,body) -> str:
        
        path = path.strip('/')
        subcarpetas = path.split('/')

        carpeta_principal_id = '1UtnT-_UsMEnCO9pdltTUoxEe9wNptPii'
        carpeta_principal = None
        try:
            carpeta_principal = self.drive.CreateFile({'id': carpeta_principal_id})
        except Exception as e:
            print(f"No se pudo obtener la carpeta principal con el ID {carpeta_principal_id}: {str(e)}")
            return "Error al obtener la carpeta principal"

        
        id_carpeta_actual = carpeta_principal_id
        for subcarpeta in subcarpetas:
            id_subcarpeta = self.buscar(subcarpeta)
            if not id_subcarpeta:
                print(f"No se encontró la subcarpeta {subcarpeta} en la carpeta con ID {id_carpeta_actual}")
                return "Error al buscar subcarpeta"
            id_carpeta_actual = id_subcarpeta 
        
        try:
                print(f"Buscando archivo {name} en la carpeta con ID {id_carpeta_actual}")
                if self.buscar(name, id_carpeta_actual):
                    eliminarArchivo = self.drive.CreateFile({'id': self.buscar(name, id_carpeta_actual)})
                    contenido = eliminarArchivo.GetContentString()
                    añadiendo = contenido + "\n" + body
                    eliminarArchivo.SetContentString(añadiendo)
                    eliminarArchivo.Upload()
                    return "Contenido del archivo modificado Exitosamente"  
                else:
                    print(f"No se encontró el archivo {name} en la carpeta con ID {id_carpeta_actual}")
                    return "Error al buscar archivo"
        except Exception as e:
            print(f"No se pudo encontrar el archivo {name} en la carpeta con ID {id_carpeta_actual}: {str(e)}")
            return "Error al agregar archivo"
    
    def backup_nube(self):
            pass
        
    def backup_local(self, folder_path: str):
        parent_id='1UtnT-_UsMEnCO9pdltTUoxEe9wNptPii'
        if not os.path.isdir(folder_path):
            print(f"No se encontró el directorio local {folder_path}")
            return "Error al encontrar el directorio local"
        folder_name = os.path.basename(folder_path)
        print(f"Creando carpeta {folder_name} en Google Drive...")
        gd_folder = self.drive.CreateFile({
            'title': folder_name,
            'parents': [{'id': parent_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        })
        gd_folder.Upload()
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                print(f"Subiendo archivo {file_path}...")
                mime_type = mimetypes.guess_type(file_path)[0]
                mime_type = mime_type if mime_type else 'text/plain'

                gd_file = self.drive.CreateFile({
                    'title': file_name,
                    'parents': [{'id': gd_folder['id']}],
                    'mimeType': mime_type
                })
                gd_file.SetContentFile(file_path)
                gd_file.Upload()

        print(f"Carpeta {folder_path} subida con éxito a Google Drive!")
        return "Subida de carpeta completada"

    def descargar_carpeta(self, id_carpeta, ruta_local):
        if not os.path.exists(ruta_local):
            os.makedirs(ruta_local)
        query = f"'{id_carpeta}' in parents and trashed=false"
        items = self.drive.ListFile({'q': query}).GetList()

        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                print(f"Descargando carpeta {item['title']}...")
                self.descargar_carpeta(item['id'], os.path.join(ruta_local, item['title']))
            else:  
                print(f"Descargando archivo {item['title']}...")
                gd_file = self.drive.CreateFile({'id': item['id']})
                gd_file.GetContentFile(os.path.join(ruta_local, item['title']))

    def backup_nube(self, local_path: str):
        folder_id='1UtnT-_UsMEnCO9pdltTUoxEe9wNptPii'
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        gd_folder = self.drive.CreateFile({'id': folder_id})
        self.descargar_carpeta(folder_id, os.path.join(local_path, gd_folder['title']))
        print(f"Carpeta {gd_folder['title']} descargada con éxito a {local_path}!")


