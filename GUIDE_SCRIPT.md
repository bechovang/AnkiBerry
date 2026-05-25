# AnkiBerry - Kịch Bản Hướng Dẫn Sử Dụng Chi Tiết / Comprehensive User Guide & Interactive Script

File hướng dẫn này chứa kịch bản từng bước (Bản Tiếng Việt & Bản Tiếng Anh) giúp bạn cài đặt, cấu hình và trải nghiệm AnkiBerry một cách dễ dàng nhất trên máy tính và thiết bị BlackBerry 10.

---

# PHẦN 1: BẢN TIẾNG VIỆT (VIETNAMESE VERSION)

## 🎬 Cảnh 1: Cài đặt và Chuẩn bị (Clone & Setup)

**Bước 1**: Mở Terminal (CMD / PowerShell / Bash) trên máy tính và clone mã nguồn dự án về máy:
```bash
git clone https://github.com/bechovang/AnkiBerry.git
cd AnkiBerry
```

**Bước 2**: Cài đặt các thư viện cần thiết (yêu cầu máy tính đã cài đặt Python 3):
```bash
pip install -r requirements.txt
```

---

## 🎬 Cảnh 2: Lấy Cookie AnkiWeb và tạo các file cấu hình

AnkiBerry cần cookie để thay mặt bạn giao tiếp với máy chủ AnkiWeb. Bạn cần tạo 2 file text chứa cookie dạng JSON đặt tại thư mục gốc của dự án.

**Bước 1: Lấy Cookie AnkiWeb (ankiweb.net)**
1. Mở trình duyệt Chrome/Firefox trên máy tính và cài đặt tiện ích mở rộng **Cookie Editor**.
2. Truy cập `https://ankiweb.net` và đăng nhập tài khoản Anki của bạn.
3. Nhấp vào biểu tượng **Cookie Editor** trên thanh công cụ $\rightarrow$ Chọn **Export** $\rightarrow$ Chọn **JSON**.
4. Tạo một file mới tên là `cookie_ankiweb.txt` đặt tại thư mục dự án và dán (Paste) toàn bộ nội dung vừa copy vào đó.

**Bước 2: Lấy Cookie AnkiUser (ankiuser.net)**
1. Trên trình duyệt máy tính, nhấp vào một bộ thẻ bất kỳ để bắt đầu học (trình duyệt sẽ chuyển hướng sang trang `https://ankiuser.net/study/...`).
2. Nhấp vào biểu tượng **Cookie Editor** $\rightarrow$ Chọn **Export** $\rightarrow$ Chọn **JSON**.
3. Tạo một file mới tên là `cookie_ankiuser.txt` đặt tại thư mục dự án và dán (Paste) nội dung vừa copy vào đó.

---

## 🎬 Cảnh 3: Khởi chạy Máy chủ Proxy (Start Server)

**Bước 1**: Từ cửa sổ Terminal tại thư mục dự án, gõ lệnh khởi động máy chủ Flask:
```bash
python app.py
```
*Màn hình sẽ hiển thị thông báo server đang chạy thành công tại địa chỉ `http://0.0.0.0:5000`.*

**Bước 2**: Tìm IP Wi-Fi nội bộ của máy tính.
- Trên Windows (PowerShell/CMD): Gõ lệnh `ipconfig` và tìm dòng **IPv4 Address** của adapter mạng Wi-Fi (Ví dụ: `192.168.1.6`).
- Trên macOS/Linux: Gõ lệnh `ifconfig` hoặc `ip a`.

---

## 🎬 Cảnh 4: Kết nối và Trải nghiệm trên BlackBerry 10

**Bước 1**: Đảm bảo điện thoại BlackBerry và máy tính của bạn đang **kết nối chung một mạng Wi-Fi**.

**Bước 2**: 
1. Mở Trình duyệt (Browser) mặc định trên BlackBerry 10.
2. Truy cập vào địa chỉ IP của máy tính kèm cổng 5000:
   `http://<IP_MÁY_TÍNH>:5000` (Ví dụ: `http://192.168.1.6:5000`).
   
> [!IMPORTANT]
> **Lưu ý chống Cache trình duyệt**: 
> Browser của BlackBerry 10 có xu hướng lưu cache rất nặng. Khi truy cập lần đầu hoặc sau khi cập nhật giao diện, hãy truy cập bằng **Tab ẩn danh (Incognito Tab)** hoặc vào Cài đặt trình duyệt chọn **Xóa lịch sử và bộ nhớ đệm (Clear History and Cache)** để chắc chắn tải về phiên bản giao diện mới nhất.

---

## 🎬 Cảnh 5: Giới thiệu Phím tắt & Tính năng đặc biệt trên BlackBerry

Màn hình cảm ứng của BlackBerry 10 khá nhỏ, do đó AnkiBerry đã được tối ưu hóa vượt bậc để bạn có thể học thẻ **100% bằng bàn phím vật lý QWERTY** mà không cần chạm màn hình:

