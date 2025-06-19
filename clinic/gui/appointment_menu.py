import sys
from clinic.controller import Controller
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTabWidget, QToolBar, QDialog, QLineEdit, QMessageBox, QStackedWidget, QPlainTextEdit
import clinic.exception

class AppointmentMenuWindow(QWidget):
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.appointment_menu_content = QStackedWidget()
        
        self.appointment_menu_content.addWidget(self.open_current_patient())
        self.appointment_menu_content.addWidget(self.open_search_note())
        self.appointment_menu_content.addWidget(self.open_create_note())
        self.appointment_menu_content.addWidget(self.open_retrieve_note())
        self.appointment_menu_content.addWidget(self.open_update_note())
        self.appointment_menu_content.addWidget(self.open_delete_note())
        self.appointment_menu_content.addWidget(self.open_list_note())

        self.layout = QVBoxLayout(self)
        self.toolbar = QToolBar("Appointment toolbar")
        
        current_patient_action = QAction("Current Patient", self)
        current_patient_action.triggered.connect(lambda: self.appointment_menu_content.setCurrentIndex(0))
        self.toolbar.addAction(current_patient_action)
        
        search_note_action = QAction("Search Note", self)
        search_note_action.triggered.connect(lambda: self.appointment_menu_content.setCurrentIndex(1))
        self.toolbar.addAction(search_note_action)
        
        create_note_action = QAction("Create Note", self)
        create_note_action.triggered.connect(lambda: self.appointment_menu_content.setCurrentIndex(2))
        self.toolbar.addAction(create_note_action)
        
        retrieve_notes_action = QAction("Retrieve Notes", self)
        retrieve_notes_action.triggered.connect(lambda: self.appointment_menu_content.setCurrentIndex(3))
        self.toolbar.addAction(retrieve_notes_action)
        
        update_note_action = QAction("Update Note", self)
        update_note_action.triggered.connect(lambda: self.appointment_menu_content.setCurrentIndex(4))
        self.toolbar.addAction(update_note_action)
        
        delete_note_action = QAction("Delete Note", self)
        delete_note_action.triggered.connect(lambda: self.appointment_menu_content.setCurrentIndex(5))
        self.toolbar.addAction(delete_note_action)
        
        list_notes_action = QAction("List Notes", self)
        list_notes_action.triggered.connect(lambda: self.appointment_menu_content.setCurrentIndex(6))
        self.toolbar.addAction(list_notes_action)
        
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.appointment_menu_content)
        
        
        
    def open_current_patient(self):
        
        def refresh_widget():
            refreshed_widget = self.open_current_patient()
            parent = widget.parentWidget()
            parent.layout().replaceWidget(widget, refreshed_widget)
            widget.deleteLater()
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("The Current Patient"))
        
        patient = self.get_current_patient()
        
        if patient is None:
            layout.addWidget(QLabel(f"PHN: None"))
            layout.addWidget(QLabel(f"Name: None"))
            layout.addWidget(QLabel(f"Birth Date: None"))
            layout.addWidget(QLabel(f"Phone: None"))
            layout.addWidget(QLabel(f"Email: None"))
            layout.addWidget(QLabel(f"Address: None"))
            
        else:
            layout.addWidget(QLabel(f"PHN: {patient.PHN}"))
            layout.addWidget(QLabel(f"Name: {patient.name}"))
            layout.addWidget(QLabel(f"Birth Date: {patient.birth_date}"))
            layout.addWidget(QLabel(f"Phone: {patient.phone}"))
            layout.addWidget(QLabel(f"Email: {patient.email}"))
            layout.addWidget(QLabel(f"Address: {patient.address}"))
        
        layout.addWidget(QLabel("Set Current Patient by PHN"))
        layout.addWidget(QLabel("Enter Patient's PHN:"))
        
        set_current_patient_phn = QLineEdit()
        set_current_patient_phn.setMaxLength(10)
        set_current_patient_phn.setPlaceholderText("PHN")
        set_current_patient_phn.setInputMask('0000000000')
        
        layout.addWidget(set_current_patient_phn)
        
        button_layout = QHBoxLayout()
        
        set_button = QPushButton("Set")
        button_layout.addWidget(set_button)
        
        unset_button = QPushButton("Unset")
        button_layout.addWidget(unset_button)
        
        layout.addLayout(button_layout)
        
        set_button.clicked.connect(lambda: self.check_fields([set_current_patient_phn], lambda: self.set_current_patient(int(set_current_patient_phn.text()))))
        set_button.clicked.connect(lambda: set_current_patient_phn.clear())
        set_button.clicked.connect(refresh_widget)
        unset_button.clicked.connect(lambda: self.unset_current_patient())
        unset_button.clicked.connect(refresh_widget)
        
        
        widget.setLayout(layout)
        return widget
    
    def get_current_patient(self):
        
        patient = self.controller.get_current_patient()
        
        if patient is None:
            return None
        else:
            return patient
    
    def set_current_patient(self, PHN):
        try:
            self.controller.set_current_patient(PHN)
            
            dlg = self.create_dialog("Set Patient", "Set the Current Patient Successfully")
            dlg.exec()
                
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to set patient: {str(e)}")
            dlg.exec()
            
    def unset_current_patient(self):
        try:
            self.controller.unset_current_patient()
            
            dlg = self.create_dialog("Unset Patient", "Unset the Current Patient Successfully")
            dlg.exec()
                
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to unset patient: {str(e)}")
            dlg.exec()
            
            
        
    def open_search_note(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Search Note by Code"))
        layout.addWidget(QLabel("Code:"))
        
        searched_note_code = QLineEdit()
        searched_note_code.setMaxLength(10)
        searched_note_code.setPlaceholderText("Code")
        searched_note_code.setInputMask('0000000000')
        
        layout.addWidget(searched_note_code)
        
        search_button = QPushButton("Search")
        layout.addWidget(search_button)
        
        search_button.clicked.connect(lambda: self.check_fields([searched_note_code], lambda: self.search_note(int(searched_note_code.text()))))

        widget.setLayout(layout)
        return widget
    
    def search_note(self, code):
        try:
            note = self.controller.search_note(code)
        
            if note is None:
                dlg = self.create_dialog("Error", "No Note Exists")
                dlg.exec()
            
            else:
            
                dlg = QDialog(self)
                dlg.setWindowTitle("Note")
        
                layout = QVBoxLayout()

                layout.addWidget(QLabel(f"Code: {note.code}"))
                layout.addWidget(QLabel(f"Text: {note.text}"))
                layout.addWidget(QLabel(f"Timestamp: {note.timestamp}"))
            
                close_button = self.close_button(dlg)
                layout.addWidget(close_button)
            
                dlg.setLayout(layout)
        
                dlg.exec()
                
        except Exception as e:
            dlg = self.create_dialog("Error", f"Error Searching Note: {str(e)}")
            dlg.exec()
            
            
        
    def open_create_note(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Create Note"))
        
        text = QLineEdit()
        text.setPlaceholderText("Write Note Here")
        layout.addWidget(text)
        
        create_button = QPushButton("Create")
        create_button.clicked.connect(lambda: self.check_fields([text], lambda: self.create_note(text.text())))
        create_button.clicked.connect(lambda: text.clear())
        
        layout.addWidget(create_button)

        widget.setLayout(layout)
        return widget

    def create_note(self, text):
        try:
            self.controller.create_note(text)
            
            dlg = self.create_dialog("Created Note", "Created Note Successfully")
            dlg.exec()
            
        except Exception as e:
            dlg = self.create_dialog("Error", f"Error Creating Note: {str(e)}")
            dlg.exec()
    
    def open_retrieve_note(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Retrieve notes by words within text"))
        
        notes_text = QLineEdit()
        notes_text.setPlaceholderText("Text")
        layout.addWidget(notes_text)
        
        notes_retrieve_button = QPushButton("Retrieve")
        layout.addWidget(notes_retrieve_button)
        
        notes_retrieve_button.clicked.connect(lambda: self.check_fields([notes_text], lambda: self.retrieve_notes_from_text(notes_text.text())))
        
        widget.setLayout(layout)
        return widget
    
    def retrieve_notes_from_text(self, text):
        try:
            notes_list = self.controller.retrieve_notes(text)
            
            text = QPlainTextEdit()
            text.setPlainText("")
            text.setReadOnly(True)
        
            for notes in notes_list:
                text.appendPlainText(self.turn_note_into_str(notes))
            
            dlg = QDialog(self)
            layout = QVBoxLayout()
            layout.addWidget(text)
        
            close_button = self.close_button(dlg)
            layout.addWidget(close_button)
        
            dlg.setLayout(layout)
            dlg.resize(550, 310)
            dlg.exec()
            
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to find note: {str(e)}")
            dlg.exec()
        
    
    def open_update_note(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Update Note by Code"))
        
        searched_note_code = QLineEdit()
        searched_note_code.setMaxLength(10)
        searched_note_code.setPlaceholderText("Code")
        searched_note_code.setInputMask('00000000000')
        
        layout.addWidget(searched_note_code)
        
        find_button = QPushButton("Find")
        layout.addWidget(find_button)
        
        find_button.clicked.connect(lambda: self.check_fields([searched_note_code], lambda: self.find_note_to_update(int(searched_note_code.text()))))
        
        widget.setLayout(layout)
        return widget
    
    def find_note_to_update(self, code):
        try:
            note = self.controller.search_note(code)
            
            if note is None:
                dlg = self.create_dialog("Error", "No Note Found")
                dlg.exec()
                
            else:
                dlg = QDialog(self)
                dlg.setWindowTitle("Update Note")
                
                layout = QVBoxLayout()
                
                layout.addWidget(QLabel("Update Note"))
                layout.addWidget(QLabel(f"Code: {code}"))
                
                layout.addWidget(QLabel("New Text:"))
                update_note_text = QLineEdit()
                layout.addWidget(update_note_text)
                
                button_layout = QHBoxLayout()
                update_button = QPushButton("Update")
                button_layout.addWidget(update_button)
                close_button = self.close_button(dlg)
                button_layout.addWidget(close_button)
            
                layout.addLayout(button_layout)
                
                update_button.clicked.connect(lambda: self.check_fields([update_note_text], lambda: self.update_note(code, update_note_text.text())))
                
                dlg.setLayout(layout)
                dlg.exec()
                
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to Find Note: {str(e)}")
            dlg.exec()
                
    def update_note(self, code, text):
        try:
            self.controller.update_note(code, text)
            dlg = self.create_dialog("Updated Note", "Updated Note Successfully")
            dlg.exec()
            
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to Update Patient: {str(e)}")
            dlg.exec()
    
    def open_delete_note(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Delete Note by Code"))
        layout.addWidget(QLabel("Code:"))
        
        searched_note_code = QLineEdit()
        searched_note_code.setMaxLength(10)
        searched_note_code.setPlaceholderText("Code")
        searched_note_code.setInputMask('0000000000')
        
        layout.addWidget(searched_note_code)
        
        searched_button = QPushButton("Search")
        layout.addWidget(searched_button)
        
        searched_button.clicked.connect(lambda: self.check_fields([searched_note_code], lambda: self.delete_searched_note(int(searched_note_code.text()))))
        
        widget.setLayout(layout)
        return widget
    
    def delete_searched_note(self, code):
        try:
            note = self.controller.search_note(code)
            
            if note is None:
                dlg = self.create_dialog("Error", "No Note Exists")
                dlg.exec()
                
            else:
                dlg = QDialog(self)
                dlg.setWindowTitle("Note to Delete")
                
                layout = QVBoxLayout()
                
                layout.addWidget(QLabel(f"Code: {note.code}"))
                layout.addWidget(QLabel(f"Text: {note.text}"))
                layout.addWidget(QLabel(f"Timestamp: {note.timestamp}"))
                
                layout.addWidget(QLabel("Are you sure you want to detele this note?"))
            
                button_layout = QHBoxLayout()
            
                delete_button = QPushButton("Delete")
                button_layout.addWidget(delete_button)
            
                close_button = self.close_button(dlg)
                button_layout.addWidget(close_button)
                layout.addLayout(button_layout)
            
                delete_button.clicked.connect(lambda: self.delete_this_note(note))
            
                dlg.setLayout(layout)
        
                dlg.exec()
                
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to find note: {str(e)}")
            dlg.exec()
            
    def delete_this_note(self, note):
        try:
            self.controller.delete_note(note.code)
            
            dlg = self.create_dialog("Deleted Note", "Deleted Note Successfully")
            dlg.exec()
                
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to delete note: {str(e)}")
            dlg.exec()
        
            
    
    def open_list_note(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Retrieve all notes"))

        notes_retrieve_button = QPushButton("Retrieve")
        layout.addWidget(notes_retrieve_button)
        
        notes_retrieve_button.clicked.connect(lambda: self.retrieve_all_notes())
        
        widget.setLayout(layout)
        return widget
    
    def retrieve_all_notes(self):
        try:
            notes_list = self.controller.list_notes()
            
            text = QPlainTextEdit()
            text.setPlainText("")
            text.setReadOnly(True)
        
            for notes in notes_list:
                text.appendPlainText(self.turn_note_into_str(notes))
            
            dlg = QDialog(self)
            layout = QVBoxLayout()
            layout.addWidget(text)
        
            close_button = self.close_button(dlg)
            layout.addWidget(close_button)
        
            dlg.setLayout(layout)
            dlg.resize(550, 310)
            dlg.exec()
            
        except Exception as e:
            dlg = self.create_dialog("Error", f"Failed to find note: {str(e)}")
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
            
    def turn_note_into_str(self, note):
        return f"Code #: {note.code}\t\t\tTimestamp: {note.timestamp}\n\n{note.text}\n"
    
    def update_data():
        pass
    