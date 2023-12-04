import mysql.connector
from tkinter import Tk, Label, Entry, Button, messagebox, Listbox, Scrollbar, END, Toplevel, simpledialog

class PatientRecordManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Record Management")

        # Set the initial size of the window
        self.root.geometry("800x600")

        # Initialize the database
        self.init_db()

        # GUI components
        Label(root, text="Name:").grid(row=0, column=0)
        Label(root, text="Age:").grid(row=1, column=0)
        Label(root, text="Gender:").grid(row=2, column=0)
        Label(root, text="Diagnosis:").grid(row=3, column=0)
        Label(root, text="Phone:").grid(row=4, column=0)
        Label(root, text="Aadhar:").grid(row=5, column=0)

        self.name_entry = Entry(root)
        self.age_entry = Entry(root)
        self.gender_entry = Entry(root)
        self.diagnosis_entry = Entry(root)
        self.phone_entry = Entry(root)
        self.aadhar_entry = Entry(root)

        self.name_entry.grid(row=0, column=1)
        self.age_entry.grid(row=1, column=1)
        self.gender_entry.grid(row=2, column=1)
        self.diagnosis_entry.grid(row=3, column=1)
        self.phone_entry.grid(row=4, column=1)
        self.aadhar_entry.grid(row=5, column=1)

        # Buttons
        Button(root, text="Add Record", command=self.add_record).grid(row=6, column=0, columnspan=2)
        Button(root, text="Fetch Records", command=self.fetch_records).grid(row=7, column=0, columnspan=2)
        Button(root, text="Update Record", command=self.update_record).grid(row=8, column=0, columnspan=2)
        Button(root, text="Fetch by Aadhar", command=self.fetch_patient_by_aadhar).grid(row=9, column=0, columnspan=2)

        # Listbox for displaying patient records
        self.records_listbox = Listbox(root, height=10, width=50)
        self.records_listbox.grid(row=10, column=0, columnspan=2)
        scrollbar = Scrollbar(root, orient="vertical", command=self.records_listbox.yview)
        scrollbar.grid(row=10, column=2, sticky="ns")
        self.records_listbox.config(yscrollcommand=scrollbar.set)

    def init_db(self):
        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Manish123',
                database='patient_record'
            )

            cursor = connection.cursor()

            # Create the patients table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    age INT NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    diagnosis VARCHAR(255) NOT NULL,
                    phone VARCHAR(15),
                    aadhar VARCHAR(20) UNIQUE
                )
            ''')

            # Commit changes and close the connection
            connection.commit()
            connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error initializing database: {e}")
            self.root.destroy()

    def add_record(self):
        try:
            # Extract data from GUI components
            name = self.name_entry.get()
            age = self.age_entry.get()
            gender = self.gender_entry.get()
            diagnosis = self.diagnosis_entry.get()
            phone = self.phone_entry.get()
            aadhar = self.aadhar_entry.get()

            # Data validation
            if not all([name, age, gender, diagnosis, aadhar]):
                messagebox.showwarning("Warning", "Please fill in all required fields.")
                return

            if len(phone) < 10:
                messagebox.showwarning("Warning", "Invalid phone number. It should be at least 10 digits.")
                return

            if len(aadhar) < 12:
                messagebox.showwarning("Warning", "Invalid Aadhar number. It should be at least 12 digits.")
                return

            # Connect to the database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Manish123',
                database='patient_record'
            )

            cursor = connection.cursor()

            # Check if the Aadhar number already exists
            cursor.execute('SELECT * FROM patients WHERE aadhar = %s', (aadhar,))
            existing_patient = cursor.fetchone()

            if existing_patient:
                messagebox.showwarning("Warning", "Patient with the same Aadhar number already exists.")
                connection.close()
                return

            # Insert new patient record
            cursor.execute('''
                INSERT INTO patients (name, age, gender, diagnosis, phone, aadhar)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (name, age, gender, diagnosis, phone, aadhar))

            # Commit changes and close the connection
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Patient record added successfully.")
            self.clear_entries()
            self.fetch_records()

        except Exception as e:
            messagebox.showerror("Error", f"Error adding patient record: {e}")

    def update_record(self):
        # Get the selected record from the listbox
        selected_index = self.records_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a record to update.")
            return

        selected_index = int(selected_index[0])

        # Extract the patient ID from the selected record
        selected_record = self.records_listbox.get(selected_index)
        patient_id = selected_record.split()[0]

        # Open a new window for updating the record
        update_window = Toplevel(self.root)
        update_window.title("Update Patient Record")

        # Fetch the existing record from the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Manish123',
            database='patient_record'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        existing_record = cursor.fetchone()
        connection.close()

        # Populate the entry fields in the update window with existing data
        Label(update_window, text="Name:").grid(row=0, column=0)
        Label(update_window, text="Age:").grid(row=1, column=0)
        Label(update_window, text="Gender:").grid(row=2, column=0)
        Label(update_window, text="Diagnosis:").grid(row=3, column=0)
        Label(update_window, text="Phone:").grid(row=4, column=0)
        Label(update_window, text="Aadhar:").grid(row=5, column=0)

        name_entry = Entry(update_window)
        age_entry = Entry(update_window)
        gender_entry = Entry(update_window)
        diagnosis_entry = Entry(update_window)
        phone_entry = Entry(update_window)
        aadhar_entry = Entry(update_window)

        name_entry.grid(row=0, column=1)
        age_entry.grid(row=1, column=1)
        gender_entry.grid(row=2, column=1)
        diagnosis_entry.grid(row=3, column=1)
        phone_entry.grid(row=4, column=1)
        aadhar_entry.grid(row=5, column=1)

        name_entry.insert(END, existing_record['name'])
        age_entry.insert(END, existing_record['age'])
        gender_entry.insert(END, existing_record['gender'])
        diagnosis_entry.insert(END, existing_record['diagnosis'])
        phone_entry.insert(END, existing_record['phone'])
        aadhar_entry.insert(END, existing_record['aadhar'])

        # Function to update the record in the database
        def perform_update():
            try:
                # Extract updated data from entry fields
                updated_name = name_entry.get()
                updated_age = age_entry.get()
                updated_gender = gender_entry.get()
                updated_diagnosis = diagnosis_entry.get()
                updated_phone = phone_entry.get()
                updated_aadhar = aadhar_entry.get()

                # Data validation
                if not all([updated_name, updated_age, updated_gender, updated_diagnosis, updated_aadhar]):
                    messagebox.showwarning("Warning", "Please fill in all required fields.")
                    return

                # Connect to the database
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='Manish123',
                    database='patient_record'
                )

                cursor = connection.cursor()

                # Check if the updated Aadhar number already exists
                cursor.execute('SELECT * FROM patients WHERE aadhar = %s AND id != %s', (updated_aadhar, patient_id))
                existing_patient = cursor.fetchone()

                if existing_patient:
                    messagebox.showwarning("Warning", "Patient with the updated Aadhar number already exists.")
                    connection.close()
                    return

                # Update the record in the database
                cursor.execute('''
                    UPDATE patients
                    SET name = %s, age = %s, gender = %s, diagnosis = %s, phone = %s, aadhar = %s
                    WHERE id = %s
                ''', (updated_name, updated_age, updated_gender, updated_diagnosis, updated_phone, updated_aadhar, patient_id))

                # Commit changes and close the connection
                connection.commit()
                connection.close()

                messagebox.showinfo("Success", "Patient record updated successfully.")
                update_window.destroy()
                self.fetch_records()

            except Exception as e:
                messagebox.showerror("Error", f"Error updating patient record: {e}")

        # Button to perform the update
        Button(update_window, text="Update Record", command=perform_update).grid(row=6, column=0, columnspan=2)

    def fetch_records(self):
        try:
            # Connect to the database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Manish123',
                database='patient_record'
            )

            cursor = connection.cursor()

            # Fetch all patient records
            cursor.execute('SELECT * FROM patients')
            records = cursor.fetchall()

            # Close the connection
            connection.close()

            # Clear the existing items in the listbox
            self.records_listbox.delete(0, END)

            # Display records in the listbox
            for record in records:
                record_str = f"{record[0]} - {record[1]} - {record[2]} - {record[3]} - {record[4]} - {record[5]} - {record[6]}"
                self.records_listbox.insert(END, record_str)

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching patient records: {e}")

    def fetch_patient_by_aadhar(self):
        try:
            # Get Aadhar number from user input
            aadhar_to_fetch = simpledialog.askstring("Fetch Patient by Aadhar", "Enter Aadhar number:")
            if not aadhar_to_fetch:
                return

            # Connect to the database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Manish123',
                database='patient_record'
            )

            cursor = connection.cursor()

            # Fetch patient details by Aadhar number
            cursor.execute('SELECT * FROM patients WHERE aadhar = %s', (aadhar_to_fetch,))
            patient_details = cursor.fetchone()

            # Close the connection
            connection.close()

            if patient_details:
                messagebox.showinfo("Patient Details",
                                    f"Name: {patient_details[1]}\nAge: {patient_details[2]}\nGender: {patient_details[3]}\nDiagnosis: {patient_details[4]}\nPhone: {patient_details[5]}\nAadhar: {patient_details[6]}")
            else:
                messagebox.showinfo("Patient Details", "Patient not found.")

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching patient details: {e}")

    def clear_entries(self):
        # Clear entry fields after adding a record
        self.name_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.gender_entry.delete(0, END)
        self.diagnosis_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.aadhar_entry.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    app = PatientRecordManagementApp(root)
    root.mainloop()
