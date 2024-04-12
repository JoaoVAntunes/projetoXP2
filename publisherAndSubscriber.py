import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

# Variáveis com os tópicos utilizados
myTopicTemperatura = "/Temperatura"
myTopicUmidade = "/Umidade" 
myTopicDistancia = "/Distancia"
myTopicMensagem = "/Mensagem/alerta"
myTopicAction = "/Action/alerta"
myTopicButton = "/Botao/alerta"

# Variáveis que receberão os valores de temp. e umid. do sensor DHT22 (Wokwi)
temperature = 0
humidity = 0
#variável para a distância
distance = 0

# Conexão com o Broker
mqttBroker ="mqtt-dashboard.com"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(mqttBroker) 


def tratarSens():
    
    #tratando da distância da água
    if distance < 100 and (humidity > 70 and temperature < 20):
        client.loop()
        mensagem = "O nível da água está alto! Riscos de alagamento!"
        client.publish(myTopicMensagem, mensagem)

    elif distance < 100 and (humidity > 70 and temperature < 25):
        client.loop()
        mensagem = "Provavelmente choverá forte! Riscos de alagamento!"
        client.publish(myTopicMensagem, mensagem)
    else:
        client.loop()
        mensagem = "Sem riscos de alagamento!"
        client.publish(myTopicMensagem, mensagem)


# Esta função analisa o tópico que deverá ser escutado e armazena o conteúdo do tópico (payload) em uma variável
def callback(client, userdata, message):
    global myTopicTemperatura, myTopicUmidade, myTopicDistancia, temperature, humidity, distance, botao

    #print("Tópico: ", str(message.topic))
    if (message.topic == myTopicTemperatura):
               temperature = int(str(message.payload.decode("utf-8")))
    if (message.topic == myTopicUmidade):
                humidity = int(str(message.payload.decode("utf-8")))
    if (message.topic == myTopicDistancia):
                distance = int(str(message.payload.decode("utf-8")))
    if (message.topic == myTopicButton):
                botao = str(message.payload.decode("utf-8"))
                # Depuração
                print("Status do alerta: ", botao)
                client.publish(myTopicAction, botao)


client.message_callback_add(myTopicTemperatura, callback)
client.subscribe(myTopicTemperatura)

client.message_callback_add(myTopicUmidade, callback)
client.subscribe(myTopicUmidade)

client.message_callback_add(myTopicDistancia, callback)
client.subscribe(myTopicDistancia)

client.message_callback_add(myTopicButton, callback)
client.subscribe(myTopicButton)


# Aqui haverá as comparações (previsão de chuva), de acordo com as informações nos tópicos do Broker. A partir daí, serão publicados no respectivo tópico as ações a serem tomadas na ESP32
while True:
    client.loop()
    
    tratarSens()

    # Indica o assunto de cada tópico
    print("Temperatura: ", temperature)
    print("Umidade: ", humidity)

    #time.sleep(3)
