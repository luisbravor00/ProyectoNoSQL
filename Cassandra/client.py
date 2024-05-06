#!/usr/bin/env python3
import logging
import os
import getpass
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
    password = getpass.getpass('Password: ')
    return (True, username) if username=='admin' and password=='123' else (False, username)

def print_menu():
    mm_options = {
        1: "Consult Information",
        2: "Modify Information",
        3: "Create Information",
        4: "Delete Information",
        5: "Delete General Data",
        6: "Exit"
    }
    print(f"\n\n\033[1;35;40m███████████████████████ MENU ███████████████████████\033[0m")
    for key in mm_options.keys():
        print(f"\033[1;36;40m{key}\033[0m -- {mm_options[key]}")

def print_consult_menu():
    mm_options = {
        1: "View all Hospitals",
        2: "Get Hospital Information",
        3: "Get Patient Information",
        4: "Get Patient Appointments",
        5: "View All Doctors of a Hospital",
        6: "View Appointments for a Specific Day",
        7: "Exit Consult Menu"
    }
    print(f"\n\n\033[1;32;40m███████████████████████ CONSULT MENU ███████████████████████\033[0m")
    for key in mm_options.keys():
        print(f"\033[1;33;40m{key}\033[0m -- {mm_options[key]}")

def print_modify_menu():
    mm_options = {
        1: "Cancel Appointment",
        2: "Reschedule Appointment (hour & date)",
        3: "Change Appointment Hour",
        4: "Exit Modify Menu"
    }
    print(f"\n\n\033[1;32;40m███████████████████████ MODIFY MENU ███████████████████████\033[0m")
    for key in mm_options.keys():
        print(f"\033[1;33;40m{key}\033[0m -- {mm_options[key]}")

def print_create_menu():
    mm_options = {
        1: "Create Appointments for Patients",
        2: "Create Patients",
        3: "Exit Create Menu"
    }
    print(f"\n\n\033[1;32;40m███████████████████████ CREATE MENU ███████████████████████\033[0m")
    for key in mm_options.keys():
        print(f"\033[1;33;40m{key}\033[0m -- {mm_options[key]}")

def print_delete_menu():
    mm_options = {
        1: "Delete Appointment",
        2: "Delete Patient",
        3: "Exit Delete Menu"
    }
    print(f"\n\n\033[1;32;40m███████████████████████ DELETE MENU ███████████████████████\033[0m")
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

    clear_terminal()

    correct = False
    username = ""
    while (correct is False):
        correct, username = login()
        if correct is False:
            print("\nYou don't have rights to enter the app.\nPlease try again.\n")

    clear_terminal()

    while(True):
        print_menu()
        option = int(input(f"Enter your choice ({username}): "))

        if option == 1:
            print_consult_menu()
            option2 = int(input("Enter your choice: "))
            
            if option2 == 1:
                # Getting all of the hospitals on the database
                model.get_all_hospitals(session)
            if option2 == 2:
                # Getting the specific hospital information
                hospital_id = input("Enter your hospital ID: ")
                model.get_hospital_information(session, hospital_id)
            if option2 == 3:
                # Getting the patient information to get it from the database
                last_name = input("Last Name: ")
                first_name = input("First Name: ")
                birth_date = input("Date of birth (yyyy-mm-dd): ")
                model.get_patient_information(session, last_name, first_name, birth_date)
            if option2 == 4:
                # Getting the patient appointments
                patient_id = input("Enter the patient ID: ") 
                model.get_patient_appointments(session, patient_id)
            if option2 == 5:
                # Getting all the doctors of a specific hospital
                hospital_id = input("Enter the hospital ID: ")
                model.get_doctor_by_hospital(session, hospital_id)        
            if option2 == 6:
                # Getting the appointments for the day
                date = input("Date to search for (yyyy-mm-dd): ")
                model.get_appointments_for_a_day(session, date)
                pass
            if option2 == 7:
                pass

        if option == 2:
            print_modify_menu()
            option2 = int(input("Enter your choice: "))

            if option2 == 1:
                # Cancel an appointment
                appointment_id = input("Enter the appointment ID you want to CANCEL: ")
                model.cancel_appointment(session, appointment_id)

            if option2 == 2:
                # Reschedule the appointment
                pass

            if option2 == 3:
                # Change the hour of the appointment
                pass

        if option == 3:
            print_create_menu()
            option2 = int(input("Enter your choice: "))

            if option2 == 1:
                # Create appointments for patients
                doctor_id = input("Your doctor ID: ")
                patient_id = input("Your patient ID: ")
                start = input("Start Hour (HH:MM): ")
                hour, minute = map(int, start.split(':'))
                # Incrementa la hora en 1 y ajusta si excede 20:59
                # Formatea la hora final
                end = f"{hour+1:02d}:00"
                date = input("Date (yyyy-mm-dd): ")
                status = "Scheduled"
                hospital_id = input("Your hospital ID: ")
                model.create_appointments_for_users(session, doctor_id, patient_id, start, end, date, status, hospital_id)


            if option2 == 2:
                # Create patients
                last_name = input("Last Name: ")
                first_name = input("First Name: ")
                birth_date = input("Birth Date (yyyy-mm-dd): ")
                address = input("Patient Address: ")
                nss = input("Patient NSS: ")
                hospital_id = input("Patient Hospital ID: ")
                model.create_new_patients(session, first_name, last_name, birth_date, address, nss, hospital_id)

            if option2 == 3:
                pass

        if option == 4:
            print_delete_menu()
            option2 = int(input("Enter your choice: "))

            if option2 == 1:
                # Delete appointment for user
                appointment_id = input("Enter the appointment ID you want to delete: ")
                date = input("Enter the date of the appointment: ")
                model.delete_appointments(session, appointment_id, date)

            if option2 == 2:
                # Delete user from database
                last_name = input("Last Name: ")
                first_name = input("First Name: ")
                birth_date = input("Date of birth (yyyy-mm-dd): ")
                model.delete_patient(session, last_name, first_name, birth_date)
            
            if option2 == 3:
                pass
        
        if option == 5:
            print("\n\033[1;31;40mAre you sure you really want to delete all the information from the database?\033[0m")
            answer = input("Your answer ('y' for yes or anything else for no): ")
            if answer == 'y':
                print("Deleting all the information from the database...")
                model.delete_all_information(session)

        if option == 6:
            exit(0)

if __name__ == '__main__':
    main()
