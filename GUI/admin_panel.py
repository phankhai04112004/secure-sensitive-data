from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget,
    QInputDialog, QMessageBox, QLineEdit, QHBoxLayout
)
from crypto.aes_cipher import decrypt_aes
from crypto.triple_des_cipher import decrypt_3des
from database import get_user_by_id, delete_user_by_id
from logs.access import write_log
import sqlite3


class AdminPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bảng điều khiển Quản trị viên")
        self.resize(500, 400)

        self.parent_window = parent  # Gán parent riêng biệt để dễ gọi sau

        layout = QVBoxLayout()
        self.user_list = QListWidget()

        # Nút chức năng
        self.view_btn = QPushButton("Xem chi tiết người dùng")
        self.delete_btn = QPushButton("Xoá người dùng")

        self.view_btn.clicked.connect(self.view_user)
        self.delete_btn.clicked.connect(self.delete_user)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.view_btn)
        btn_layout.addWidget(self.delete_btn)

        layout.addWidget(self.user_list)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

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

    def ask_admin_password(self):
        password, ok = QInputDialog.getText(
            self, "Xác minh quyền Admin", "Nhập mật khẩu admin:",
            echo=QLineEdit.Password
        )
        return ok and password == "admin123"

    def get_selected_user_id(self):
        selected = self.user_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn người dùng từ danh sách!")
            return None
        try:
            return int(selected.text().split(" - ")[0])
        except:
            QMessageBox.warning(self, "Lỗi", "Không thể phân tích ID người dùng!")
            return None

    def view_user(self):
        user_id = self.get_selected_user_id()
        if user_id is None:
            return

        if not self.ask_admin_password():
            QMessageBox.warning(self, "Lỗi", "Xác thực thất bại!")
            return

        user = get_user_by_id(user_id)
        if not user:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy người dùng!")
            return

        try:
            cmnd = decrypt_3des(user[2], 'key3des')
            diachi = decrypt_aes(user[3], 'keyaes')
            baohiem = decrypt_aes(user[4], 'keyaes')
            stk = decrypt_aes(user[5], 'keyaes')
        except Exception as e:
            QMessageBox.critical(self, "Lỗi giải mã", f"Không thể giải mã: {str(e)}")
            return

        QMessageBox.information(self, "Chi tiết người dùng",
            f"Họ tên: {user[1]}\n"
            f"CMND: {cmnd}\n"
            f"Địa chỉ: {diachi}\n"
            f"Số BHXH: {baohiem}\n"
            f"Số tài khoản: {stk}"
        )

        write_log("admin", "Xem thông tin người dùng", f"user_id={user_id}", is_admin=True)

    def delete_user(self):
        user_id = self.get_selected_user_id()
        if user_id is None:
            return

        if not self.ask_admin_password():
            QMessageBox.warning(self, "Lỗi", "Xác thực thất bại!")
            return

        confirm = QMessageBox.question(
            self, "Xác nhận xoá",
            f"Bạn có chắc muốn xoá user_id={user_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        try:
            delete_user_by_id(user_id)
            self.load_users()
            write_log("admin", "Xoá người dùng", f"user_id={user_id}", is_admin=True)
            QMessageBox.information(self, "Thành công", "Đã xoá người dùng.")

            # ✅ Nếu có parent (ví dụ PublicView), reload lại danh sách
            if self.parent_window and hasattr(self.parent_window, 'load_users'):
                self.parent_window.load_users()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể xoá: {str(e)}")
