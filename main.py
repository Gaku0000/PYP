#==============================================================================================================
#============================================ADMIN Functions===================================================
#=============================================Bektay Abdinur===================================================
#===============================================TP076035=======================================================
#==============================================================================================================
import os
from dataclasses import field

# File names
STATS_FILE = "Database/admin_hospital_stats11.txt"
ADMIN_USERS_FILE = "Database/admin_login.txt"
DOCTOR_USERS_FILE = "Database/doctor.account.txt"
NURSE_USERS_FILE = "Database/nurse_credentials.txt"
RECEPTIONIST_USERS_FILE = "Database/receptAccounts.txt"
PATIENT_USERS_FILE = "Database/patient.account.txt"

# Initialize files if they do not exist
def initialize_files():
    if not os.path.exists(ADMIN_USERS_FILE):
        with open(ADMIN_USERS_FILE, "w") as f:
            pass  # Create an empty file

    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, "w") as f:
            f.write("0\n0\n50\n50")  # total_patients, total_doctors, available_beds, total_beds

    if not os.path.exists(ADMIN_USERS_FILE):
        with open(ADMIN_USERS_FILE, "w") as f:
            f.write("Abdi,7077\n")  # Default admin login

# Load users from file into a list
def load_users(role):
    if role == 'admin':
        with open(ADMIN_USERS_FILE, "r") as f:
            users = [line.strip().split(",") for line in f.readlines()]
        return users
    if role == 'doctor':
        with open(DOCTOR_USERS_FILE, "r") as f:
            users = [line.strip().split(",") for line in f.readlines()]
        return users
    if role == 'nurse':
        with open(NURSE_USERS_FILE, "r") as f:
            users = [line.strip().split(",") for line in f.readlines()]
        return users
    if role == 'receptionist':
        with open(RECEPTIONIST_USERS_FILE, "r") as f:
            users = [line.strip().split(",") for line in f.readlines()]
        return users
    if role == 'patient':
        with open(PATIENT_USERS_FILE, "r") as f:
            users = [line.strip().split(",") for line in f.readlines()]
        return users

# Save users from a list into the file
def save_users(users, role):
    if role == 'admin':
        with open(ADMIN_USERS_FILE, "w") as f:
            for user in users:
                f.write(",".join(user) + "\n")
    if role == 'doctor':
        with open(DOCTOR_USERS_FILE, "w") as f:
            for user in users:
                f.write(",".join(user) + "\n")
    if role == 'nurse':
        with open(NURSE_USERS_FILE, "w") as f:
            for user in users:
                f.write(",".join(user) + "\n")
    if role == 'receptionist':
        with open(RECEPTIONIST_USERS_FILE, "w") as f:
            for user in users:
                f.write(",".join(user) + "\n")
    if role == 'patient':
        with open(PATIENT_USERS_FILE, "w") as f:
            for user in users:
                f.write(",".join(user) + "\n")

# Load hospital stats from file into a list
def load_stats():
    with open(STATS_FILE, "r") as f:
        stats = [int(line.strip()) for line in f.readlines()]
    return stats  # [total_patients, total_doctors, available_beds, total_beds]

# Save hospital stats from a list into the file
def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        for stat in stats:
            f.write(str(stat) + "\n")

# Validate login
def validate_login():
    with open(ADMIN_USERS_FILE, "r") as f:
        credentials = [line.strip().split(",") for line in f.readlines()]

    attempts = 0
    while attempts < 3:
        username = input("Enter username (max 4 letters, no numbers): ")
        if not username.isalpha() or len(username) > 4:
            print("Invalid username. Try again.")
            attempts += 1
            continue

        password = input("Enter password (exactly 4 digits): ")
        if not password.isdigit() or len(password) != 4:
            print("Invalid password. Try again.")
            attempts += 1
            continue

        if any(user[0] == username and user[1] == password for user in credentials):
            print("Login successful.")
            return True

        print("Incorrect username or password. Try again.")
        attempts += 1

    print("Maximum attempts reached. Exiting.")
    return False

# Update hospital statistics based on current users
def update_stats_from_users():
    patient_users = load_users('patient')
    total_patients = sum(1 for user in patient_users if user[1].lower() == "patient")
    doctor_users = load_users('doctor')
    total_doctors = sum(1 for user in doctor_users if user[1].lower() == "doctor")
    stats = load_stats()
    stats[0] = total_patients
    stats[1] = total_doctors
    save_stats(stats)

# Administrator functionalities
def create_user():
    stats = load_stats()
    role = input("Enter role (admin, doctor, nurse, receptionist, patient): ")
    role = role.lower()
    if role == 'admin' or role == 'doctor' or role == 'nurse' or role == 'receptionist' or role == 'patient':
        #Create user based on role
        users = load_users(role)
        username = input("Enter username: ")
        password = input("Enter password: ")
        for user in users:
            if user[0] == username:
                print("User already exists.")
                return
        users.append([username, password])
        save_users(users, role)
        print(f"User {username} created successfully.")
        if role == "doctor":
            stats[1] += 1  # Increment total_doctors
        elif role == "patient":
            stats[0] += 1  # Increment total_patients
            if stats[2] > 0:  # Reduce available beds if available
                stats[2] -= 1
            else:
                print("Warning: No available beds!")
        save_stats(stats)
    else:
        print("Invalid role.")

def update_user():
    role = input("Enter role (admin, doctor, nurse, receptionist, patient): ")
    role = role.lower()
    if role == 'admin' or role == 'doctor' or role == 'nurse' or role == 'receptionist' or role == 'patient':
        users = load_users(role)
        username = input("Enter username to update: ")

        for user in users:
            if user[0] == username:
                new_password = input("Enter new password (leave blank to keep current password): ")
                if new_password:
                    user[1] = new_password
                save_users(users, role)
                update_stats_from_users()
                print(f"User {username} updated successfully.")
                return
        print("User not found.")
    else:
        print("Invalid role.")

def delete_user():
    role = input("Enter role (admin, doctor, nurse, receptionist, patient): ")
    role = role.lower()
    if role == 'admin' or role == 'doctor' or role == 'nurse' or role == 'receptionist' or role == 'patient':
        users = load_users(role)
        username = input("Enter username to delete: ")

        # Check if the user exists
        user_found = any(user[0] == username for user in users)
        if not user_found:
            print("User not found.")
            return

        # Delete the user if found
        users = [user for user in users if user[0] != username]
        save_users(users,role)
        update_stats_from_users()
        print(f"User {username} deleted successfully.")
    else:
        print("Invalid role.")

def view_hospital_statistics():
    stats = load_stats()
    print(f"""
    Total Patients: {stats[0]}
    Total Doctors: {stats[1]}
    Available Beds: {stats[2]} / {stats[3]}
    """)

def generate_report():
    stats = load_stats()
    occupancy_rate = 100 - (stats[2] / stats[3] * 100)
    print(f"""
    HOSPITAL USAGE REPORT
    ---------------------
    Total Patients: {stats[0]}
    Total Doctors: {stats[1]}
    Available Beds: {stats[2]} / {stats[3]}
    Occupancy Rate: {occupancy_rate:.2f}%
    """)

def manage_resources():
    stats = load_stats()
    choice = input("Do you want to add or remove beds? (add/remove): ").lower()

    if choice == "add":
        beds = int(input("Enter the number of beds to add: "))
        stats[3] += beds
        stats[2] += beds
        print(f"{beds} beds added successfully.")
    elif choice == "remove":
        beds = int(input("Enter the number of beds to remove: "))
        stats[3] -= beds
        stats[2] -= beds
        if stats[2] < 0:
            stats[2] = 0
        if stats[3] < 0:
            stats[3] = 0
        print(f"{beds} beds removed successfully.")
    else:
        print("Invalid option.")

    save_stats(stats)

def rules_and_policies():
    print("""
    HOSPITAL RULES AND POLICIES
    ---------------------------
    1. Masks are mandatory for all visitors.
    2. Maintain social distancing in waiting areas.
    3. Visiting hours are from 10 AM to 8 PM.
    4. No smoking on hospital premises.
    5. Report emergencies to the reception immediately.
    """)

