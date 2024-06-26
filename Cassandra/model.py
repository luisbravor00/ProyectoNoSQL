#!/usr/bin/env python3
import logging
import uuid
import datetime

# Set logger
log = logging.getLogger()

CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""
# HOSPITAL TABLE
CREATE_HOSPITAL_TABLE = """
    CREATE TABLE IF NOT EXISTS hospital (
        hospital_id UUID,
        hospital_name TEXT,
        location TEXT,
        PRIMARY KEY (hospital_id, hospital_name, location)
    )
"""
# PATIENT TABLE
CREATE_PATIENT_TABLE = """
    CREATE TABLE IF NOT EXISTS patient (
        patient_id UUID,
        first_name TEXT,
        last_name TEXT,
        date_of_birth DATE,
        address TEXT,
        NSS TEXT,
        hospital_id UUID,
        PRIMARY KEY (last_name, first_name, date_of_birth, NSS, patient_id)
    ) WITH CLUSTERING ORDER BY (first_name ASC, date_of_birth ASC)
"""
# DOCTOR TABLE
CREATE_DOCTOR_TABLE = """
    CREATE TABLE IF NOT EXISTS doctor (
        doctor_id UUID,
        first_name TEXT,
        last_name TEXT,
        license_number TEXT,
        speciality TEXT,
        hospital_id UUID,
        PRIMARY KEY (last_name, first_name, speciality, doctor_id, hospital_id)
    ) WITH CLUSTERING ORDER BY (first_name ASC, speciality ASC)
"""
CREATE_DOCTOR_TABLE_BY_ID = """
    CREATE TABLE IF NOT EXISTS doctor_by_id (
        doctor_id UUID,
        first_name TEXT,
        last_name TEXT,
        license_number TEXT,
        speciality TEXT,
        hospital_id UUID,
        PRIMARY KEY (doctor_id, last_name, first_name, speciality, hospital_id)
    ) WITH CLUSTERING ORDER BY (last_name ASC, first_name ASC, speciality ASC)
"""
CREATE_DOCTOR_TABLE_BY_HOSPITAL_ID = """
    CREATE TABLE IF NOT EXISTS doctor_by_hospital_id (
        doctor_id UUID,
        first_name TEXT,
        last_name TEXT,
        license_number TEXT,
        speciality TEXT,
        hospital_id UUID,
        PRIMARY KEY (hospital_id, last_name, first_name, speciality)
    ) WITH CLUSTERING ORDER BY (last_name ASC, first_name ASC, speciality ASC)
"""
# APPOINTMENT TABLE
CREATE_APPOINTMENT_TABLE = """
    CREATE TABLE IF NOT EXISTS appointment (
        appointment_id UUID,
        doctor_id UUID,
        patient_id UUID,
        hospital_id UUID,
        start_hour TEXT,
        end_hour TEXT,
        date DATE,
        status TEXT,
        PRIMARY KEY (patient_id, status, date, start_hour, hospital_id)
    ) WITH CLUSTERING ORDER BY (status ASC, date DESC, start_hour DESC)
"""
CREATE_APPOINTMENT_TABLE_BY_ID = """
    CREATE TABLE IF NOT EXISTS appointment_by_id (
        appointment_id UUID,
        doctor_id UUID,
        patient_id UUID,
        hospital_id UUID,
        start_hour TEXT,
        end_hour TEXT,
        date DATE,
        status TEXT,
        PRIMARY KEY (appointment_id, status, date, start_hour, hospital_id)
    ) WITH CLUSTERING ORDER BY (status ASC, date DESC, start_hour DESC)
"""
CREATE_APPOINTMENT_TABLE_BY_DATE = """
    CREATE TABLE IF NOT EXISTS appointment_by_date (
        appointment_id UUID,
        doctor_id UUID,
        patient_id UUID,
        hospital_id UUID,
        start_hour TEXT,
        end_hour TEXT,
        date DATE,
        status TEXT,
        PRIMARY KEY (date, appointment_id, status, start_hour)
    ) WITH CLUSTERING ORDER BY (appointment_id DESC, status ASC, start_hour ASC)
"""

