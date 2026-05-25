# Hướng dẫn cập nhật Cookie AnkiWeb

Cookie hết hạn sau ~14 ngày hoặc khi bạn đăng xuất AnkiWeb. Khi app báo lỗi kết nối, làm lại các bước dưới đây.

## Cài đặt Cookie Editor (một lần duy nhất)

1. Mở Chrome trên máy tính
2. Cài extension **Cookie Editor** từ Chrome Web Store
3. Xong - không cần cấu hình gì thêm

## Lấy Cookie

### Bước 1: Lấy cookie ankiweb.net

1. Mở Chrome, truy cập **https://ankiweb.net**
2. Đăng nhập bằng tài khoản AnkiWeb
3. Bấm vào icon **Cookie Editor** trên thanh công cụ Chrome
4. Bấm **Export** (góc dưới) > **Export as JSON**
5. Nội dung sẽ giống thế này:

```json
[
    {
        "domain": "ankiweb.net",
        "expirationDate": 1811623511.100636,
        "hostOnly": true,
        "httpOnly": true,
        "name": "ankiweb",
        "path": "/",
        "sameSite": null,
        "secure": true,
        "session": false,
        "storeId": null,
        "value": "eyJvcCI6ImNrIiwiaWF0IjoxNzc3MDYzMzIzLCJqdiI6MCwiayI6ImRac2xtMDdMcUdCRDR0dXkiLCJjIjoxLCJ0IjoxNzc3MDYzMzIzfQ.EO6eP8hdD_TV9yDp-4Bc6kM3Gt-1CoWsAx5F0jgvKKQ"
    }
]
```

6. **Lưu vào file** `cookie_ankiweb.txt` (đặt cùng thư mục với `app.py`)

### Bước 2: Lấy cookie ankiuser.net

1. Vẫn trên Chrome, mở một bộ thẻ bất kỳ để vào **https://ankiuser.net/study**
2. Bấm **Cookie Editor** lại
3. Bấm **Export** > **Export as JSON**
4. **Lưu vào file** `cookie_ankiuser.txt` (đặt cùng thư mục với `app.py`)

### Bước 3: Khởi động lại server

```bash
# Dừng server đang chạy (Ctrl+C) rồi khởi động lại
python app.py
```

Kiểm tra console - nếu thấy:
```
Loading cookies...
  cookie_ankiweb.txt: 1 cookie(s).
  cookie_ankiuser.txt: 1 cookie(s).
Total: 2 cookie(s) loaded.
```
là cookie đã hợp lệ.

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách sửa |
|---|---|---|
| `not found` | File cookie không đúng vị trí | Đặt file cùng thư mục với `app.py` |
| Decks rỗng / 500 error | Cookie `ankiweb.net` hết hạn | Lấy lại Bước 1 |
| `Failed to load study cards` | Thiếu cookie `ankiuser.net` | Lấy lại Bước 2 |

## Tóm tắt nhanh

```
1. ankiweb.net → Cookie Editor → Export as JSON → lưu thành cookie_ankiweb.txt
2. ankiuser.net → Cookie Editor → Export as JSON → lưu thành cookie_ankiuser.txt
3. Restart python app.py
```
