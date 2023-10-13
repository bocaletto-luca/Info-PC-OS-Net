# Software Name: Info PC/OS/Net
# Author: Bocaletto Luca
# Site Web: https://www.elektronoide.it
# License: GPLv3

import tkinter as tk
import platform
import psutil
import socket
import GPUtil
import requests
import uuid
import wmi
import getpass
import locale
import time

# Funzione per ottenere informazioni sulla scheda madre
def get_motherboard_info():
    c = wmi.WMI()
    motherboard_info = [
        ("Produttore Scheda Madre", c.Win32_BaseBoard()[0].Manufacturer),
        ("Chipset Scheda Madre", c.Win32_BaseBoard()[0].Product)
    ]
    return motherboard_info

# Funzione per ottenere informazioni sul sistema operativo e il computer
def get_system_info():
    system_info = [
        ("Sistema Operativo", f"{platform.system()} {platform.release()}"),
        ("Versione di Build", platform.win32_ver()[1]),
        ("Nome Utente", getpass.getuser()),  # Aggiunto Nome Utente
        ("Architettura", platform.architecture()),  # Aggiunta Architettura
        ("Lingua del Sistema", locale.getlocale()[0]),  # Aggiunta Lingua del Sistema
        ("Fuso Orario", time.tzname[0])  # Aggiunto Fuso Orario
    ]
    return system_info


# Funzione per ottenere l'indirizzo IP con il formato desiderato
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return [("Indirizzo IP", ip_address)]

# Funzione per ottenere il provider IP
def get_ip_provider():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        ip = data.get("ip", "IP sconosciuto")
        provider = data.get("org", "Provider IP sconosciuto")
        return [("Indirizzo IP", ip), ("Provider IP", provider)]
    except Exception as e:
        return [("Indirizzo IP", "N/A"), ("Provider IP", "N/A")]

def get_network_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
        network_info = [
            ("Indirizzo IP", ip_address),
            ("Indirizzo MAC", mac_address)
        ]
        return network_info
    except Exception as e:
        return [("Informazioni sulla rete", "N/A")]

# Funzione per ottenere informazioni sulla CPU
def get_cpu_info():
    cpu_info = [
        ("CPU", f"{psutil.cpu_percent()}% in uso"),
        ("Nome Processore", platform.processor()),
        ("Numero di Core", psutil.cpu_count(logical=False)),
        ("Numero di Thread", psutil.cpu_count(logical=True))
    ]
    return cpu_info

# Funzione per ottenere informazioni sulla GPU, inclusa la VRAM in GB
def get_gpu_info():
    try:
        gpu_info = GPUtil.getGPUs()[0]
        gpu_name = gpu_info.name
        gpu_load = gpu_info.load
        gpu_memory_total_mb = gpu_info.memoryTotal
        gpu_memory_free_mb = gpu_info.memoryFree
        gpu_memory_total_gb = gpu_memory_total_mb / 1024  # Conversione da MB a GB
        gpu_memory_free_gb = gpu_memory_free_mb / 1024  # Conversione da MB a GB
        return [
            ("GPU", gpu_name),
            ("Utilizzo GPU", f"{gpu_load * 100:.2f}%"),
            ("VRAM totale", f"{gpu_memory_total_gb:.2f} GB"),
            ("VRAM libera", f"{gpu_memory_free_gb:.2f} GB")
        ]
    except Exception as e:
        return [("GPU", "N/A")]

# Funzione per ottenere informazioni sulle risorse del sistema
def get_system_resources():
    ram_info = [
        ("RAM totale", f"{psutil.virtual_memory().total/1e9:.2f} GB"),
        ("RAM in uso", f"{psutil.virtual_memory().used/1e9:.2f} GB")
    ]

    def get_hdd_info():
        partitions = psutil.disk_partitions()
        hdd_info = [("HDD", "")]
        for partition in partitions:
            hdd_info.append(
                (f"{partition.device}", f"{psutil.disk_usage(partition.device).total/1e9:.2f} GB totale, {psutil.disk_usage(partition.device).used/1e9:.2f} GB in uso")
            )
        return hdd_info

    hdd_info = get_hdd_info()
    ip_provider = get_ip_provider()
    network_info = get_network_info()

    return get_motherboard_info() + get_cpu_info() + ram_info + get_gpu_info() + hdd_info + ip_provider + network_info

# Funzione per ottenere tutte le informazioni
def get_all_info():
    info = get_system_info() + get_system_resources()
    return info

# Creazione della finestra principale
root = tk.Tk()
root.title("INFO PC/OS/NET")

# Creazione di una tabella
for i, (name, data) in enumerate(get_all_info()):
    label_name = tk.Label(root, text=name, font=("Arial", 12))
    label_name.grid(row=i, column=0, sticky="W")

    if isinstance(data, list):  # Verifica se i dati sono una lista (per l'HDD, GPU e altri)
        for j, (sub_name, sub_data) in enumerate(data):
            label_sub_name = tk.Label(root, text=sub_name, font=("Arial", 12))
            label_sub_name.grid(row=i + j, column=1, sticky="W")

            label_sub_data = tk.Label(root, text=sub_data, font=("Arial", 12))
            label_sub_data.grid(row=i + j, column=2, sticky="W")
    else:
        label_data = tk.Label(root, text=data, font=("Arial", 12))
        label_data.grid(row=i, column=1, columnspan=2, sticky="W")

# Esecuzione del loop principale della GUI
root.mainloop()
