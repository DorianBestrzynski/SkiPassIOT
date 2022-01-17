#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter
import time
import datetime
import re

broker = "192.168.64.13"

client = mqtt.Client()

window = tkinter.Tk()
uid_table = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
counter = 0

gatesList = []


# importy i setup dla platformy rzeczywistej
# from mfrc522 import MFRC522
# from datetime import datetime
# import neopixel
# import board

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

# def execute_hours(hours, frame):
#     global read
#     global cardNumber
#     global flag
#
#     while True:
#         if flag:
#             break
#         rfidRead()
#         if read:
#             call_server_hours(cardNumber, hours, frame)
#             for i in range(8):
#                 pixels[i] = (255, 140, 0)
#                 pixels.show()
#
#             time.sleep(1)
#             off(pixels)
#             read = False
#
#
# def execute_days(days, frame):
#     global read
#     global cardNumber
#     global flag
#
#     while True:
#         if flag:
#             break
#         rfidRead()
#         if read:
#             call_server_days(cardNumber, days, frame)
#             for i in range(8):
#                 pixels[i] = (128, 0, 128)
#                 pixels.show()
#
#             time.sleep(1.5)
#             off(pixels)
#             read = False
#
#
# def execute_days(rides, frame):
#     global read
#     global cardNumber
#     global flag
#
#     while True:
#         if flag:
#             break
#         rfidRead()
#         if read:
#             call_server_rides(cardNumber, rides, frame)
#             for i in range(8):
#                 pixels[i] = (255, 255, 0)
#                 pixels.show()
#
#             time.sleep(1.5)
#             off(pixels)
#             read = False


def clean_frame(frame, flag=True):
    frame.pack_forget()
    if not flag:
        create_main_window()


def call_server_rides(uid, rides, frame):
    global counter
    counter += 1
    print(uid)
    print(rides)
    client.publish("checkout", uid + "," + rides)
    success_window(frame, 0)


def call_server_hours(uid, hours, frame):
    global counter
    counter += 1
    print(uid)
    print(hours)
    date = datetime.datetime.now()
    if date.hour > 15:
        print("We are closed, try tomorrow at 8!")

    hours_added = datetime.timedelta(hours=hours)

    future_date = date + hours_added
    if future_date.hour > 24:
        future_date = future_date.replace(hour=16, minute=00, second=00)
    future_date = future_date.strftime('%d/%m/%y %H:%M:%S')
    client.publish("checkout", uid + "," + future_date + "," + "01/12/99 15:32:56")
    success_window(frame, 2)


def call_server_days(uid, days, frame):
    global counter
    counter += 1
    date = datetime.datetime.now()

    days_added = datetime.timedelta(days=days - 1)
    future_date = date + days_added
    future_date = future_date.replace(hour=16, minute=00, second=00)
    future_date = future_date.strftime('%d/%m/%y %H:%M:%S')
    client.publish("checkout", uid + "," + future_date + "," + "01/12/99 15:32:56")
    success_window(frame, 1)


def not_enough_tickets_window(frame):
    clean_frame(frame)
    main_frame = tkinter.Frame(window)
    main_frame.pack()
    intro_label = tkinter.Label(main_frame, text="Ski Pass:", font=40).pack()
    intro_label1 = tkinter.Label(main_frame, text="Niestety nie ma juz karnetow", font=40).pack()
    button_4 = tkinter.Button(main_frame, text="Menu",
                              command=lambda: clean_frame(main_frame, False))
    button_4.pack(side=tkinter.BOTTOM)


def create_circle(x, y, r, canvasName, color):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    canvasName.create_oval(x0, y0, x1, y1, fill=color)
    canvasName.pack()
    return canvasName


def success_window(frame, carnetType):
    clean_frame(frame)
    window.geometry("380x200")
    main_frame = tkinter.Frame(window)
    main_frame.pack()
    my_canvas = tkinter.Canvas(main_frame)

    if carnetType == 0:
        color = "yellow"
    elif carnetType == 1:
        color = "orange"
    else:
        color = "purple"

    intro_label = tkinter.Label(main_frame, text="Ski Pass:", font=40, wraplength=300).pack()
    intro_label1 = tkinter.Label(main_frame, text="Karnet zeskanowany poprawnie", font=40, wraplength=300).pack()
    button_4 = tkinter.Button(main_frame, text="Menu", wraplength=300,
                              command=lambda: clean_frame(main_frame, False))
    button_4.pack()
    create_circle(190, 50, 40, my_canvas, color)


def card_reading_days(days, frame):
    global counter
    clean_frame(frame)
    if counter >= len(uid_table):
        not_enough_tickets_window(frame)
    else:
        main_frame = tkinter.Frame(window)
        main_frame.pack()

        # execute_days(days, frame)

        intro_label = tkinter.Label(main_frame, text="Wczytaj karte uid:", font=40).pack()

        button_1 = tkinter.Button(main_frame, text="Wczytaj karte UID",
                                  command=lambda: call_server_days(uid_table[counter], days, main_frame))
        button_1.pack(side=tkinter.TOP)

        button_4 = tkinter.Button(main_frame, text="Menu",
                                  command=lambda: clean_frame(main_frame, False))
        button_4.pack(side=tkinter.BOTTOM)


