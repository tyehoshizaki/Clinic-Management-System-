import sys
from clinic.controller import Controller
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTabWidget, QToolBar, QDialog, QLineEdit, QMessageBox, QStackedWidget
from .main_menu import MainMenuWindow
from .appointment_menu import AppointmentMenuWindow

class LoginWindow(QDialog):
    

    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller
        
        self.setWindowTitle("Login into Clinic")
        self.setFixedSize(400,300)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Username: "))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)
        
        layout.addWidget(QLabel("Password: "))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        buttons = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.quit_button = QPushButton("Quit")
        buttons.addWidget(self.login_button)
        buttons.addWidget(self.quit_button)
        
        layout.addLayout(buttons)
        self.setLayout(layout)
        
        self.login_button.clicked.connect(self.login)
        self.quit_button.clicked.connect(self.quit)
        
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        try:
            self.controller.login(username, password)
            self.accept()
            
        except Exception as e:
            QMessageBox.warning(self, "Login Failed", "Error: Invalid Login")
            
    def quit(self):
        sys.exit()
        
class ClinicGUI(QMainWindow):

    def __init__(self, controller):
        super().__init__() 
        self.controller = controller
        
        self.setWindowTitle("Clinic")
        
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.setCentralWidget(self.tabs)
        
        self.tabs.addTab(MainMenuWindow(self.controller), "Main Menu")
        self.tabs.addTab(AppointmentMenuWindow(self.controller), "Appointment Menu")
        self.logout_tab()

    
        
    def logout_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Are you sure you want to logout?"))
        logout_button = QHBoxLayout()
        self.logout_button = QPushButton("Logout")
        logout_button.addWidget(self.logout_button)
        layout.addLayout(logout_button)
        tab.setLayout(layout)
        
        self.logout_button.clicked.connect(self.logout)
        
        self.tabs.addTab(tab, "Logout Menu")
    
    def logout(self):
        
        try:
            self.controller.logout()
            QMessageBox.information(self, "Logged Out", "Logged Out")
            self.close()
            self.login_window()
        except Exception as e:
            QMessageBox.warning(self, "Logged Out Failed", f"Logged Out Failed: {str(e)}")
            
            
    def login_window(self):
        login_window = LoginWindow(self.controller)
        if login_window.exec():
            self.show()
            
def main():
    controller = Controller(autosave=True)
    
    app = QApplication(sys.argv)
    window = LoginWindow(controller)
    
    if window.exec():
        window = ClinicGUI(controller)
        window.show()
        app.exec()
        
    else:
        sys.exit()

if __name__ == '__main__':
    main()
