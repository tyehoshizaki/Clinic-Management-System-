import sys
from clinic.controller import Controller
from clinic.patient import Patient
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTabWidget, QToolBar, QDialog, QLineEdit, QMessageBox, QStackedWidget
from PyQt6 import QtCore, QtGui, QtWidgets
from .table_view import TableModel

class MainMenuWindow(QWidget):
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.main_menu_content = QStackedWidget()
        
        self.main_menu_content.addWidget(self.open_search_patient())
        self.main_menu_content.addWidget(self.open_create_patient())
        self.main_menu_content.addWidget(self.open_retrieve_patient())
        self.main_menu_content.addWidget(self.open_update_patient())
        self.main_menu_content.addWidget(self.open_delete_patient())
        self.main_menu_content.addWidget(self.open_list_patient())
        
        self.layout = QVBoxLayout(self)
        self.toolbar = QToolBar("Main menu toolbar")
        
        search_patient_action = QAction("Search Patient", self)
        search_patient_action.triggered.connect(lambda: self.main_menu_content.setCurrentIndex(0))
        self.toolbar.addAction(search_patient_action)
        
        create_patient_action = QAction("Create Patient", self)
        create_patient_action.triggered.connect(lambda: self.main_menu_content.setCurrentIndex(1))
        self.toolbar.addAction(create_patient_action)
        
        retrieve_patients_action = QAction("Retrieve Patients", self)
        retrieve_patients_action.triggered.connect(lambda: self.main_menu_content.setCurrentIndex(2))
        self.toolbar.addAction(retrieve_patients_action)
        
        update_patient_action = QAction("Update Patient", self)
        update_patient_action.triggered.connect(lambda: self.main_menu_content.setCurrentIndex(3))
        self.toolbar.addAction(update_patient_action)
        
        delete_patient_action = QAction("Delete Patient", self)
        delete_patient_action.triggered.connect(lambda: self.main_menu_content.setCurrentIndex(4))
        self.toolbar.addAction(delete_patient_action)
        
        list_patients_action = QAction("List Patients", self)
        list_patients_action.triggered.connect(lambda: self.main_menu_content.setCurrentIndex(5))
        self.toolbar.addAction(list_patients_action)
        
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.main_menu_content)
        
        
        
    def open_search_patient(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Search Patient by PHN"))
        layout.addWidget(QLabel("Personal Health Number (PHN):"))
        
        searched_patient_phn = QLineEdit()
        searched_patient_phn.setMaxLength(10)
        searched_patient_phn.setPlaceholderText("Personal Health Number")
        searched_patient_phn.setInputMask('0000000000')
        
        layout.addWidget(searched_patient_phn)
        
        search_button = QPushButton("Search")
        layout.addWidget(search_button)
        
        search_button.clicked.connect(lambda: self.check_fields([searched_patient_phn], lambda: self.search_patient(int(searched_patient_phn.text()))))

        widget.setLayout(layout)
        return widget
    
    def search_patient(self, PHN):
        patient = self.controller.search_patient(PHN)
        
        if patient is None:
            dlg = self.create_dialog("Error", "No Patient Exists")
            dlg.exec()
            
        else:
            
            dlg = QDialog(self)
            dlg.setWindowTitle("Patient")
        
            layout = QVBoxLayout()

            layout.addWidget(QLabel(f"PHN: {patient.PHN}"))
            layout.addWidget(QLabel(f"Name: {patient.name}"))
            layout.addWidget(QLabel(f"Birth Date: {patient.birth_date}"))
            layout.addWidget(QLabel(f"Phone: {patient.phone}"))
            layout.addWidget(QLabel(f"Email: {patient.email}"))
            layout.addWidget(QLabel(f"Address: {patient.address}"))
            
            close_button = self.close_button(dlg)
            layout.addWidget(close_button)
            
            dlg.setLayout(layout)
        
            dlg.exec()

        
        
    def open_create_patient(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Create Patient"))
        PHN_layout = QHBoxLayout()
        PHN_layout.addWidget(QLabel("Personal Health Number:"))
        
        create_patient_PHN = QLineEdit()
        create_patient_PHN.setMaxLength(10)
        create_patient_PHN.setPlaceholderText("PHN")
        create_patient_PHN.setInputMask('0000000000')
        
        PHN_layout.addWidget(create_patient_PHN)
        layout.addLayout(PHN_layout)
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Patient's Name:"))
        
        create_patient_name= QLineEdit()
        create_patient_name.setPlaceholderText("Name")
        
        name_layout.addWidget(create_patient_name)
        layout.addLayout(name_layout)
        
        birthdate_layout = QHBoxLayout()
        birthdate_layout.addWidget(QLabel("Birth Date (YYYY-MM-DD):"))
        
        create_patient_birthdate = QLineEdit()
        create_patient_birthdate.setMaxLength(8)
        create_patient_birthdate.setPlaceholderText("YYYY-MM-DD")
        create_patient_birthdate.setInputMask('0000-00-00')
        
        birthdate_layout.addWidget(create_patient_birthdate)
        layout.addLayout(birthdate_layout)
        
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(QLabel("Phone Number:"))
        
        create_patient_phone = QLineEdit()
        create_patient_phone.setMaxLength(10)
        create_patient_phone.setPlaceholderText("***-***-****")
        create_patient_phone.setInputMask('000-000-0000')
        
        phone_layout.addWidget(create_patient_phone)
        layout.addLayout(phone_layout)
        
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("Email:"))
        
        create_patient_email = QLineEdit()
        create_patient_email.setPlaceholderText("Email")
        
        email_layout.addWidget(create_patient_email)
        layout.addLayout(email_layout)
        
        address_layout = QHBoxLayout()
        address_layout.addWidget(QLabel("Address:"))
        
        create_patient_address = QLineEdit()
        
        address_layout.addWidget(create_patient_address)
        layout.addLayout(address_layout)
        
        create_button = QPushButton("Create Patient")
        layout.addWidget(create_button)
        
        create_button.clicked.connect(lambda: self.check_fields([create_patient_PHN, create_patient_name, create_patient_birthdate, create_patient_phone, create_patient_email, create_patient_address], 
            lambda: self.create_patient(
            Patient(
                int(create_patient_PHN.text()), 
                create_patient_name.text(), 
                create_patient_birthdate.text(), 
                create_patient_phone.text(), 
                create_patient_email.text(), 
                create_patient_address.text()))))

        widget.setLayout(layout)
        return widget

    def create_patient(self, patient):
        try:
            self.controller.create_patient(patient.PHN, patient.name, patient.birth_date, patient.phone, patient.email, patient.address)
            
            dlg = self.create_dialog("Created Patient", "Created Patient Successfully")
            dlg.exec()
            
        except Exception as e:
            dlg = self.create_dialog("Error", f"Error Creating Patient: {str(e)}")
            dlg.exec()
            
            
            
    def open_retrieve_patient(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Retrieve Patients by name"))
        
        patients_name = QLineEdit()
        patients_name.setPlaceholderText("Name")
        layout.addWidget(patients_name)
        
        patients_retrieve_button = QPushButton("Retrieve")
        layout.addWidget(patients_retrieve_button)
        
        patients_retrieve_button.clicked.connect(lambda: self.check_fields([patients_name], lambda: self.retrieve_patients(patients_name.text())))
        
        widget.setLayout(layout)
        return widget
    
    def retrieve_patients(self, name):
        patient_list = self.controller.retrieve_patients(name)
        if len(patient_list) == 0:
            dlg = self.create_dialog("Error", "No Patients Found")
            dlg.exec()
        else:
            
            data_list = []
        
            for patient in patient_list:
                data_list.append(self.make_patient_into_list(patient))
        
            dlg = QDialog(self)
            layout = QVBoxLayout()
        
            table = QtWidgets.QTableView()
            model = TableModel(data_list)
            table.setModel(model)
        
            table.resizeColumnsToContents()
            table.resizeRowsToContents()
        
            layout.addWidget(table)
        
            close_button = self.close_button(dlg)
            layout.addWidget(close_button)
        
            dlg.setLayout(layout)
            dlg.resize(1000, 563)
            dlg.exec()

    
    
    def open_update_patient(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Update Patient by PHN"))
        
        searched_patient_phn = QLineEdit()
        searched_patient_phn.setMaxLength(10)
        searched_patient_phn.setPlaceholderText("Personal Health Number")
        searched_patient_phn.setInputMask('0000000000')
        
        layout.addWidget(searched_patient_phn)
        
        find_button = QPushButton("Find")
        layout.addWidget(find_button)
        
        find_button.clicked.connect(lambda: self.check_fields([searched_patient_phn], lambda: self.find_patient_to_update(int(searched_patient_phn.text()))))
        
        widget.setLayout(layout)
        return widget
    
    def find_patient_to_update(self, PHN):
        patient = self.controller.search_patient(PHN)
        
        if patient is None:
            dlg = self.create_dialog("Error", "No Patient Found")
            dlg.exec()
            
        else:
            dlg = QDialog(self)
            dlg.setWindowTitle("Update Patient")
            
            layout = QVBoxLayout()
            
            layout.addWidget(QLabel("Update Patient"))
            PHN_layout = QHBoxLayout()
            PHN_layout.addWidget(QLabel("Personal Health Number:"))
        
            update_patient_PHN = QLineEdit()
            update_patient_PHN.setMaxLength(10)
            update_patient_PHN.setText(f"{patient.PHN}")
            update_patient_PHN.setInputMask('0000000000')
        
            PHN_layout.addWidget(update_patient_PHN)
            layout.addLayout(PHN_layout)
        
            name_layout = QHBoxLayout()
            name_layout.addWidget(QLabel("Patient's Name:"))
        
            update_patient_name= QLineEdit()
            update_patient_name.setText(f"{patient.name}")
        
            name_layout.addWidget(update_patient_name)
            layout.addLayout(name_layout)
        
            birthdate_layout = QHBoxLayout()
            birthdate_layout.addWidget(QLabel("Birth Date (YYYY-MM-DD):"))
        
            update_patient_birthdate = QLineEdit()
            update_patient_birthdate.setMaxLength(10)
            update_patient_birthdate.setText(f"{patient.birth_date}")
            update_patient_birthdate.setInputMask('0000-00-00')
        
            birthdate_layout.addWidget(update_patient_birthdate)
            layout.addLayout(birthdate_layout)
        
            phone_layout = QHBoxLayout()
            phone_layout.addWidget(QLabel("Phone Number:"))
        
            update_patient_phone = QLineEdit()
            update_patient_phone.setMaxLength(12)
            update_patient_phone.setText(f"{patient.phone}")
            update_patient_phone.setInputMask('000-000-0000')
        
            phone_layout.addWidget(update_patient_phone)
            layout.addLayout(phone_layout)
        
            email_layout = QHBoxLayout()
            email_layout.addWidget(QLabel("Email:"))
        
            update_patient_email = QLineEdit()
            update_patient_email.setText(f"{patient.email}")
        
            email_layout.addWidget(update_patient_email)
            layout.addLayout(email_layout)
        
            address_layout = QHBoxLayout()
            address_layout.addWidget(QLabel("Address:"))
        
            update_patient_address = QLineEdit()
            update_patient_address.setText(f"{patient.address}")
        
            address_layout.addWidget(update_patient_address)
            layout.addLayout(address_layout)
            
            button_layout = QHBoxLayout()
            update_button = QPushButton("Update")
            button_layout.addWidget(update_button)
            close_button = self.close_button(dlg)
            button_layout.addWidget(close_button)
            
            layout.addLayout(button_layout)
            
            dlg.setLayout(layout)
            
            update_button.clicked.connect(lambda: self.check_fields([update_patient_PHN, update_patient_name, update_patient_birthdate, update_patient_phone, update_patient_email, update_patient_address], lambda: self.update_patient(PHN, 
                Patient(
                    int(update_patient_PHN.text()), 
                    update_patient_name.text(), 
                    update_patient_birthdate.text(), 
                    update_patient_phone.text(), 
                    update_patient_email.text(), 
                    update_patient_address.text()))))
            
            dlg.exec()
            
    def update_patient(self, PHN, patient):
        try:
            self.controller.update_patient(PHN, patient.PHN, patient.name, patient.birth_date, patient.phone, patient.email, patient.address)
            
            dlg = self.create_dialog("Updated Patient", "Updated Patient Successfully")
            dlg.exec()
            
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to Update Patient: {str(e)}")
            dlg.exec()
            
            
    
    def open_delete_patient(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Delete Patient by PHN"))
        layout.addWidget(QLabel("Personal Health Number (PHN):"))
        
        searched_patient_phn = QLineEdit()
        searched_patient_phn.setMaxLength(10)
        searched_patient_phn.setPlaceholderText("Personal Health Number")
        searched_patient_phn.setInputMask('0000000000')
        
        layout.addWidget(searched_patient_phn)
        
        search_button = QPushButton("Search")
        layout.addWidget(search_button)
        
        search_button.clicked.connect(lambda: self.check_fields([searched_patient_phn], lambda: self.delete_searched_patient(int(searched_patient_phn.text()))))

        widget.setLayout(layout)
        return widget
    
    def delete_searched_patient(self, PHN):
        try:
            patient = self.controller.search_patient(PHN)
        
            if patient is None:
                dlg = self.create_dialog("Error", "No Patient Exists")
                dlg.exec()
            
            else:
            
                dlg = QDialog(self)
                dlg.setWindowTitle("Patient to Detele")
        
                layout = QVBoxLayout()

                layout.addWidget(QLabel(f"PHN: {patient.PHN}"))
                layout.addWidget(QLabel(f"Name: {patient.name}"))
                layout.addWidget(QLabel(f"Birth Date: {patient.birth_date}"))
                layout.addWidget(QLabel(f"Phone: {patient.phone}"))
                layout.addWidget(QLabel(f"Email: {patient.email}"))
                layout.addWidget(QLabel(f"Address: {patient.address}"))
            
                layout.addWidget(QLabel("Are you sure you want to detele this patient?"))
            
                button_layout = QHBoxLayout()
            
                delete_button = QPushButton("Delete")
                button_layout.addWidget(delete_button)
            
                close_button = self.close_button(dlg)
                button_layout.addWidget(close_button)
                layout.addLayout(button_layout)
            
                delete_button.clicked.connect(lambda: self.delete_this_patient(patient))
            
                dlg.setLayout(layout)
        
                dlg.exec()
                
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to find patient: {str(e)}")
            dlg.exec()
            
    def delete_this_patient(self, patient):
            try:
                self.controller.delete_patient(patient.PHN)
                
                dlg = self.create_dialog("Deleted Patient", "Deleted Patient Successfully")
                dlg.exec()
                
            except Exception as e:
                dlg = self.create_dialog("Error", f"Failed to delete patient: {str(e)}")
                dlg.exec()
    
    
    
    def open_list_patient(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Retrieve All Patients"))
        
        patients_retrieve_button = QPushButton("Retrieve")
        layout.addWidget(patients_retrieve_button)
        
        patients_retrieve_button.clicked.connect(lambda: self.retrieve_all_patients())
        
        widget.setLayout(layout)
        return widget
    
    def retrieve_all_patients(self):
        patient_list = self.controller.list_patients()
        if len(patient_list) == 0:
            dlg = self.create_dialog("Error", f"No Patients On Record")
            dlg.exec()
        
        else:
            data_list = []
        
            for patient in patient_list:
                data_list.append(self.make_patient_into_list(patient))
        
            dlg = QDialog(self)
            layout = QVBoxLayout()
        
            table = QtWidgets.QTableView()
            model = TableModel(data_list)
            table.setModel(model)
        
            table.resizeColumnsToContents()
            table.resizeRowsToContents()
        
            layout.addWidget(table)
        
            close_button = self.close_button(dlg)
            layout.addWidget(close_button)
        
            dlg.setLayout(layout)
            dlg.resize(1000, 563)
            dlg.exec()
        
        
    
    def close_button(self, dialog):
        button = QPushButton("Close")
        button.clicked.connect(dialog.close)
        return button
    
    def create_dialog(self, title, message):
        dlg = QDialog(self)
        dlg.setWindowTitle(title)
        
        dlg_layout = QVBoxLayout()
        dlg_layout.addWidget(QLabel(message))
        
        close_button = self.close_button(dlg)
        dlg_layout.addWidget(close_button)
        dlg.setLayout(dlg_layout)
        
        return dlg
    
    def check_fields(self, fields):
        missing_fields = False
        for field in fields:
            if not field.text().strip():
                missing_fields = True
            else:
                field.setStyleSheet("")
                
        if missing_fields:
            QMessageBox.warning(self, "All Fields Mandatory", "All Fields Mandatory")
            return False
        return True
    
    def check_fields(self, fields, action):
        missing_fields = False
        go_ahead = True
        for field in fields:
            if not field.text().strip():
                missing_fields = True
                
        if missing_fields:
            QMessageBox.warning(self, "All Fields Mandatory", "All Fields Mandatory")
            go_ahead = False
    
        if go_ahead:
            action()

    def make_patient_into_list(self, patient):
        return [f"PHN: {patient.PHN}", f"Name: {patient.name}", f"Birth Date: {patient.birth_date}", f"Phone: {patient.phone}", f"Email: {patient.email}", f"Address: {patient.address}"]