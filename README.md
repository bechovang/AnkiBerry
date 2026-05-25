# AnkiBerry

**AnkiWeb Super Lite** - Ứng dụng web học flashcard AnkiWeb tối giản, thiết kế riêng cho BlackBerry 10 (Classic, Q10, Passport) và các trình duyệt cũ.

## Tổng quan

AnkiBerry là một Flask proxy chuyển giao tiếp protobuf của AnkiWeb sang JSON, kết hợp với giao diện web siêu nhẹ tương thích ES5. Ứng dụng cho phép học flashcard Anki trên các thiết bị có trình duyệt cũ không thể truy cập AnkiWeb trực tiếp.

## Kiến trúc

```
BlackBerry 10 Browser
        |
     HTTP / JSON
        |
  Flask Proxy (app.py)  <--- json cookie.txt
        |
  HTTPS / Protobuf
        |
  ankiweb.net / ankiuser.net
```

| Thành phần | Mô tả |
|---|---|
| `app.py` | Flask server proxy - chuyển protobuf sang JSON |
| `templates/index.html` | Giao diện web ES5 thuần, tối ưu cho màn hình vuông 1:1 |
| `json cookie.txt` | Cookie session AnkiWeb (không commit vào repo) |
| `ankiweb_pb2.py` | Protobuf bindings cho AnkiWeb API (cần có sẵn) |

## Tính năng

- **Danh sách bộ thẻ** - Xem tất cả deck với số lượng thẻ mới/đang học/cần ôn
- **Học thẻ** - Lật thẻ, xem câu hỏi/đáp án, chấm điểm (Again/Hard/Good/Easy)
- **Điều hướng bàn phím vật lý** - Tối ưu cho bàn phím QWERTY BlackBerry
- **Tương thích BB10** - ES5 thuần, không framework, không CSS variables, không font ngoài
- **Màn hình vuông** - Tối ưu layout cho 720x720 (Q10, Classic) và 1440x1440 (Passport)
- **Truy cập LAN** - Chạy trên `0.0.0.0:5000`, thiết bị cùng mạng có thể truy cập

## Yêu cầu

- Python 3
- File `ankiweb_pb2.py` (protobuf đã compile từ `ankiweb.proto`)

## Cài đặt

```bash
pip install -r requirements.txt
```

Nếu chưa có file protobuf:
```bash
protoc --python_out=. ankiweb.proto
```

## Chuẩn bị Cookie

App cần cookie từ cả `ankiweb.net` và `ankiuser.net`. Cách đơn giản nhất:

1. Cài extension **Cookie Editor** trên Chrome
2. Đăng nhập https://ankiweb.net → Cookie Editor → Export as JSON → copy
3. Mở deck để vào https://ankiuser.net → Cookie Editor → Export as JSON → copy
4. Gộp cả 2 cookie vào file `json cookie.txt` (đặt cùng thư mục với `app.py`)

```json
[
    {
        "domain": "ankiweb.net",
        "name": "ankiweb",
        "value": "GIÁ_TRỊ_COOKIE_ANKIWEB",
        "path": "/",
        "secure": true
    },
    {
        "domain": "ankiuser.net",
        "name": "ankiweb",
        "value": "GIÁ_TRỊ_COOKIE_ANKIUSER",
        "path": "/",
        "secure": true
    }
]
```

> Hướng dẫn chi tiết kèm hình ảnh từng bước: [COOKIES.md](COOKIES.md)

## Chạy

```bash
python app.py
```

Server chạy tại `http://0.0.0.0:5000`.

### Kết nối từ BlackBerry

Tìm IP Wi-Fi của máy tính:
```bash
ipconfig
```

Mở trên BlackBerry: `http://<wifi-ip>:5000`

### Firewall

Nếu BlackBerry không truy cập được, mở port trên Windows (PowerShell Admin):
```powershell
New-NetFirewallRule -DisplayName "AnkiWeb Flask 5000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000
```

## Phím tắt

### Danh sách bộ thẻ

| Phím | Hành động |
|---|---|
| `J` / `K` | Di chuyển lên/xuống |
| `L` / `Enter` | Chọn bộ thẻ |

### Học thẻ

| Phím | Hành động |
|---|---|
| `Space` / `Enter` | Lật thẻ |
| `Y` / `1` | Again |
| `U` / `2` | Hard |
| `I` / `3` | Good |
| `O` / `4` | Easy |
| `J` / `D` | Cuộn xuống |
| `K` / `F` | Cuộn lên |
| `H` / `Backspace` | Quay lại |

## API Endpoints

| Method | Route | Mô tả |
|---|---|---|
| `GET` | `/` | Giao diện web |
| `GET` | `/api/decks` | Lấy danh sách bộ thẻ |
| `POST` | `/api/select` | Chọn bộ thẻ để học |
| `GET` | `/api/cards` | Lấy thẻ học |
| `POST` | `/api/answer` | Gửi kết quả chấm điểm |

## Deploy

### Chạy local (development)

```bash
python app.py
```

### Chạy trên server Linux (production)

Dùng `systemd` hoặc `screen`/`tmux` để giữ process sống:

```bash
# Dùng nohup (đơn giản)
nohup python3 app.py > ankiberry.log 2>&1 &

# Hoặc dùng systemd service
sudo cp ankiberry.service /etc/systemd/system/
sudo systemctl enable ankiberry
sudo systemctl start ankiberry
```

### Chạy với tunnel (truy cập từ xa)

```bash
# Serveo (không cần cài gì)
ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:5000 serveo.net

# ngrok
ngrok http 5000
```

> Ưu tiên link `http://` vì HTTPS dễ lỗi chứng chỉ trên BB10 cũ.

### Cookie hết hạn

Cookie AnkiWeb hết hạn sau ~14 ngày. Khi app báo lỗi kết nối:
1. Lấy lại cookie theo hướng dẫn [COOKIES.md](COOKIES.md)
2. Thay nội dung file `json cookie.txt`
3. Restart server

## Tài liệu

| File | Nội dung |
|---|---|
| [README_WEB.md](README_WEB.md) | Tối ưu UI cho BlackBerry 10, caveats cho browser cũ |
| [COOKIES.md](COOKIES.md) | Hướng dẫn cập nhật cookie chi tiết bằng Cookie Editor |

## License

[MIT](LICENSE)
