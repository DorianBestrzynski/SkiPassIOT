import paho.mqtt.client as mqtt
import time
import datetime
from tkinter import *
import pygame
from netifaces import interfaces, ifaddresses, AF_INET

DATE_PATTERN_NO_SECONDS = '%d/%m/%y %H:%M'
DATE_PATTERN_WITH_SECONDS = '%d/%m/%y %H:%M:%S'
SONG_NAME_SUCCESS = "imperialMarch.mp3"
SONG_NAME_FAIL = "fail.mp3"

uid_table = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

ipServer = "192.168.64.13"
ipGate = ""

for ifaceName in interfaces():
    for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr '}]):
        if i['addr'].startswith('192.168.64'):
            ipGate = i['addr']
            break

window = Tk()
mainFrame = Frame(window)
mainFrame.pack()

clientReceiver = mqtt.Client()

client = mqtt.Client()
pygame.mixer.init()
errorFlag = False

# importy i setup dla platformy rzeczywistej
# from mfrc522 import MFRC522
# from datetime import datetime
# import neopixel
# import board
# import w1thermsensor

# read = False
# flag = False
# cardNumber = ""
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
#
# led1 = 13
# led2 = 12
# led3 = 19
# led4 = 26
# GPIO.setup(led1, GPIO.OUT)
# GPIO.setup(led2, GPIO.OUT)
# GPIO.setup(led3, GPIO.OUT)
# GPIO.setup(led4, GPIO.OUT)
#
# buttonRed = 5
# buttonGreen = 6
# encoderLeft = 17
# encoderRight = 27
# GPIO.setup(buttonRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(buttonGreen, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(encoderLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(encoderRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
# buzzerPin = 23
# GPIO.setup(buzzerPin, GPIO.OUT)
# GPIO.output(buzzerPin, 1)
#
# ws2812pin = 8
#
# MIFAREReader = MFRC522()

# kod dla platformy rzeczywistej
# def off(pixels):
#     pixels[0] = (0, 0, 0)
#     pixels[1] = (0, 0, 0)
#     pixels[2] = (0, 0, 0)
#     pixels[3] = (0, 0, 0)
#     pixels[4] = (0, 0, 0)
#     pixels[5] = (0, 0, 0)
#     pixels[6] = (0, 0, 0)
#     pixels[7] = (0, 0, 0)
#     pixels.show()
#
#
# def buzzer(state):
#     GPIO.output(buzzerPin, not state)
#
#
# def rfidRead():
#     global read
#     global cardNumber
#
#     (status, tagName) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
#
#     if status == MIFAREReader.MI_OK:
#         (status, uid) = MIFAREReader.MFRC522_Anticoll()
#         if status == MIFAREReader.MI_OK:
#             read = True
#             buzzer(True)
#             print(datetime.now())
#             GPIO.output(led1, True)
#             time.sleep(0.2)
#             buzzer(False)
#             GPIO.output(led1, False)
#             num = 0
#             for i in range(0, len(uid)):
#                 num += uid[i] << (i * 8)
#
#             cardNumber = str(num)

# def execute():
#     global read
#     global cardNumber
#     global flag
#
#     while True:
#         if flag:
#             break
#         rfidRead()
#         if read:
#             call_server(cardNumber)
#             read = False


def load_song(song_name):
    pygame.mixer.music.load(song_name)


def play_song():
    pygame.mixer.music.play()
    time.sleep(3)
    pygame.mixer.music.stop()


def get_temperature():
    temperature = " -1 °C "
    # sensor = w1thermsensor.W1ThermSensor()
    # temperature = sensor.get_temperature()
    # return temperature + chr(176) +'C'
    return temperature


def clean_frame(flag=True):
    global mainFrame
    mainFrame.pack_forget()
    if not flag:
        default_window()