# Administrator menu
def administrator_menu():
    while True:
        print("""
        ADMINISTRATOR MENU
        ------------------
        1. Manage User Accounts
        2. View Hospital Statistics
        3. Generate Reports
        4. Manage Hospital Resources
        5. Rules and Policies
        6. Exit to Main Menu
        """)
        choice = input("Enter your choice: ")
        if choice == "1":
            while True:
                print("""
                MANAGE USER ACCOUNTS
                --------------------
                1. Create User
                2. Update User
                3. Delete User
                4. Exit to Administrator Menu
                """)
                sub_choice = input("Enter your choice: ")
                if sub_choice == "1":
                    create_user()
                elif sub_choice == "2":
                    update_user()
                elif sub_choice == "3":
                    delete_user()
                elif sub_choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == "2":
            view_hospital_statistics()
        elif choice == "3":
            generate_report()
        elif choice == "4":
            manage_resources()
        elif choice == "5":
            rules_and_policies()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

#==============================================================================================================
#============================================DOCTOR Functions==================================================
#============================================Gaku Kobayakawa===================================================
#===============================================TP084690=======================================================
#==============================================================================================================
import  datetime

def save_data(file_,doctor_id,patient_id,diagnosis,prescription,treatment_plan,time):
    with open(file_,"a") as df:
        df.write(f"{doctor_id},{patient_id},{diagnosis},{prescription},{treatment_plan},{time}\n")

    print("Your input has been saved.\n")
    check_file(doctor_id,patient_id)

def write_h_file(doctor_id,patient_id):
    reason=input("Please enter the purpose of your hospitalization:")
    date1=input("Please enter the start date of the hospitalization:")
    date2=""

    with open("Database/doctor_hospitalization.txt","a") as file:
        file.write(f"{doctor_id},{patient_id},{reason},{date1},{date2}\n")
        appointment_or(doctor_id, patient_id)

def read_h_file(patient_id):
    try:
        with open("Database/doctor_hospitalization.txt","r")as file:
            while True:
                for line in file:
                    data=line.strip().split(",")

                    if len(data)<5:
                        continue

                    if data[1]==patient_id and (data[4]==None or data[4]==""):
                        return data
                return None
    except FileNotFoundError:
        return None

def check_file(doctor_id,patient_id):
    result = read_h_file(patient_id)
    if result:
        discharge_check(doctor_id,patient_id, result)
    else:
        hospitalization(doctor_id, patient_id)

def hospitalization(doctor_id,patient_id):
    choice=input("Does this patient need to be hospitalized?[y/n]：")
    if choice=="y":
        write_h_file(doctor_id,patient_id)
    elif choice=="n":
        appointment_or(doctor_id, patient_id)
    else:
        print("Please enter y or n.")
        hospitalization(doctor_id,patient_id)

def discharge_check(doctor_id,patient_id,result):
    choice = input("Do you give permission for discharge?[y/n]：")
    if choice=="y":
        line_number=discharge_1(patient_id)
        discharge_2(doctor_id,patient_id,line_number,result)
    elif choice=="n":
        appointment_or(doctor_id, patient_id)
    else:
        print("Please enter y or n.")
        discharge_check(doctor_id,patient_id,result)

def discharge_1(patient_id):
    try:
        with open("Database/doctor_hospitalization.txt","r") as file:
            for line_number,line in enumerate(file,start=1):
                data=line.strip().split(",")

                if len(data)<5:
                    continue

                if data[1] == patient_id and (data[4] == None or data[4] == ""):
                    return line_number

            return None
    except FileNotFoundError:
        return None

def discharge_2(doctor_id,patient_id,line_number,result):
    discharge_date=input("Please enter the date of discharge：")
    try:
        with open("Database/doctor_hospitalization.txt","r") as file:
            lines = file.readlines()
            d_id=result[0]
            reason=result[2]
            start_date=result[3]
            new_line=f"{d_id},{patient_id},{reason},{start_date},{discharge_date}"
            lines[line_number-1]=new_line+"\n"

        with open("Database/doctor_hospitalization.txt","w") as file:
            file.writelines(lines)
            appointment_or(doctor_id,patient_id)
    except FileNotFoundError:
        print("An unexpected error has occurred.\nReturn to the doctor's menu.")
        doctor_main(doctor_id)

def save_new_appointment(doctor_id,_id,date,time,purpose):
    a="A"
    try:
        with open("Database/recept_appointment.txt", "r") as rfile:
            lines=rfile.readlines()

            if lines:
                last_appointment=lines[-1].split(",")[0]
                last_id=int(last_appointment[len(a):])
            else:
                last_id=0
    except FileNotFoundError:
        last_id=0

    with open("Database/recept_appointment.txt", "a") as af:
        appointment_id = f"{a}{last_id + 1}"
        af.write(f"{appointment_id},{doctor_id},{_id},{date},{time},{purpose}\n")
    print("Your input has been saved.\n")
    print("\n\nThis concludes the diagnosis\n\nReturn to menu\n\n")
    doctor_main(doctor_id)

def appointment_check(doctor_id,patient_id,appointment_date,appointment_time,purpose):
    yn = input("Are there any mistakes in this information you entered?[y/n]:")
    if yn == "y":
        save_new_appointment(doctor_id,patient_id, appointment_date, appointment_time,purpose)
    elif yn == "n":
        print("\nPlease enter again...\n\n")
        _appointment(doctor_id,patient_id)
    else:
        print("Please enter y or n again....")
        appointment_check(doctor_id,patient_id, appointment_date, appointment_time,purpose)

def _appointment(doctor_id,patient_id):
    appointment_date=input("Please enter the date of next appointment(YYYY/DD/MM):")
    appointment_time=input("Please enter the time(00:00):")
    purpose=input("Please enter purpose:")
    appointment_check(doctor_id,patient_id,appointment_date, appointment_time,purpose)

def appointment_or(doctor_id,patient_id):
    yn=input("Would you  like to schedule a date for next diagnostic?[y/n]:")
    if yn=="y":
        _appointment(doctor_id,patient_id)
    elif yn=="n":
        print("\n\nThis concludes the diagnosis\n\nReturn to menu\n\n")
        doctor_main(doctor_id)
    else:
        print("Please enter again...\n")
        appointment_or(doctor_id,patient_id)

def go_back(doctor_id,a,b,c,d):
    yn=input("Do you want to save what you entered?[y/n]:")
    if yn=="y":
        _time=datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        print("Saves your input...\n\n\n")
        f="Database/doctor_diagnosis.txt"
        save_data(f,doctor_id,a,b,c,d,_time)
    elif yn=="n":
        print("Please enter agin.\n\n")
        _diagnosis(doctor_id,a)
    else:
        print("Please enter y or n...\n")
        go_back(doctor_id,a,b,c,d)

def _treatment_plan(doctor_id,patient_id,diagnosis,prescription):
    print("="*5,"Please fill patient's treatment plan","="*5)
    treatment_plan=input("")
    go_back(doctor_id,patient_id,diagnosis,prescription,treatment_plan)

def _prescription(doctor_id,patient_id,diagnosis):
    print("="*5,"Please fill the prescriptions","="*5)
    prescription=input("")
    _treatment_plan(doctor_id,patient_id,diagnosis,prescription)

def _diagnosis(doctor_id,patient_id):
    print("="*5,"Please fill in the diagnosis","="*5)
    diagnosis=input("")
    _prescription(doctor_id,patient_id,diagnosis)

def show_history(patient_id,data_number):
    history=[]
    try:
        with open("Database/doctor_diagnosis.txt","r") as rf:
            for line in rf:
                data=line.strip().split(",")
                if patient_id==data[1]:
                    diagnosis=data[data_number]
                    time=data[5]
                    history.append(f"({time})")
                    history.append(diagnosis)

        return history

    except FileNotFoundError:
        print("The file where the medical history was saved does not exist.\nPlease enter a new diagnosis and try again.")

def dia_or(doctor_id,patient_id):
    print("="*20,"\n1.Return to menu screen\n2.Continue diagnosis")
    choice=input("Please enter 1 or 2:")
    if choice=="1":
        print("\n\nReturn to menu\n\n")
        doctor_main(doctor_id)
    elif choice=="2":
        _diagnosis(doctor_id,patient_id)
    else:
        print("Your input is not valid.\nPlease try again...")
        dia_or(doctor_id,patient_id)

