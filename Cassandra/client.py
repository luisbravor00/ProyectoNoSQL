#!/usr/bin/env python3
import logging
import os
import random
import datetime

from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('hospital.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'hospital')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')

def login():
    print(f"\n\n\033[1;31;40m███████████████████████ LOGIN ███████████████████████\033[0m")
    username = input('\nUsername: ')
    password = input('Password: ')
    return (True, username) if username=='admin' and password=='123' else (False, username)

def print_menu():
    mm_options = {
        1: "Consult Information",
        2: "Delete",
        3: "Delete all data",
        4: "Exit"
    }
    print(f"\n\n\033[1;35;40m███████████████████████ MENU ███████████████████████\033[0m")
    for key in mm_options.keys():
        print(f"\033[1;36;40m{key}\033[0m -- {mm_options[key]}")

def print_consult_menu():
    mm_options = {
        1: "Consult Patient Information",
        2: "Consult Patient Appointments",
        3: "Consult All Doctors",
        4: "Exit Submenu"
    }
    print(f"\n\n\033[1;32;40m███████████████████████ CONSULT MENU ███████████████████████\033[0m")
    for key in mm_options.keys():
        print(f"\033[1;33;40m{key}\033[0m -- {mm_options[key]}")

def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    # Creating the keyspace and the schema for the database
    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)
    model.create_schema(session)

    correct = False
    username = ""
    while (correct is False):
        correct, username = login()
        if correct is False:
            print("\nYou don't have rights to enter the app.\nPlease try again.\n")

    # Clearing the terminal
    clear_terminal()

    while(True):
        print_menu()
        option = int(input(f"Enter your choice ({username}): "))

        if option == 1:
            print_consult_menu()
            option2 = int(input("Enter your choice: "))
            
            if option2 == 1:
                # Getting the patient information to get it from the database
                last_name = input("Last Name: ")
                first_name = input("First Name: ")
                birth_date= input("Date of birth (yyyy-mm-dd): ")
                model.get_patient_information(session, last_name, first_name, birth_date)

            if option2 == 2:
                pass
            if option2 == 3:
                pass
            if option2 == 4:
                pass

        if option == 2:
            pass

        if option == 3:
            model.delete_all_information(session)

        if option == 4:
            exit(0)

if __name__ == '__main__':
    main()