# QUERIES
SELECT_ALL_HOSPITALS = """
    SELECT * FROM hospital;
"""
SELECT_HOSPITAL_INFORMATION = """
    SELECT * FROM hospital WHERE hospital_id = ?;
"""
SELECT_PATIENT_INFORMATION = """
    SELECT patient_id, first_name, last_name, date_of_birth, address, NSS, hospital_id
    FROM patient
    WHERE last_name = ? and first_name = ? and date_of_birth = ?
"""
SELECT_PATIENT_APPOINTMENT = """
    SELECT appointment_id, status, date, start_hour, doctor_id, hospital_id
    FROM appointment
    WHERE patient_id = ?
"""
SELECT_DOCTOR_INFORMATION = """
    SELECT *
    FROM doctor
    WHERE last_name = ? and first_name = ? speciality = ?
"""
SELECT_DOCTOR_INFORMATION_BY_ID = """
    SELECT last_name, first_name, speciality
    FROM doctor_by_id
    WHERE doctor_id = ?
"""
SELECT_DOCTOR_INFORMATION_BY_HOSPITAL_ID = """
    SELECT last_name, first_name, speciality, license_number
    FROM doctor_by_hospital_id
    WHERE hospital_id = ?
"""
SELECT_APPOINTMENTS_FOR_A_DAY = """
    SELECT appointment_id, status, date, start_hour, doctor_id, hospital_id
    FROM appointment_by_date
    WHERE date = ?
"""

