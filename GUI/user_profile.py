from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit,
    QMessageBox, QFormLayout, QHBoxLayout
)
from crypto.aes_cipher import decrypt_aes, encrypt_aes
from crypto.triple_des_cipher import decrypt_3des, encrypt_3des
from database import update_user_by_username, delete_user_by_id
from logs.access import write_log
class UserProfileWindow(QWidget):
    def __init__(self, user_data, on_deleted=None):
        super().__init__()
        self.setWindowTitle("Thông tin người dùng")
        self.resize(400, 350)
        self.user_data = user_data
        self.on_deleted = on_deleted
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()
        self.name_edit = QLineEdit(self.user_data[1])
        self.cmnd_edit = QLineEdit(decrypt_3des(self.user_data[2], 'key3des'))
        self.diachi_edit = QLineEdit(decrypt_aes(self.user_data[3], 'keyaes'))
        self.baohiem_edit = QLineEdit(decrypt_aes(self.user_data[4], 'keyaes'))
        self.stk_edit = QLineEdit(decrypt_aes(self.user_data[5], 'keyaes'))
        form = QFormLayout()
        form.addRow("Họ tên:", self.name_edit)
        form.addRow("CMND:", self.cmnd_edit)
        form.addRow("Địa chỉ:", self.diachi_edit)
        form.addRow("Số BHXH:", self.baohiem_edit)
        form.addRow("Số tài khoản:", self.stk_edit)
        layout.addLayout(form)
        btn_layout = QHBoxLayout()
        self.update_btn = QPushButton("Cập nhật thông tin")
        self.delete_btn = QPushButton("Xoá tài khoản")
        self.update_btn.clicked.connect(self.update_info)
        self.delete_btn.clicked.connect(self.delete_account)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    def update_info(self):
        try:
            new_data = {
                'name': self.name_edit.text(),
                'cmnd': encrypt_3des(self.cmnd_edit.text(), 'key3des'),
                'diachi': encrypt_aes(self.diachi_edit.text(), 'keyaes'),
                'baohiem': encrypt_aes(self.baohiem_edit.text(), 'keyaes'),
                'stk': encrypt_aes(self.stk_edit.text(), 'keyaes')
            }
            username = self.user_data[6]
            update_user_by_username(username, new_data)
            write_log(username, "Sửa thông tin", "field=all", is_admin=False)
            QMessageBox.information(self, "Thành công", "Thông tin đã được cập nhật.")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể cập nhật: {str(e)}")
    def delete_account(self):
        confirm = QMessageBox.question(
            self, "Xác nhận xoá",
            "Bạn có chắc chắn muốn xoá tài khoản này?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                user_id = self.user_data[0]
                delete_user_by_id(user_id)
                write_log(self.user_data[6], "Xoá thông tin", f"user_id={user_id}", is_admin=False)
                QMessageBox.information(self, "Xoá", "Tài khoản đã bị xoá.")
                self.close()
                if self.on_deleted:
                    self.on_deleted()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Xoá thất bại: {str(e)}")