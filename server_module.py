import os
import logging
from tb_gateway_mqtt import TBDeviceMqttClient
import json

# Load sensitive information from environment variables
ACCESS_TOKEN = "lcG8H24n5ftlbLz6zFoY"  # Fallback to default if not set
THINGSBOARD_SERVER = 'thingsboard.cloud'

# Set up logging
logging.basicConfig(filename='logfile.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize Thingsboard client
client = None

def TB_server_connect():
    """
    Connect to the Thingsboard server using MQTT client.
    """
    global client
    try:
        client = TBDeviceMqttClient(THINGSBOARD_SERVER, username=ACCESS_TOKEN)
        client.connect()
        logger.info("Successfully connected to Thingsboard server.")
    except Exception as e:
        logger.error(f"Failed to connect to Thingsboard server: {e}")
        raise  # Re-raise exception after logging

def get_network_attributes():
    """
    Retrieve network attributes such as IP address and MAC address.
    
    Returns:
        dict: A dictionary containing 'ip_address' and 'mac_address'.
    """
    try:
        ip_address = os.popen('hostname -I').read().strip().split(' ')[0]
        mac_address = os.popen('cat /sys/class/net/eth0/address').read().strip()

        ip_address = "test";
        mac_address = "test";

        attributes = {
            'ip_address': ip_address,
            'mac_address': mac_address
        }

        logger.debug(f"Network attributes retrieved: {attributes}")
        return attributes

    except Exception as e:
        logger.error(f"Failed to retrieve network attributes: {e}")
        return {}

def send_telemetry(data):
    """
    Send telemetry data to ThingsBoard server.

    Args:
        data (dict): The telemetry data to send.

    Returns:
        bool: True if telemetry data was sent successfully, False otherwise.
    """
    global client
    try:
        if not client:
            raise ConnectionError("MQTT client is not connected.")

        # Ensure the data is in JSON format
        if not isinstance(data, dict):
            raise ValueError("Telemetry data must be a dictionary.")

        client.send_telemetry(data)
        logger.info(f"Telemetry data sent successfully: {data}")
        return True

    except Exception as e:
        logger.error(f"Failed to send telemetry data: {e}")
        return False

# Improved cleanup and resource management
def cleanup():
    """
    Clean up resources like the MQTT client connection.
    """
    global client
    if client:
        try:
            client.disconnect()
            logger.info("Disconnected from Thingsboard server.")
        except Exception as e:
            logger.error(f"Error while disconnecting from Thingsboard server: {e}")

'''
Unit test to see if the connection works:
**This part of the code does not run if the library is imported.**
'''
if __name__ == "__main__":
    TB_server_connect()

    try:
        # Main loop (simulated example)
        while True:
            network_attrs = get_network_attributes()
            if network_attrs:
                # Send network attributes as telemetry
                send_telemetry(network_attrs)
            else:
                logger.warning("No network attributes to send.")
            
            # For demo purposes, we sleep and loop indefinitely
            import time
            time.sleep(5)
            
    except KeyboardInterrupt:
        logger.info("Program terminated by user.")
    finally:
        cleanup()
        logger.info("Program ended.")
