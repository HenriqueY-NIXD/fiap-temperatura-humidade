import os
import time
import random
from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient, Message

load_dotenv()

CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
TEMPERATURE = 22.0
HUMIDITY = 70
MSG_TXT = '{{"Temperatura": {temperature}, "Humidade": {humidity}}}'

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def run():
    try:
        client = iothub_client_init()

        while True:
            temperature = TEMPERATURE + (random.random() * 15)
            humidity = HUMIDITY + (random.random() * 20)
            msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
            message = Message(msg_txt_formatted)

            if temperature < 15 or temperature > 25:
              message.custom_properties["temperatureAlert"] = "true"
            else:
              message.custom_properties["temperatureAlert"] = "false"

            print("Mensagem: {}".format(message))

            client.send_message(message)

            print ("Mensagem enviada")
            time.sleep(5)

    except KeyboardInterrupt:
        print ("Fecho")

if __name__ == '__main__':
    print ( "Pressione Ctrl-C para sair" )
    run()