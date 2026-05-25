# Hướng dẫn cập nhật Cookie AnkiWeb

Cookie hết hạn sau ~14 ngày hoặc khi bạn đăng xuất AnkiWeb. Khi app báo lỗi kết nối, làm lại các bước dưới đây.

## Cài đặt Cookie Editor (một lần duy nhất)

1. Mở Chrome trên máy tính
2. Cài extension **Cookie Editor** từ Chrome Web Store
3. Xong - không cần cấu hình gì thêm

## Lấy Cookie

### Bước 1: Lấy cookie `cookie_ankiweb.txt`

1. Mở Chrome, truy cập **https://ankiweb.net** và đăng nhập
2. Bạn sẽ thấy trang danh sách bộ thẻ (deck list)
3. Bấm icon **Cookie Editor** trên thanh công cụ Chrome
4. Bấm **Export** (góc dưới) > **Export as JSON**
5. **Lưu thẳng vào file** `cookie_ankiweb.txt` (đặt cùng thư mục với `app.py`)

Nội dung file sẽ giống thế này:

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

> Export ra sao lưu y như vậy, không cần sửa gì.

### Bước 2: Lấy cookie `cookie_ankiuser.txt`

1. Vẫn trên Chrome, **bấm vào một bộ thẻ bất kỳ** trên trang deck list
2. Bạn sẽ được chuyển sang **https://ankiuser.net/study**
3. Bấm **Cookie Editor** lại
4. Bấm **Export** > **Export as JSON**
5. **Lưu thẳng vào file** `cookie_ankiuser.txt` (đặt cùng thư mục với `app.py`)

Nội dung file sẽ giống thế này:

```json
[
    {
        "domain": "ankiuser.net",
        "expirationDate": 1811623512.182425,
        "hostOnly": true,
        "httpOnly": true,
        "name": "ankiweb",
        "path": "/",
        "sameSite": null,
        "secure": true,
        "session": false,
        "storeId": null,
        "value": "eyJvcCI6ImNrIiwiaWF0IjoxNzc3MDYzMzI0LCJqdiI6MCwiayI6ImRac2xtMDdMcUdCRDR0dXkiLCJjIjoyLCJ0IjoxNzc3MDYzMzI0fQ.vhV0WfGc_e6ikHOpew0Zchf66bfHzasjRnFC818vbTI"
    }
]
```

> Lưu ý: cả 2 cookie đều có tên `ankiweb` nhưng **domain khác nhau** (`ankiweb.net` vs `ankiuser.net`) và **value khác nhau**.

### Bước 3: Khởi động lại server

```bash
# Dừng server đang chạy (Ctrl+C) rồi khởi động lại
python app.py
```

Console hiện thế này là OK:

```
Loading cookies...
  cookie_ankiweb.txt: OK
  cookie_ankiuser.txt: OK
Total: 2 cookie(s) loaded.
```

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách sửa |
|---|---|---|
| `not found` | File cookie không đúng vị trí | Đặt file cùng thư mục với `app.py` |
| Decks rỗng / 500 error | Cookie `ankiweb.net` hết hạn | Lấy lại Bước 1 |
| `Failed to load study cards` | Thiếu cookie `ankiuser.net` | Lấy lại Bước 2 |

## Tóm tắt nhanh

```
1. ankiweb.net (trang deck list) → Cookie Editor → Export as JSON → cookie_ankiweb.txt
2. ankiuser.net (bấm vào 1 deck) → Cookie Editor → Export as JSON → cookie_ankiuser.txt
3. Restart python app.py
```
