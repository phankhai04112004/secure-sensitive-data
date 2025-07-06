from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database import add_user, get_user
from crypto.aes_cipher import encrypt_aes
from crypto.triple_des_cipher import encrypt_3des


class RegisterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Đăng ký người dùng mới")
        self.resize(300, 400)
        self.parent_view = parent  # Lưu cửa sổ gọi đến

        layout = QVBoxLayout()

        self.name = QLineEdit(self)
        self.cmnd = QLineEdit(self)
        self.diachi = QLineEdit(self)
        self.baohiem = QLineEdit(self)
        self.stk = QLineEdit(self)
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Họ tên:"))
        layout.addWidget(self.name)
        layout.addWidget(QLabel("CMND:"))
        layout.addWidget(self.cmnd)
        layout.addWidget(QLabel("Địa chỉ:"))
        layout.addWidget(self.diachi)
        layout.addWidget(QLabel("Số BHXH:"))
        layout.addWidget(self.baohiem)
        layout.addWidget(QLabel("Số tài khoản:"))
        layout.addWidget(self.stk)
        layout.addWidget(QLabel("Tên đăng nhập:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Mật khẩu:"))
        layout.addWidget(self.password)

        self.register_btn = QPushButton("Đăng ký", self)
        self.register_btn.clicked.connect(self.register)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def register(self):
        try:
            # Kiểm tra trùng username
            if get_user(self.username.text()):
                QMessageBox.warning(self, "Lỗi", "Tên đăng nhập đã tồn tại!")
                return

            # Mã hóa dữ liệu
            cmnd_enc = encrypt_3des(self.cmnd.text(), 'key3des')
            diachi_enc = encrypt_aes(self.diachi.text(), 'keyaes')
            bhxh_enc = encrypt_aes(self.baohiem.text(), 'keyaes')
            stk_enc = encrypt_aes(self.stk.text(), 'keyaes')

            data = (
                self.name.text(),
                cmnd_enc,
                diachi_enc,
                bhxh_enc,
                stk_enc,
                self.username.text(),
                self.password.text()
            )
            add_user(data)

            QMessageBox.information(self, "Thành công", "Đăng ký thành công!")
            self.close()

            # ✅ Hiện lại giao diện PublicView nếu có
            if self.parent_view:
                self.parent_view.show()
                self.parent_view.load_users()

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể đăng ký: {str(e)}")
