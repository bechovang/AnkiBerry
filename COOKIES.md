# Hướng dẫn cập nhật Cookie AnkiWeb

Cookie là thứ duy nhất cần cập nhật định kỳ để AnkiBerry hoạt động. Cookie hết hạn sau ~14 ngày hoặc khi bạn đăng xuất AnkiWeb.

## Cài đặt Cookie Editor (một lần duy nhất)

1. Mở Chrome trên máy tính
2. Cài extension **Cookie Editor** từ Chrome Web Store
3. Xong - không cần cấu hình gì thêm

## Lấy Cookie (mỗi khi hết hạn)

### Bước 1: Lấy cookie ankiweb.net

1. Mở Chrome, truy cập **https://ankiweb.net**
2. Đăng nhập bằng tài khoản AnkiWeb
3. Bấm vào icon **Cookie Editor** trên thanh công cụ Chrome
4. Tìm cookie có tên **`ankiweb`** trong danh sách
5. Bấm **Export** (nút xuất ra JSON ở góc dưới) > chọn **Export as JSON**
6. Nội dung sẽ giống thế này:

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

7. **Lưu tạm** nội dung này (copy vào notepad)

### Bước 2: Lấy cookie ankiuser.net

1. Vẫn trên Chrome, mở một bộ thẻ bất kỳ để vào trang **https://ankiuser.net/study**
2. Bấm **Cookie Editor** lại
3. Tìm cookie tên **`ankiweb`** (domain sẽ là `ankiuser.net`)
4. Bấm **Export** > **Export as JSON**
5. **Lưu tạm** nội dung này

### Bước 3: Gộp vào file

1. Mở file `json cookie.txt` trong thư mục AnkiBerry bằng Notepad hoặc VS Code
2. Gộp cả 2 mảng JSON lại thành một mảng duy nhất:

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
        "value": "GIÁ_TRỊ_COOKIE_ANKIWEB_NET"
    },
    {
        "domain": "ankiuser.net",
        "expirationDate": 1811623511.100636,
        "hostOnly": true,
        "httpOnly": true,
        "name": "ankiweb",
        "path": "/",
        "sameSite": null,
        "secure": true,
        "session": false,
        "storeId": null,
        "value": "GIÁ_TRỊ_COOKIE_ANKIUSER_NET"
    }
]
```

3. Lưu file

### Bước 4: Khởi động lại server

```bash
# Dừng server đang chạy (Ctrl+C) rồi khởi động lại
python app.py
```

Kiểm tra console - nếu thấy `Successfully loaded 2 cookies into session.` là cookie đã hợp lệ.

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách sửa |
|---|---|---|
| `Warning: Cookie file not found` | File `json cookie.txt` không đúng vị trí | Đặt file cùng thư mục với `app.py` |
| `Error loading cookies` | JSON format sai | Kiểm tra dấu phẩy, ngoặc vuông |
| Decks rỗng / 500 error | Cookie hết hạn hoặc sai domain | Lấy lại cookie từ Bước 1 |
| `Failed to load study cards` | Thiếu cookie `ankiuser.net` | Làm thêm Bước 2 |

## Tóm tắt nhanh

```
1. Đăng nhập ankiweb.net → Cookie Editor → Export → copy
2. Mở deck sang ankiuser.net → Cookie Editor → Export → copy
3. Gộp 2 cookie vào json cookie.txt
4. Restart python app.py
```
