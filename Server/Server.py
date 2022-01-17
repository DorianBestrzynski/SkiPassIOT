import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time
import datetime

broker = "localhost"

# The MQTT client.
client = mqtt.Client()

connection = sqlite3.connect("tickets.db", check_same_thread=False)
cursor = connection.cursor()

ip_set = set()
blocked_ip = set()


def admin_process(message_decoded):
    if message_decoded[0] == "getGatesList":
        client.publish("admin/server_response", str(ip_set))
    elif message_decoded[0] == "block":
        blocked_ip.add(message_decoded[1])
    elif message_decoded[0] == "unblock":
        if message_decoded[1] in blocked_ip:
            blocked_ip.remove(message_decoded[1])


def checkout_process(message_decoded):
    uid_card = message_decoded[0]
    if len(message_decoded) == 3:
        start_date = ""
        end_date = message_decoded[1]
        last_used = message_decoded[2]
        cursor.execute("INSERT INTO time_tickets VALUES(?,?,?,?)", (uid_card, start_date, end_date, last_used))
    else:
        rides = message_decoded[1]
        cursor.execute("INSERT INTO ride_tickets VALUES(?,?)", (uid_card, rides))

    connection.commit()

    cursor.execute("SELECT * FROM time_tickets")

    cursor.execute("SELECT * FROM ride_tickets")


def gates_process(message_decoded):
    uid_card = message_decoded[0]
    current_date = message_decoded[1]
    ip_addr = message_decoded[2]
    ip_set.add(ip_addr)

    if ip_addr in blocked_ip:
        return

    cursor.execute("SELECT * FROM time_tickets WHERE uidCard = " + uid_card)
    ticket = cursor.fetchall()

    if len(ticket) == 0:
        cursor.execute("SELECT * FROM ride_tickets WHERE uidCard = " + uid_card)
        ticket = cursor.fetchall()
        if len(ticket) != 0:
            ticket = ticket[0]
            rides = int(ticket[1])
            rides = rides - 1

            if rides == 0:
                cursor.execute("DELETE FROM ride_tickets WHERE uidCard = " + uid_card)
                client.publish("gates/" + ip_addr, "1, Uwaga to twoj ostatni zjazd")
            else:
                rides = str(rides)
                rides = rides + ""
                cursor.execute("UPDATE ride_tickets SET rides = ? WHERE uidCard = " + uid_card, (rides,))
                client.publish("gates/" + ip_addr, "1, Zostalo " + rides + " zjazdow")

        else:
            client.publish("gates/" + ip_addr, "0, Nie masz juz zjazdow")

    else:
        ticket = ticket[0]

        current_date = datetime.datetime.strptime(current_date, '%d/%m/%y %H:%M:%S')
        end_date = datetime.datetime.strptime(ticket[2], '%d/%m/%y %H:%M:%S')
        last_used = datetime.datetime.strptime(ticket[3], '%d/%m/%y %H:%M:%S')

        if current_date <= end_date:
            if ticket[1] == "":
                current_date = current_date.strftime('%d/%m/%y %H:%M:%S')
                cursor.execute("UPDATE time_tickets SET startDate = ? , lastUsed = ?  WHERE uidCard = " + uid_card,
                               (current_date, current_date))
                client.publish("gates/" + ip_addr, "1, Karnet wazny do: " + ticket[2])

            else:
                time = current_date - last_used
                timeInSec = time.total_seconds()
                totalMinutes = timeInSec / 60.0
                if (timeInSec > 20):
                    current_date = current_date.strftime('%d/%m/%y %H:%M:%S')
                    cursor.execute("UPDATE time_tickets SET lastUsed = ?  WHERE uidCard = " + uid_card, (current_date,))
                    client.publish("gates/" + ip_addr, "1, Karnet wazny do: " + ticket[2])


                else:
                    # nie wpuszczamy
                    client.publish("gates/" + ip_addr, "0, Nie minelo 20 sekund od ostatniego przylozenia karty ")
        else:
            cursor.execute("DELETE * FROM time_tickets WHERE uidCard = " + uid_card)
            client.publish("gates/" + ip_addr, "0, Karnet nie jest juz wazny ")

    connection.commit()


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(",")
    if message.topic == "checkout":
        checkout_process(message_decoded)
    elif message.topic == "gates":
        gates_process(message_decoded)
    elif message.topic == "admin":
        gates_process(message_decoded)


def connect_to_broker():
    client.connect(broker)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("gates")
    client.subscribe("checkout")
    client.subscribe("admin")


def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()
    while True:
        pass
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()