def card_reading_hours(hours, frame):
    global counter
    clean_frame(frame)
    if counter >= len(uid_table):
        not_enough_tickets_window(frame)
    else:
        main_frame = tkinter.Frame(window)
        main_frame.pack()

        intro_label = tkinter.Label(main_frame, text="Wczytaj karte uid:", font=40).pack()

        # execute_hour(hours, frame)

        button_1 = tkinter.Button(main_frame, text="Wczytaj karte UID",
                                  command=lambda: call_server_hours(uid_table[counter], hours, main_frame))
        button_1.pack(side=tkinter.TOP)

        button_4 = tkinter.Button(main_frame, text="Menu",
                                  command=lambda: clean_frame(main_frame, False))
        button_4.pack(side=tkinter.BOTTOM)


def card_reading_rides(rides, frame):
    global counter
    clean_frame(frame)
    if counter >= len(uid_table):
        not_enough_tickets_window(frame)
    else:
        main_frame = tkinter.Frame(window)
        main_frame.pack()

        intro_label = tkinter.Label(main_frame, text="Wczytaj karte uid:", font=40).pack()

        # execute_rides(rides, frame)
        button_1 = tkinter.Button(main_frame, text="Wczytaj karte UID",
                                  command=lambda: call_server_rides(uid_table[counter], rides, main_frame))
        button_1.pack(side=tkinter.TOP)

        button_4 = tkinter.Button(main_frame, text="Menu",
                                  command=lambda: clean_frame(main_frame, False))
        button_4.pack(side=tkinter.BOTTOM)


def day_window(frame):
    clean_frame(frame)
    main_frame = tkinter.Frame(window)
    main_frame.pack()

    button_1 = tkinter.Button(main_frame, text="1 dzien",
                              command=lambda: card_reading_days(1, main_frame))
    button_1.pack(side=tkinter.TOP)
    button_2 = tkinter.Button(main_frame, text="3 dni",
                              command=lambda: card_reading_days(3, main_frame))
    button_2.pack(side=tkinter.TOP)
    button_3 = tkinter.Button(main_frame, text="5 dni",
                              command=lambda: card_reading_days(5, main_frame))
    button_3.pack(side=tkinter.TOP)
    button_4 = tkinter.Button(main_frame, text="tydzien",
                              command=lambda: card_reading_days(7, main_frame))
    button_4.pack(side=tkinter.TOP)

    button_5 = tkinter.Button(main_frame, text="Menu",
                              command=lambda: clean_frame(main_frame, False))
    button_5.pack(side=tkinter.TOP)


def hour_window(frame):
    clean_frame(frame)
    main_frame = tkinter.Frame(window)
    main_frame.pack()

    button_1 = tkinter.Button(main_frame, text="1 godzina",
                              command=lambda: card_reading_hours(1, main_frame))
    button_1.pack(side=tkinter.TOP)
    button_2 = tkinter.Button(main_frame, text="2 godziny",
                              command=lambda: card_reading_hours(2, main_frame))
    button_2.pack(side=tkinter.TOP)
    button_3 = tkinter.Button(main_frame, text="4 godziny",
                              command=lambda: card_reading_hours(4, main_frame))
    button_3.pack(side=tkinter.TOP)
    button_4 = tkinter.Button(main_frame, text="6 godzin",
                              command=lambda: card_reading_hours(6, main_frame))
    button_4.pack(side=tkinter.TOP)

    button_5 = tkinter.Button(main_frame, text="Menu",
                              command=lambda: clean_frame(main_frame, False))
    button_5.pack(side=tkinter.TOP)


def times_window(frame):
    clean_frame(frame)
    main_frame = tkinter.Frame(window)
    main_frame.pack()

    intro_label = tkinter.Label(main_frame, text="Ski Pass:", font=40).pack()

    button_1 = tkinter.Button(main_frame, text="Bilety godzinowe",
                              command=lambda: hour_window(main_frame))
    button_1.pack(side=tkinter.TOP)
    button_2 = tkinter.Button(main_frame, text="Bilety wielodniowe",
                              command=lambda: day_window(main_frame))
    button_2.pack(side=tkinter.TOP)
    button_4 = tkinter.Button(main_frame, text="Menu",
                              command=lambda: clean_frame(main_frame, False))
    button_4.pack(side=tkinter.TOP)


