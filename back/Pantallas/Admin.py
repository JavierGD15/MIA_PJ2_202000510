import tkinter as tk
import sys
sys.path.append(r'Archivos_P1\Archivos_P1-develop\Archivos_P1\org')
from accion.accion import configure, create, delete, copy, transfer, rename, modify, add, devolver_ecrypt_read, backup
from Pantallas.login import Registro
from tkinter import ttk
from tkinter import scrolledtext
from Pantallas.Analizador import parse_command
from tkinter import scrolledtext, PhotoImage
from Pantallas.encriptado import desencriptar

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg='orange')
        self.photo = PhotoImage(file="Archivos_P1\\Archivos_P1-develop\\Archivos_P1\\org\\Pantallas\\foto.png")
        self.photo = self.photo.subsample(2, 2)
        self.img_label = tk.Label(self, image=self.photo, bg='orange')
        self.img_label.grid(row=0, column=0, columnspan=1, sticky="ew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.text_area = scrolledtext.ScrolledText(self, width=40, height=10)
        self.text_area.grid(row=1, column=0, rowspan=10, padx=10, pady=10, sticky='nsew')
        commands = ['Configure', 'Create', 'Delete', 'Copy', 'Transfer', 'Rename', 'Modify', 'Add', 'Exec']
        for i, command in enumerate(commands):
            button = tk.Button(self, text=command, command=lambda cmd=command: self.open_window(cmd), bg='light blue', borderwidth=2, width=10)
            button.grid(row=i//2, column=1+i%2, padx=20, pady=20)

        self.Backup = tk.Button(self, text="Backup", command=self.comand_backup, bg='light blue', borderwidth=2, width=10)
        self.Backup.grid(row=4, column=2, padx=20, pady=20)

        self.ejecutar_button = tk.Button(self, text="Ejecutar", command=self.ejecutar, bg='light blue', borderwidth=2, width=10)
        self.ejecutar_button.grid(row=5, column=1, padx=20, pady=20)

        self.quit_button = tk.Button(self, text="Cerrar sesión", command=self.cerrar, bg='light blue', borderwidth=2, width=10)
        self.quit_button.grid(row=5, column=2, padx=20, pady=20)


    def open_window(self, command):
        window = tk.Toplevel(self)
        window.configure(bg='orange')
        window.title(command)
        if command == 'Configure':            
            tk.Label(window, text="-type").grid(row=0, column=0, padx=10, pady=10)
            combo1 = ttk.Combobox(window)
            combo1['values'] = ("Local", "Cloud")
            combo1.current(0)
            combo1.grid(row=0, column=1, padx=10, pady=10)           
            tk.Label(window, text="-encrypt_log").grid(row=1, column=0, padx=10, pady=10)
            combo2 = ttk.Combobox(window)
            combo2['values'] = ("true", "false")
            combo2.current(0)
            combo2.grid(row=1, column=1, padx=10, pady=10)         
            tk.Label(window, text="-encrypt_read").grid(row=2, column=0, padx=10, pady=10)
            combo3 = ttk.Combobox(window)
            combo3['values'] = ("true", "false")
            combo3.current(0)
            combo3.grid(row=2, column=1, padx=10, pady=10)            
            tk.Label(window, text="llave").grid(row=3, column=0, padx=10, pady=10)
            entry1 = tk.Entry(window)
            entry1.grid(row=3, column=1, padx=10, pady=10)             
            tk.Button(window, text="Ejecutar", command= lambda: self.comand_configure(combo1.get(),combo2.get(),combo3.get(),entry1.get()), bg='light blue', borderwidth=2).grid(row=4, column=0, padx=10, pady=10)
            tk.Button(window, text="Cancelar", command=window.destroy, bg='light blue', borderwidth=2).grid(row=4, column=1, padx=10, pady=10) 
        elif command == 'Create':
            tk.Label(window, text="-name").grid(row=1, column=0, padx=10, pady=10)
            entry1 = tk.Entry(window)
            entry1.grid(row=1, column=1, padx=10, pady=10)

            tk.Label(window, text="-body").grid(row=2, column=0, padx=10, pady=10)
            entry2 = tk.Entry(window)
            entry2.grid(row=2, column=1, padx=10, pady=10)

            tk.Label(window, text="path").grid(row=3, column=0, padx=10, pady=10)
            entry3 = tk.Entry(window)
            entry3.grid(row=3, column=1, padx=10, pady=10)             
            tk.Button(window, text="Ejecutar", command= lambda: self.comand_create(entry1.get(), entry3.get(), entry2.get())).grid(row=4, column=0, padx=10, pady=10)         
            tk.Button(window, text="Cancelar", command=window.destroy).grid(row=4, column=1, padx=10, pady=10)
        elif command == 'Delete':
            tk.Label(window, text="-path").grid(row=1, column=0, padx=10, pady=10)
            entry1 = tk.Entry(window)
            entry1.grid(row=1, column=1, padx=10, pady=10)

            tk.Label(window, text="-name").grid(row=2, column=0, padx=10, pady=10)
            entry2 = tk.Entry(window)
            entry2.grid(row=2, column=1, padx=10, pady=10)
            tk.Button(window, text="Ejecutar", command= lambda: self.comand_delete(entry1.get(), entry2.get())).grid(row=4, column=0, padx=10, pady=10)             
            tk.Button(window, text="Cancelar", command=window.destroy).grid(row=4, column=1, padx=10, pady=10)
        elif command == 'Copy':
            
            tk.Label(window, text="-from").grid(row=1, column=0, padx=10, pady=10)
            entry1 = tk.Entry(window)
            entry1.grid(row=1, column=1, padx=10, pady=10)

            tk.Label(window, text="-to").grid(row=2, column=0, padx=10, pady=10)
            entry2 = tk.Entry(window)
            entry2.grid(row=2, column=1, padx=10, pady=10)     
             
            tk.Button(window, text="Ejecutar", command= lambda: self.comand_copy(entry1.get(), entry2.get())).grid(row=4, column=0, padx=10, pady=10)
            tk.Button(window, text="Cancelar", command=window.destroy).grid(row=4, column=1, padx=10, pady=10)
        elif command == 'Transfer':
            
            tk.Label(window, text="-from").grid(row=1, column=0, padx=10, pady=10)
            entry1 = tk.Entry(window)
            entry1.grid(row=1, column=1, padx=10, pady=10)

            tk.Label(window, text="-to").grid(row=2, column=0, padx=10, pady=10)
            entry2 = tk.Entry(window)
            entry2.grid(row=2, column=1, padx=10, pady=10)  
            
            tk.Label(window, text="-mode").grid(row=3, column=0, padx=10, pady=10)
            entry3 = tk.Entry(window)
            entry3.grid(row=3, column=1, padx=10, pady=10)
            
            tk.Button(window, text="Ejecutar", command= lambda: self.comand_transfer(entry1.get(), entry2.get(), entry3.get())).grid(row=4, column=0, padx=10, pady=10)     
            tk.Button(window, text="Cancelar", command=window.destroy).grid(row=4, column=1, padx=10, pady=10)
        elif command == 'Rename':
            
            tk.Label(window, text="-path").grid(row=1, column=0, padx=10, pady=10)
            entry1 = tk.Entry(window)
            entry1.grid(row=1, column=1, padx=10, pady=10)

            tk.Label(window, text="-name").grid(row=2, column=0, padx=10, pady=10)
            entry2 = tk.Entry(window)
            entry2.grid(row=2, column=1, padx=10, pady=10)          
            tk.Button(window, text="Ejecutar", command= lambda: self.comand_rename(entry1.get(), entry2.get())).grid(row=4, column=0, padx=10, pady=10)             
            tk.Button(window, text="Cancelar", command=window.destroy).grid(row=4, column=1, padx=10, pady=10)
        elif command == 'Modify':
            # Crear la etiqueta y el campo de entrada para "path".
            tk.Label(window, text="path").grid(row=0, column=0, padx=10, pady=10)
            entry_path = tk.Entry(window)
            entry_path.grid(row=0, column=1, padx=10, pady=10)

            # Crear la etiqueta y el campo de texto para "body".
            tk.Label(window, text="body").grid(row=1, column=0, padx=10, pady=10)
            text_body = tk.Text(window, height=5, width=30)
            text_body.grid(row=1, column=1, padx=10, pady=10)         
            tk.Button(window, text="Ejecutar", command= lambda: self.comand_modify(entry_path.get(),text_body.get("1.0", tk.END))).grid(row=4, column=0, padx=10, pady=10)
            tk.Button(window, text="Cancelar", command=window.destroy).grid(row=4, column=1, padx=10, pady=10)
        elif command == 'Add':
            # Crear la etiqueta y el campo de entrada para "path".
            tk.Label(window, text="path").grid(row=0, column=0, padx=10, pady=10)
            entry_path = tk.Entry(window)
            entry_path.grid(row=0, column=1, padx=10, pady=10)

            # Crear la etiqueta y el campo de texto para "body".
            tk.Label(window, text="body").grid(row=1, column=0, padx=10, pady=10)
            text_body = tk.Text(window, height=5, width=30)
            text_body.grid(row=1, column=1, padx=10, pady=10)                   
            tk.Button(window, text="Ejecutar", command= lambda: self.comand_add(entry_path.get(),text_body.get("1.0", tk.END))).grid(row=4, column=0, padx=10, pady=10)            
            tk.Button(window, text="Cancelar", command=window.destroy).grid(row=4, column=1, padx=10, pady=10)        
        elif command == 'Exec':
            # Crear la etiqueta y el campo de entrada para "path".
            tk.Label(window, text="path").grid(row=0, column=0, padx=10, pady=10)
            entry_path = tk.Entry(window)
            entry_path.grid(row=0, column=1, padx=10, pady=10)           
            tk.Button(window, text="Ejecutar", command= lambda: self.comand_exec(entry_path.get())).grid(row=4, column=0, padx=10, pady=10)
            tk.Button(window, text="Cancelar", command=window.destroy).grid(row=4, column=1, padx=10, pady=10)
        else:
            message = f"Ventana para el comando {command}"

    def ejecutar(self):
        texto = self.text_area.get("1.0", "end")
        for line in texto.splitlines():
            cmd, params = parse_command(line)
            if params is not None:
                if cmd == 'Configure':
                    if params[3] == None:
                        if configure(params[0], params[1], params[2]):
                            print("Configuración exitosa")
                        else:
                            print("Error en la configuración")
                    else:
                        if configure(params[0], params[1], params[2] ,params[4].replace('"', '')):
                            print("Configuración exitosa")
                        else:
                            print("Error en la configuración")
                elif cmd == 'create':
                    if create(params[0], params[2], params[1].replace('"', '')):
                        print("Creación exitosa")
                    else:
                        print("Error en la creación")
                elif cmd == 'delete':
                    
                    print(params)
                    if params[1] == None:
                        if delete(params[0]):
                            print("Eliminación exitosa")
                        else:
                            print("Error en la eliminación")
                    else:
                        if delete(params[0], params[2].replace('"', '')):
                            print("Eliminación exitosa")
                        else:
                            print("Error en la eliminación")
                elif cmd == 'copy':
                    if copy(params[0].rsplit('/', 1)[0]+'/'.replace('"', ''), params[1].replace('"', ''), params[0].split("/")[-1]):
                        print("Copia exitosa")
                    else:
                        print("Error en la copia")
                elif cmd == 'transfer':
                    if params[2] == 'local':
                        tipo = '1'
                    else:
                        tipo = '2'
                    if transfer(params[0].rsplit('/', 1)[0]+'/'.replace('"', ''), params[1].replace('"', ''),tipo,params[0].split("/")[-1]):
                        print("Transferencia exitosa")
                    else:
                        print("Error en la transferencia")
                elif cmd == 'rename':
                    if rename(params[0].rsplit('/', 1)[0]+'/'.replace('"', ''), params[0].split("/")[-1], params[1]):
                        print("Renombrado exitoso")
                    else:
                        print("Error en el renombrado")
                elif cmd == 'modify':
                    if modify((params[0].rsplit('/', 1)[0]+'/').replace('"', ''), params[0].split("/")[-1], params[1]):
                        print("Modificación exitosa")
                    else:
                        print("Error en la modificación")
                elif cmd == 'add':
                    if add((params[0].rsplit('/', 1)[0]+'/').replace('"', ''), params[0].split("/")[-1], params[1]):
                        print("Adición exitosa")
                    else:
                        print("Error en la adición")
                elif cmd == 'backup':
                    if backup():
                        print("backup exitosa")
                    else:
                        print("Error en el backup")
                elif cmd == 'exec':
                    print(params)
                    with open(params[0], 'r') as f:
                                self.ejecutar_texto(f.read())
                    # try:
                    #     if devolver_ecrypt_read() == 2:
                    #         with open(params[0], 'r') as f:
                    #             self.ejecutar_texto(f.read())
                    #     elif devolver_ecrypt_read() == 1:
                    #         with open(params[0], 'r') as f:
                    #             datos = desencriptar(b'miaproyecto12345')
                    #             texto = datos.desencriptare(f.read())
                    #             self.ejecutar_texto(texto)
                    #     else:
                    #         print('falta configurar el archivo')
                            
                    # except FileNotFoundError:
                    #     print(f"La ruta especificada '{params[0]}' no existe")
                else:
                    print("Comando no reconocido")
            
            else:
                print("No hay parámetros")
    
    def comand_configure(self,tipo,encrypt_log,encrypt_read,llave):
        if llave == "":
            self.text_area.insert("end", "configure -type->"+tipo+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read+" -llave->"+llave)
        else:
            self.text_area.insert("end", "configure -type->"+tipo+" -encrypt_log->"+encrypt_log+" -encrypt_read->"+encrypt_read+" -llave->"+llave)
        #configure -type->local -encrypt_log->false -encrypt_read->false 
        self.ejecutar()
        self.text_area.delete("1.0", "end")
    def comand_create(self,name,path,body):
        self.text_area.insert("end", "create -name->"+name+" -path->"+path+" -body->"+body)
        #create -name->prueba1.txt  -path->/carpeta1/ -body->"Este es el contenido del archivo1"
        self.ejecutar()
        self.text_area.delete("1.0", "end")
    def comand_delete(self,path,name):
        if name == "":
            self.text_area.insert("end", "delete -path->"+path+" ")
        else:
            self.text_area.insert("end", "delete -path->"+path+" -name->"+name)
        #delete -path->/carpeta1/ -name->prueba2.txt
        self.ejecutar()
        self.text_area.delete("1.0", "end")
    def comand_copy(self,from_,to_):
        self.text_area.insert("end", "copy -from->"+from_+" -to->"+to_+"")
        #copy -from->/carpeta1/nuevo_nombre1.txt -to->/"Carpeta Ejemplo"/ 
        self.ejecutar()
        self.text_area.delete("1.0", "end")
    def comand_transfer(self,from_,to_,mode):
        self.text_area.insert("end", "transfer -from->"+from_+" -to->"+to_+" -mode->"+mode+"")
        #transfer -from->/carpeta1/nuevo_nombre2.txt -to->/"Carpeta Ejemplo"/ -mode->"local"
        self.ejecutar()
        self.text_area.delete("1.0", "end")
    def comand_rename(self,path,name):
        self.text_area.insert("end", "rename -path->"+path+" -name->"+name+"")
        #rename -path->/carpeta1/prueba1.txt -name->nuevo_nombre1.txt
        self.ejecutar()
        self.text_area.delete("1.0", "end")
    def comand_modify(self,path,body):
        self.text_area.insert("end", "modify -path->"+path+" -body->"+body+"")
        #modify -path->/"Carpeta Ejemplo"/nuevo_nombre1.txt -body->"Almacenen"
        self.ejecutar()
        self.text_area.delete("1.0", "end")
    def comand_add(self,path,body):
        self.text_area.insert("end", "add -path->"+path+" -body->"+body+"")
        #add -path->/"Carpeta Ejemplo"/nuevo_nombre1.txt  -body->"De esa"
        self.ejecutar()
        self.text_area.delete("1.0", "end")
    def comand_backup(self):
        if backup():
            print("backup exitosa")
        else:
            print("Error en el backup")
    def comand_exec(self,path):
        self.text_area.insert("end", "exec -path->"+path+"")
        #exec -path->/carpeta1/prueba1.txt
        self.ejecutar()
        self.text_area.delete("1.0", "end")
    
    
    def ejecutar_texto(self, texto):
        for line in texto.splitlines():
            cmd, params = parse_command(line)
            if params is not None:
                if cmd == 'Configure':
                    if params[3] == None:
                        if configure(params[0], params[1], params[2]):
                            print("Configuración exitosa")
                        else:
                            print("Error en la configuración")
                    else:
                        if configure(params[0], params[1], params[2] ,params[4].replace('"', '')):
                            print("Configuración exitosa")
                        else:
                            print("Error en la configuración")
                elif cmd == 'create':
                    if create(params[0], params[2], params[1].replace('"', '')):
                        print("Creación exitosa")
                    else:
                        print("Error en la creación")
                elif cmd == 'delete':
                    print(params)
                    if params[1] == None:
                        if delete(params[0]):
                            print("Eliminación exitosa")
                        else:
                            print("Error en la eliminación")
                    else:
                        if delete(params[0], params[2].replace('"', '')):
                            print("Eliminación exitosa")
                        else:
                            print("Error en la eliminación")
                elif cmd == 'copy':
                    if copy(params[0].rsplit('/', 1)[0]+'/'.replace('"', ''), params[1].replace('"', ''), params[0].split("/")[-1]):
                        print("Copia exitosa")
                    else:
                        print("Error en la copia")
                elif cmd == 'transfer':
                    if params[2] == 'local':
                        tipo = '1'
                    else:
                        tipo = '2'
                    if transfer(params[0].rsplit('/', 1)[0]+'/'.replace('"', ''), params[1].replace('"', ''),tipo,params[0].split("/")[-1]):
                        print("Transferencia exitosa")
                    else:
                        print("Error en la transferencia")
                elif cmd == 'rename':
                    if rename(params[0].rsplit('/', 1)[0]+'/'.replace('"', ''), params[0].split("/")[-1], params[1]):
                        print("Renombrado exitoso")
                    else:
                        print("Error en el renombrado")
                elif cmd == 'modify':
                    if modify((params[0].rsplit('/', 1)[0]+'/').replace('"', ''), params[0].split("/")[-1], params[1]):
                        print("Modificación exitosa")
                    else:
                        print("Error en la modificación")
                elif cmd == 'add':
                    if add((params[0].rsplit('/', 1)[0]+'/').replace('"', ''), params[0].split("/")[-1], params[1]):
                        print("Adición exitosa")
                    else:
                        print("Error en la adición")
                elif cmd == 'backup':
                    if backup():
                        print("backup exitosa")
                    else:
                        print("Error en el backup")
                elif cmd == 'exec':
                    print(params[0])
                    try:
                        if devolver_ecrypt_read() == 2:
                            with open(params[0], 'r') as f:
                                guardar = self.text_area.get("1.0", "end")
                                self.text_area.delete("1.0", "end")
                                self.text_area.insert("1.0", f.read())
                                self.ejecutar()
                                self.text_area.delete("1.0", "end")
                                self.text_area.insert("1.0", guardar)
                        elif devolver_ecrypt_read() == 1:
                            with open(params[0], 'r') as f:
                                datos = desencriptar(b'miaproyecto12345')
                                texto = datos.desencriptare(f.read())
                                self.ejecutar_texto(texto)
                        else:
                            print('falta configurar el archivo')
                            
                    except FileNotFoundError:
                        print(f"La ruta especificada '{params[0]}' no existe")
                else:
                    print("Comando no reconocido")
            
            else:
                print("No hay parámetros")
    
    def cerrar(self):
        self.master.destroy()
        Registro()
        

root = tk.Tk()
app = Application(master=root)
app.mainloop()
