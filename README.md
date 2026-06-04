# Thinking Arena 🏟️



Web app luyện kỹ năng tư duy và giao tiếp mỗi ngày — **Streamlit** + **Google Gemini API** (tuỳ chọn).



## Mục tiêu



Rèn: giải quyết vấn đề, ra quyết định, phản biện, nói rõ trọng tâm, thuyết phục và ứng biến trong tình huống thật.



---



## Bắt đầu nhanh (không cần biết lập trình)



Làm lần lượt 4 bước sau:



1. **Cài Python** (bản 3.10 trở lên) từ [python.org](https://www.python.org/downloads/) — khi cài trên Windows, tick **“Add Python to PATH”**.

2. Mở **Terminal** (Windows: PowerShell) → vào thư mục `thinking-arena` → chạy lệnh cài thư viện (xem mục [Cài đặt](#cài-đặt) bên dưới).

3. Chạy `streamlit run app.py` → trình duyệt mở `http://localhost:8501`.

4. Vào **Practice** → bấm **Dùng tình huống demo** (không cần API key để thử).



Muốn AI chấm thật theo câu trả lời của bạn → thêm **GEMINI_API_KEY** (mục [Cấu hình API key](#cấu-hình-api-key-local)).



---



## Bạn cần chuẩn bị gì



| Thứ | Bắt buộc? | Ghi chú |

|-----|-----------|---------|

| Python 3.10+ | Có | Để chạy app trên máy |

| Kết nối Internet | Có | Cài thư viện; gọi Gemini khi dùng AI thật |

| Trình duyệt (Chrome, Edge, Safari…) | Có | App chạy trong trình duyệt |

| GEMINI_API_KEY | Không | Không có vẫn dùng được **chế độ demo** |



Lấy API key miễn phí (Google AI Studio): [aistudio.google.com/apikey](https://aistudio.google.com/apikey)



---



## Cấu trúc thư mục



```

thinking-arena/

  app.py                 ← file chính, Streamlit chạy file này

  requirements.txt       ← danh sách thư viện cần cài

  README.md

  .streamlit/

    config.toml

    secrets.toml.example ← mẫu cấu hình API key

  src/

    schemas.py           # Kiểu dữ liệu (Pydantic)

    prompts.py           # Prompt cho AI

    gemini_client.py     # Gọi Gemini API

    demo_data.py         # Dữ liệu demo

    ui.py                # Giao diện

    utils.py             # Phiên luyện, xuất Markdown

    styles.py            # Giao diện mobile-first

```



---



## Cài đặt



Mở terminal trong thư mục `thinking-arena`, chạy **từng khối** (copy cả khối dán vào PowerShell):



```powershell

cd đường-dẫn-tới\thinking-arena

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

```



**macOS / Linux** — thay dòng activate:



```bash

cd đường-dẫn-tới/thinking-arena

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

```



Nếu lệnh `python` không chạy, thử `py` (Windows) hoặc `python3`.



### Thư viện trong `requirements.txt`



| Gói | Vai trò (đơn giản) |

|-----|---------------------|

| `streamlit` | Giao diện web của app |

| `pydantic` | Kiểm tra dữ liệu AI trả về đúng định dạng |

| `google-genai` | Kết nối Google Gemini |



Phiên bản tối thiểu đã ghi trong file; không cần chỉnh tay trừ khi bạn biết mình đang làm gì.



---



## Cấu hình API key (local)



**Cách 1 — File secrets (khuyên dùng khi chạy `streamlit run`):**



```powershell

# Windows PowerShell — trong thư mục thinking-arena

copy .streamlit\secrets.toml.example .streamlit\secrets.toml

```



```bash

# macOS / Linux

cp .streamlit/secrets.toml.example .streamlit/secrets.toml

```



Mở `.streamlit/secrets.toml` bằng Notepad / VS Code, thay key:



```toml

GEMINI_API_KEY = "dán-key-của-bạn-vào-đây"

GEMINI_MODEL = "gemini-2.5-flash"   # tuỳ chọn, có thể bỏ dòng này

```



**Cách 2 — Biến môi trường (một phiên terminal):**



```powershell

# Windows PowerShell

$env:GEMINI_API_KEY = "dán-key-của-bạn-vào-đây"

streamlit run app.py

```



```bash

# macOS / Linux

export GEMINI_API_KEY="dán-key-của-bạn-vào-đây"

streamlit run app.py

```



> `.streamlit/secrets.toml` và `.env` **không** được commit lên Git — đã có trong `.gitignore`.



Sau khi thêm key, **tắt app (Ctrl+C) và chạy lại** `streamlit run app.py` để Streamlit đọc key mới.



---



## Chạy local



Đảm bảo đã `activate` môi trường `.venv` (nếu dùng venv), rồi:



```bash

streamlit run app.py

```



Mở trình duyệt: **http://localhost:8501**



Sidebar (cột trái): **Home**, **Practice**, **Result**, **About**.



### Chế độ demo (không API key)



1. Sidebar → **Practice**

2. Bấm **Dùng tình huống demo**

3. Chọn tình huống → viết câu trả lời → **Chấm câu trả lời**



Feedback là **mẫu cố định**, không phân tích câu bạn vừa gõ — chỉ để làm quen flow.



---



## Đưa lên GitHub & Deploy Streamlit Community Cloud

**Quan trọng:** Thư mục gốc của repo GitHub phải chứa `app.py`, `requirements.txt` và thư mục `src/` **cùng một cấp** (đẩy nội dung thư mục `thinking-arena/`, không đẩy nhầm thư mục cha).

File `.streamlit/secrets.toml` (key thật) **không** được commit — đã có trong `.gitignore`. Chỉ commit `secrets.toml.example`.

### Bước 1 — Tạo repo trên GitHub

1. Đăng nhập [github.com](https://github.com).
2. **New repository** → đặt tên (vd: `thinking-arena`) → **Create repository** (chưa cần README nếu bạn đã có code local).

### Bước 2 — Push code từ máy

Mở terminal trong thư mục `thinking-arena` (nơi có `app.py`). Xem [lệnh Git ở cuối README](#lệnh-git-đẩy-code-lên-github) hoặc dùng danh sách lệnh agent gửi kèm.

Trước khi `git add`, kiểm tra không có key thật:

```powershell
git status
# Không được thấy .streamlit/secrets.toml trong "Changes to be committed"
```

### Bước 3 — Deploy trên Streamlit Community Cloud

1. Vào [share.streamlit.io](https://share.streamlit.io) → đăng nhập bằng GitHub.
2. **Create app** (hoặc **New app**).
3. **Repository:** chọn repo vừa push.
4. **Branch:** `main` (hoặc `master` tùy repo).
5. **Main file path:** `app.py`
6. **App URL** (tuỳ chọn) → **Deploy** lần đầu (có thể chưa có AI cho đến bước Secrets).

### Bước 4 — Thêm Secrets trên Cloud

1. Mở app đã deploy → **⚙️ Settings** (góc phải) → **Secrets**.
2. Dán (thay key thật của bạn):

```toml
GEMINI_API_KEY = "your-gemini-api-key"
GEMINI_MODEL = "gemini-2.5-flash"
```

3. **Save** → **Reboot app** (hoặc **Manage app** → **Reboot**).

Sau reboot: vào **Practice** → phải thấy nút **Tạo 3 tình huống** (không chỉ demo). Trên **Home** hiện “Gemini API đã cấu hình”.

### Bước 5 — Không có API key trên Cloud

App vẫn chạy: **Practice** → **Dùng tình huống demo**. Trên UI có cảnh báo thân thiện hướng dẫn thêm Secrets.

### Cấu trúc repo & import

- Entry point: `app.py` (Streamlit Cloud chạy file này).
- Import dạng `from src.ui import ...` — `app.py` tự thêm thư mục repo vào `sys.path` để deploy ổn định.
- Dependencies: `requirements.txt` (Cloud cài tự động).

### Lệnh Git — đẩy code lên GitHub

Thay `YOUR_USER` và `YOUR_REPO` bằng tên GitHub của bạn:

```powershell
cd đường-dẫn-tới\thinking-arena
git init
git add .
git status
git commit -m "Initial commit: Thinking Arena"
git branch -M main
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

Nếu repo đã có commit trên GitHub, có thể cần `git pull origin main --rebase` trước khi push.

---



## Session & reset



Dữ liệu phiên nằm trong bộ nhớ trình duyệt (không database): tình huống, câu trả lời, feedback, v.v.



Sidebar → **Reset phiên** → xóa hết và bắt đầu lại (giữ trang hiện tại).



---



## Tính năng chính



| Trang | Mô tả |

|-------|--------|

| Home | Giới thiệu + **Bắt đầu luyện hôm nay** |

| Practice | Tạo/chọn tình huống → trả lời → chấm → phản biện |

| Result | Tổng kết + copy / tải Markdown |

| About | Thông tin app |



---



## Manual Test Checklist



Dùng checklist này sau mỗi lần sửa code hoặc trước khi demo. Đánh dấu `[x]` khi pass.



**Chuẩn bị:** Đã chạy `streamlit run app.py`, trình duyệt mở `http://localhost:8501`.



---



### 1. Mở app khi chưa có API key



- [ ] **Bước:** Đảm bảo **không** có `GEMINI_API_KEY` trong `secrets.toml` và **không** set biến môi trường → chạy app.

- [ ] **Kỳ vọng:** App mở bình thường; vào **Practice** thấy cảnh báo kiểu *“chưa cấu hình Gemini API key… chế độ demo”*; **không** có nút **Tạo 3 tình huống** (chỉ khi có key).



---



### 2. Dùng demo mode



- [ ] **Bước:** **Practice** → **Dùng tình huống demo**.

- [ ] **Kỳ vọng:** Hiện **3** card tình huống; toast *“Đã tải 3 tình huống demo”*; banner **Dữ liệu DEMO** xuất hiện sau khi chấm.



---



### 3. Thêm API key và gọi Gemini thật



- [ ] **Bước:** Thêm key vào `secrets.toml` (hoặc `$env:GEMINI_API_KEY`) → **tắt app (Ctrl+C)** → chạy lại `streamlit run app.py`.

- [ ] **Bước:** **Practice** → mở **Thiết lập phiên luyện** → **Tạo 3 tình huống** (đợi vài giây–vài chục giây).

- [ ] **Kỳ vọng:** 3 tình huống **khác** demo; không banner DEMO khi chấm; lỗi mạng/key hiển thị rõ nếu key sai.



---



### 4. Tạo tình huống theo category



- [ ] **Bước:** Có API key → chọn **Nhóm chủ đề** (vd: Marketing) → để **Keyword** trống → **Tạo 3 tình huống**.

- [ ] **Kỳ vọng:** 3 tình huống liên quan chủ đề; mỗi card có badge độ khó + kỹ năng.



---



### 5. Tạo tình huống bằng keyword tự nhập



- [ ] **Bước:** Nhập keyword (vd: `TikTok Shop`, `trễ deadline`) → **Tạo 3 tình huống** (hoặc **Tạo lại tình huống khác**).

- [ ] **Kỳ vọng:** Bối cảnh/câu hỏi phản ánh keyword; bộ tình huống có thể khác lần trước.



---



### 6. Chọn tình huống



- [ ] **Bước:** Bấm **✓ Chọn tình huống này** trên một card.

- [ ] **Kỳ vọng:** Form **Câu trả lời của bạn** + **Chấm câu trả lời**; card được chọn có viền/highlight; nút **← Chọn tình huống khác** quay lại danh sách.



---



### 7. Gửi câu trả lời quá ngắn



- [ ] **Bước:** Gõ ít hơn **20 ký tự** (vd: `ok` hoặc `em nghĩ vậy`) → **Chấm câu trả lời**.

- [ ] **Kỳ vọng:** Thông báo lỗi *“quá ngắn (cần ít nhất 20 ký tự)”*; **không** có feedback mới.



---



### 8. Gửi câu trả lời hợp lệ



- [ ] **Bước:** Viết ≥ 20 ký tự, có quyết định/lý do (vd 3–5 câu như trong họp) → **Chấm câu trả lời**.

- [ ] **Kỳ vọng:** Spinner chấm → hiện feedback (điểm, insight, câu mẫu…); demo = mẫu cố định; AI thật = nội dung khác theo câu bạn gõ.



---



### 9. Xem feedback



- [ ] **Bước:** Sau khi chấm, cuộn trên **Practice**.

- [ ] **Kỳ vọng:** Điểm tổng nổi bật → **Vì sao người nghe dễ phớt lờ** → expander 8 tiêu chí → **Nói lại tốt hơn** (khối copy) → **Câu chốt** (quote card) → **AI phản biện bạn** + nút **Trả lời phản biện này**.



---



### 10. Trả lời counter question



- [ ] **Bước:** **Trả lời phản biện này** → nhập câu phản biện ≥ 20 ký tự → **Chấm câu trả lời phản biện**.

- [ ] **Kỳ vọng:** Điểm phản biện + bản mẫu + lời khuyên cuối; thử dưới 20 ký tự → lỗi tương tự bước 7.



---



### 11. Xem Result



- [ ] **Bước:** Sidebar → **Result** (sau khi đã có feedback).

- [ ] **Kỳ vọng:** Tổng kết điểm, bài học, phần phản biện (nếu đã chấm); nếu chưa luyện → thông báo trống + **Bắt đầu luyện ở Practice**.



---



### 12. Tải Markdown



- [ ] **Bước:** Trên **Result** → **📋 Copy nội dung tổng kết** và/hoặc **Tải kết quả dạng Markdown**.

- [ ] **Kỳ vọng:** Copy được vào clipboard; file `thinking_arena_result.md` tải về; expander **Xem trước** khớp nội dung.



---



### 13. Reset phiên luyện



- [ ] **Bước:** Sidebar → **Reset phiên** (một lần bấm là xóa ngay).

- [ ] **Kỳ vọng:** Mất tình huống / câu trả lời / feedback; **Practice** về trạng thái ban đầu; **Result** trống hoặc nhắc luyện lại.



---



### 14. Kiểm tra trên mobile



- [ ] **Bước (chọn một):**

  - Điện thoại cùng Wi-Fi: mở `http://<IP-máy-tính>:8501` (IP hiện khi chạy Streamlit, vd `192.168.x.x:8501`), hoặc

  - Trên máy tính: Chrome/Edge → F12 → biểu tượng điện thoại (responsive) → rộng ~375px.

- [ ] **Kỳ vọng:** Không tràn ngang; chữ đọc được; nút chính full-width; không bảng rộng; Home / Practice / Feedback cuộn mượt.



---



## Gặp sự cố thường gặp



| Triệu chứng | Gợi ý xử lý |

|-------------|-------------|

| `python` không nhận lệnh | Cài lại Python, tick **Add to PATH**; hoặc dùng `py -m pip` |

| `streamlit` không nhận lệnh | Chạy lại `pip install -r requirements.txt` trong `.venv` đã activate |

| Vẫn báo thiếu API key sau khi thêm | Tắt app (Ctrl+C), chạy lại `streamlit run app.py` |

| **Tạo 3 tình huống** lỗi | Kiểm tra key đúng, có mạng, quota Gemini; thử model trong `secrets.toml` |

| Trang trắng / lỗi ở điện thoại | Dùng đúng URL `http://IP:8501`, cùng mạng Wi-Fi, tắt firewall chặn cổng 8501 |



---



## License



Private / educational use.

