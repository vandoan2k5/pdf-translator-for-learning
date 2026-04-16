## README.md

# Dịch tài liệu ebook để học nhe !!!
Dự án này sử dụng công nghệ AI được tích hợp vào giao diện web đơn giản. Dưới đây là hướng dẫn chi tiết để cài đặt và chạy ứng dụng dưới máy local.

## 🚀 Hướng dẫn cài đặt

Dự án sử dụng **uv** để quản lý môi trường và gói thư viện, giúp tốc độ cài đặt và chạy nhanh hơn.

1.  **Truy cập vào thư mục chính:**
    Mở terminal và di chuyển đến thư mục chứa mã nguồn của dự án.

2.  **Đồng bộ môi trường:**
    Chạy lệnh sau để tự động tạo môi trường ảo và cài đặt các thư viện cần thiết:
    ```bash
    uv sync
    ```

3.  **Cấu hình API Key:**
    * Bạn cần có một API Key để ứng dụng có thể hoạt động.
    * Hãy xem hình ảnh hướng dẫn `cofig_apikey.png` (lưu ý tên file trong ảnh đang là *cofig* thay vì *config*) trong thư mục gốc để biết vị trí dán API Key vào code.
    * *Lưu ý: Vì chạy local nên bạn hoàn toàn yên tâm về vấn đề bảo mật key.*

## 💻 Cách sử dụng

1.  **Chạy server Backend:**
    Sau khi đã sync xong, khởi động ứng dụng bằng lệnh:
    ```bash
    python main.py
    ```

2.  **Mở giao diện người dùng:**
    Sử dụng trình duyệt **Google Chrome** để mở file:
    `index.html`

3.  **Tận hưởng kết quả!**

## 📂 Cấu trúc thư mục
* `main.py`: File xử lý logic chính (Backend).
* `index.html`: Giao diện hiển thị (Frontend).
* `pyproject.toml` & `uv.lock`: Các file quản lý dependency của hệ thống `uv`.
* `.python-version`: Quy định phiên bản Python sử dụng cho dự án.

---

### Một vài góp ý nhỏ cho bạn:
* **Chỉnh lỗi chính tả:** Trong ảnh mình thấy file ảnh tên là `cofig_apikey.png`. Bạn nên đổi lại thành `config_apikey.png` (thêm chữ **n**) cho đúng chuẩn nhé.
* **Bảo mật:** Mặc dù chạy local không sợ mất, nhưng nếu sau này bạn đẩy code lên GitHub, hãy nhớ thêm các file chứa Key vào `.gitignore` để tránh bị lộ công khai.

Chúc dự án của bạn chạy mượt mà!
