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
        PRIMARY KEY ((hospital_id), location, hospital_name)
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
        PRIMARY KEY ((patient_id), last_name, first_name, date_of_birth, NSS)
    ) WITH CLUSTERING ORDER BY (last_name ASC, first_name ASC, date_of_birth ASC)
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
        PRIMARY KEY ((doctor_id), last_name, first_name, speciality, license_number)
    ) WITH CLUSTERING ORDER BY (last_name DESC, first_name DESC)
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
        PRIMARY KEY ((appointment_id), patient_id, start_hour, date, status)
    ) WITH CLUSTERING ORDER BY (patient_id ASC, start_hour ASC, date ASC, status ASC)
"""
SELECT_PATIENT_INFORMATION = """
    SELECT patient_id, first_name, last_name, date_of_birth, address, NSS, hospital_id
    FROM patient
    WHERE first_name = ? and last_name = ? and date_of_birth = ?
"""
SELECT_HOSPITAL = """
    SELECT hospital_id, hospital_name, location
    FROM hospital
"""
SELECT_DOCTOR = """
    SELECT doctor_id, first_name, last_name, speciality, license_number, hospital_id
    FROM doctor
"""
SELECT_APPOINTMENT = """
    SELECT appointment_id, patient_id, doctor_id, start_hour, end_hour, date, status, hospital_id
    FROM appointment
"""
DELETE_APPOINTMENT = """
    TRUNCATE hospital.appointment;
"""
DELETE_HOSPITAL = """
    TRUNCATE hospital.hospital;
"""
DELETE_DOCTOR = """
    TRUNCATE hospital.doctor;
"""
DELETE_PATIENT = """
    TRUNCATE hospital.patient;
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_HOSPITAL_TABLE)
    session.execute(CREATE_PATIENT_TABLE)
    session.execute(CREATE_DOCTOR_TABLE)
    session.execute(CREATE_APPOINTMENT_TABLE)

def get_patient_information(session, last, first, birth_date):
    log.info(f"Retrieving information of patient {first} {last} born on {birth_date}")
    stmt = session.prepare(SELECT_PATIENT_INFORMATION)
    rows = session.execute(stmt, [last, first, birth_date])
    if rows:
        for row in rows:
            print(row)
    else:
        print("Not information found")


def delete_all_information(session):
    log.info(f"Deleting all the information from every table on the database.")
    session.execute(DELETE_DOCTOR)
    session.execute(DELETE_HOSPITAL)
    session.execute(DELETE_PATIENT)
    session.execute(DELETE_APPOINTMENT)
    print("\033[1;31;40mAll data has been deleted succesfully!\n\033[0m")
            