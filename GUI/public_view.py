from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QMessageBox, QInputDialog, QLineEdit
)
from database import get_user
from crypto.aes_cipher import decrypt_aes
from crypto.triple_des_cipher import decrypt_3des
import sqlite3

# ✅ Import các cửa sổ cần mở
from GUI.register_window import RegisterWindow
from GUI.login_window import LoginWindow
from GUI.admin_panel import AdminPanel
from PyQt5.QtCore import Qt
class PublicView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Danh sách người dùng")
        self.resize(600, 500)

        self.is_admin = False
        self.current_user = None  # username người dùng hiện tại

        main_layout = QVBoxLayout()
        self.user_list = QListWidget()
        self.view_btn = QPushButton("Xem thông tin chi tiết")
        self.view_btn.clicked.connect(self.show_detail)

        # Thêm các nút bên dưới
        bottom_layout = QHBoxLayout()
        self.register_btn = QPushButton("Đăng ký")
        self.login_btn = QPushButton("Đăng nhập")
        self.admin_btn = QPushButton("Admin đăng nhập")

        self.register_btn.clicked.connect(self.register)
        self.login_btn.clicked.connect(self.login_user)
        self.admin_btn.clicked.connect(self.login_admin)

        bottom_layout.addWidget(self.register_btn)
        bottom_layout.addWidget(self.login_btn)
        bottom_layout.addWidget(self.admin_btn)

        main_layout.addWidget(self.user_list)
        main_layout.addWidget(self.view_btn)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        self.load_users()

    def load_users(self):
        conn = sqlite3.connect("data/users.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM users")
        users = c.fetchall()
        conn.close()

        self.user_list.clear()
        for u in users:
            self.user_list.addItem(f"{u[0]} - {u[1]}")

    def show_detail(self):
        selected = self.user_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn người dùng.")
            return

        user_id = int(selected.text().split(" - ")[0])
        user = self.get_user_by_id(user_id)
        if not user:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy người dùng.")
            return

        if self.is_admin:
            self.show_user_detail(user)
        else:
            username, ok1 = QInputDialog.getText(self, "Xác minh", "Nhập tên đăng nhập:")
            if not ok1:
                return

            password, ok2 = QInputDialog.getText(self, "Xác minh", "Nhập mật khẩu:", echo=QLineEdit.Password)
            if not ok2:
                return

            auth_user = get_user(username)
            if not auth_user or auth_user[7] != password or auth_user[0] != user_id:
                QMessageBox.warning(self, "Lỗi", "Thông tin xác thực không đúng!")
                return

            self.show_user_detail(auth_user)

    def show_user_detail(self, user):
        try:
            cmnd = decrypt_3des(user[2], 'key3des')
            diachi = decrypt_aes(user[3], 'keyaes')
            baohiem = decrypt_aes(user[4], 'keyaes')
            stk = decrypt_aes(user[5], 'keyaes')
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Giải mã thất bại: {str(e)}")
            return

        QMessageBox.information(self, "Thông tin chi tiết",
            f"Họ tên: {user[1]}\n"
            f"CMND: {cmnd}\n"
            f"Địa chỉ: {diachi}\n"
            f"Số BHXH: {baohiem}\n"
            f"Số tài khoản: {stk}"
        )

    def get_user_by_id(self, user_id):
        conn = sqlite3.connect("data/users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()
        conn.close()
        return user

    # ==== Mở cửa sổ khác ====
    def register(self):
        self.hide()  # Ẩn cửa sổ PublicView
        self.register_window = RegisterWindow(parent=self)
        self.register_window.show()

    def login_user(self):
        self.login_window = LoginWindow()
        self.login_window.show()

    def login_admin(self):
        self.admin_window = AdminPanel(parent=self)
        self.admin_window.setWindowFlag(Qt.Window)  # 🚀 Đảm bảo đây là một cửa sổ độc lập
        self.admin_window.setWindowTitle("Cửa sổ Quản trị viên")
        self.admin_window.resize(600, 400)
        self.admin_window.show()  # ✅ Show cửa sổ mới hoàn toàn