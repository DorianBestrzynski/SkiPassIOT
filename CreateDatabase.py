#!/usr/bin/env python3

import sqlite3
import time
import os


def create_database():
    if os.path.exists("tickets.db"):
        os.remove("tickets.db")
        print("An old database removed.")
    connection = sqlite3.connect("tickets.db")
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE time_tickets(
        uidCard text primary key,
        startDate text,
        endDate text,
        lastUsed text
    )""")
    
    cursor.execute(""" CREATE TABLE ride_tickets(
        uidCard text primary key,
        rides integer
    )""")
    print("Dorian")
    connection.commit()
    print("Boba")
    connection.close()
    print("The new database created.")


if __name__ == "__main__":
    create_database()