def rides_window(frame):
    clean_frame(frame)
    main_frame = tkinter.Frame(window)
    main_frame.pack()

    intro_label = tkinter.Label(main_frame, text="Bilety zjazdowe:", font=40).pack()

    button_1 = tkinter.Button(main_frame, text="2 zjazdy",
                              command=lambda: card_reading_rides("2", main_frame))
    button_1.pack(side=tkinter.TOP)
    button_2 = tkinter.Button(main_frame, text="5 zjazdow",
                              command=lambda: card_reading_rides("5", main_frame))
    button_2.pack(side=tkinter.TOP)
    button_3 = tkinter.Button(main_frame, text="10 zjazdow",
                              command=lambda: card_reading_rides("10", main_frame))
    button_3.pack(side=tkinter.TOP)
    button_4 = tkinter.Button(main_frame, text="15 zjazdow",
                              command=lambda: card_reading_rides("15", main_frame))
    button_4.pack(side=tkinter.TOP)
    button_5 = tkinter.Button(main_frame, text="Menu",
                              command=lambda: clean_frame(main_frame, False))
    button_5.pack(side=tkinter.TOP)

def call_server_gates():
    client.publish("admin", "getGatesList")
 
def block_gate(gateIp, frame):
    print(gateIp)
    client.publish("admin", "block," + gateIp)
    
def unblock_gate(gateIp, frame):
    print(gateIp)
    client.publish("admin", "unblock," + gateIp)

def choose_admin_action(frame):
    clean_frame(frame)
    main_frame = tkinter.Frame(window)
    main_frame.pack()
    
    intro_label = tkinter.Label(main_frame, text="Admin: ", font=40).pack()

    button_1 = tkinter.Button(main_frame, text="Zablokuj bramke",
                              command=lambda: choose_gate_block(main_frame))
    button_1.pack(side=tkinter.TOP)
    button_2 = tkinter.Button(main_frame, text="Odblokuj bramke",
                              command=lambda: choose_gate_unblock(main_frame))
    button_2.pack(side=tkinter.TOP)


def choose_gate_unblock(frame):
    global gatesList
    clean_frame(frame)
    main_frame = tkinter.Frame(window)
    main_frame.pack()
    call_server_gates()

    intro_label = tkinter.Label(main_frame, text="Odblokuj bramke: ", font=40).pack()

    button_1 = tkinter.Button(main_frame, text="Bramka 1",
                              command=lambda: unblock_gate(gatesList[0], main_frame))
    button_1.pack(side=tkinter.TOP)
    button_2 = tkinter.Button(main_frame, text="Bramka 2",
                              command=lambda: unblock_gate(gatesList[1], main_frame))
    button_2.pack(side=tkinter.TOP)
    
    button_5 = tkinter.Button(main_frame, text="Menu",
                              command=lambda: clean_frame(main_frame, False))
    button_5.pack(side=tkinter.TOP)
    
def choose_gate_block(frame):
    global gatesList
    clean_frame(frame)
    main_frame = tkinter.Frame(window)
    main_frame.pack()
    call_server_gates()

    intro_label = tkinter.Label(main_frame, text="Zablokuj bramke: ", font=40).pack()

    button_1 = tkinter.Button(main_frame, text="Bramka 1",
                              command=lambda: block_gate(gatesList[0], main_frame))
    button_1.pack(side=tkinter.TOP)
    button_2 = tkinter.Button(main_frame, text="Bramka 2",
                              command=lambda: block_gate(gatesList[1], main_frame))
    button_2.pack(side=tkinter.TOP)
    button_5 = tkinter.Button(main_frame, text="Menu",
                              command=lambda: clean_frame(main_frame, False))
    button_5.pack(side=tkinter.TOP)
    
def create_main_window():
    window.geometry("300x200")
    window.title("Cash Desk")
    main_frame = tkinter.Frame(window)
    main_frame.pack()

    intro_label = tkinter.Label(main_frame, text="Ski Pass:", font=40).pack()

    button_1 = tkinter.Button(main_frame, text="Bilety Zjazdowe",
                              command=lambda: rides_window(main_frame))
    button_1.pack(side=tkinter.TOP)
    button_2 = tkinter.Button(main_frame, text="Bilety Czasowe",
                              command=lambda: times_window(main_frame))
    button_2.pack(side=tkinter.TOP)
    button_3 = tkinter.Button(main_frame, text="Admin",
                              command=lambda: choose_admin_action(main_frame))
    button_3.pack(side=tkinter.TOP)
    


def connect_to_broker():
    client.connect(broker)


def disconnect_from_broker():
    client.disconnect()

def process_message(client, userdata, message):
    global gatesList
    message_decoded = (str(message.payload.decode("utf-8"))).split(",")
    
    if (message.topic == "admin/server_response"):
        for i in message_decoded:
            x= re.search("(?<=')[\d.]{2,}",i)
            print(x.group())
            gatesList.append(x.group())

#         for i in message_decoded:
#             print(i)
    
    
    
def run_sender():
    connect_to_broker()
    client.on_message = process_message
    client.subscribe("admin/server_response")
    create_main_window()
    
    client.loop_start()
    window.mainloop()
    

    disconnect_from_broker()


if __name__ == "__main__":
    run_sender()
