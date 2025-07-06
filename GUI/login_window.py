from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox
from database import get_user
from GUI.user_profile import UserProfileWindow
from GUI.admin_panel import AdminPanel

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng nhập")
        self.resize(300, 250)
        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Tên đăng nhập")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Mật khẩu")
        self.password.setEchoMode(QLineEdit.Password)

        self.login_user_btn = QPushButton("Đăng nhập người dùng")
        self.login_admin_btn = QPushButton("Đăng nhập quản trị viên")

        self.login_user_btn.clicked.connect(self.login_user)
        self.login_admin_btn.clicked.connect(self.login_admin)

        layout.addWidget(QLabel("Tên đăng nhập:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Mật khẩu:"))
        layout.addWidget(self.password)
        layout.addWidget(self.login_user_btn)
        layout.addWidget(self.login_admin_btn)

        self.setLayout(layout)

    def login_user(self):
        user = get_user(self.username.text())
        if user and user[7] == self.password.text():
            self.user_window = UserProfileWindow(user)
            self.user_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Lỗi", "Sai thông tin đăng nhập người dùng!")

    def login_admin(self):
        # Hardcoded admin login
        if self.username.text() == "admin" and self.password.text() == "admin123":
            self.admin_panel = AdminPanel()
            self.admin_panel.show()
            self.close()
        else:
            QMessageBox.warning(self, "Lỗi", "Sai thông tin đăng nhập quản trị viên!")
