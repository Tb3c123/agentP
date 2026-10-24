<div align="center">

# 🚀 agentP — Developer Multi-Agent Desktop Suite
### *Nền Tảng Điều Phối Đa Tác Nhân Trí Tuệ Nhân Tạo Dành Cho Lập Trình Viên & Doanh Nghiệp*

[![Release](https://img.shields.io/badge/Release-v2.9.0-0D9488.svg?style=flat-square)](CHANGELOG.md)
[![Preflight Doctor](https://img.shields.io/badge/Pre--flight%20Doctor-7%2F7%20Criteria%20PASS-10B981.svg?style=flat-square)](scripts/preflight.py)
[![Test Suite](https://img.shields.io/badge/Quality%20Gate-83%2F83%20Tests%20PASS%20(100%25)-0284C7.svg?style=flat-square)](test/)
[![Production Quality Gate](https://img.shields.io/badge/Release%20Audit-5%2F5%20Dimensions%20APPROVED-059669.svg?style=flat-square)](reports/production_quality_gate.md)
[![Desktop Packaging](https://img.shields.io/badge/Tauri%20v2-macOS%20%7C%20Windows%20%7C%20Linux-7C3AED.svg?style=flat-square)](src-tauri/)
[![UI Design](https://img.shields.io/badge/UI%2FUX-Clean%20Light%20Mode-D97706.svg?style=flat-square)](docs/UI_UX_DESIGN_SYSTEM.md)
[![License Guard](https://img.shields.io/badge/License-Hardware--Locked%20Offline-4338CA.svg?style=flat-square)](src/services/license_guard.py)

<br/>

**[Giới Thiệu](#-giới-thiệu-tổng-quan)** •
**[Điểm Nhấn Đột Phá](#-những-tính-năng-đột-phá-cốt-lõi)** •
**[Kiến Trúc Swarm 14 Roles](#-ban-kỹ-thuật-14-chuyên-viên-ai)** •
**[Khởi Chạy Nhanh](#-khởi-chạy-nhanh-quick-start)** •
**[Kho Tài Liệu Kỹ Thuật (Docs)](#-kho-tài-liệu-hệ-thống-docs-navigator)**

<br/>

</div>

---

## 🌟 Giới Thiệu Tổng Quan

**agentP** là nền tảng máy trạm (Desktop & Local Daemon) điều phối đa tác nhân trí tuệ nhân tạo (Multi-Agent Swarm) được xây dựng dành riêng cho các kỹ sư phần mềm, kiến trúc sư hệ thống và nhà quản lý dự án.

Thay vì phải mở hàng chục cửa sổ chat rời rạc hoặc sao chép mã nguồn qua lại giữa các AI chatbot, **agentP** định hình lại toàn bộ trải nghiệm phát triển phần mềm với **Triết Lý Đơn Bàn (Single-Desk Command)**:
* Bạn chỉ làm việc và trao đổi duy nhất với **Alex (Trưởng Dự Án / Lead PM)**.
* Đội ngũ **13 Chuyên viên Kỹ thuật Hậu trường (Backstage Swarm)** tự động tiếp nhận phân rã nhiệm vụ, viết code, sửa giao diện, kiểm thử tự động và báo cáo tiến độ theo thời gian thực.
* Mọi tiến trình đều được cô lập phiên làm việc 1:1, lưu trữ bền vững trên **CSDL SQLite WAL Mode** và vận hành qua **agentP Core Daemon cục bộ** an toàn tuyệt đối.

---

## 💎 Những Tính Năng Đột Phá Cốt Lõi

### 1. 🧑‍💼 Bàn Làm Việc Điều Hành Duy Nhất (Single-Desk Command)
* **Alex (Lead PM) làm đầu mối duy nhất (SPOC)**: Nhận lệnh từ thanh chat, phân tích suy nghĩ đa chiều trong thẻ `<thinking>`, tự động phân rã User Story thành Subtask kỹ thuật.
* **Cổng Kiểm Duyệt Hổ Phách (User Checkpoint Gate)**: Bất kỳ thay đổi mã nguồn, xóa file hay merge nhánh git đều phải được Bạn trực tiếp phê duyệt tại Checkpoint màu hổ phách sang trọng `#FFFBEB`.
* **Nút Dừng Đột Ngột (Emergency Stop ESC)**: Hủy bỏ toàn bộ luồng suy nghĩ và tiến trình ngầm của các agent chỉ trong `<15ms`.

### 2. 👥 Quản Lý Nhân Sự & Phân Bổ AI Model Linh Hoạt
* Quản lý chuyên sâu **14 Chuyên viên AI** của dự án (Alex PM, Marcus BA, Maya Architect, Elena UI, David FE, Carlos BE, Lucas Senior, Viktor QA, Liam DevOps, Frank SRE, Sophia Security, Chloe Data, Sarah Docs, Oliver Perf).
* **Tuỳ chọn AI Model động (Dropdown 11 models)**: Không gán cứng! Bạn tự do gán Claude 3.7 Sonnet cho Alex, DeepSeek R1 cho Viktor QA, GPT-4o cho Lucas, Gemini 2.5 cho David FE.
* Hiển thị Session ID 1:1, đo độ trễ Latency thực tế và đồng bộ tự động vào SQLite `.agents/db.sqlite`.

### 3. 🔌 Hub Kết Nối AI Providers & 9router In-House Core Engine
* **Trang Kết Nối Toàn Cục Riêng Biệt (Global Providers Hub)**: Tái hiện chuẩn xác kiến trúc 9router với 4 phân khúc:
  * **OAuth Providers**: Claude Code CLI, Cursor IDE Bridge, Codex, Gemini CLI.
  * **Free Providers**: Antigravity Core, Qwen Code Free, Kimi Moonshot, GLM-4.
  * **API Key Providers**: OpenRouter, DeepSeek, Anthropic, OpenAI, Groq, Cerebras, Cohere.
  * **Compatible Providers**: Alibaba Custom, các endpoint OpenAI / Anthropic tương thích.
* **Dynamic Proxy & Failover**: Gateway tự thân chạy trực tiếp trong daemon (`127.0.0.1:9090`), hỗ trợ `/v1/messages` và `/v1/chat/completions`. Khi một provider bị nghẽn, hệ thống tự động chuyển mạch dự phòng (Failover Safe Guard) tức thì.
* **CLI Bridge Cho Developer**: Tự động nhận diện công cụ CLI và sinh script môi trường `.agents/bin/activate_bridge.sh` để Claude Code và Cursor kết nối trực tiếp.

### 4. 🎨 Xưởng Thiết Kế UI/UX Kép (Dual-Mode Studio)
* **Tab 1 - Tldraw Whiteboard**: Vẽ wireframe vector, sticky notes, liên kết luồng người dùng và xuất file `.tldr`.
* **Tab 2 - Onlook DOM-to-Code**: Click-to-inspect phần tử UI, chỉnh sửa màu sắc sang Clean Light Mode và đồng bộ trực tiếp vào mã nguồn thật qua cơ chế AST 2 chiều với độ trễ `<50ms`.

### 5. 📱 Mobile Remote Controller & AVD Android Runner
* Quét mã QR (`AGENTP-PAIR-7749`) để ghép đôi điện thoại qua Wi-Fi cục bộ.
* Theo dõi tiến độ Swarm, kiểm tra log và bấm phê duyệt Checkpoint Gate ngay trên điện thoại di động khi đang di chuyển.
* Tích hợp bộ điều khiển máy ảo **Android Pixel 8 Pro** (chế độ Cửa sổ GUI hoặc Headless ngầm).

### 6. 🛡️ Khóa An Toàn Antigravity Danger Zone
* Cơ chế bảo vệ dữ liệu 2 lớp: Để xóa vĩnh viễn dự án, bắt buộc phải nhập chính xác 100% tên dự án để mở khóa nút xóa.
* Thùng rác an toàn `.agents/trash/` cho phép khôi phục mọi tệp tin đã xóa trong vòng 30 ngày.

### 7. 📦 Đóng Gói Tauri v2 Desktop & Bản Quyền Phần Cứng Offline 100%
* **Desktop Shell Tauri v2 (Rust + Web)**: Tối ưu bộ nhớ siêu nhẹ `<40MB` (so với Electron `>250MB`), thời gian khởi động tức thì `<1.2s`, phân phối đa nền tảng macOS (`.dmg`), Windows (`.msi`) và Linux.
* **Khóa Bản Quyền Khóa Cứng Phần Cứng (Hardware-Locked License)**: Ký điện tử HMAC-SHA256 gắn chặt vào mã máy tính (`AP-{ARCH}-{HASH}`), chạy offline hoàn toàn không cần server xác thực.
* **Cổng Kiểm Định Chất Lượng Sản Xuất (Production Quality Gate)**: Đạt điểm tuyệt đối 5/5 tiêu chí: WCAG 2.2 AA/AAA (Alpine Teal & Tuscan Amber), SQLite WAL không vi phạm ràng buộc khoá ngoại, hiệu năng phản hồi `<15ms`, Pre-flight 7/7 và Desktop Bundle Ready.

---

## 🐝 Ban Kỹ Thuật 14 Chuyên Viên AI

```
[Alex - PM]        ──► Tiếp nhận chỉ đạo, tư duy đa chiều <thinking>, điều phối Swarm
[Marcus - BA]       ──► Rã nhỏ User Story, gán Story Points & Tiêu chí nghiệm thu DoD
[Elena - UI/UX]     ──► Thiết kế Clean Light Mode, Tldraw Canvas & Onlook Inspector
[Maya - Architect]  ──► Thiết kế CSDL SQLite WAL, Contract API & C4 Architecture
[David - FE Dev]    ──► Lập trình React 19, Tailwind CSS & State Management
[Carlos - BE Dev]   ──► Xây dựng REST API, Daemon Router & Repository Layer
[Lucas - Senior]    ──► Lập trình Core Engine, AST Sync 2 chiều & Dynamic Proxy
[Viktor - QA Lead]  ──► Kiểm thử tự động E2E, Unit Tests (56/56 Tests PASS)
[Liam - DevOps]     ──► Quản lý máy ảo AVD Pixel 8, Docker Bundle & Mobile Bridge
[Frank - SRE]       ──► Khả năng chịu lỗi, chống sập tiến trình & WAL recovery
[Sophia - Security] ──► Kiểm toán quyền truy cập, RBAC & Khóa an toàn Danger Zone
[Chloe - Data]      ──► Báo cáo KPI doanh nghiệp, xuất bảng tính Excel .csv / .xlsx
[Sarah - Docs]      ──► Biên dịch tài liệu hệ thống & Keep a Changelog
[Oliver - Perf]     ──► Tối ưu hóa độ trễ render <16.6ms & Token Prompt Caching
```

---

## ⚡ Khởi Chạy Nhanh (Quick Start)

### 1. Kiểm tra môi trường với Bác Sĩ Tiền Kiểm (Pre-flight Doctor)
```bash
python3 scripts/preflight.py
```
> *Xác nhận 7/7 tiêu chí kỹ thuật: SQLite WAL, Node.js, Git, Daemon, Flutter, AVD, và 14 AI Roles sẵn sàng 100%.*

### 2. Chạy toàn bộ bộ kiểm thử tự động (83 Tests)
```bash
python3 -m unittest discover -s test -p "test_*.py"
```
> *Tất cả 83/83 ca kiểm thử tự động chạy hoàn tất trong <0.28 giây.*

### 3. Kiểm định Cổng Chất Lượng Sản Xuất (5/5 Quality Gate)
```bash
python3 scripts/quality_gate.py
```
> *Xác nhận 5/5 chiều chất lượng: WCAG 2.2 Contrast, SQLite WAL, RAM Benchmark, Pre-flight, và Desktop Packaging.*

### 4. Kiểm tra gói đóng gói Tauri v2 Desktop
```bash
python3 scripts/package_desktop.py
```

### 5. Khởi chạy agentP Core Daemon
```bash
python3 src/daemon/router.py
```
*Mở trình duyệt và trải nghiệm giao diện làm việc tại: **[http://127.0.0.1:9090](http://127.0.0.1:9090)***

### 6. Kích hoạt CLI Bridge cho Claude Code hoặc Cursor (Tuỳ chọn)
```bash
source .agents/bin/activate_bridge.sh
```

---

## 📚 Kho Tài Liệu Hệ Thống (Docs Navigator)

Mọi chi tiết kỹ thuật sâu rộng được chuẩn hóa và lưu trữ đầy đủ trong thư mục `docs/`:

| Tài Liệu | Mô Tả Trọng Tâm | Người Phụ Trách |
| :--- | :--- | :--- |
| **[AGENTP_MASTER_ARCHITECTURE.md](docs/AGENTP_MASTER_ARCHITECTURE.md)** | Cẩm nang kiến trúc tổng thể, Design Patterns, Directory Map & Nguyên tắc bảo toàn | **Alex & Carlos** |
| **[AGENTP_IMPLEMENTATION_PLAN.md](docs/AGENTP_IMPLEMENTATION_PLAN.md)** | Lộ trình chi tiết 6 Sprints, Tiêu chuẩn nghiệm thu DoD & Phân bổ nhiệm vụ | **Alex & Marcus** |
| **[UI_UX_DESIGN_SYSTEM.md](docs/UI_UX_DESIGN_SYSTEM.md)** | Đặc tả 10 màn hình chuẩn Antigravity, Design Tokens & Hệ màu Clean Light Mode | **Elena (UI/UX)** |
| **[DATABASE_SCHEMA_SPEC.md](docs/DATABASE_SCHEMA_SPEC.md)** | Cấu trúc 17 bảng CSDL SQLite WAL, Foreign Keys, Triggers & Chống sập tiến trình | **Maya (Architect)** |
| **[DESIGN_PATTERNS_RESEARCH.md](docs/DESIGN_PATTERNS_RESEARCH.md)** | Báo cáo nghiên cứu 8 mẫu thiết kế phần mềm kinh điển áp dụng trong source code | **Marcus (Lead BA)** |
| **[MULTI_AGENT_APP_SPEC.md](docs/MULTI_AGENT_APP_SPEC.md)** | Hồ sơ chuyên môn, Persona và cơ chế cô lập Session 1:1 của 14 Chuyên viên AI | **Alex & Sarah** |

---

<div align="center">
  <sub>Được phát triển và bảo chứng chất lượng bởi Ban Kỹ Thuật agentP Swarm • 2026</sub>
</div>
