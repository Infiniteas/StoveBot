from machine import Pin, PWM, Timer

from time import sleep

import network

import sys

from mqttclient import MQTTClient




session = 'stoveBot/project'
BROKER = 'broker.hivemq.com'
qos = 0

# check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# connect to MQTT broker

print("hi")
mqtt = MQTTClient(BROKER, port='1883')

print(mqtt)




def runMotor(u, message):
    # extract data from MQTT message
    m1 = PWM(Pin(26),freq=200,duty=0,timer=3)
    m2 = PWM(Pin(27),freq=200,duty=0,timer=2)
    m3 = PWM(Pin(17),freq=200,duty=0,timer=0)
    m4 = PWM(Pin(21),freq=200,duty=0,timer=1)

    message = message.decode("utf-8")


    angle1,angle2 = str(message).split(",")



    anglefactor1 = float(angle1)/360
    anglefactor2 = float(angle2) / 360


    m1.duty(14)
    m2.duty(0)

    sleep(2.9 * anglefactor1)
    m1.duty(0)
    m2.duty(0)

    m3.duty(14)
    m4.duty(0)
    sleep(2.9* anglefactor2)
    m3.duty(0)
    m4.duty(0)

    m1.deinit()
    m2.deinit()
    m3.deinit()
    m4.deinit()


topic = "{}/motor".format(session)
mqtt.set_callback(runMotor)
mqtt.subscribe(topic)
print("wow")


# wait for MQTT messages
# this function never returns
print("waiting for data ...")

while True:
    mqtt.check_msg()

    time.sleep(1)





# Set up motor control PWM pins

# Initially forward at 50% speed






# dec.count()
# dec.count_and_clear()
# dec.clear()
# dec.pause()
# dec.resume()

# def tcb(timer):
#
#     global dec
#     print(dec.count())
#
# t1 = Timer(1)
# t1.init(period=500, mode=t1.PERIODIC, callback=tcb)
