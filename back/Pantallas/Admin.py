
import sys
sys.path.append(r'Archivos 2/back/accion')
from accion.accion import create, delete, copy, transfer, rename, modify,backup, recovery, delete_all, opens
from Pantallas.Analizador import parse_command
from Pantallas.encriptado import desencriptar

class Application:
        
    def ejecutar(self,texto):
        resultado = ''
        for line in texto.splitlines():
            
            cmd, params = parse_command(line)
            
            if params is not None:
                if cmd == 'create':
                    if create(params['name'], params['body'], params['path'].replace('"', ''), params['type']):
                        resultado+="Creación exitosa en "+params['path']+ "\n"
                    else:
                        resultado+= "Error en la creación en "+params['path']+ "\n"
                elif cmd == 'delete':
                    if len(params) == 2:
                        if delete(params['path'].replace('"', ''), params['type']):
                            resultado+= "Eliminacion exitosa en "+params['path']+ "\n"
                        else:
                             resultado+= "Error en Eliminacion en "+params['path']+ "\n"
                    else:
                        if delete(params['path'].replace('"', ''), params['type'], params['name']):
                            resultado+= "Eliminacion exitosa en "+params['path']+ "\n"
                        else:
                             resultado+= "Error en Eliminacion en "+params['path']+ "\n"
                elif cmd == 'copy':
                    if copy(params['from'].replace('"', ''), params['to'].replace('"', ''), params['type_to'], params['type_from']):
                        resultado+= "Copia exitosa en "+params['to']+ "\n"
                    else:
                        resultado+= "Error en copia en "+params['to']+ "\n"
                elif cmd == 'transfer':
                    if transfer(params['from'].replace('"', ''), params['to'].replace('"', ''), params['type_to'], params['type_from']):
                        resultado+= "Transferencia exitosa en "+params['to']+ "\n"
                    else:
                        resultado+= "Error en la transferencia en "+params['to']+ "\n"
                elif cmd == 'rename':
                    if rename(params['path'].rsplit('/', 1)[0]+'/'.replace('"', ''), params['path'].split("/")[-1], params['name'].replace('"', ''), params['type']):
                        resultado+= "Renombrado exitoso"+ "\n"
                    else:
                        resultado+= "Error en el renombrado"+ "\n"
                elif cmd == 'modify':
                    print('entraaaaaaaaa')
                    if modify((params['path'].rsplit('/', 1)[0]+'/').replace('"', ''), params['path'].split("/")[-1], params['body'], params['type']):
                        resultado+= "Modificación exitosa"+ "\n"
                    else:
                        resultado+= "Error en la modificación"+ "\n"
                elif cmd == 'backup':
                    if len(params) == 3:
                        if backup(params['type_to'], params['type_from'], params['name']):
                            resultado+= "Backup exitoso en "+params['type_from']+ "\n"
                        else:
                             resultado+= "Error en Backup en "+params['type_from']+ "\n"
                    else:
                        if backup(params['type_to'], params['type_from'], params['name'], params['ip'], params['port']):
                            resultado+= "Backup exitoso en "+params['type_from']+ "\n"
                        else:
                             resultado+= "Error en Backup en "+params['type_from']+ "\n"
                elif cmd == 'recovery':
                    if len(params) == 3:
                        if recovery(params['type_to'], params['type_from'], params['name']):
                            resultado+= "recovery exitoso en "+params['type_from']+ "\n"
                        else:
                             resultado+= "Error en recovery en "+params['type_from']+ "\n"
                    else:
                        if recovery(params['type_to'], params['type_from'], params['name'], params['ip'], params['port']):
                            resultado+= "recovery exitoso en "+params['type_from']+ "\n"
                        else:
                             resultado+= "Error en recovery en "+params['type_from']+ "\n"
                elif cmd == 'delete_all':
                    if delete_all(params['type']):
                        resultado+= "delete_all exitoso" + "\n"
                    else:
                        resultado+= "Error delete_all"
                elif cmd == 'open':
                    if len(params) == 2:
                        if opens(params['type'], params['name']):
                            resultado+= "Apertura exitosa"
                        else:
                             resultado+= "Error en apertura"
                    else:
                        if opens(params['type'], params['name'], params['ip'], params['port']):
                            resultado+= "Apertura exitosa"
                        else:
                            resultado+= "Error en apertura"
                else:
                    resultado+= "Comando no reconocido"+ "\n"
            
            else:
                 resultado+= "No hay parámetros"+ "\n"
        return resultado
    
    # def comand_configure(self,tipo,encrypt_log,encrypt_read,llave):
    #     if llave == "":
    #         self.text_area.insert("end", "configure -type->"+tipo+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read+" -llave->"+llave)
    #     else:
    #         self.text_area.insert("end", "configure -type->"+tipo+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read+" -llave->"+llave)
    #     #configure -type->local -encrypt_log->false -encrypt_read->false 
    #     self.ejecutar()
    #     self.text_area.delete("1.0", "end")
    # def comand_create(self,name,path,body):
    #     self.text_area.insert("end", "create -name->"+name+" -path->"+path+" -body->"+body)
    #     #create -name->prueba1.txt  -path->/carpeta1/ -body->"Este es el contenido del archivo1"
    #     self.ejecutar()
    #     self.text_area.delete("1.0", "end")
    # def comand_delete(self,path,name):
    #     if name == "":
    #         self.text_area.insert("end", "delete -path->"+path+" ")
    #     else:
    #         self.text_area.insert("end", "delete -path->"+path+" -name->"+name)
    #     #delete -path->/carpeta1/ -name->prueba2.txt
    #     self.ejecutar()
    #     self.text_area.delete("1.0", "end")
    # def comand_copy(self,from_,to_):
    #     self.text_area.insert("end", "copy -from->"+from_+" -to->"+to_+"")
    #     #copy -from->/carpeta1/nuevo_nombre1.txt -to->/"Carpeta Ejemplo"/ 
    #     self.ejecutar()
    #     self.text_area.delete("1.0", "end")
    # def comand_transfer(self,from_,to_,mode):
    #     self.text_area.insert("end", "transfer -from->"+from_+" -to->"+to_+" -mode->"+mode+"")
    #     #transfer -from->/carpeta1/nuevo_nombre2.txt -to->/"Carpeta Ejemplo"/ -mode->"local"
    #     self.ejecutar()
    #     self.text_area.delete("1.0", "end")
    # def comand_rename(self,path,name):
    #     self.text_area.insert("end", "rename -path->"+path+" -name->"+name+"")
    #     #rename -path->/carpeta1/prueba1.txt -name->nuevo_nombre1.txt
    #     self.ejecutar()
    #     self.text_area.delete("1.0", "end")
    # def comand_modify(self,path,body):
    #     self.text_area.insert("end", "modify -path->"+path+" -body->"+body+"")
    #     #modify -path->/"Carpeta Ejemplo"/nuevo_nombre1.txt -body->"Almacenen"
    #     self.ejecutar()
    #     self.text_area.delete("1.0", "end")
    # def comand_add(self,path,body):
    #     self.text_area.insert("end", "add -path->"+path+" -body->"+body+"")
    #     #add -path->/"Carpeta Ejemplo"/nuevo_nombre1.txt  -body->"De esa"
    #     self.ejecutar()
    #     self.text_area.delete("1.0", "end")
    # def comand_backup(self):
    #     if backup():
    #         print("backup exitosa")
    #     else:
    #         print("Error en el backup")
    # def comand_exec(self,path):
    #     self.text_area.insert("end", "exec -path->"+path+"")
    #     #exec -path->/carpeta1/prueba1.txt
    #     self.ejecutar()
    #     self.text_area.delete("1.0", "end")
    
    
    # def ejecutar_texto(self, texto):
    #     for line in texto.splitlines():
    #         cmd, params = parse_command(line)
    #         if params is not None:
    #             if cmd == 'Configure':
    #                 if params[3] == None:
    #                     if configure(params[0], params[1], params[2]):
    #                         print("Configuración exitosa")
    #                     else:
    #                         print("Error en la configuración")
    #                 else:
    #                     if configure(params[0], params[1], params[2] ,params[4].replace('"', '')):
    #                         print("Configuración exitosa")
    #                     else:
    #                         print("Error en la configuración")
    #             elif cmd == 'create':
    #                 if create(params[0], params[2], params[1].replace('"', '')):
    #                     print("Creación exitosa")
    #                 else:
    #                     print("Error en la creación")
    #             elif cmd == 'delete':
    #                 print(params)
    #                 if params[1] == None:
    #                     if delete(params[0]):
    #                         print("Eliminación exitosa")
    #                     else:
    #                         print("Error en la eliminación")
    #                 else:
    #                     if delete(params[0], params[2].replace('"', '')):
    #                         print("Eliminación exitosa")
    #                     else:
    #                         print("Error en la eliminación")
    #             elif cmd == 'copy':
    #                 if copy(params[0].rsplit('/', 1)[0]+'/'.replace('"', ''), params[1].replace('"', ''), params[0].split("/")[-1]):
    #                     print("Copia exitosa")
    #                 else:
    #                     print("Error en la copia")
    #             elif cmd == 'transfer':
    #                 if params[2] == 'local':
    #                     tipo = '1'
    #                 else:
    #                     tipo = '2'
    #                 if transfer(params[0].rsplit('/', 1)[0]+'/'.replace('"', ''), params[1].replace('"', ''),tipo,params[0].split("/")[-1]):
    #                     print("Transferencia exitosa")
    #                 else:
    #                     print("Error en la transferencia")
    #             elif cmd == 'rename':
    #                 if rename(params[0].rsplit('/', 1)[0]+'/'.replace('"', ''), params[0].split("/")[-1], params[1]):
    #                     print("Renombrado exitoso")
    #                 else:
    #                     print("Error en el renombrado")
    #             elif cmd == 'modify':
    #                 if modify((params[0].rsplit('/', 1)[0]+'/').replace('"', ''), params[0].split("/")[-1], params[1]):
    #                     print("Modificación exitosa")
    #                 else:
    #                     print("Error en la modificación")
    #             elif cmd == 'add':
    #                 if add((params[0].rsplit('/', 1)[0]+'/').replace('"', ''), params[0].split("/")[-1], params[1]):
    #                     print("Adición exitosa")
    #                 else:
    #                     print("Error en la adición")
    #             elif cmd == 'backup':
    #                 if backup():
    #                     print("backup exitosa")
    #                 else:
    #                     print("Error en el backup")
    #             elif cmd == 'exec':
    #                 print(params[0])
    #                 try:
    #                     if devolver_ecrypt_read() == 2:
    #                         with open(params[0], 'r') as f:
    #                             guardar = self.text_area.get("1.0", "end")
    #                             self.text_area.delete("1.0", "end")
    #                             self.text_area.insert("1.0", f.read())
    #                             self.ejecutar()
    #                             self.text_area.delete("1.0", "end")
    #                             self.text_area.insert("1.0", guardar)
    #                     elif devolver_ecrypt_read() == 1:
    #                         with open(params[0], 'r') as f:
    #                             datos = desencriptar(b'miaproyecto12345')
    #                             texto = datos.desencriptare(f.read())
    #                             self.ejecutar_texto(texto)
    #                     else:
    #                         print('falta configurar el archivo')
                            
    #                 except FileNotFoundError:
    #                     print(f"La ruta especificada '{params[0]}' no existe")
    #             else:
    #                 print("Comando no reconocido")
            
    #         else:
    #             print("No hay parámetros")
    
    