# Create Information
CREATE_APPOINTMENT_FOR_PATIENT_1 = """
    INSERT INTO appointment (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""
CREATE_APPOINTMENT_FOR_PATIENT_2 = """
    INSERT INTO appointment_by_id (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""
CREATE_APPOINTMENT_FOR_PATIENT_3 = """
    INSERT INTO appointment_by_date (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""
CREATE_PATIENTS = """
    INSERT INTO patient (patient_id, first_name, last_name, date_of_birth, address, NSS, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?);
"""


# Delete Specific Information
DELETE_APPOINTMENT_FOR_USER_1 = """
    DELETE FROM appointment_by_date WHERE date = ? AND appointment_id = ? IF EXISTS;
"""
DELETE_APPOINTMENT_FOR_USER_2 = """
    DELETE FROM appointment_by_id WHERE appointment_id = ? IF EXISTS;
"""
DELETE_APPOINTMENT_FOR_USER_3 = """
    DELETE FROM appointment WHERE patient_id = ? AND status = ? AND date = ? AND start_hour = ? IF EXISTS;
"""
SEARCH_APPOINTMENT_BY_DATE = """
    SELECT patient_id, status, date, start_hour
    FROM appointment_by_date WHERE date = ? AND appointment_id = ?
"""
DELETE_PATIENT = """
    DELETE FROM patient WHERE last_name = ? AND first_name = ? AND date_of_birth = ?;
"""

# Modify Information
CANCEL_APPOINTMENT = """
    BEGIN BATCH
    DELETE FROM appointment_by_date WHERE date = ? AND appointment_id = ?;
    DELETE FROM appointment_by_id WHERE appointment_id = ?;
    DELETE FROM appointment WHERE patient_id = ? AND status = ? AND date = ? AND start_hour = ?;
    APPLY BATCH;
"""
CANCEL_APPOINTMENT_INSERT = """
    BEGIN BATCH
    INSERT INTO appointment_by_date (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    INSERT INTO appointment_by_id (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    INSERT INTO appointment (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    APPLY BATCH;
"""
RESCHEDULE_APPOINTMENT = """
    BEGIN BATCH
    DELETE FROM appointment_by_date WHERE date = ? AND appointment_id = ?;
    DELETE FROM appointment_by_id WHERE appointment_id = ?;
    DELETE FROM appointment WHERE patient_id = ? AND status = ? AND date = ? AND start_hour = ?;
    APPLY BATCH
"""
RESCHEDULE_APPOINTMENT_INSERT = """
    BEGIN BATCH
    INSERT INTO appointment_by_date (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    INSERT INTO appointment_by_id (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    INSERT INTO appointment (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    APPLY BATCH
"""
SELECT_APPOINTMENT_BY_ID = """
    SELECT *
    FROM appointment_by_id
    WHERE appointment_id = ?
"""


# Delete All Information
DELETE_HOSPITAL_TABLE = """
    TRUNCATE hospital.hospital;
"""
DELETE_PATIENT_TABLE = """
    TRUNCATE hospital.patient;
"""
DELETE_DOCTOR_TABLE = """
    TRUNCATE hospital.doctor;
"""
DELETE_DOCTOR_TABLE_BY_ID = """
    TRUNCATE hospital.doctor_by_id;
"""
DELETE_DOCTOR_TABLE_BY_HOSPITAL_ID = """
    TRUNCATE hospital.doctor_by_hospital_id;
"""
DELETE_APPOINTMENT_TABLE = """
    TRUNCATE hospital.appointment;
"""
DELETE_APPOINTMENT_TABLE_BY_ID = """
    TRUNCATE hospital.appointment_by_id;
"""
DELETE_APPOINTMENT_TABLE_BY_DATE = """
    TRUNCATE hospital.appointment_by_date;
"""


def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_HOSPITAL_TABLE)
    session.execute(CREATE_PATIENT_TABLE)
    session.execute(CREATE_DOCTOR_TABLE)
    session.execute(CREATE_DOCTOR_TABLE_BY_ID)
    session.execute(CREATE_DOCTOR_TABLE_BY_HOSPITAL_ID)
    session.execute(CREATE_APPOINTMENT_TABLE)
    session.execute(CREATE_APPOINTMENT_TABLE_BY_ID)
    session.execute(CREATE_APPOINTMENT_TABLE_BY_DATE)

def get_all_hospitals(session):
    log.info(f"Retrieving all hospitals information")
    stmt = session.prepare(SELECT_ALL_HOSPITALS)
    rows = session.execute(stmt)
    if rows:
        print(f"\033[1;36;40m\n{'Name':30}{'City':20}{'Hospital ID'}\033[0m")
        for row in rows:
            print(f"{row.hospital_name:30}{row.location:20}{row.hospital_id}")
    else:
        print("\nInformation of hospitals not found")


def get_hospital_information(session, hospital_id):
    log.info(f"Retrieving information of hospital with id equal to {hospital_id}")
    stmt = session.prepare(SELECT_HOSPITAL_INFORMATION)
    rows = session.execute(stmt, [uuid.UUID(hospital_id)])
    if rows:
        print(f"\033[1;36;40m\n{'Name':30}{'City':20}{'Hospital ID'}\033[0m")
        for row in rows:
            print(f"{row.hospital_name:30}{row.location:20}{row.hospital_id}")
    else:
        print("\nThe hospital you are looking for couldn't be found.")
    

def get_patient_information(session, last, first, birth_date):
    log.info(f"Retrieving information of patient {first} {last} born on {birth_date}")
    stmt = session.prepare(SELECT_PATIENT_INFORMATION)
    rows = session.execute(stmt, [last, first, birth_date])
    if rows:
        print(f"\033[1;36;40m\n{'Patient ID':40}{'Patient Name':20}{'Birth Date':12}{'NSS':10}{'Address':15}{'Hospital Assigned':30}\033[0m")
        for row in rows:
            stmt2 = session.prepare(SELECT_HOSPITAL_INFORMATION)
            rows2 = session.execute(stmt2, [row.hospital_id])
            print(f"{str(row.patient_id):40}{row.last_name+' '+row.first_name:20}{str(row.date_of_birth):12}{row.nss:10}{row.address:15}{rows2[0].hospital_name:30}")
    else:
        print("\nPatient information not found!")

def get_patient_appointments(session, patient_id):
    log.info(f"Retrieving appointments for user with ID equal to {patient_id}")
    stmt = session.prepare(SELECT_PATIENT_APPOINTMENT)
    rows = session.execute(stmt, [uuid.UUID(patient_id)])
    if rows:
        print(f"\033[1;36;40m\n{'Appointment ID':40}{'Status':14}{'Date':12}{'Hour':12}{'With Doctor':50}{'In Hospital':30}\033[0m")
        for row in rows:
            stmt2 = session.prepare(SELECT_DOCTOR_INFORMATION_BY_ID)
            rows2 = session.execute(stmt2, [row.doctor_id])
            stmt3 = session.prepare(SELECT_HOSPITAL_INFORMATION)
            rows3 = session.execute(stmt3, [row.hospital_id])
            print(f"{str(row.appointment_id):40}{row.status:14}{str(row.date):12}{row.start_hour:12}{rows2[0].last_name+' '+rows2[0].first_name+' ('+rows2[0].speciality+')':50}{rows3[0].hospital_name:30}")
    else:
        print("\nThere are no appointments for this user.")

def get_doctor_by_hospital(session, hospital_id):
    # Printing the hospital information
    get_hospital_information(session, hospital_id)
    # Getting all the doctors information for this hospital
    log.info(f"Retrieving all the doctors from the hospital with ID equal to {hospital_id}")
    stmt = session.prepare(SELECT_DOCTOR_INFORMATION_BY_HOSPITAL_ID)
    rows = session.execute(stmt, [uuid.UUID(hospital_id)])
    if rows:
        print(f"\033[1;36;40m\n{'Last Name':15}{'First Name':15}{'Speciality':30}{'License Number':20}\033[0m")
        for row in rows:
            print(f"{row.last_name:15}{row.first_name:15}{row.speciality:30}{row.license_number:20}")
    else:
        print("\nThere are no doctors for this specific hospital.")

def get_appointments_for_a_day(session, date):
    log.info(f"Retrieving all the appointments for this date: {date}")
    stmt = session.prepare(SELECT_APPOINTMENTS_FOR_A_DAY)
    rows = session.execute(stmt, [date])
    if rows:
        print(f"\033[1;36;40m\n{'Appointment ID':40}{'Status':14}{'Date':12}{'Hour':12}{'With Doctor':50}{'In Hospital':30}\033[0m")
        for row in rows:
            stmt2 = session.prepare(SELECT_DOCTOR_INFORMATION_BY_ID)
            rows2 = session.execute(stmt2, [row.doctor_id])
            stmt3 = session.prepare(SELECT_HOSPITAL_INFORMATION)
            rows3 = session.execute(stmt3, [row.hospital_id])
            print(f"{str(row.appointment_id):40}{row.status:14}{str(row.date):12}{row.start_hour:12}{rows2[0].last_name+' '+rows2[0].first_name+' ('+rows2[0].speciality+')':50}{rows3[0].hospital_name+' ('+rows3[0].location+')':30}")
    else:
        print(f"\nThere are no appointments for {date}")

def create_appointments_for_users(session, doctor_id, patient_id, start, end, date, status, hospital_id):
    log.info(f"Creating appointment for user with ID equal to {patient_id}")
    new_appointment_id = uuid.uuid4()
    stmt = session.prepare(CREATE_APPOINTMENT_FOR_PATIENT_1)
    session.execute(stmt, [new_appointment_id, uuid.UUID(doctor_id), uuid.UUID(patient_id), start, end, date, status, uuid.UUID(hospital_id)])
    stmt = session.prepare(CREATE_APPOINTMENT_FOR_PATIENT_2)
    session.execute(stmt, [new_appointment_id, uuid.UUID(doctor_id), uuid.UUID(patient_id), start, end, date, status, uuid.UUID(hospital_id)])
    stmt = session.prepare(CREATE_APPOINTMENT_FOR_PATIENT_3)
    session.execute(stmt, [new_appointment_id, uuid.UUID(doctor_id), uuid.UUID(patient_id), start, end, date, status, uuid.UUID(hospital_id)])
    print(f"\nYour appointment has been created succesfuly!")

def create_new_patients(session, first_name, last_name, birth_date, address, nss, hospital_id):
    log.info(f"Creating a new user")
    stmt = session.prepare(CREATE_PATIENTS)
    session.execute(stmt, [uuid.uuid4(), first_name, last_name, birth_date, address, nss, uuid.UUID(hospital_id)])
    print(f"\nYour user has been created succesfuly!")

def get_appointment_data(session, appointment_id):
    data = []
    stmt = session.prepare(SELECT_APPOINTMENT_BY_ID)
    rows = session.execute(stmt, [uuid.UUID(appointment_id)])
    if rows:
        data.append(rows[0].appointment_id) #0
        data.append(rows[0].doctor_id)      #1
        data.append(rows[0].patient_id)     #2
        data.append(rows[0].start_hour)     #3
        data.append(rows[0].end_hour)       #4
        data.append(rows[0].date)           #5
        data.append(rows[0].status)         #6
        data.append(rows[0].hospital_id)    #7
    else:
        return []
    return data


def cancel_appointment(session, appointment_id):
    log.info(f"Cancel the appointment with ID equal to: {appointment_id}")
    
    data = get_appointment_data(session, appointment_id)

    stmt1 = session.prepare(CANCEL_APPOINTMENT)
    session.execute(stmt1, [data[5], data[0], data[0], data[2], data[6], data[5], data[3]])
    stmt2 = session.prepare(CANCEL_APPOINTMENT_INSERT)
    session.execute(stmt2, [data[0], data[1], data[2], data[3], data[4], data[5], "Cancelled", data[7], data[0], data[1], data[2], data[3], data[4], data[5], "Cancelled", data[7], data[0], data[1], data[2], data[3], data[4], data[5], "Cancelled", data[7],] )
    print(f"\nYour appointment has been CANCELED.")

def reschedule_appointment(session, appointment_id, start_hour, date):
    log.info(f"Rescheduling the appointment with ID equal to {appointment_id} with new hour {start_hour} and date {date}")
    
    data = get_appointment_data(session, appointment_id)

    hour, minute = map(int, start_hour.split(':'))
    end_hour = f"{hour+1:02d}:00"

    stmt1 = session.prepare(RESCHEDULE_APPOINTMENT)
    session.execute(stmt1, [data[5], data[0], data[0], data[2], data[6], data[5], data[3]])
    stmt2 = session.prepare(RESCHEDULE_APPOINTMENT_INSERT)
    session.execute(stmt2, [data[0], data[1], data[2], start_hour, end_hour, date, "Rescheduled", data[7], data[0], data[1], data[2], start_hour, end_hour, date, "Rescheduled", data[7], data[0], data[1], data[2], start_hour, end_hour, date, "Rescheduled", data[7]] )
    print(f"\nYour appointment has been RESCHEDULED to {date} @ {start_hour}.")


# Helps deleting an appointment on every table
def get_specific_appointment(session, appointment_id, date):
    data = []
    stmt = session.prepare(SEARCH_APPOINTMENT_BY_DATE)
    rows = session.execute(stmt, [date, uuid.UUID(appointment_id)])
    if rows:
        data.append(rows[0].patient_id)
        data.append(rows[0].status)
        data.append(rows[0].date)
        data.append(rows[0].start_hour)
    else:
        return []
    return data

def delete_appointments(session, appointment_id, date):
    log.info(f"Deleting the appointment with ID equal to: {appointment_id} on {date}")

    data = get_specific_appointment(session, appointment_id, date)
    if data:
        stmt = session.prepare(DELETE_APPOINTMENT_FOR_USER_1)
        session.execute(stmt, [date, uuid.UUID(appointment_id)])
        stmt = session.prepare(DELETE_APPOINTMENT_FOR_USER_2)
        session.execute(stmt, [uuid.UUID(appointment_id)])
        stmt = session.prepare(DELETE_APPOINTMENT_FOR_USER_3)
        session.execute(stmt, [data[0], data[1], data[2], data[3]])
        print(f"\nYour appointment has been deleted succesfuly!")
    else:
        print(f"\nThe appointment couldn't be deleted.")

def delete_patient(session, last, first, birth):
    log.info(f"Deleting the patient named {last + ' ' + first} born on {birth}")
    stmt = session.prepare(DELETE_PATIENT)
    session.execute(stmt, [last, first, birth])
    print(f"\nYour patient has been deleted succesfuly!")

def delete_all_information(session):
    log.info(f"Deleting all the information from every table on the database.")
    session.execute(DELETE_DOCTOR_TABLE)
    session.execute(DELETE_DOCTOR_TABLE_BY_ID)
    session.execute(DELETE_DOCTOR_TABLE_BY_HOSPITAL_ID)
    session.execute(DELETE_HOSPITAL_TABLE)
    session.execute(DELETE_PATIENT_TABLE)
    session.execute(DELETE_APPOINTMENT_TABLE)
    session.execute(DELETE_APPOINTMENT_TABLE_BY_ID)
    session.execute(DELETE_APPOINTMENT_TABLE_BY_DATE)
    print("\033[1;31;40mAll data has been deleted from the tables succesfully!\n\033[0m")
            