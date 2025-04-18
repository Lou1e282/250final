
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):

    print("Connected to server (i.e., broker) with result code "+str(rc))
    #replace user with your USC username in all subscriptions
    client.subscribe("louieshen/ping")

    
    #Add the custom callbacks by indicating the topic and the name of the callback handle
    client.message_callback_add("louieshen/ping", on_message_from_ping)


def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

#Custom message callback. info
def on_message_from_ping(client, userdata, message):

   num = (message.payload.decode())+ 1

   print(f"Custom callback - num {num}")

   
if __name__ == '__main__':
    
    client = mqtt.Client()

    client.on_message = on_message

    client.on_connect = on_connect
   
    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

    client.loop_forever()