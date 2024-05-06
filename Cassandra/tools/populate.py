#!/usr/bin/env python3
import datetime
import random
import uuid

import time_uuid

CQL_FILE = 'tools/data.cql'

# Hospital Data
HOSPITAL_NAMES = ["Hospital General", "Hospital Universitario", "Clinica San Jose", "Centro Medico", "Hospital Regional",
                  "Clinica Santa Maria", "Hospital Infantil", "Clinica del Carmen", "Hospital de la Esperanza", "Centro de Salud"]
LOCATIONS = ["Ciudad de Mexico", "Buenos Aires", "Madrid", "Santiago de Chile", "Lima", "Bogota", "Sao Paulo", "Caracas", 
             "La Habana", "Quito", "San Jose", "Panama", "Montevideo", "Asuncion", "Guatemala City"]
# Patient and Doctor data
FIRST_NAMES = ["Luis", "Ana", "Juan", "Maria", "Carlos", "Laura", "Pedro", "Sofia", "Diego", "Valentina",
               "Alejandro", "Camila", "Javier", "Isabella", "Miguel", "Paula", "Fernando", "Daniela", "Andres", "Lucia",
               "Gabriel", "Luisa", "Mateo", "Elena", "Ricardo", "Valeria", "Emilio", "Alicia", "Santiago", "Carolina"]
LAST_NAMES = ["Garcia", "Martinez", "Lopez", "Gonzalez", "Rodriguez", "Hernandez", "Sanchez", "Perez", "Gomez", "Martin",
              "Jimenez", "Ruiz", "Diaz", "Alvarez", "Moreno", "Molina", "Ortega", "Delgado", "Nunez", "Cabrera",
              "Vargas", "Castro", "Fernandez", "Torres", "Rivera", "Rojas", "Navarro", "Marquez", "Santos", "Reyes"]
SPECIALTIES = ["Cardiologia", "Dermatologia", "Endocrinologia", "Gastroenterologia", "Hematologia", "Inmunologia",
               "Neurologia", "Oftalmologia", "Oncologia", "Otorrinolaringologia", "Pediatria", "Psiquiatria",
               "Radiologia", "Reumatologia", "Traumatologia", "Urologia", "Ginecologia", "Obstetricia",
               "Anestesiologia", "Medicina Interna", "Cirugia General", "Neumologia", "Nefrologia", "Geriatria",
               "Medicina Familiar", "Endocrinologia Pediatrica", "Cirugia Plastica", "Medicina Deportiva", "Oncologia Pediatrica"]
APP_STATUS = ["Scheduled", "Confirmed", "Cancelled", "Rescheduled"]

def cql_stmt_generator(hospital=20, patient=100, doctor=100, appointments=10000):
    hospital_stmt = "INSERT INTO hospital (hospital_id, hospital_name, location) VALUES ({}, '{}', '{}');"
    patient_stmt = "INSERT INTO patient (patient_id, first_name, last_name, date_of_birth, address, NSS, hospital_id) VALUES ({}, '{}', '{}', '{}', '{}', '{}', {});"
    doctor_stmt = "INSERT INTO doctor (doctor_id, first_name, last_name, speciality, license_number, hospital_id) VALUES({}, '{}', '{}', '{}', '{}', {});"
    doctor_by_id_stmt = "INSERT INTO doctor_by_id (doctor_id, first_name, last_name, speciality, license_number, hospital_id) VALUES({}, '{}', '{}', '{}', '{}', {});"
    doctor_by_hospital_id_stmt = "INSERT INTO doctor_by_hospital_id (doctor_id, first_name, last_name, speciality, license_number, hospital_id) VALUES({}, '{}', '{}', '{}', '{}', {});"
    appointment_stmt = "INSERT INTO appointment (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES({}, {}, {}, '{}', '{}', '{}', '{}', {});"
    appointment_by_date_stmt = "INSERT INTO appointment_by_date (appointment_id, doctor_id, patient_id, start_hour, end_hour, date, status, hospital_id) VALUES({}, {}, {}, '{}', '{}', '{}', '{}', {});"

    hospital_ids = []
    patients_ids = []
    doctors_ids = []
    # Generate HOSPITALS CQL
    with open(CQL_FILE, "w") as fd:
        for i in range(hospital):
            hospital_id = str(uuid.uuid4())
            hospital_name = random.choice(HOSPITAL_NAMES)
            hospital_location = random.choice(LOCATIONS)
            # Update the ids that we have created
            hospital_ids.append(hospital_id)
            # Write the statement with the data created
            fd.write(hospital_stmt.format(hospital_id, hospital_name, hospital_location))
            fd.write('\n')
        fd.write('\n\n')

        # Generate PATIENTS CQL
        for i in range(patient):
            patient_id = str(uuid.uuid4())
            patient_first = random.choice(FIRST_NAMES)
            patient_last = random.choice(LAST_NAMES)
            birth = random_date(datetime.datetime(1970, 1, 1), datetime.datetime(2000, 1, 1))
            address = "Calle #"+str(i+1)
            nss = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            hospital_id = random.choice(hospital_ids)
            # update the ids that we have created
            patients_ids.append(patient_id)
            # Write the statement with the data created
            fd.write(patient_stmt.format(patient_id, patient_first, patient_last, birth, address, nss, hospital_id))
            fd.write('\n')
        fd.write('\n\n')

        # Generate DOCTORS CQL
        for i in range(doctor):
            doctor_id = str(uuid.uuid4())
            doctor_first = random.choice(FIRST_NAMES)
            doctor_last = random.choice(LAST_NAMES)
            speciality = random.choice(SPECIALTIES)
            license = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            hospital_id = random.choice(hospital_ids)
            # update the ids that we have created
            doctors_ids.append(doctor_id)
            # Write the statement with the data created
            fd.write(doctor_stmt.format(doctor_id, doctor_first, doctor_last, speciality, license, hospital_id))
            fd.write('\n')
            fd.write(doctor_by_id_stmt.format(doctor_id, doctor_first, doctor_last, speciality, license, hospital_id))
            fd.write('\n')
            fd.write(doctor_by_hospital_id_stmt.format(doctor_id, doctor_first, doctor_last, speciality, license, hospital_id))
            fd.write('\n')
        fd.write('\n\n')

        # Generate APPOINTMENTS CQL
        for i in range(appointments):
            app_id = str(uuid.uuid4())
            doc_id = random.choice(doctors_ids)
            pat_id = random.choice(patients_ids)

            start_hour = f"{random.randint(7, 20):02d}:00"
            hour, minute = map(int, start_hour.split(':'))
            # Incrementa la hora en 1 y ajusta si excede 20:59
            # Formatea la hora final
            end_hour = f"{hour+1:02d}:00"
            date = random_date(datetime.datetime(2024, 1, 1), datetime.datetime(2025, 12, 12))
            status = random.choice(APP_STATUS)
            hospital_id = random.choice(hospital_ids)
            # Write the statement with the data created
            fd.write(appointment_stmt.format(app_id, doc_id, pat_id, start_hour, end_hour, date, status, hospital_id))
            fd.write('\n')
            fd.write(appointment_by_date_stmt.format(app_id, doc_id, pat_id, start_hour, end_hour, date, status, hospital_id))
            fd.write('\n')
        fd.write('\n\n')
    fd.close()

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return rand_date.strftime('%Y-%m-%d')

def main():
    cql_stmt_generator()


if __name__ == "__main__":
    main()