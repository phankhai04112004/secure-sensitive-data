import datetime
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "access.log")

def write_log(actor, action, detail, is_admin=False):
    """Ghi một dòng log vào file access.log với định dạng phân biệt ADMIN và USER"""

    # Tạo thư mục logs nếu chưa tồn tại
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Lấy timestamp hiện tại
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Phân loại actor
    actor_type = "ADMIN" if is_admin else "USER"

    # Ghi log
    log_line = f"{timestamp} - {actor_type}({actor}) - {action} - {detail}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)