def diagnosis_or(doctor_id,patient_id):
    print("="*30,"\n1.Move on to the diagnosis of this patient\n2.View more information about this patient"
                 "\n3.Close this patient's information")
    choice = input("Please enter 1-3:")

    if choice == "1":
        print("\n\nGo to diagnosis")
        _diagnosis(doctor_id,patient_id)
    elif choice == "2":
        print("\n\nView more\n")
        result1=show_history(patient_id,2)
        print("=" * 5, "Medical history", "=" * 5)
        if result1:
            for one in result1:
                print(one)
        else:
            print("No history")
        result2=show_history(patient_id,3)
        print("=" * 5, "Prescription history", "=" * 5)
        if result2:
            for two in result2:
                print(two)
        else:
            print("No history")
        result3=show_history(patient_id,4)
        print("="*5,"Treatment history","="*5)
        if result3:
            for three in result3:
                print(three)
        else:
            print("No history")
        dia_or(doctor_id,patient_id)
    elif choice=="3":
        doctor_main(doctor_id)

    else:
        print("Please enter again...")
        diagnosis_or(doctor_id,patient_id)

def search_id_inf(file_name, patient_id):
    try:
        with open(file_name, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == patient_id:
                    return data
        return None
    except FileNotFoundError:
        print("The file does not exist.\nPlease register a new ID and try again.")
        return None

def access_mode(doctor_id):
    print("=" * 5, "This is access to patient information mode", "=" * 5, "\nSearch by entered patient ID")
    patient_id = input("Please enter patient ID:")
    result = search_id_inf("Database/patientlist.txt", patient_id)
    if result:
        print(f"ID:{result[0]}\nName:{result[1]}\nAge:{result[2]}\nGender:{result[3]}\nBlood type:{result[6]}\nAddress:{result[4]}\nContacto number:{result[5]}\n")
        diagnosis_or(doctor_id,patient_id)

    else:
        print(f"Patient ID not found...\nPlease try again")
        access_mode(doctor_id)

def doctor_main(doctor_id):
    print("="*5,"This is Doctor's Main menu","="*5,"\n1.Access to Patient information\n2.Logout")
    choice=input("Please enter 1 or 2:")
    if choice=="1":
        print("\n\nGo to access mode\n\n")
        access_mode(doctor_id)
    elif choice=="2":
        print("\n\nLogout.....\n\n")
        login_doctor()
    elif choice=="0515":
        print("Please enter the information")
        i = input("ID:")
        n = input("Name:")
        a = input("Age:")
        g = input("Gender:")
        add=input("Address:")
        p=input("Contact number:")
        b=input("Blood type:")

        with open("Database/patientlist.text", "a") as file:
            file.write(f"{i}, {n}, {a}, {g}, {add}, {p}, {b}\n")

    else:
        print("Please try again\n\n")
        doctor_main(doctor_id)

def login_doctor():
    print("=" * 5, "This is Doctor's login System", "=" * 5)
    de=input("1.login\n2.return to main menu\nPlease enter 1 or 2:")
    if de=="1":
        dr_id=input("Please enter your ID:")
        result=search_id_inf("Database/doctor.account.txt",dr_id)

        if result:
            result_login(result)
        else:
            login_doctor()

    elif de=="2":
        print("Return to main menu")
        return

    elif de=="0515":
        d_id=input("ID")
        name=input("name")
        password=input("password")

        with open("Database/doctor.account.txt","a") as df:
            df.write(f"{d_id},{name},{password}\n")
        print("done")
    else:
        print("Please try again")
        login_doctor()

def result_login(result):
    password = input("Please enter your password:")
    if result[1] == password:
        print("Your login is complete.\nGo to the Doctor's Main menu\n\n")
        doctor_id=result[0]
        doctor_main(doctor_id)
    else:
        print("The password you entered is incorrect\n\nPlease try again")
        result_login(result)

#==============================================================================================================
#=============================================Nurse Functions==================================================
#==============================================Zayyan Munir====================================================
#===============================================TP083364=======================================================
#==============================================================================================================

def main_menu():
    print("\n=== Hospital Management System ===")
    print("1. Administrator")
    print("2. Doctor")
    print("3. Nurse")
    print("4. Receptionist")
    print("5. Patient")
    print("6. Exit")

    choice = input("Enter your role (1-6): ")
    return choice

def nurse_login():
    print("\n--- Nurse Login ---")
    username = input("Enter Nurse Username: ")
    password = input("Enter Nurse Password: ")


    try:
        with open("Database/nurse_credentials.txt", "r") as file:
            credentials = [line.strip().split(",") for line in file]
            for user, pwd in credentials:
                if username == user and password == pwd:
                    print("Login successful. Welcome, Nurse!")
                    nurse_menu()
                    return
            print("Invalid credentials. Please try again.")
    except FileNotFoundError:
        print("Credentials file not found. Please contact the administrator.")

def nurse_menu():
    while True:
        print("\n--- Nurse Menu ---")
        print("1. View Daily Patient List")
        print("2. Update Patient Vitals")
        print("3. Manage Medication Logs")
        print("4. Prepare Rooms for Procedures")
        print("5. Report Emergency")
        print("6. Back to Main Menu")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            view_daily_patient_list()
        elif choice == "2":
            update_patient_vitals()
        elif choice == "3":
            manage_medication_logs()
        elif choice == "4":
            prepare_rooms()
        elif choice == "5":
            report_emergency()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def view_daily_patient_list():
    print("\n--- Daily Patient List ---")
    try:
        with open("Database/patientlist.txt", "r") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("No patient data found.")

def update_patient_vitals():
    print("\n--- Update Patient Vitals ---")
    patient_id = input("Enter Patient ID: ")
    vitals = input("Enter updated vitals (e.g., BP: 120/80, Temp: 98.6): ")

    with open("Database/nurse_vitals_logs.txt", "a") as file:
        file.write(f"Patient ID: {patient_id}, Vitals: {vitals}\n")

    print("Vitals updated successfully.")

def manage_medication_logs():
    print("\n--- Manage Medication Logs ---")
    patient_id = input("Enter Patient ID: ")
    medication = input("Enter medication details (e.g., Drug: Dosage, Time: 8AM): ")

    with open("Database/nurse_medication_logs.txt", "a") as file:
        file.write(f"Patient ID: {patient_id}, Medication: {medication}\n")

    print("Medication log updated successfully.")

def prepare_rooms():
    print("\n--- Prepare Rooms for Procedures ---")
    room_id = input("Enter Room ID: ")
    procedure = input("Enter procedure details: ")

    with open("Database/nurse_rooms.txt", "a") as file:
        file.write(f"Room ID: {room_id}, Procedure: {procedure}\n")

    print("Room preparation logged successfully.")

def report_emergency():
    print("\n--- Report Emergency ---")
    patient_id = input("Enter Patient ID: ")
    details = input("Enter emergency details: ")

    with open("Database/nurse_emergencies.txt", "a") as file:
        file.write(f"Patient ID: {patient_id}, Emergency: {details}\n")

    print("Emergency reported successfully.")

#==============================================================================================================
#=========================================RECEPTIONIST Functions===============================================
#===========================================Ekin Lunar Limarya=================================================
#===============================================TP079963=======================================================
#==============================================================================================================
def checkAlpha(userInput):
    space = set(' ')
    chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
    isSpace = ''.join(filter(lambda c:c in space, userInput))
    tempInput = ''.join(filter(lambda c: c in chars, userInput))
    if tempInput != userInput:
        print('Please enter alphabets only')
        return True
    elif tempInput == isSpace:
        print('Please enter a value')
        return True
    elif len(userInput) < 3:
        print('Please enter a proper value')
        return True         # True is try again
    else:
        return tempInput != userInput       # That's why this returns True only if this is false.

def checkID(who):
    if who == 'patient':
        tempID = str(input("Please enter a Patient ID: "))  # get the ID to search
        if tempID == '-1':
            return tempID
        tempRes = 0  # temp result
        data = readFile('Database/patientlist.txt')
    elif who == 'doctor':
        tempID = str(input("Please enter a Doctor ID: "))  # get the ID to search
        if tempID == '-1':
            return tempID
        tempRes = 0  # temp result
        data = readFile('Database/doctorlist.txt')
    elif who == 'bill':
        tempID = str(input("Please enter billing ID: "))
        if tempID == '-1':
            return tempID
        tempRes = 0  # temp result
        data = readFile('Database/billing.txt')
    elif who == 'appointment':
        tempID = str(input("Please enter appointment ID: "))
        if tempID == '-1':
            return tempID
        tempRes = 0
        data = readFile('Database/recept_appointment.txt')
        tempRes = 0
    elif who == 'services':
        tempID = str(input("Please enter service ID: "))
        if tempID == '-1':
            return tempID
        tempRes = 0
        data = readFile('Database/services.txt')
        tempRes = 0
    for line in data:
        info = line.split(', ')
        if tempID.upper() == info[0].upper():  # check if the ID is matching (ID is always at index 0)
            tempRes = 1  # means the data has been found
            return tempID
    if tempRes == 0:
        print("No ID Found, Please Try Again <'-1' To Break>")
        return None

def getName(ID, who):
    if who == 'patient':
        File = open('Database/patientlist.txt', 'r')
        data = File.readlines()
        for line in data:
            info = line.split(', ')
            if ID.upper() == info[0].upper():  # check if the ID is matching (ID is always at index 0)
                tempRes = 1  # means the data has been found
                return info[1]
    if who == 'department':
        File = open('Database/departments.txt', 'r')
        data = File.readlines()
        for line in data:
            info = line.split(', ')
            if (ID.rstrip()).upper() == (info[0].rstrip()).upper():  # check if the ID is matching (ID is always at index 0)
                tempRes = 1  # means the data has been found
                return info[1]
    if who == 'doctorInDept':
        File = open('Database/doctorlist.txt', 'r')
        data = File.readlines()
        for line in data:
            info = line.split(', ')
            if (ID.rstrip()).upper() == (info[-1].rstrip()).upper():  # check if the ID is matching (ID is always at index 0)
                tempRes = 1  # means the data has been found
                print(info[1])
        return
    if who == 'doctor':
        File = open('Database/doctorlist.txt', 'r')
        data = File.readlines()
        for line in data:
            info = line.split(', ')
            if ID.upper() == info[0].upper():  # check if the ID is matching (ID is always at index 0)
                tempRes = 1  # means the data has been found
                return info[1]


def checkDate(dateYYYY, dateDD, dateMM):
    proper = 0
    if (dateMM > 12):
        proper = 0
    elif (dateYYYY % 4 == 0):
        if (dateMM == '02' and dateDD > 29):
            proper = 0
        elif (dateMM == '04' or dateMM == '06' or dateMM == '09' or dateMM == '11'):
            if dateDD > 30:
                proper = 0
        elif (dateDD > 31):
            proper = 0
        else:
            return True
    elif (dateYYYY % 4 != 0):
        if (dateMM == '02' and dateDD > 28):
            proper = 0
        elif (dateMM == '04' or dateMM == '06' or dateMM == '09' or dateMM == '11'):
            if dateDD > 30:
                proper = 0
        elif (dateDD > 31):
            proper = 0
        else:
            return True
    else:
        return True
    if proper == 0:
        print('Invalid Date was inserted')
        return False

def checkTime(timeHH, timeMM):
    proper = 0
    if (timeHH > 24):
        proper = 0
    elif (timeHH == 24 and timeMM > 0):
        proper = 0
    elif (timeMM > 60):
        proper = 0
    else:
        return True
    if proper == 0:
        print('Invalid Time was inserted')
        return False

def checkLength(fileName):
    with open(fileName,'r') as File:
        length = File.readlines()  # - to check amount of patient
    return len(length)


def inputID(person):
    tempID = None
    while tempID == None:
        tempID = checkID(person)  # get the ID to search whether it's an ID or not
    return tempID

def inputName():
    again = True
    while again == True:
        tempName = str(input("Patient Name: "))
        again = checkAlpha(tempName)
    return tempName

def inputNumber(pm):
    if pm == 'Age':
        tempAge = ''
        while tempAge.isnumeric() != True:
            tempAge = str(input("Patient Age <Num>: "))
            if tempAge.isnumeric() == False or len(tempAge) < 1 or tempAge == '0':
                print('Please input a valid age')
                tempAge = ''
        return tempAge

    if pm == 'Contact':
        tempContact = ''
        while tempContact.isnumeric() != True:  # checks if the inserted contact is only in numbers
            tempContact = str(input("Patient Contact Number (8-13 digits): "))
            if tempContact.isnumeric() == False or len(tempContact) <= 7 or len(tempContact) >=  12:
                print('Please input a valid contact number')
                tempContact = ''
        return tempContact

    if pm == 'Amount':
        amountOfService = None
        while amountOfService == None:
            try:
                amountOfService = int(input('Please enter amount of services the patient used <Number>: '))
                if (amountOfService <= 0):
                    amountOfService = None
                    print('Please enter a number larger than 0')
            except ValueError:
                print('Please enter a number')
                amountOfService = None
        return amountOfService

    if pm == 'Price':
        paid = None
        while paid == None:
            try:
                paid = int(input('How much do you want to pay? <Number>: '))
                if (paid <= 0):
                    paid = None
                    print('Please enter a number larger than 0')
            except ValueError:
                print('Please enter a number')
                paid = None
        return paid

def inputGender():
    tempGender = ''
    while tempGender.upper() != 'MALE' and tempGender.upper() != 'FEMALE':
        tempGender = str(input("Patient Gender <Male/Female>: "))
        if tempGender.upper() != 'MALE' and tempGender.upper() != 'FEMALE':
            print("Please enter your biological gender ('Male' or 'Female')")
    return tempGender

def inputText(pm):
    if pm == 'Address':
        again = True
        while again == True:  # checks if inserted address is only in letters
            tempAddress = str(input("Patient Address <City>: "))
            again = checkAlpha(tempAddress)
        return tempAddress
    elif pm == 'Issue':
        again = True
        while again == True:
            tempIssue = str(input("Appointment Details: "))
            again = checkAlpha(tempIssue)
        return tempIssue

def inputBlood():
    again = True
    while again == True:
        tempBlood = str(input("Patient Blood Type & Rh (+/-): "))
        bloodTypes = ['O+', 'O-', 'AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', ]
        for i in bloodTypes:    # Checks whether the input matches with any of the bloodtypes
            if tempBlood.upper() == i:
                again = False
                return tempBlood.upper()
        if again == True:
            print('Please enter a valid blood type')

def inputDate():
    getDate = False
    while getDate == False:
        try:
            dateYYYY, dateDD, dateMM = input("Insert Date <YYYY DD MM>: ").split()
            if (len(dateYYYY) == 4 and len(dateDD) == 2 and len(dateMM) == 2 and
                dateYYYY.isnumeric() == True and dateDD.isnumeric() == True and dateMM.isnumeric() == True):
                getDate = checkDate(int(dateYYYY), int(dateDD), int(dateMM))
        except:
            print('Inserted Data is not a proper date, please try again')
    tempDate = f"{dateYYYY}:{dateDD}:{dateMM}"      # Combines 3 input in the format specified
    return tempDate

def inputTime():
    getTime = False
    while getTime == False:
        try:
            timeHH, timeMM = input("Insert Time <HH MM>: ").split()
            if (len(timeHH) == 2 and len(timeMM) == 2 and
                    timeHH.isnumeric() == True and timeMM.isnumeric() == True):
                getTime = checkTime(int(timeHH), int(timeMM))
            else:
                print('Inserted time is not a proper time, please try again')
        except:
            print('Inserted time is not in the proper format, please try again')
    tempTime = f"{timeHH}:{timeMM}"
    return tempTime

def readFile(fileName):
    with open(fileName, 'r') as File:
        temp = File.readlines()
    return temp

def writeFile(fileName, newFile):
    with open(fileName, 'w') as File:
        File.writelines(newFile)
    return

def appendFile(fileName, newFile):
    with open(fileName, 'a') as File:
        fileInsert = ', '.join(newFile) + '\n'
        File.write(fileInsert)

#=========================================Data Managing==================================================
def receptInputNewData():      #To Input new Data
    print('\n' + '='*40)
    print('Inputting a New Patient Data')
    print('='*40)
    tempName = inputName()
    tempAge = inputNumber('Age')
    tempGender = inputGender()
    tempAddress = inputText('Address')
    tempContact = inputNumber('Contact')
    tempBlood = inputBlood()

    amountOfPatient = checkLength('Database/patientlist.txt')  # Get the amount of patients that are currently in patientlist.txt
    tempID = tempName[:3] + str(amountOfPatient + 1) #creation of ID
    print('Patient ID is = ' + tempID)
    try:
        newList = [tempID, tempName, tempAge, tempGender, tempAddress, tempContact, tempBlood]
        appendFile('Database/patientlist.txt', newList)
    except FileNotFoundError:   
        print("File is not found")

    #Update Existing Patient Data
def receptUpdateData():
    print('\n' + '='*30)
    print('Updating a patient data')
    print('='*30)
    tempID = inputID('patient')
    data = readFile('Database/patientlist.txt')
    dataIsFound = 0
    dataList = []
    for line in data:
        info = line.split(', ')
        if tempID.upper() == info[0].upper():
            dataIsFound = 1
            print(f"Patient Name: {info[1]}\nAge: {info[2]}\nGender: {info[3]}\n"
                  f"Address: {info[4]}\nContact: {info[5]}\nBlood Type: {info[6]}")
            print('Which information do you want to update?\n'
                  '1. Name\n'
                  '2. Age\n'
                  '3. Gender\n'
                  '4. Address\n'
                  '5. Contact Number\n'
                  '6. Blood Type')
            updatePrompt = None
            while updatePrompt == None:
                try:
                    updatePrompt = int(input('Select a number: '))
                    if (updatePrompt < 1 or updatePrompt > 6):
                        print("Please enter a valid choice")
                        updatePrompt = None
                except ValueError:
                    print('Please input a number')
            if updatePrompt == 1:
                newData = inputName()
            elif updatePrompt == 2:
                newData = inputNumber('Age')
            elif updatePrompt == 3:
                newData = inputGender()
            elif updatePrompt == 4:
                newData = inputText('Address')
            elif updatePrompt == 5:
                newData = inputNumber('Contact')
            elif updatePrompt == 6:
                newData = inputBlood()
            info[updatePrompt] = newData    # update the information based on which input selected
            tempData = ', '.join(info)       # Make all the data in the list as string
            line = tempData
            print('\nHere is your new data:')
            print(f"Patient Name: {info[1]}\nAge: {info[2]}\nGender: {info[3]}\n"
                  f"Address: {info[4]}\nContact: {info[5]}\nBlood Type: {info[6]}")
        dataList.append(line)
    writeFile('Database/patientlist.txt', dataList)
    if dataIsFound == 0:
        print("The ID you searched for doesn't exist")

#Function to view data of a specific patient
def receptViewData():
    print('\n' + '='*20)
    print('Viewing Data')
    print('='*20)
    tempID = inputID('patient')
    tempRes = 0 #temp result
    data = readFile('Database/patientlist.txt')
    for line in data:
        info = line.split(', ')
        if tempID.upper() == info[0].upper(): #check if the ID is matching (ID is always at index 0)
            tempRes = 1 # means the data has been found
            print(f"Patient Name: {info[1]}\nAge: {info[2]}\nGender: {info[3]}\n"
                  f"Address: {info[4]}\nContact: {info[5]}\nBlood Type: {info[6]}")
            return
    if tempRes == 0:
        print("The ID you searched for doesn't exist")

#Delete Existing Patient Data
def receptDeleteData():
    print('\n' + '='*30)
    print('Deleting Patient Data')
    print('='*30)
    tempID = inputID('patient')
    tempRes = 0     #temp result, returns whether the file is found or not
    data = readFile('Database/patientlist.txt')      # read all lines from patientFile as an array/list
    tempFile = []
    for line in data:
        info = line.split(',')
        if tempID.upper() == info[0].upper(): #check if the ID is matching (ID is always at index 0)
            tempRes = 1 # means the data has been found
            line = '[Data has been deleted], ' + info[0] + '\n'   # Changing the line into a new line
            print('The selected data has been deleted')
            print(line)
        tempFile.append(line)
    if tempRes == 1:
        writeFile('Database/patientlist.txt', tempFile)
    elif tempRes == 0:
        print("The ID you searched for doesn't exist")

#Main patient data managing Function
def receptManagePatientData():
    print('\n\n' + '='*50)
    print('Here are the available programs\n'
          '1. Register new patient\n'
		  '2. Update existing patient\n'
          '3. View existing patient\n'
		  '4. Delete existing patient\n'
          '0. Return'
          )
    try:
        prompt = int(input('Please type the number of what you want to do (in number): ')) #to get which one the user is using
        if prompt == 1:
            receptInputNewData()
        elif prompt == 2:
            receptUpdateData()
        elif prompt == 3:
            receptViewData()
        elif prompt == 4:
            receptDeleteData()
        elif prompt == 0:
            return
        else:
            print("That is not a valid function, please try again: ")
            receptManagePatientData()
        useAgain = str(input('Do you want to manage patient data again? <y/n> '))  # to use again
        if useAgain.upper() == 'Y':
            receptManagePatientData()
        else:
            print('Thank you for using patient data management service!!!\n\n')
            return
    except ValueError:
        print('Input Error, please try again')
        receptManagePatientData()

#Patient Data Managing completed at 12/1/2024 19:30 ~ Ekin

#=========================================APPOINTMENT SYSTEM====================================================
#Functions to manage doctor Appointments
#Main doctor appointment managing Function
def receptScheduleNewAppointment():      # To Input new Data
    print('\n' + '='*40)
    print('Scheduling a new appointment')
    print('='*40)
    tempDoctorID = inputID('doctor')
    if tempDoctorID == '-1':
        return
    tempPatientID = inputID('patient')
    if tempPatientID == '-1':
        return
    tempDate = inputDate()
    tempTime = inputTime()
    tempIssue = inputText('Issue')
    amountOfAppointment = checkLength('Database/recept_appointment.txt')  # Get the amount of appointments that are currently in the .txt
    tempID = 'A' + str(amountOfAppointment + 1) #creation of ID
    print('Appointment ID is = ' + tempID)
    try:
        newFile = [tempID, tempDoctorID, tempPatientID, tempDate, tempTime, tempIssue]
        appendFile('Database/recept_appointment.txt', newFile)
    except FileNotFoundError:
        print("File is not found")

#Function to view data of appointments from a doctor
def receptViewAppointments():
    print('\n' + '='*20)
    print('Viewing Appointments')
    print('='*20)
    tempID = inputID('appointment')
    tempRes = 0 #temp result
    data = readFile('Database/recept_appointment.txt')      # read all lines from appointmentFile as a list of arrays
    for line in data:
        info = line.split(', ')
        if tempID.upper() == info[0].upper(): #check if the appointment ID is matching (ID is at index 0)
            tempRes = 1 # means at least a data has been found
            doctor = getName(info[1], 'doctor')
            patient = getName(info[2], 'patient')
            print("Here is the appointment details:")
            print(f"Patient Name: {patient}\nDoctor Name: {doctor}\nAppointment Date: {info[3]}\n"
                  f"Appointment Time: {info[4]}\nIssue: {info[5]}")
            # this only prints if the ID is suitable, and is going to print all lines with the specific doctor
    if  tempRes == 0:
        print("No appointment exist for the specified doctor")

def receptDeleteAppointment():
    print('\n' + '='*20)
    print('Deleting Appointments')
    print('='*20)
    tempID = inputID('appointment')
    tempRes = 0     #temp result, returns whether the file is found or not
    data = readFile('Database/recept_appointment.txt')      # read all lines from patientFile as a list of arrays
    tempFile = []
    for line in data:
        info = line.split(',')
        if tempID.upper() == info[0].upper(): #check if the ID is matching (ID is always at index 0)
            tempRes = 1 # means the data has been found
            line = '[Appointment has been deleted], ' + info[0] + '\n'   # Changing the line into a new line
            print('The selected data has been deleted')
            print(line)
        tempFile.append(line)
    if tempRes == 1:
        writeFile('Database/recept_appointment.txt', tempFile)
    elif tempRes == 0:
        print("The ID you searched for doesn't exist")

#Main Doctor Appointment scheduling Function
def receptDoctorAppointment():
    print('\n' + '='*40)
    print('Here are the available programs\n'
          '1. Add new Appointments\n'
          '2. View Appointments\n'
          '3. Delete existing Appointment\n'
          '0. Return\n')
    try:
        prompt = int(input('Please type the number of what you want to do (in number): '))  # to get which one the user is using
        if prompt == 1:
            receptScheduleNewAppointment()
        elif prompt == 2:
            receptViewAppointments()
        elif prompt == 3:
            receptDeleteAppointment()
        elif prompt == 0:
            return
        else:
            print("That is not a valid function, please try again: ")
            receptDoctorAppointment()
        useAgain = str(input('Do you want to manage doctor appointments again? <y/n> '))  # to use again
        if useAgain.upper() == 'Y':
            receptDoctorAppointment()
        else:
            print('Thank you for using doctor appointment scheduling service!!!\n\n')
    except ValueError:
        print('Input Error, please try again')
        receptDoctorAppointment()

#Doctor Appointment function Completed at 12/1/24 22:43 ~ Ekin

#==========================================SHOW SERVICES SYSTEM=================================================
#Functions to manage available services
#Function to show the available services of the Hospital with it's details
def receptShowServices():
    print('\n' + '='*50)
    print('Available Services in the Hospital')
    print('='*50)
    servicesFile = readFile('Database/services.txt')
    for lines in servicesFile:
        info = lines.split(', ')
        print(f"{info[0]}. {info[1]}, Price: {info[-1].rstrip()}")

def receptShowDoctors():
    print('\n' + '='*30)
    print('Doctors in the Hospital')
    print('='*30)
    doctorFile = readFile('Database/doctorlist.txt')
    for lines in doctorFile:
        info = lines.split(', ')
        department = getName(info[-1],'department')
        print(f"Doctor Name: {info[1]}, Department: {department}")

def receptShowDepartments():
    print('\n' + '='*30)
    print('Departments in the Hospital')
    print('='*30)
    departmentFile = readFile('Database/departments.txt')
    for lines in departmentFile:
        info = lines.split(', ')
        print(f"Department Name: {info[1]}, Doctor Names:")
        getName(info[0], 'doctorInDept')


#Main available services Function
def receptAvailableServices():
    print('\n' + '='*50)
    print('Here are the available services:\n'
          '1. View Available Hospital Services\n'
          '2. View Doctors of the Hospital\n'
          '3. View Departments of the Hospital\n'
          '0. Return')
    try:
        prompt = int(input('Please type the number of what you want to do (in number): '))  # to get which one the user is using
        if prompt == 1:
            receptShowServices()
        elif prompt == 2:
            receptShowDoctors()
        elif prompt == 3:
            receptShowDepartments()
        elif prompt == 0:
            return
        else:
            print("That is not a valid function, please try again: ")
            receptAvailableServices()
        useAgain = str(input('Do you want to manage view again? <y/n> '))  # to use again
        if useAgain.upper() == 'Y':
            receptAvailableServices()
        else:
            print('Thank you for using doctor appointment scheduling service!!!\n\n')
    except:
        print('Invalid Input, Please Try Again')
        receptAvailableServices()

#Available Services Function Completed at 12/1/24 22:58  ~ Ekin

#============================================CHECK IN SYSTEM=====================================================
#Functions to Check In & Check Out
def receptViewPatientStatus():
    print('\n' + '='*50)
    print('Viewing Patient Check In Status')
    print('='*50)
    tempID = inputID('patient')
    if tempID == '-1':
        return
    data = readFile('Database/recept_checkInOut.txt')
    dataFound = 0
    status = 0
    for lines in data:
        info = lines.split(', ')
        if tempID.upper() == info[0].upper():
            dataFound = 1
            if info[1] == "Checked In":
                status = 1
                print("Patient is currently Checked In")
                print(f"Check In Date: {info[2]}\nCheck In Time: {info[3]}")
        else:
            continue
    if dataFound == 1 and status == 0:
        print("Patient is currently Checked Out")
    elif dataFound == 0:
        print ("Patient has never checked in")


def receptViewPatientHistory():
    print('\n' + '='*50)
    print('Viewing Patient Check In History')
    print('='*50)
    tempID = inputID('patient')
    if tempID == '-1':
        return
    data = readFile('Database/recept_checkInOut.txt')
    dataFound = 0
    for lines in data:
        info = lines.split(', ')
        if tempID.upper() == info[0].upper():       # Checks whether searched ID = ID in info
            dataFound = 1
            print(lines)
        else:
            continue
    if dataFound == 0:
        print("Patient has no check in history")

def receptCheckIn():
    print('\n' + '='*30)
    print('Checking In A Patient')
    print('='*30)
    tempID = inputID('patient')
    if tempID == '-1':
        return
    data =  readFile("Database/recept_checkInOut.txt")
    for lines in data:
        info = lines.split(', ')
        if tempID.upper() == info[0].upper():
            dataFound = 1
            if info[1] == "Checked In":
                status = 1
                print("Patient is currently Checked In\n")
                return
    print('Please enter check in timing details:')
    tempInDate = inputDate()
    tempInTime = inputTime()
    try:
        newList = [tempID, 'Checked In', tempInDate, tempInTime, "[Hasn't Checked Out]", "[Hasn't Checked Out]"]
        print("Patient Checked In\n")
        appendFile('Database/recept_checkInOut.txt', newList)
    except FileNotFoundError:
            print("File is not found")


def receptCheckOut():
    print('\n' + '='*30)
    print('Checking Out A Patient')
    print('='*30)
    tempID = inputID('patient')
    if tempID == '-1':
        return
    data =  readFile("Database/recept_checkInOut.txt")
    for lines in data:
        info = lines.split(', ')
        if tempID.upper() == info[0].upper():
            if info[1] == "Checked In":
                dataFound = 1
                print('Please enter check out timing details')
                tempOutDate = inputDate()
                tempOutTime = inputTime()
                tempList = []
                info[1] = "Checked Out"
                info[-2] = tempOutDate
                info[-1] = tempOutTime + '\n'
                line = ', '.join(info)       # Changing the line into a new line
                print('Patient Checked Out!\n')
                print(line)
                tempList.append(line)
                writeFile('Database/recept_checkInOut.txt', tempList)
                return
    print("This person doesn't have any unchecked out session")


#Main Check In & Check Out Function
def receptCheckInOut():
    print('\n' + '='*50)
    print('Here are the available programs:\n'
          '1. View Patient Status\n'
          '2. View Patient History\n'
          '3. Check In\n'
          '4. Check Out\n'
          '0. Return'
          )
    try:
        prompt = int(input('Please type the number of what you want to do (in number): '))  # to get which one the user is using
        if prompt == 1:
            receptViewPatientStatus()
        elif prompt == 2:
            receptViewPatientHistory()
        elif prompt == 3:
            receptCheckIn()
        elif prompt == 4:
            receptCheckOut()
        elif prompt == 0:
            return
        else:
            print("That is not a valid function, please try again: ")
            receptCheckInOut()
        useAgain = str(input('Do you want to manage patient check in & out again? <y/n> '))  # to use again
        if useAgain.upper() == 'Y':
            receptCheckInOut()
        else:
            print('Thank you for using patient check in & out service!!!\n\n')
    except:
        print('Invalid input, please try again')
        receptCheckInOut()
    return
#Check in & Check out system program finished 12/03/2024 10:15 ~ Ekin


#===========================================BILLING SYSTEM======================================================
#Functions to manage patient billing

def receptAddBill():
    print('\n' + '='*20)
    print('Creating A Bill')
    print('='*20)
    patientID = inputID('patient')
    if patientID == '-1':
        return
    amountOfService = inputNumber('Amount')
    serviceID = []
    totalPrice = 0
    for i in range(1,amountOfService+1):
        tempInput = ''
        while tempInput.isnumeric() != True:
            try:
                tempInput = inputID('services')
                services = readFile('Database/services.txt')
                #Counts total price while inputting the values
                for availServices in services:  # Find the used service ID inside the services
                    details = availServices.split(', ')
                    if tempInput == details[0]:
                        totalPrice += int(details[2])
            except ValueError:
                print('Please enter a number')
                tempInput = ''
        data = readFile('Database/services.txt')
        for lines in data:
            info = lines.split(', ')
            if tempInput == info[0]:
                print(str(i) + '. ' + info[1])
                serviceID.append(info[0])
    lines = readFile('Database/billing.txt')
    billNumber = len(lines)
    tempID = 'B' + str(billNumber + 1)  # creation of ID
    print('Bill ID is = ' + tempID)
    try:
        line = ', '.join(serviceID)
        newList = [tempID, patientID, line, str(totalPrice)]
        print('Total Price:', totalPrice, 'RM')
        paymentStatus = ''
        payPrompt = ''
        while payPrompt == '':
            payPrompt = str(input('Do you want to pay now? <y/n>: '))
            if payPrompt.upper() == 'Y':
                paidAmt = str(inputNumber('Price'))
                if int(paidAmt) == totalPrice:
                    newList.append(paidAmt)
                    newList.append('Paid')
                    print('The bill has been paid')
                elif int(paidAmt) > totalPrice:
                    newList.append(str(totalPrice))
                    newList.append('Paid')
                    change = int(paidAmt) - totalPrice
                    paidAmt = str(totalPrice)
                    print('You have paid ' + str(change) + 'RM too much\n')
                elif int(paidAmt) < totalPrice:
                    newList.append(paidAmt)
                    newList.append('Not Paid')
                    lacking = totalPrice - int(paidAmt)
                    print('You still need to pay ' + str(lacking) + 'RM\n')
                appendFile('Database/billing.txt', newList)
            elif (payPrompt.upper() == 'N'):
                newList.append('0')
                newList.append('Not Paid')
                appendFile('Database/billing.txt', newList)
            else:
                payPrompt = ''
                print("Please enter 'y' or 'n'")
        print('You have successfully created a bill for ' + patientID)
        print('Here are the services used: ' + line)
        print('Total Price:', totalPrice, 'RM')
        print('You have paid: ' + paidAmt + 'RM')
    except FileNotFoundError:
        print("File is not found")

def receptPayBill():
    print('\n' + '='*20)
    print('Paying Bill')
    print('='*20)
    tempID = inputID('bill')
    if tempID == '-1':
        return
    data = readFile('Database/billing.txt')
    totalPrice = 0
    tempList = []
    for lines in data:
        info = lines.split(', ')
        if tempID.upper() == info[0].upper():       # Checks if the inserted ID is equals to the Bill ID searched
            if info[-1].rstrip() == 'Not Paid':      # Checks if the bill has been paid
                tempName = getName(info[1],'patient')         #finds the name of the patient ID from the bill
                print(tempName + ', you have used these services:')
                for usedDetails in info:    #repeats as much time as there are data
                    services = readFile('Database/services.txt')
                    for availServices in services:  # Find the used service ID inside the services
                        details = availServices.split(', ')
                        if usedDetails == details[0]:
                            print(details[1] + ", Price: " + details[2].rstrip() + ' RM')  # Prints out the name of services, price
                            totalPrice += int(details[2])
                print('Total Price:', totalPrice, 'RM')
                print('You have paid:', info[-2], 'RM')
                lacking = int(info[-3]) - int(info[-2])
                print('You still need to pay ' + str(lacking) + 'RM')
                paymentStatus = ''
                while paymentStatus == '':
                    paymentStatus = str(input('Do you want to update payment status? <y/n> '))
                    if paymentStatus.upper() == 'Y':
                        paidAmt = str(inputNumber('Price'))
                        if int(paidAmt) + int(info[-2]) == int(info[-3]):
                            tmp = int(info[-2]) + int(paidAmt)
                            info[-2] = str(tmp)
                            info[-1] = 'Paid'
                            print('The bill has been paid')
                        elif int(paidAmt) + int(info[-2]) > int(info[-3]):
                            change = (int(paidAmt) + int(info[-2])) - int(info[-3])
                            info[-2] = str(info[-3])
                            info[-1] = 'Paid'
                            print('You have paid ' + str(change) + 'RM too much\n')
                        elif int(paidAmt) + int(info[-2]) < int(info[-3]):
                            tmp = int(info[-2]) + int(paidAmt)
                            info[-2] = str(tmp)
                            lacking = int(info[-3]) - int(info[-2])
                            print('You still need to pay ' + str(lacking) + 'RM\n')
                        print('Your payment status has been updated!')
                        lines = ', '.join(info) + '\n'       # updates the data

                    elif paymentStatus.upper() == 'N':
                        print('Alright, you may proceed\n')
                    else:
                        paymentStatus = ''
                        print("Please enter 'Y' or 'N'\n")
            else:
                print('This bill has been paid')
        tempList.append(lines)
    writeFile('Database/billing.txt', tempList)

def receptViewBill():
    print('\n' + '='*20)
    print('Viewing Bill')
    print('='*20)
    totalBill = 0
    tempID = inputID('bill')
    if tempID == '-1':
        return
    data = readFile('Database/billing.txt')
    dataFound = 0
    for lines in data:
        info = lines.split(', ')
        if tempID.upper() == info[0].upper():       # Checks if the inserted ID is equals to the ID
            dataFound = 1
            tempName = getName(info[1],'patient')
            print('\n' + tempName + ', Here is your Billing Details:')
            print('Total Bill: ' + info[-3] + ' RM')
            print('You have paid: ' + info[-2] + 'RM')
            print('Status: ' + info[-1])
    if dataFound == 0:
        print("The searched ID haven't used any services")

def receptUsedServices():
    print('\n' + '='*30)
    print('Services Used By Patient')
    print('='*30)
    tempID = inputID('patient')
    if tempID == '-1':
        return
    data = readFile('Database/billing.txt')
    dataFound = 0
    for lines in data:
        info = lines.split(', ')
        if tempID.upper() == info[1].upper():       # Checks all services that a patient has ever used
            dataFound = 1
            tempName = getName(tempID,'patient')
            print('Bill ID: ' + info[0] + ', have used these services:')
            for usedDetails in info[2:-3]:    #repeats as much time as there are data
                services = readFile('Database/services.txt')
                for availServices in services:  # Find the used service ID inside the services
                    details = availServices.split(', ')
                    if usedDetails == details[0]:
                        print(details[1])  # Prints out the name of services, price
            print('Status: ' + info[-1])
    if dataFound == 0:
        print("The searched ID haven't used any services")


#Main Billing Management Function
def receptPatientBilling():
    print('\n' + '='*50)
    print('Here are the available programs:\n'
            '1. Create a Bill\n'
            '2. Pay Bills \n'
            '3. View Bill Details\n'
            '4. View Patient Used Services\n'
            '0. Return')
    try:
        prompt = int(input('Please type the number of what you want to do (in number): '))  # to get which one the user is using
        if prompt == 1:
            receptAddBill()
        elif prompt == 2:
            receptPayBill()
        elif prompt == 3:
            receptViewBill()
        elif prompt == 4:
            receptUsedServices()
        elif prompt == 0:
            return
        else:
            print("That is not a valid function, please try again: ")
            receptPatientBilling()
        useAgain = str(input('Do you want to manage billing system again? <y/n> '))  # to use again
        if useAgain.upper() == 'Y':
            receptPatientBilling()
        else:
            print('Thank you for using the billing management service!!!\n\n')
    except ValueError:
        print("Invalid input, please try again")
        receptPatientBilling()

#Billing system program finished 12/12/2024 13:28 ~ Ekin

#=============================================MAIN SYSTEMS=======================================================
def receptMainFunction():
    print('\n' + '='*50)
    print ('Welcome Receptionist! Select between this services:\n'
           '1. Registering new patients and update existing patient information\n'
           '2. Schedule and manage appointments for doctors\n'
           '3. Provide patients with information on hospital services, doctors, and departments\n'
           '4. Handle patient check-in and check-out processes\n'
           '5. Generate billing details based on services used by the patient\n'
           '0. Log Out')
    try:
        selectedService = str(input('Enter the service you want to select (in numbers): '))
            #ifs to go to the function based on selected services
        if selectedService == '1':
            receptManagePatientData()
        elif selectedService == '2':
            receptDoctorAppointment()
        elif selectedService == '3':
            receptAvailableServices()
        elif selectedService == '4':
           receptCheckInOut()
        elif selectedService == '5':
            receptPatientBilling()
        elif selectedService == '0':
            return False
        else:
            print('Invalid input, please try again\n\n\n' )     # if input isn't in the choice, reruns the function
            receptMainFunction()
            return False
    except ValueError:
        print('Input Error, please try again')
        receptMainFunction()
    return True


def receptionistLogin():
    idCreds = input('Username: ')
    if idCreds == '-1':
        return False
    else:
        idFound = False
        pwCreds = input('Password: ')
        receptionistAccountFile = 'Database/receptAccounts.txt'
        with open(receptionistAccountFile) as File:
            for lines in File:
                info = lines.split(',')
                if idCreds == info[0].rstrip():
                    idFound = True
                    if pwCreds == info[1].rstrip():
                        continueProgram = True
                        while continueProgram == True:  # use this instead of asking to use again everytime
                            continueProgram = receptMainFunction()  # main function returns false ONLY WHEN 0/Break is inserted
                        return False
            if idFound == False:
                print('Invalid username, please try again')
                receptionistLogin()
            else:
                print('Invalid password, please try again')
                receptionistLogin()
    return False

#MAIN RECEPTIONIST
def ReceptionistProgram():
    print('\n' + '='*50)
    print('Please login as a Receptionist! <-1 to return>')
    login = True
    while login == True:
        login = receptionistLogin()
    print('\n\nThanks for using the receptionist services\n')



#==============================================================================================================
#===========================================PATIENT Functions==================================================
#==========================================Islomjon Oripjonov==================================================
#===============================================TP076526=======================================================
#==============================================================================================================
# File names
PATIENTS_RECORDS_FILE = 'Database/patient_records.txt'
APPOINTMENTS_FILE = 'Database/patient_appointments.txt'
BILLING_DETAILS_FILE = 'Database/billing.txt'
DOCTORS_FILE = 'Database/doctorlist.txt'

# Patient menu function
def patient_menu():
    print("\nWelcome, dear patient!")
    while True:
        print("\n--- Patient Menu ---")
        print("1. View Medical Records")
        print("2. Manage Appointments")
        print("3. Update Personal Information")
        print("4. View Billing Details")
        print("5. View Doctors")
        print("6. Request Specific Services")
        print("7. Log Out")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_medical_records()
        elif choice == "2":
            manage_appointments()
        elif choice == "3":
            update_personal_information()
        elif choice == "4":
            view_billing_details()
        elif choice == "5":
            view_doctors()
        elif choice == "6":
            request_services()
        elif choice == "7":
            if logout_confirmation():
                break
        else:
            print("Invalid choice. Please try again.")


# Function to view medical records
def view_medical_records():
    print("\n--- Medical Records ---")
    patient_id = input("Enter your Patient ID: ").strip()
    try:
        with open(PATIENTS_RECORDS_FILE, 'r') as file:
            found = False
            for line in file:
                fields = line.strip().split(',')
                if fields[0] == patient_id:
                    print(f"Diagnosis: {fields[5]}")
                    print(f"Prescription: {fields[6]}")
                    found = True
                    break
            if not found:
                print("No medical records found for the given Patient ID.")
    except FileNotFoundError:
        print("Error: Medical records file not found.")
    input("Press Enter to go back to the menu...")


# Function for managing appointments
def manage_appointments():
    print("\n--- Manage Appointments ---")
    patient_id = input("Enter your Patient ID: ").strip()
    try:
        with open(APPOINTMENTS_FILE, 'r') as file:
            appointments = [line.strip() for line in file if line.startswith(patient_id)]

        if appointments:
            print("Your Appointments:")
            for appt in appointments:
                print(appt)
        else:
            print("No appointments found.")
            schedule_new = input("Do you want to schedule a new appointment? (yes/no): ").strip().lower()
            if schedule_new == "yes":
                schedule_appointment(patient_id)
    except FileNotFoundError:
        print("Error: Appointments file not found.")
    input("Press Enter to go back to the menu...")

# Function to schedule a new appointment
def schedule_appointment(patient_id):
    try:
        date = input("Enter the appointment date (YYYY-MM-DD): ").strip()
        time = input("Enter the appointment time (HH:MM): ").strip()
        doctor = input("Enter the doctor you want to schedule with: ").strip()
        with open(APPOINTMENTS_FILE, 'a') as file:
            file.write(f"{patient_id},{date},{time},{doctor}\n")
        print("Appointment scheduled successfully!")
    except Exception as e:
        print(f"Error: Unable to schedule appointment. ({e})")


# Function to update personal information
def update_personal_information():
    print("\n--- Update Personal Information ---")
    patient_id = input("Enter your Patient ID: ").strip()
    try:
        with open(PATIENTS_RECORDS_FILE, 'r') as file:
            records = file.readlines()

        updated_records = []
        found = False
        for record in records:
            fields = record.strip().split(',')
            if fields[0] == patient_id:
                found = True
                print(f"Current Information: {record.strip()}")
                new_address = input("Enter new address (leave blank to keep current): ").strip() or fields[2]
                new_contact = input("Enter new contact number (leave blank to keep current): ").strip() or fields[3]
                new_insurance = input("Enter new insurance details (leave blank to keep current): ").strip() or fields[
                    4]
                updated_records.append(f"{fields[0]},{fields[1]},{new_address},{new_contact},{new_insurance}\n")
                print("Information updated successfully!")
            else:
                updated_records.append(record)

        if not found:
            print("Patient ID not found.")
        else:
            with open(PATIENTS_RECORDS_FILE, 'w') as file:
                file.writelines(updated_records)

    except FileNotFoundError:
        print("Error: Patient records file not found.")
    input("Press Enter to go back to the menu...")


# Function to view billing details
def view_billing_details():
    print("\n--- Billing Details ---")
    patient_id = input("Enter your Patient ID: ").strip()
    try:
        with open(BILLING_DETAILS_FILE, 'r') as file:
            found = False
            for line in file:
                fields = line.strip().split(', ')
                if fields[1] == patient_id:
                    outstanding = int(fields[-3]) - int(fields[-2])
                    print(f"Bill ID: {fields[0]}")
                    print(f"Total Bill: {fields[-3]}")
                    print(f"Balance Paid: {fields[-2]}")
                    print(f"Outstanding Balance: {outstanding}\n")
                    found = True
            if not found:
                print("No billing details found for the given Patient ID.")
    except FileNotFoundError:
        print("Error: Billing details file not found.")
    input("Press Enter to go back to the menu...")


# Function to view doctors
def view_doctors():
    print("\n--- Doctors List ---")
    try:
        with open(DOCTORS_FILE, 'r') as file:
            doctors = file.readlines()
            if not doctors:
                print("No doctors found.")
            else:
                print("Available Doctors:")
                for doctor in doctors:
                    print(doctor.strip())
    except FileNotFoundError:
        print("Error: Doctors file not found.")
    input("Press Enter to go back to the menu...")


# Function to request specific services
def request_services():
    print("\n--- Request Specific Services ---")
    print("1. Request a Follow-Up Appointment")
    print("2. Request a Specific Doctor")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        def request_follow_up():
            print("Follow-up appointment requested.")

        request_follow_up()
    elif choice == "2":
        def request_specific_doctor():
            doctor_name = input("Enter the name of the doctor you want to request: ").strip()
            print(f"Request for Dr. {doctor_name} has been submitted.")

        request_specific_doctor()
    else:
        print("Invalid choice. Returning to the menu...")


# Function to log out with confirmation
def logout_confirmation():
    confirm = input("Are you sure you want to log out? (yes/no): ").strip().lower()
    return confirm == "yes"


def patient_main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Login as a Patient")
        print("2. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            username = input('Username: ')
            userFound = False
            password = input('Password: ')
            if username == '-1' or password == '-1':
                return False
            patientAccount = 'Database/patient.account.txt'
            with open(patientAccount) as File:
                for lines in File:
                    info = lines.split(',')
                    if username == info[0].rstrip() and password == info[1].rstrip():
                        continueP = True
                        while continueP == True:  # use this instead of asking to use again everytime
                            continueP = patient_menu()  # main function returns false ONLY WHEN 0/Break is inserted
                        return False
                if not userFound:
                    print('Invalid username')
                    patient_main_menu()
                else:
                    print('Invalid password, please try again')
                    patient_main_menu()
        elif choice == "2":
            print("Goodbye, dear patient!")
            break
        else:
            print("Invalid choice. Please try again.")


#==============================================================================================================
#==============================================================================================================
#============================================GLOBAL FUNCTIONS==================================================
#==============================================================================================================
#==============================================================================================================


#MAIN
def loginMenu():
    print('='*50)
    print('Welcome to the hospital user management! <-1 to Stop>')
    print('Choose your role:\n'
          '1. Admin\n'
          '2. Doctor\n'
          '3. Nurse\n'
          '4. Receptionist\n'
          '5. Patient\n'
          '0. Stop Program')
    try:
        enterMenu = str(input('Please enter a number: '))
        # ifs to go to the programs based on selected services
        if enterMenu == '1':
            if validate_login():
                administrator_menu()
        elif enterMenu == '2':
            login_doctor()
        elif enterMenu == '3':
            nurse_login()
        elif enterMenu == '4':
            ReceptionistProgram()
        elif enterMenu == '5':
            patient_main_menu()
        elif enterMenu == '0' or enterMenu == '-1':
            return False
        else:
            print('Invalid input, please try again\n\n\n')  # if input isn't in the choice, reruns the function
            loginMenu()
            return False
    except ValueError:
        print('Input Error, please try again')
        loginMenu()
    return True

#start of program
mainProgram = True
while mainProgram == True:  # use this instead of asking to use again everytime
    mainProgram = loginMenu()  # main function returns false ONLY WHEN 0/Break is inserted
print('Thank you for using the Hospital Program')