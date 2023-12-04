# Patient-Record-Management-System
This is a simple Patient Record Management application developed in Python using the Tkinter library for the graphical user interface and MySQL database for storing patient records. The application allows users to add, update, fetch records, and retrieve patient details by Aadhar number.

# Features
Add Record: Enter patient details such as name, age, gender, diagnosis, phone, and Aadhar number. The application performs data validation and checks for duplicate Aadhar numbers.

Update Record: Select a record from the list and update patient information in a new window. The application validates data and ensures that the updated Aadhar number is unique.

Fetch Records: Display a list of all patient records in a scrollable listbox.

Fetch by Aadhar: Retrieve patient details by entering the Aadhar number. The application provides a pop-up with the patient's information if found.

# Database
The application uses MySQL to store patient records. The patients table includes fields such as id, name, age, gender, diagnosis, phone, and aadhar. The database is initialized on startup, creating the table if it does not exist.

# Requirements
Python
Tkinter (GUI)
MySQL Connector (Database)

# How To Use
Install the required dependencies using pip install mysql-connector-python for MySQL Connector.

Run the application by executing the app.py file.

Use the provided GUI to perform actions such as adding, updating, and fetching patient records.