def default_window():
    global mainFrame
    date = datetime.datetime.now().strftime('%d/%m/%y %H:%M')
    temp = get_temperature()

    window.geometry("300x380")
    window.title("Gate")
    window.configure(bg='#D9D9D9')

    mainFrame = Frame(window)
    mainFrame.pack()

    label = Label(mainFrame, text="Ski Pass Gate").pack()

    button1 = Button(mainFrame, text="Karnet 1", command=lambda: call_server(uid_table[0]))
    button1.pack(side=TOP)
    button2 = Button(mainFrame, text="Karnet 2", command=lambda: call_server(uid_table[1]))
    button2.pack(side=TOP)
    button3 = Button(mainFrame, text="Karnet 3", command=lambda: call_server(uid_table[2]))
    button3.pack(side=TOP)
    button4 = Button(mainFrame, text="Karnet 4", command=lambda: call_server(uid_table[3]))
    button4.pack(side=TOP)
    button5 = Button(mainFrame, text="Karnet 5", command=lambda: call_server(uid_table[4]))
    button5.pack(side=TOP)
    button6 = Button(mainFrame, text="Karnet 6", command=lambda: call_server(uid_table[5]))
    button6.pack(side=TOP)
    button7 = Button(mainFrame, text="Karnet 7", command=lambda: call_server(uid_table[6]))
    button7.pack(side=TOP)
    button8 = Button(mainFrame, text="Karnet 8", command=lambda: call_server(uid_table[7]))
    button8.pack(side=TOP)
    button9 = Button(mainFrame, text="Karnet 9", command=lambda: call_server(uid_table[8]))
    button9.pack(side=TOP)
    button10 = Button(mainFrame, text="Karnet 10", command=lambda: call_server(uid_table[9]))
    button10.pack(side=TOP)
    label1 = Label(mainFrame, text=date).pack()
    label2 = Label(mainFrame, text=temp).pack()


def call_server(uid_card):
    date = datetime.datetime.now().strftime(DATE_PATTERN_WITH_SECONDS)
    client.publish("gates", uid_card + "," + date + "," + ipGate)


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(",")

    if message_decoded[0] == "1":
        successful_validation_process(message_decoded)
    else:
        failed_validation_process(message_decoded)


def successful_validation_process(message_decoded):
    global mainFrame
    clean_frame()
    load_song(SONG_NAME_SUCCESS)
    date = datetime.datetime.now().strftime(DATE_PATTERN_NO_SECONDS)
    temp = get_temperature()
    text = message_decoded[1]

    window.geometry("300x200")
    window.configure(bg="green")

    mainFrame = Frame(window, bg="green")
    mainFrame.pack()

    label = Label(mainFrame, text="Ski Pass Gate", bg="green", wraplength=300).pack()
    message_label = Label(mainFrame, text=text, bg="green", wraplength=300).pack()
    label1 = Label(mainFrame, text=date, bg="green").pack()
    label2 = Label(mainFrame, text=temp, bg="green").pack()

    # pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)
    # for i in range(8):
    #     pixels[i] = (0, 128, 0)
    #     pixels.show()
    # off(pixels)

    play_song()
    clean_frame(False)


def failed_validation_process(message_decoded):
    global mainFrame
    clean_frame()
    load_song(SONG_NAME_FAIL)
    date = datetime.datetime.now().strftime(DATE_PATTERN_NO_SECONDS)
    temp = get_temperature()
    text = message_decoded[1]

    window.geometry("300x200")
    window.configure(bg="red")

    mainFrame = Frame(window, bg="red")
    mainFrame.pack()

    label = Label(mainFrame, text="Ski Pass Gate", bg="red", wraplength=300).pack()

    message_label = Label(mainFrame, text=text, bg="red", wraplength=300).pack()
    label1 = Label(mainFrame, text=date, bg="red").pack()
    label2 = Label(mainFrame, text=temp, bg="red").pack()

    # pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)
    # for i in range(8):
    #     pixels[i] = (255, 0, 0)
    #     pixels.show()
    # off(pixels)

    play_song()
    clean_frame(False)

def on_connect(client,userdata,flags,rc):
    global errorFlag
    print("Connected flags", str(flags), "Result Code", str(rc))
    if rc != 0:
        errorFlag = True
        print("Authorization error")
port = 8883
def connect_to_broker():
    global errorFlag
    client.on_connect = on_connect
    client.tls_set('/home/pi/Documents/ca.crt')
    client.tls_insecure_set(True)
    client.username_pw_set(username='gate1', password='gate1')
    client.connect(ipServer,port)

    client.on_message = process_message

    client.loop_start()
    client.subscribe("gates/" + ipGate)
    time.sleep(3)
    if errorFlag:
        sys.exit()


def run_gate():
    connect_to_broker()
    default_window()
    window.mainloop()
    # execute()
    disconnect_from_broker()


def disconnect_from_broker():
    client.disconnect()


if __name__ == "__main__":
    run_gate()
