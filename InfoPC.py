# Software Name: Info PC/OS/Net
# Author: Luca Bocaletto
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

# Function to get motherboard information
def get_motherboard_info():
    c = wmi.WMI()
    motherboard_info = [
        ("Motherboard Manufacturer", c.Win32_BaseBoard()[0].Manufacturer),
        ("Motherboard Chipset", c.Win32_BaseBoard()[0].Product)
    ]
    return motherboard_info

# Function to get information about the operating system and the computer
def get_system_info():
    system_info = [
        ("Operating System", f"{platform.system()} {platform.release()}"),
        ("Build Version", platform.win32_ver()[1]),
        ("Username", getpass.getuser()),
        ("Architecture", platform.architecture()),
        ("System Language", locale.getlocale()[0]),
        ("Timezone", time.tzname[0])
    ]
    return system_info

# Function to get IP address in the desired format
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return [("IP Address", ip_address)]

# Function to get the IP provider
def get_ip_provider():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        ip = data.get("ip", "Unknown IP")
        provider = data.get("org", "Unknown IP Provider")
        return [("IP Address Global", ip), ("IP Provider", provider)]
    except Exception as e:
        return [("IP Address", "N/A"), ("IP Provider", "N/A")]

def get_network_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
        network_info = [
            ("IP Address PC", ip_address),
            ("MAC Address", mac_address)
        ]
        return network_info
    except Exception as e:
        return [("Network Information", "N/A")]

# Function to get CPU information
def get_cpu_info():
    cpu_info = [
        ("CPU", f"{psutil.cpu_percent()}% in use"),
        ("Processor Name", platform.processor()),
        ("Number of Cores", psutil.cpu_count(logical=False)),
        ("Number of Threads", psutil.cpu_count(logical=True))
    ]
    return cpu_info

# Function to get GPU information, including VRAM in GB
def get_gpu_info():
    try:
        gpu_info = GPUtil.getGPUs()[0]
        gpu_name = gpu_info.name
        gpu_load = gpu_info.load
        gpu_memory_total_mb = gpu_info.memoryTotal
        gpu_memory_free_mb = gpu_info.memoryFree
        gpu_memory_total_gb = gpu_memory_total_mb / 1024
        gpu_memory_free_gb = gpu_memory_free_mb / 1024
        return [
            ("GPU", gpu_name),
            ("GPU Usage", f"{gpu_load * 100:.2f}%"),
            ("Total VRAM", f"{gpu_memory_total_gb:.2f} GB"),
            ("Free VRAM", f"{gpu_memory_free_gb:.2f} GB")
        ]
    except Exception as e:
        return [("GPU", "N/A")]

# Function to get system resource information
def get_system_resources():
    ram_info = [
        ("Total RAM", f"{psutil.virtual_memory().total/1e9:.2f} GB"),
        ("Used RAM", f"{psutil.virtual_memory().used/1e9:.2f} GB")
    ]

    def get_hdd_info():
        partitions = psutil.disk_partitions()
        hdd_info = [("HDD", "")]
        for partition in partitions:
            hdd_info.append(
                (f"{partition.device}", f"{psutil.disk_usage(partition.device).total/1e9:.2f} GB total, {psutil.disk_usage(partition.device).used/1e9:.2f} GB used")
            )
        return hdd_info

    hdd_info = get_hdd_info()
    ip_provider = get_ip_provider()
    network_info = get_network_info()

    return get_motherboard_info() + get_cpu_info() + ram_info + get_gpu_info() + hdd_info + ip_provider + network_info

# Function to get all information
def get_all_info():
    info = get_system_info() + get_system_resources()
    return info

# Create the main window
root = tk.Tk()
root.title("Info PC/OS/NET")

# Create a table
for i, (name, data) in enumerate(get_all_info()):
    label_name = tk.Label(root, text=name, font=("Arial", 12))
    label_name.grid(row=i, column=0, sticky="W")

    if isinstance(data, list):  
        for j, (sub_name, sub_data) in enumerate(data):
            label_sub_name = tk.Label(root, text=sub_name, font=("Arial", 12))
            label_sub_name.grid(row=i + j, column=1, sticky="W")

            label_sub_data = tk.Label(root, text=sub_data, font=("Arial", 12))
            label_sub_data.grid(row=i + j, column=2, sticky="W")
    else:
        label_data = tk.Label(root, text=data, font=("Arial", 12))
        label_data.grid(row=i, column=1, columnspan=2, sticky="W")

# Run the main GUI loop
root.mainloop()
