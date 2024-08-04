# Testprogramm zum Aufruf der Funktionen des Server-Moduls
# Aktionen des Testprogramms:
# - verbindet mit dem THINGSBOARD_SERVER
# - Loop:
#   . holt Daten vom Raspberry Pi
#   . sendet Daten zum Server
#   . schläft 5 
#   . toggelt die alive-Variable
# Quelle: https://thingsboard.io/docs/devices-library/raspberry-pi-4/
# Quelle verteilt auf server_module.py und server_main.py

# Bibliotheken importieren
import logging.handlers
import time
import server_module

ACCESS_TOKEN = "vu3FCDn3RH6VeWgHyX4n"
THINGSBOARD_SERVER = 'thingsboard.cloud'

logging.basicConfig(level=logging.DEBUG)
    
# globale Variable
client = None

def main():
    global client, alive
    client = server_module.TBDeviceMqttClient(THINGSBOARD_SERVER, username=ACCESS_TOKEN)
    client.connect()
       
    try: 
        while not client.stopped:
            attributes, telemetry = server_module.get_data()
            client.send_attributes(attributes)
            client.send_telemetry(telemetry)
            time.sleep(5)
            server_module.alive = not server_module.alive
    except KeyboardInterrupt:
        print("Program terminated by user")
        client.disconnect()
   
if __name__=='__main__':
    if ACCESS_TOKEN != "TEST_TOKEN":
        main()
    else:
        print("Please change the ACCESS_TOKEN variable to match your device access token and run script again.")
