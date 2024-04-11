import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

# Variáveis com os tópicos utilizados
myTopicTemperatura = "/Temp/infLed"
myTopicUmidade = "/Umid/infLed" 
myTopicDistancia = "/Dist/infLed"
myTopicActionDistance = "/Act/Sonoro"
myTopicAction = "/Action/Buzzer"


# Variáveis que receberão os valores de temp. e umid. do sensor DHT22 (Wokwi)
temperature = 0.0
humidity = 0.0
#variável para a distância
distance = 0

# Conexão com o Broker
mqttBroker ="broker.hivemq.com" 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(mqttBroker) 

def tratarSens():
    comando = ''
    
    #tratando da distância da água
    if distance < 100 and (humidity > 70 and temperature < 20):
        client.loop()
        client.publish(myTopicActionDistance, '1')
        comando = '1'
        print("O nível da água está alto! Riscos de alagamento!")

    elif distance < 100 and (humidity > 70 and temperature > 25):
        client.loop()
        client.publish(myTopicAction, '1') # Ativar alarme
        comando = '1'
        print("Provavelmente choverá forte! Riscos de alagamento!")
    else:
        client.loop()
        client.publish(myTopicAction, '0') # Não ativar alarme
        comando = '0'
        print("Sem riscos de alagamento.")

    return comando

# Esta função analisa o tópico que deverá ser escutado e armazena o conteúdo do tópico (payload) em uma variável
def callback(client, userdata, message):
    global myTopicTemperatura, myTopicUmidade, myTopicDistancia, temperature, humidity, distance

    print("Tópico: ", str(message.topic))
    if (message.topic == myTopicTemperatura):
               temperature = int(str(message.payload.decode("utf-8"))) 
    if (message.topic == myTopicUmidade):
                humidity = int(str(message.payload.decode("utf-8")))
    if (message.topic == myTopicDistancia):
                distance = int(str(message.payload.decode("utf-8")))
    
# Indica o assunto de cada tópico
#print("Temperatura: " + str(myTopicTemperatura))
#print("Umidade: " + str(myTopicUmidade))
    
client.message_callback_add("/Temp/infLed", callback)
client.subscribe("/Temp/infLed")

client.message_callback_add("/Umid/infLed", callback)
client.subscribe("/Umid/infLed")

client.message_callback_add("/Dist/infLed", callback)
client.subscribe("/Dist/infLed")


# Aqui haverá as comparações (previsão de chuva), de acordo com as informações nos tópicos do Broker. A partir daí, serão publicados no respectivo tópico as ações a serem tomadas na ESP32
while True:
    ###### colocar as variaveis de distancia e possibilidade de chuva em um if apenas, apenas se as duas forem True ligar alarme.
    client.loop()
    
    comando = tratarSens()
    
    time.sleep(3)
        
        
    
