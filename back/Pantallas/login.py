from tkinter import *
from tkinter import messagebox
from org.Pantallas.encriptado import desencriptar


class Registro:
    def __init__(self):
                       
        self.root = Tk()
        self.root.title("Iniciar sesión")
        self.root.geometry("300x200")
           
        username_label = Label(self.root, text="Nombre de Usuario")
        username_label.pack(pady=10)

        self.username_entry = Entry(self.root, width=30)
        self.username_entry.pack()

        password_label = Label(self.root, text="Contraseña")
        password_label.pack(pady=10)

        self.password_entry = Entry(self.root, width=30, show="*")
        self.password_entry.pack()


        login_button = Button(self.root, text="Ingresar", command=self.login)
        login_button.pack(pady=10)

        
        self.root.mainloop()
        

    def login(self):
        
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        registro = desencriptar(b'miaproyecto12345')
        if registro.leer_archivo(user,pwd) == True:
            self.root.destroy()
            from org.Pantallas.Admin import Application
            Application()
            #apagar ventana
            
            
            
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)

    



