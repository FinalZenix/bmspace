# Inhalt des Moduls
# - Funktion zum Einlesen von:
#   . Raspberry Pi Daten
#   . Netzwerk-Attribute 
# Quelle: https://thingsboard.io/docs/devices-library/raspberry-pi-4/
# Quelle verteilt auf server_module.py und server_main.py

import os
from tb_gateway_mqtt import TBDeviceMqttClient

# alive Variable definieren
alive = False

# Funktion zum Einlesen der Daten
def get_data():
    cpu_usage = round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline().replace('\n', '').replace(',', '.')), 2)
    ip_address = os.popen('''hostname -I''').readline().replace('\n', '').replace(',', '.')[:-1]
    mac_address = os.popen('''cat /sys/class/net/*/address''').readline().replace('\n', '').replace(',', '.')
    processes_count = os.popen('''ps -Al | grep -c bash''').readline().replace('\n', '').replace(',', '.')[:-1]
    swap_memory_usage = os.popen("free -m | grep Swap | awk '{print ($3/$2)*100}'").readline().replace('\n', '').replace(',', '.')[:-1]
#     ram_usage = float(os.popen("free -m | grep Mem | awk '{print ($3/$2) * 100}'").readline().replace('\n', '').replace(',', '.')[:-1])
    ram_usage = 0.0
    st = os.statvfs('/')
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    boot_time = os.popen('uptime -p').read()[:-1]
    avg_load = (cpu_usage + ram_usage) / 2
   
    attributes = {
        'ip_address': ip_address,
        'macaddress': mac_address
    }
    telemetry = {
        'cpu_usage': cpu_usage,
        'processes_count': processes_count,
        'disk_usage': used,
        'RAM_usage': ram_usage,
        'swap_memory_usage': swap_memory_usage,
        'boot_time': boot_time,
        'avg_load': avg_load,
        'alive': alive
    }
    print(attributes, telemetry)
    return attributes, telemetry
