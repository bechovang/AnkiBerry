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
  Flask Proxy (app.py)  <--- cookie_ankiweb.txt + cookie_ankiuser.txt
        |
  HTTPS / Protobuf
        |
  ankiweb.net / ankiuser.net
```

| Thành phần | Mô tả |
|---|---|
| `app.py` | Flask server proxy - chuyển protobuf sang JSON |
| `templates/index.html` | Giao diện web ES5 thuần, tối ưu cho màn hình vuông 1:1 |
| `cookie_ankiweb.txt` | Cookie ankiweb.net (Cookie Editor export, không commit) |
| `cookie_ankiuser.txt` | Cookie ankiuser.net (Cookie Editor export, không commit) |
| `ankiweb_pb2.py` | Protobuf bindings cho AnkiWeb API (cần có sẵn) |

## Tính năng

- **Danh sách bộ thẻ** - Xem tất cả deck với số lượng thẻ mới/đang học/cần ôn
- **Học thẻ** - Lật thẻ, xem câu hỏi/đáp án, chấm điểm (Again/Hard/Good/Easy)
- **Hỗ trợ Âm thanh & Hình ảnh (Media Proxy)** - Tự động tải và stream ngược các tệp âm thanh (MP3, WAV, OGG,...) và hình ảnh trực tiếp từ AnkiWeb qua Flask proxy để vượt qua hạn chế bảo mật SSL/Cookie của trình duyệt cũ.
- **Tự động Phát Âm Thanh (Autoplay)** - Tự động phát âm thanh của thẻ ngay khi tải câu hỏi và khi lật xem đáp án, hỗ trợ học ngoại ngữ cực kỳ mượt mà.
- **Tự động chuyển đổi thẻ `[sound:...]`** - Chuyển đổi trực tiếp các thẻ âm thanh thô của Anki sang thẻ HTML5 `<audio>` chuẩn trên backend, hiển thị thanh điều khiển đẹp mắt và tương thích hoàn toàn với ES5.
- **Điều hướng bàn phím vật lý** - Tối ưu cho bàn phím QWERTY BlackBerry
- **Tương thích BB10** - ES5 thuần, không framework, không CSS variables, không font ngoài
- **Màn hình vuông** - Tối ưu layout cho 720x720 (Q10, Classic) và 1440x1440 (Passport)
- **Truy cập LAN** - Chạy trên `0.0.0.0:5000`, thiết bị cùng mạng có thể truy cập

## Yêu cầu

- Python 3
- File `ankiweb_pb2.py` (protobuf đã compile từ `ankiweb.proto`)

## Cài đặt

```bash
git clone https://github.com/bechovang/AnkiBerry.git
cd AnkiBerry
pip install -r requirements.txt
```

## Chuẩn bị Cookie

App cần 2 file cookie (đặt cùng thư mục với `app.py`):

| File | Lấy ở đâu |
|---|---|
| `cookie_ankiweb.txt` | Đăng nhập https://ankiweb.net → Cookie Editor → Export as JSON → lưu |
| `cookie_ankiuser.txt` | Mở deck vào https://ankiuser.net → Cookie Editor → Export as JSON → lưu |

Dùng extension **Cookie Editor** trên Chrome, bấm Export as JSON rồi lưu thẳng vào file tương ứng. Không cần sửa gì thêm.

> Hướng dẫn chi tiết từng bước: [COOKIES.md](COOKIES.md)

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
| `Space` / `L` / `Enter` | Lật thẻ / Kích hoạt phần tử đang được chọn (ví dụ: nút rating) |
| `R` | Phát lại âm thanh (Replay Audio) của thẻ |
| `Y` / `1` | Again |
| `U` / `2` | Hard |
| `I` / `3` | Good |
| `O` / `4` | Easy |
| `F` / `J` | Di chuyển tiêu điểm xuống dưới (Câu hỏi $\rightarrow$ Đáp án $\rightarrow$ Nút chấm điểm) |
| `D` / `K` | Di chuyển tiêu điểm lên trên (Nút chấm điểm $\rightarrow$ Đáp án $\rightarrow$ Câu hỏi) |
| `H` / `Backspace` | Quay lại danh sách bộ thẻ |

> [!NOTE]
> Phím `D`/`F` và `J`/`K` trong màn hình học thẻ đã được đồng bộ hóa thành cơ chế **State-based focus**, vẽ viền xanh sky-blue phát sáng bao quanh vùng đang học. Khi di chuyển, hệ thống tự động tính toán tọa độ hình học DOM và cuộn màn hình mượt mà trên cả Laptop (window viewport) lẫn trình duyệt WebKit của BlackBerry 10.

> [!TIP]
> - **Chống chạm nhầm khi vuốt**: Hệ thống tích hợp bộ lọc cử chỉ ở Capture Phase, tự động chặn đứng các sự kiện chạm nhầm (ghost clicks) khi bạn đang vuốt cuộn màn hình trên các thiết bị di động cảm ứng cũ (như BB10).
> - **Khi bật Bộ gõ tiếng Việt (Telex/VNI)**: Phím `D` gõ nhanh có thể bị IME Telex hóa thành chữ `Đ` (keyCode 229). Để học thẻ ổn định và không bị gián đoạn, hãy sử dụng phím **`J`** (xuống) và **`K`** (lên) để di chuyển tiêu điểm học thẻ cực kỳ trơn tru.

## API Endpoints

| Method | Route | Mô tả |
|---|---|---|
| `GET` | `/` | Giao diện web |
| `GET` | `/api/decks` | Lấy danh sách bộ thẻ |
| `POST` | `/api/select` | Chọn bộ thẻ để học |
| `GET` | `/api/cards` | Lấy thẻ học |
| `POST` | `/api/answer` | Gửi kết quả chấm điểm |
| `GET` | `/study/<path:filename>` và `/<path:filename>` | Proxy tải & truyền ngược dữ liệu âm thanh/hình ảnh từ AnkiWeb |

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
2. Ghi đè 2 file `cookie_ankiweb.txt` và `cookie_ankiuser.txt`
3. Restart server

## Tài liệu

| File | Nội dung |
|---|---|
| [README_WEB.md](README_WEB.md) | Tối ưu UI cho BlackBerry 10, caveats cho browser cũ |
| [COOKIES.md](COOKIES.md) | Hướng dẫn cập nhật cookie chi tiết bằng Cookie Editor |

## License

[MIT](LICENSE)