### 1. Màn hình chọn bộ thẻ (Deck List Screen)
* **Di chuyển lên/xuống**: Nhấn phím **`K`** (đi lên) hoặc phím **`J`** (đi xuống). Bạn sẽ thấy một viền xanh sky-blue phát sáng bao quanh bộ thẻ đang chọn.
* **Mở bộ thẻ**: Nhấn phím **`L`** hoặc phím **`Enter`** để bắt đầu học bộ thẻ được chọn.

### 2. Màn hình học thẻ (Study Screen)
* **Di chuyển tiêu điểm học (Focus)**: 
  - Nhấn phím **`K`** để di chuyển tiêu điểm lên phía trên (Ratings $\rightarrow$ Đáp án $\rightarrow$ Câu hỏi).
  - Nhấn phím **`J`** để di chuyển tiêu điểm xuống phía dưới (Câu hỏi $\rightarrow$ Đáp án $\rightarrow$ Ratings).
  *Khi tiêu điểm di chuyển, vùng tương ứng sẽ **tự động vẽ viền xanh dương phát sáng (#38bdf8)** vô cùng nổi bật, đồng thời màn hình tự động cuộn (scroll) mượt mà đưa vùng đó vào trung tâm hiển thị.*
* **Lật thẻ / Kích hoạt nhanh (Space / Enter / L)**:
  - Khi đang ở ô Câu hỏi: Nhấn **`Space`**, **`Enter`** hoặc **`L`** để lật thẻ và hiện đáp án.
  - Khi đang dùng phím `J/K` để di chuyển tiêu điểm ảo tới các nút bấm: Nhấn **`Space`** hoặc **`Enter`** sẽ tự động kích hoạt (Click) chính xác nút đó (Lật thẻ hoặc Chấm điểm tương ứng).
* **Phát lại âm thanh (Replay Audio)**:
  - Nhấn phím **`R`** bất kỳ lúc nào để phát lại âm thanh của thẻ (tự động phát âm thanh đáp án nếu đã lật, hoặc âm thanh câu hỏi nếu chưa lật).
* **Phím tắt Chấm điểm trực tiếp (Không cần chọn tiêu điểm)**:
  - Khi đáp án đã hiển thị, bạn có thể gõ nhanh các phím sau để chấm điểm và chuyển sang thẻ tiếp theo:
    - **`Y`** hoặc phím số **`1`**: Chọn **Again** (Học lại)
    - **`U`** hoặc phím số **`2`**: Chọn **Hard** (Khó)
    - **`I`** hoặc phím số **`3`**: Chọn **Good** (Tốt)
    - **`O`** hoặc phím số **`4`**: Chọn **Easy** (Dễ)
* **Quay lại danh sách bộ thẻ**: Nhấn phím **`H`** hoặc phím **`Backspace`**.

### 🌟 3. Các cải tiến nâng cấp cao cấp
- **Tương thích hoàn hảo Bộ gõ Tiếng Việt**: Cặp phím điều hướng **`J/K`** được thiết kế đặc thù để hoàn toàn miễn nhiễm với Telex/IME tiếng Việt (tránh hiện tượng phím `D` bị gõ nhầm thành chữ `Đ` do bộ gõ).
- **Chống chạm nhầm khi vuốt cuộn (Touch Scroll Filter)**: Tích hợp bộ lọc cảm ứng Capture Phase cao cấp, tự động chặn đứng các sự kiện click chạm nhầm (ghost clicks) khi bạn đang vuốt cuộn đọc nội dung thẻ dài bị lag trên BlackBerry 10.
- **Proxy Truyền Ngược Âm Thanh & Tự Động Phát (Autoplay)**: Tự động tải và stream ngược các tệp âm thanh nhị phân (MP3, WAV, OGG,...) và hình ảnh trực tiếp từ AnkiWeb qua Flask proxy nội bộ, giải quyết triệt để lỗi SSL/Cookie của trình duyệt cũ. Backend tự động chuyển đổi định dạng thô `[sound:...]` thành thẻ HTML5 `<audio>` chuẩn, kết hợp JavaScript kích hoạt tự động phát khi hiển thị câu hỏi/đáp án vô cùng mượt mà.

---
---

# PART 2: ENGLISH VERSION (BẢN TIẾNG ANH)

## 🎬 Scene 1: Clone & Setup

**Step 1**: Open your Terminal (CMD / PowerShell / Bash) on your computer and clone the repository:
```bash
git clone https://github.com/bechovang/AnkiBerry.git
cd AnkiBerry
```

**Step 2**: Install all the required dependencies (Python 3 is required):
```bash
pip install -r requirements.txt
```

---

## 🎬 Scene 2: Extracting AnkiWeb Cookies

AnkiBerry acts as a proxy and needs your session cookies to communicate with AnkiWeb servers. You need to create 2 JSON text files in the project root directory.

**Step 1: Get AnkiWeb Cookies (ankiweb.net)**
1. Open Chrome/Firefox on your PC and install the **Cookie Editor** extension.
2. Visit `https://ankiweb.net` and log in to your Anki account.
3. Click the **Cookie Editor** extension icon $\rightarrow$ Click **Export** $\rightarrow$ Click **JSON**.
4. Create a new file named `cookie_ankiweb.txt` in the project root directory and paste the copied content inside.

**Step 2: Get AnkiUser Cookies (ankiuser.net)**
1. On your PC browser, click on any deck to enter the study page (it will redirect to `https://ankiuser.net/study/...`).
2. Click the **Cookie Editor** extension icon $\rightarrow$ Click **Export** $\rightarrow$ Click **JSON**.
3. Create a new file named `cookie_ankiuser.txt` in the project root directory and paste the copied content inside.

---

## 🎬 Scene 3: Launching the Proxy Server

**Step 1**: Run the Flask development server from your terminal:
```bash
python app.py
```
*The terminal will notify you that the server is running on `http://0.0.0.0:5000`.*

**Step 2**: Find your computer's local Wi-Fi IP address.
- On Windows (PowerShell/CMD): Run `ipconfig` and find the **IPv4 Address** under your active Wi-Fi adapter (e.g., `192.168.1.6`).
- On macOS/Linux: Run `ifconfig` or `ip a`.

---

## 🎬 Scene 4: Connecting & Testing on BlackBerry 10

**Step 1**: Make sure your BlackBerry phone and your host PC are **connected to the same Wi-Fi network**.

**Step 2**: 
1. Open the default Web Browser on your BlackBerry 10 device.
2. Enter your host PC's IP address with port 5000:
   `http://<PC_IP_ADDRESS>:5000` (e.g., `http://192.168.1.6:5000`).
   
> [!IMPORTANT]
> **Anti-Caching Tip**: 
> The BlackBerry 10 WebBrowser caches static assets aggressively. To ensure you load the latest state-based interactive layout, access the app via a **Private/Incognito Tab** or clear your browser history via **Browser Settings $\rightarrow$ Privacy and Security $\rightarrow$ Clear History and Cache**.

---

## 🎬 Scene 5: Keyboard Shortcuts & Premium Navigation Controls

AnkiBerry is heavily optimized for physical QWERTY keyboards, allowing **100% keyboard-only study sessions** without ever touching the screen:

### 1. Deck Selection Screen
* **Navigate Up/Down**: Press **`K`** (move focus up) or **`J`** (move focus down). The selected deck card will be highlighted with a glowing sky-blue border.
* **Open/Select Deck**: Press **`L`** or **`Enter`** to start studying the selected deck.

### 2. Flashcard Study Screen
* **Move Focus Area**:
  - Press **`K`** to move the focus upward (Ratings $\rightarrow$ Answer $\rightarrow$ Question).
  - Press **`J`** to move the focus downward (Question $\rightarrow$ Answer $\rightarrow$ Ratings).
  *The focused element will automatically receive a **glowing sky-blue border highlight (#38bdf8)** and the viewport will smoothly scroll the active card component into center view.*
* **Reveal Card / Action Trigger (Space / Enter / L)**:
  - When focused on the Question area: Press **`Space`**, **`Enter`**, or **`L`** to flip the card and reveal the answer.
  - When focused on any button (Reveal or Score rating): Pressing **`Space`** or **`Enter`** will automatically trigger a click event on that active button.
* **Replay Card Audio**:
  - Press **`R`** at any time to replay the card's audio (automatically replays answer audio if revealed, or question audio if not).
* **Direct Rating Shortcuts (No focus required)**:
  - Once the answer is revealed, you can press these QWERTY keys directly to score the card and transition to the next card immediately:
    - **`Y`** or number **`1`**: Score **Again**
    - **`U`** or number **`2`**: Score **Hard**
    - **`I`** or number **`3`**: Score **Good**
    - **`O`** or number **`4`**: Score **Easy**
* **Back to Deck List**: Press **`H`** or **`Backspace`**.

### 🌟 3. Premium Mechanical Optimizations
- **Vietnamese IME / Telex Protection**: The **`J/K`** keys are chosen as the primary navigation shortcuts to prevent key conflicts with Vietnamese Telex input methods (avoiding phím `D` from being translated into letter `Đ` by the keyboard engine).
- **Anti-Accidental Swipe Clicks (Touch Scroll Filter)**: Intercepts and filters out lag-induced ghost click events at the Capture Phase when swiping or scrolling down on long cards.
- **Secure Audio/Media Proxying & Autoplay**: Automatically downloads and proxies media resources (MP3, WAV, OGG, etc.) and images directly from AnkiWeb via the local Flask proxy to bypass strict SSL/cookie legacy WebKit limits. Translates raw `[sound:...]` card markup into standard HTML5 `<audio>` players on the fly, with native JavaScript autoplay wrapped in robust try-catch handlers.
