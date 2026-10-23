# TÀI LIỆU THIẾT KẾ ĐA TRANG TOÀN DIỆN (FULL MULTI-PAGE UI/UX SPECIFICATION)
## DỰ ÁN: NỀN TẢNG ĐIỀU PHỐI ĐA TRÍ TUỆ NHÂN TẠO agentP (v3.8)

> **Phiên bản**: v3.8.0 (Unified 10-Screen Master Suite — Hợp Nhất Hệ Thống Kanban 3 Chế Độ: Mini-Kanban, Slide-Over Drawer & Full-Screen Studio)  
> **Chủ nhiệm thiết kế**: Elena (UI/UX Designer)  
> **Phản biện chiến lược**: Marcus (Product Strategist)  
> **Phong cách thẩm mỹ**: Clean Minimalist Light Mode, Nhận diện Precision Stealth (Alpine Teal `#0D9488`, Tuscan Amber `#D97706`, Porcelain White `#F8FAFC`, Tuyệt đối không Neon)

---

## 1. THIẾT KẾ TỔNG QUAN & BẢNG MÀU CHỦ ĐẠO (PRECISION STEALTH LIGHT THEME)

Định hình nhận diện thương hiệu độc bản cho **agentP** — hình tượng "Điệp Viên Lập Trình (The Precision Agent)": Sắc sảo, chuẩn xác và hoạt động ngầm hiệu quả. Thiết kế trừu tượng hóa hình học, tuyệt đối không sao chép nguyên mẫu hoạt hình để bảo vệ 100% bản quyền thương hiệu:

* **Canvas Nền Toàn Ứng Dụng**: `#F8FAFC` (Trắng ngà ánh xám Slate-50) & `#FFFFFF` (Trắng tinh khiết) — Giữ đúng chuẩn Light Mode sáng sủa, kiến trúc hiện đại, chống mỏi mắt, **tuyệt đối KHÔNG neon**.
* **Thẻ Bề Mặt & Bảng Điều Khiển**: `#FFFFFF` với viền hairline mỏng 1px `#E2E8F0`.
* **Sắc Xanh Mòng Két Alpine (Stealth Alpine Teal / Cyber Pine)**:
  * Nút bấm thương hiệu & Tác vụ chính: `#0D9488` (Teal-600) & `#0F766E` (Teal-700).
  * Nền nhạt làm mềm vùng chọn / thẻ active: `#CCFBF1` (Teal-100) & `#F0FDFA` (Teal-50).
  * Đường viền nhấn thanh tao: `#99F6E4` (Teal-200).
* **Sắc Cam Hổ Phách Tuscan (Tuscan Amber & Warm Citrus Accent)**:
  * Điểm nhấn hình học sắc sảo: Khung chóp kính ngắm (Stealth Visor Crest).
  * *Checkpoint Chờ Duyệt*: Nền vàng hổ phách nhạt `#FFFBEB`, viền `#FDE68A`, chữ và nút duyệt `#D97706` / `#EA580C`.
* **Màu Trạng Thái Hệ Thống (Thanh Lịch, Không Chói)**:
  * *Thành Công / Test Passed / Host Online*: Nền xanh ngọc bích `#ECFDF5`, chữ `#059669`.
  * *Dừng Khẩn Cấp / Nguy Hiểm*: Nền đỏ san hô nhạt `#FEF2F2`, nút hành động `#DC2626`.

### Bộ Nhận Diện Logo agentP (App Brand Assets):
* 🎨 **Logo Primary (Ngang)**: [**`docs/assets/agentp_logo_primary.svg`**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/agentp_logo_primary.svg) — Biểu tượng squircle Alpine Teal kèm chữ "agent" than chì + chữ "P" xanh mòng két với điểm nhấn kính ngắm Amber Visor.
* 📱 **App Icon (Vuông 512x512)**: [**`docs/assets/agentp_logo_app_icon.svg`**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/agentp_logo_app_icon.svg) — Biểu tượng ứng dụng Desktop & Mobile với chữ P hình học vát góc và kính ngắm Stealth Visor sắc nét.
* 🌐 **Favicon (64x64)**: [**`docs/assets/agentp_logo_favicon.svg`**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/agentp_logo_favicon.svg) — Biểu tượng khay hệ thống và tab trình duyệt siêu nét.

---

## 2. TRANG 1: MÀN HÌNH KHỞI TẠO Ý TƯỞNG (SMART ONBOARDING LAUNCHPAD)

Màn hình xuất hiện khi người dùng mở ứng dụng lần đầu hoặc bấm tạo project mới:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⚡ AGENTP                                                                        [⚙️ Cài đặt] [Trợ giúp]│
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                        │
│                                🌟 BẠN MUỐN TẠO PROJECT GÌ?                                             │
│                 Nhập ý tưởng sơ khởi, Lead/PM sẽ tự động lập ban kỹ thuật và thực thi                   │
│                                                                                                        │
│           ┌──────────────────────────────────────────────────────────────────────────────┐             │
│           │ ✍️ Nhập mô tả bài toán hoặc tính năng bạn muốn xây dựng...                   │             │
│           │                                                                              │             │
│           │ Ví dụ: "Tôi muốn xây dựng ứng dụng giao thức ăn trên Android và Web, có       │             │
│           │ giỏ hàng, tích điểm voucher và thanh toán quét mã QR..."                     │             │
│           │                                                                              │             │
│           └──────────────────────────────────────────────────────────────────────────────┘             │
│                                                                                                        │
│           ┌──────────────────────────────────────────────────────────────────────────────┐             │
│           │ ✨ Tên project đề xuất: [ 🏷️ FoodDelivery-Loyalty-App ] (Tự động đặt) ✏️ Đổi  │             │
│           │ 📁 Thư mục lưu trữ   : [ ~/Projects/FoodDelivery-Loyalty-App       ] [Chọn...]│             │
│           │ 🎯 Chọn Template sẵn : [x] Mobile & Web Fullstack   [ ] CLI Tool   [ ] AI API│             │
│           └──────────────────────────────────────────────────────────────────────────────┘             │
│                                                                                                        │
│                                      [ 🚀 KHỞI TẠO DỰ ÁN VỚI LEAD/PM ]                                 │
│                                                                                                        │
│           Gợi ý khởi động nhanh:                                                                       │
│           [ 🛒 App E-commerce ]   [ 📱 Flutter Mobile ]   [ 📊 Dashboard Saas ]   [ 🤖 Chatbot Bot ]   │
│                                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

* **Trải nghiệm**: Người dùng chỉ cần gõ ý tưởng $\rightarrow$ Hệ thống tự động đặt tên thông minh $\rightarrow$ 1 Click là chuyển ngay vào Bàn Làm Việc Chính.

---

## 3. TRANG 2: BÀN LÀM VIỆC ĐIỀU HÀNH CHÍNH (UNIFIED SINGLE-DESK WORKSPACE)

**Đột phá**: Bạn chỉ trao đổi trực tiếp với **Trưởng dự án (Lead/PM)**. Đội ngũ kỹ thuật ngầm chạy ở hậu trường và hiển thị tiến độ thu gọn trong một khung nhìn duy nhất.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⚡ AGENTP        [📁 FoodDelivery-Loyalty-App ▼]    [Host: 🟢 192.168.1.15:8080 📱]      [Quota: 42.5k tk ~ $0.00]  │
├──────────────────┬──────────────────────────────────────────────────────────────┬───────────────────────────────┤
│ 📋 TỔNG HỢP NHIỆM│ 💬 BÀN LÀM VIỆC TRỰC TIẾP VỚI TRƯỞNG DỰ ÁN (LEAD / PM)       │ 📚 DỮ LIỆU & KIỂM THỬ THỰC TẾ │
│ VỤ DỰ ÁN         │──────────────────────────────────────────────────────────────│ ┌───────────────────────────┐ │
│                  │ [10:30] 🧑‍💼 Bạn (Boss): Hãy làm tính năng Giỏ hàng & Voucher.│ │ 📄 Bộ nhớ chung (Shared)  │ │
│ ▶Task #01: Specs │                                                              │ │  • prd_specs.md           │ │
│  Task #02: DB    │ [10:31] 🧑‍💼 Trưởng dự án (Lead/PM):                          │ │  • db_schema.sql          │ │
│  Task #03: Code  │ Tôi đã tiếp nhận đề tài. Đang phân tích yêu cầu kỹ thuật:    │ └───────────────────────────┘ │
│  Task #04: QA    │                                                              │                               │
│                  │ ┌──────────────────────────────────────────────────────────┐ │ 🌿 Git Status: feature/cart   │
│ 👥 ĐỘI NGŨ NGẦM  │ │ 💭 RAW MODEL THINKING LOG (Claude 3.7 Sonnet - 8.4s) [▲] │ │  • 2 files modified (+45)   │
│ (BACKSTAGE SWARM)│ │ <thinking>                                               │ │  [👁️ Xem Diff] [🚀 Push Git]│
│ • BA  : 🪙 3.2k tk│ │ Phân tích bài toán giỏ hàng từ người dùng:               │ │                               │
│ • Arch: 🪙 5.1k tk│ │ 1. Cần 2 bảng: cart_items và vouchers.                   │ 📱 Android Virtual Device AVD │
│ • FE  : ⚡18.6k tk│ │ 2. Phân việc: Giao BA viết User Story -> FE/BE code ->   │ │  • Pixel 8 Pro (Port 5554)  │
│ • BE  : ⚡14.2k tk│ │    QA kiểm thử tự động trên Android AVD -> Docs xuất báo │ │  • Trạng thái: 🟢 Đang chạy │
│ • QA  : 🪙 2.8k tk│ │    cáo Excel nghiệm thu trước khi trình Boss duyệt.      │ │  [📺 Mở Màn hình] [📸 Test] │
│ • Docs: 🪙 2.1k tk│ │ </thinking>                                              │ │                               │
│ • Ops : 🪙 1.9k tk│ └──────────────────────────────────────────────────────────┘ │                               │
│                  │                                                              │ 🖥️ Hệ thống:                  │
│ ⚙️ TIỀN KIỂM MÁY │ Tôi đã điều phối các role thực hiện. Dưới đây là tiến độ:    │  • RAM: 11.2GB/16GB           │
│ • Ổ đĩa: 85GB OK │                                                              │  • Cổng: 3000 & 8080 sạch    │
│ • KVM/AVD: Sẵn   │ ┌──────────────────────────────────────────────────────────┐ │                               │
│                  │ │ 🔄 TIẾN ĐỘ THỰC THI NGẦM (SWARM LIVE ACTIVITY)           │ │                               │
│                  │ │  ✓ BA & UI/UX: Đã chốt vị trí nhãn lỗi Voucher inline    │ │                               │
│                  │ │  ✓ FE & BE Dev: Đã viết xong Component & API validate    │ │                               │
│                  │ │  ✓ Automation QA: 14/14 tests PASSED (100% Code Coverage)│ │                               │
│                  │ │  ✓ Docs/Excel: Xuất báo cáo nghiệm thu `Report_Sprint.xlsx`│ │                             │
│                  │ └──────────────────────────────────────────────────────────┘ │                               │
│                  │                                                              │                               │
│                  │ ┌──────────────────────────────────────────────────────────┐ │                               │
│                  │ │ 🛑 CỔNG DUYỆT NGHIỆM THU (User Checkpoint Gate #01)      │ │                               │
│                  │ │ Trưởng dự án (PM): Task đã hoàn tất và vượt qua bài test.│ │                               │
│                  │ │                                                          │ │                               │
│                  │ │  [ ✅ DUYỆT & MERGE ]  [ 📱 THỬ TRÊN AVD ]  [ ✍️ YÊU CẦU SỬA ]│                            │
│                  │ └──────────────────────────────────────────────────────────┘ │                               │
│                  ├──────────────────────────────────────────────────────────────┤                               │
│                  │ [ ⏹️ DỪNG ĐỘT NGỘT (Esc) ]  Nhập chỉ đạo cho Lead/PM... [Gửi]│                               │
├──────────────────┴──────────────────────────────────────────────────────────────┴───────────────────────────────┤
│ 📟 SMART TERMINAL DRAWER (Gập/Mở: Ctrl+`)  [Terminal: Bash] [Android Logcat] [Jest Output]         [▼ Gập Drawer]│
│ $ pnpm test -> 14 passed, 0 failed. All suites green in 1.28s.                                                  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. TRANG 3: KẾT NỐI TÀI KHOẢN & GÁN MODEL 1:1 THEO 9ROUTER (PROVIDER SETUP)

Màn hình cấu hình giúp tận dụng tài khoản có sẵn (CLI / OAuth Sessions) thay vì phụ thuộc API trả phí:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🔌 KẾT NỐI TÀI KHOẢN & GÁN MODEL THỦ CÔNG (PROVIDER SESSIONS 1:1 9ROUTER)                          [X]│
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. KẾT NỐI TÀI KHOẢN HIỆN CÓ TRÊN MÁY (ACCOUNT SESSIONS & CLI LOGIN):                                  │
│                                                                                                        │
│   [🟢 Claude CLI Session]   Token: claude-user-... (Hạn dùng: 28 ngày)           [ Đã kết nối ]       │
│   [🟢 Cursor Pro Session]   Tài khoản: developer@gmail.com                       [ Đã kết nối ]       │
│   [⚪ GitHub Copilot CLI]    Chưa đăng nhập                                       [ 🔗 Đăng nhập OAuth]│
│   [⚪ Local Ollama Engine]   Chưa chạy daemon                                     [ 🔄 Quét Local ]    │
│   [⚪ OpenAI API Key]        Chỉ dùng làm dự phòng khẩn cấp                       [ + Thêm Key ]       │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. GÁN THỦ CÔNG MODEL CHO TỪNG ROLE DỰ ÁN (CHỈ CHỌN ĐƯỢC MODEL TỪ PROFILE ĐÃ KẾT NỐI):                 │
│                                                                                                        │
│   • Trưởng dự án (Lead/PM)  : [ Claude 3.7 Sonnet (Thinking Enabled) (via Claude CLI)               ▼ ]│
│   • Business Analyst (BA)   : [ Claude 3.5 Sonnet (via Cursor Session)                              ▼ ]│
│   • System Architect        : [ Claude 3.7 Sonnet (Thinking Enabled) (via Claude CLI)               ▼ ]│
│   • Frontend & Backend Dev  : [ DeepSeek R1 (Reasoning Stream) (via Cursor Session)                 ▼ ]│
│   • QA & Automation Tester  : [ Claude 3.5 Haiku (Tốc độ cao) (via Claude CLI)                      ▼ ]│
│   • DevOps & Infrastructure : [ Claude 3.5 Sonnet (via Claude CLI)                                  ▼ ]│
│                                                                                                        │
│                                                                     [ Hủy bỏ ]   [ 💾 LƯU CẤU HÌNH ]   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. TRANG 4: ĐIỀU KHIỂN TỪ XA TRÊN MOBILE (ANDROID APP & REMOTE WEB VIEW)

Khi máy tính đóng vai trò là Host Server, màn hình điện thoại Android kết nối qua mã QR hiển thị giao diện tối ưu:

```
┌───────────────────────────────┐
│ ⚡ agentP Remote Host  [🟢Live]│
│ Host: Mac-Studio (Port 8080)  │
├───────────────────────────────┤
│ 📁 Project: FoodDelivery-App  │
│ 💬 Lead/PM: Đã xong Task Cart │
├───────────────────────────────┤
│ [10:31] 🧑‍💼 Trưởng dự án (PM): │
│ Đội ngũ ngầm đã code xong &   │
│ vượt qua 14/14 test cases.    │
│                               │
│ ┌───────────────────────────┐ │
│ │ 🛑 CỔNG DUYỆT CHECKPOINT  │ │
│ │ Task #01: Giỏ hàng & Code │ │
│ │ • Test: 14/14 PASSED      │ │
│ │ • Build: Android APK OK   │ │
│ │                           │ │
│ │ [ 📱 Xem Video Demo AVD ] │ │
│ │                           │ │
│ │ [   ✅ DUYỆT (APPROVE)  ] │ │
│ │ [   ✍️ GỬI GÓP Ý SỬA   ] │ │
│ └───────────────────────────┘ │
├───────────────────────────────┤
│ [ ⏹️ DỪNG ] Nhắn cho PM...[Gửi]│
└───────────────────────────────┘
```

---

## 6. TRANG 5: TIỀN KIỂM MÔI TRƯỜNG & QUẢN TRỊ GIẢ LẬP (PRE-FLIGHT DIAGNOSTICS)

Màn hình chuyên sâu của DevOps Specialist giúp kiểm tra toàn diện phần cứng, bảo mật và máy ảo:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🛠️ CHẨN ĐOÁN MÔI TRƯỜNG TIỀN TRẠM & QUẢN TRỊ GIẢ LẬP ANDROID (DEVOPS PRE-FLIGHT SYSTEM)            [X]│
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. CHỈ SỐ HẠ TẦNG VÀ ĐIỀU KIỆN TIỀN TRẠM:                                                             │
│                                                                                                        │
│   💾 Ổ đĩa khả dụng    : 🟢 85.4 GB trống (Đủ điều kiện biên dịch & cài Android SDK + AVD)             │
│   🧠 Bộ nhớ RAM        : 🟢 11.2 GB / 16.0 GB khả dụng (Đảm bảo chạy mượt Emulator)                    │
│   ⚡ Ảo hóa CPU VT/KVM : 🟢 Apple Virtualization Framework KÍCH HOẠT                                   │
│   🔌 Quét Cổng Kết nối : 🟢 Port 3000 (Trống), Port 8080 (Trống), Port 5037 (ADB Daemon Sẵn sàng)      │
│   🛡️ Mạng & Tường lửa  : 🟢 Kết nối NPM, Gradle, Maven và Docker Hub không bị chặn bởi Proxy/VPN       │
│   🔐 Quyền thực thi    : 🟢 File System Write & Terminal Execution: Đã được cấp quyền an toàn          │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. BẢNG ĐIỀU KHIỂN MÁY ẢO ANDROID (AVD LIFECYCLE CONTROLLER):                                          │
│                                                                                                        │
│   • Tên thiết bị ảo    : Google Pixel 8 Pro - API 34 (Android 14.0 Google APIs)                        │
│   • Cổng kết nối ADB   : localhost:5554 (Thiết bị: emulator-5554)                                     │
│   • Chế độ hiển thị    : [x] Có giao diện (GUI)    [ ] Chạy ngầm tiết kiệm RAM (Headless E2E)          │
│                                                                                                        │
│   [ ⏹️ Tắt Giả lập ]  [ 🔄 Khởi động lại (Cold Boot) ]  [ 📸 Chụp màn hình Test ]  [ 📺 Mở Cửa sổ AVD ]│
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. TRANG 6: KHU VỰC QUẢN LÝ FILE DỰ ÁN (PROJECT FILE EXPLORER & ASSET MANAGER)

Màn hình quản lý toàn bộ tệp tin, cấu trúc thư mục, tài sản assets và báo cáo số liệu:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⚡ AGENTP        [📁 FoodDelivery-Loyalty-App ▼]    [💬 Bàn Làm Việc] [📁 Quản Lý File] [💻 Trình Soạn Thảo]     │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [ ➕ File mới ] [ 📁 Thư mục mới ] [ 📤 Tải file lên ] [ 📥 Tải xuống Project (.zip) ]   [ 🔍 Tìm file nhanh... ] │
├──────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────┤
│ 📁 CÂY THƯ MỤC DỰ ÁN     │ 📄 DANH SÁCH FILE TRONG THƯ MỤC: src/features/cart/                                  │
│                          │                                                                                      │
│ ▼ 📁 FoodDelivery-App    │ ┌──────────────────────────────────────┬──────────┬─────────────┬──────────────────┐ │
│   ▼ 📁 src/              │ │ Tên File                             │ Dung lượng│ Ngày sửa    │ Thao tác         │ │
│     ▼ 📁 features/       │ ├──────────────────────────────────────┼──────────┼─────────────┼──────────────────┤ │
│       ▼ 📁 cart/         │ │ 📄 cart_controller.dart              │ 4.2 KB   │ 10:32 AM    │ [👁️ Xem] [✏️] [🗑️]│ │
│         • cart_view.dart │ │ 📄 cart_view.dart (Vừa sửa)          │ 8.5 KB   │ 10:34 AM    │ [👁️ Xem] [✏️] [🗑️]│ │
│         • cart_model.dart│ │ 📄 voucher_modal.dart                │ 3.1 KB   │ 10:33 AM    │ [👁️ Xem] [✏️] [🗑️]│ │
│     ► 📁 auth/           │ │ 📄 cart_model.dart                   │ 2.4 KB   │ 10:15 AM    │ [👁️ Xem] [✏️] [🗑️]│ │
│   ► 📁 lib/              │ └──────────────────────────────────────┴──────────┴─────────────┴──────────────────┘ │
│   ▼ 📁 docs/             │                                                                                      │
│     • prd_specs.md       │ 📊 BÁO CÁO DO ROLE 14 XUẤT RA GẦN NHẤT:                                              │
│     • api_contract.yaml  │ • 📊 Report_Sprint_01_Acceptance.xlsx (Định dạng Excel có công thức & màu chuẩn)     │
│   ► 📁 test/             │ • 📄 Release_Notes_v1.0.md                                                           │
│   ► 📁 .agents/          │                                                                                      │
│     • shared_knowledge/  │ 💡 Thao tác nhanh:                                                                   │
│   • pubspec.yaml         │ Kéo thả bất kỳ file nào từ máy tính vào đây để nạp vào dự án.                       │
└──────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. TRANG 7: TRÌNH SOẠN THẢO & XEM/SỬA/XÓA CODE (INTEGRATED CODE EDITOR & DIFF VIEWER)

Trang hiển thị mã nguồn chuyên nghiệp, tích hợp chế độ xem diff trước/sau khi Agent sửa, cho phép gõ code, lưu và xóa:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⚡ AGENTP        [📁 FoodDelivery-Loyalty-App ▼]    [💬 Bàn Làm Việc] [📁 Quản Lý File] [💻 Trình Soạn Thảo (Active)]│
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [Tabs]: [ 📄 cart_view.dart ✕ ] [ 📄 voucher_modal.dart ✕ ] [ 📊 Report_Sprint.xlsx ✕ ]        [ ➕ Mở file... ]│
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [Thanh công cụ]: [ 💾 Lưu thay đổi (Ctrl+S) ] [ 👁️ Chế độ: Split Diff ▼ ] [ 🤖 Nhờ AI Sửa ] [ 🗑️ XÓA FILE NÀY ] │
├──────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────┤
│ 🔴 CODE GỐC TRƯỚC KHI AGENT SỬA                      │ 🟢 CODE MỚI ĐÃ ĐƯỢC AGENT CẬP NHẬT (SẴN SÀNG CHỈNH SỬA) │
├──────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ 45   Widget _buildVoucherInput() {                   │ 45   Widget _buildVoucherInput() {                       │
│ 46     return TextField(                             │ 46     return Column(                                    │
│ 47       controller: _voucherController,             │ 47       crossAxisAlignment: CrossAxisAlignment.start,   │
│ 48 -     decoration: InputDecoration(                │ 48 +     children: [                                     │
│ 49 -       hintText: 'Nhập mã giảm giá...',          │ 49 +       TextField(                                    │
│ 50 -     ),                                          │ 50 +         controller: _voucherController,             │
│ 51     );                                            │ 51 +         decoration: InputDecoration(                │
│ 52   }                                               │ 52 +           hintText: 'Nhập voucher...',              │
│ 53                                                   │ 53 +           errorText: _errorMessage, // Inline label │
│                                                      │ 54 +         ),                                          │
│                                                      │ 55 +       ),                                            │
│                                                      │ 56 +     ],                                              │
│                                                      │ 57     );                                                │
│                                                      │ 58   }                                                   │
├──────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────┤
│ [Trạng thái]: Dòng 48, Cột 12 • UTF-8 • Dart/Flutter • 2 files modified                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

* **Thao tác trực tiếp**:
  * Người dùng có thể click chuột vào khung bên phải để gõ sửa code trực tiếp.
  * Bấm nút **[ 🗑️ XÓA FILE NÀY ]**: Xuất hiện hộp thoại xác nhận an toàn trước khi xóa file khỏi dự án.
  * Bấm nút **[ 🤖 Nhờ AI Sửa ]**: Mở thanh nhắc lệnh nhanh để yêu cầu Coder tối ưu hoặc QA viết test case ngay cho file này.

---

## 9. TRANG 8: BẢNG QUẢN LÝ DỰ ÁN & CƠ CHẾ SỬA/XÓA PROJECT (CHUẨN ANTIGRAVITY)

Cung cấp khả năng quản lý toàn diện mọi Project trong hệ thống:

### 9.1. Menu Thả Xuống Chuyển Đổi & Thao Tác Dự Án Nhanh (Project Dropdown):
Khi người dùng bấm vào tên dự án ở Top Bar (`[📁 FoodDelivery-Loyalty-App ▼]`):

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 📁 DANH SÁCH DỰ ÁN GẦN ĐÂY                                                       │
├──────────────────────────────────────────────────────────────────────────────────┤
│ ▶ 🏷️ FoodDelivery-Loyalty-App (Đang mở)     ~/Projects/FoodDelivery..  [✏️] [🗑️]│
│   🏷️ E-Commerce-Shopify-Sync                 ~/Projects/shopify-sync    [✏️] [🗑️]│
│   🏷️ Personal-Finance-Bot                    ~/Projects/finance-bot     [✏️] [🗑️]│
├──────────────────────────────────────────────────────────────────────────────────┤
│ [ ➕ Khởi tạo Project Mới ]        [ 📂 Mở Project có sẵn từ máy ]              │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 9.2. Hộp Thoại Chỉnh Sửa Thông Tin Dự Án (Edit Project Modal):
Bấm vào icon `[✏️ Sửa]` ở bất kỳ project nào:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ ✏️ CHỈNH SỬA THÔNG TIN DỰ ÁN: FoodDelivery-Loyalty-App                         [X]│
├──────────────────────────────────────────────────────────────────────────────────┤
│ 🏷️ Tên Hiển Thị (Display Name)  : [ FoodDelivery Loyalty Mobile App            ]│
│ 📁 Mã Nhận Diện (Slug / Folder) : [ FoodDelivery-Loyalty-App                   ]│
│ 📂 Thư Mục Mã Nguồn Trên Máy    : [ ~/Projects/FoodDelivery-Loyalty-App ] [Đổi] │
│                                                                                  │
│ 📝 Chỉ Đạo Cốt Lõi Cho AI (System Directives / Context):                        │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ • Sử dụng kiến trúc Flutter Clean Architecture (Bloc state management).      │ │
│ │ • Toàn bộ API Backend viết bằng NestJS + PostgreSQL.                         │ │
│ │ • Viết docstrings tiếng Việt chuẩn chỉnh cho mọi hàm nghiệp vụ.              │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
│ ⚙️ Biến Môi Trường (.env)       : [ 🔒 4 Biến đã cấu hình ] [ ✏️ Quản lý Keys ] │
│ 👥 Cấu hình Model riêng         : [ 14 Roles đã gán ]       [ ⚙️ Điều chỉnh ]   │
│                                                                                  │
│                                            [ Hủy Bỏ ]   [ 💾 LƯU THAY ĐỔI ]     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 9.3. Hộp Thoại Xóa & Gỡ Bỏ Dự Án An Toàn (Delete Project Safety Modal):
Bấm vào icon `[🗑️ Xóa]` sẽ kích hoạt hộp thoại bảo vệ 2 lớp chống bấm nhầm:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ ⚠️ BẠN ĐANG YÊU CẦU XÓA DỰ ÁN: FoodDelivery-Loyalty-App                        [X]│
├──────────────────────────────────────────────────────────────────────────────────┤
│ Vui lòng lựa chọn hình thức xóa phù hợp với mong muốn của bạn:                  │
│                                                                                  │
│ ( ) 1. CHỈ GỠ KHỎI ỨNG DỤNG (UNLINK WORKSPACE - KHUYÊN DÙNG)                     │
│     • Giữ nguyên 100% tệp tin, mã nguồn và lịch sử Git trên ổ đĩa máy tính bạn.  │
│     • Chỉ xóa project khỏi bảng điều khiển của agentP. Có thể Import lại.        │
│                                                                                  │
│ (x) 2. XÓA VĨNH VIỄN CẢ THƯ MỤC TRÊN Ổ ĐĨA (PERMANENT DISK DELETE)               │
│     • 🚨 CẢNH BÁO: Toàn bộ thư mục ~/Projects/FoodDelivery-Loyalty-App sẽ bị   │
│       xóa hoàn toàn khỏi máy tính. Hành động này KHÔNG THỂ HOÀN TÁC!            │
│                                                                                  │
│ 🔒 XÁC NHẬN BẰNG TÊN DỰ ÁN ĐỂ MỞ KHÓA:                                           │
│ Nhập lại chính xác dòng chữ: "FoodDelivery-Loyalty-App" vào ô bên dưới:          │
│ [ FoodDelivery-Loyalty-App                                                    ] │
│                                                                                  │
│                                  [ HỦY THAO TÁC ]   [ 🚨 XÓA VĨNH VIỄN PROJECT ] │
└──────────────────────────────────────────────────────────────────────────────────┘
```
* *Quy chuẩn an toàn*: Nút `[ 🚨 XÓA VĨNH VIỄN PROJECT ]` bị vô hiệu hóa (disabled). Chỉ khi người dùng gõ đúng 100% từng ký tự tên project thì nút này mới chuyển sang màu đỏ và cho phép bấm!

---

## 10. TRANG 9: STUDIO THIẾT KẾ UI/UX TRỰC QUAN (DUAL-MODE VISUAL UI STUDIO: TLDRAW & ONLOOK)

Studio tích hợp 2 chế độ làm việc liền mạch: **Chế độ 1: Tldraw (Bàn phác thảo ý tưởng)** và **Chế độ 2: Onlook (Chỉnh sửa trực quan trên code thật)**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⚡ AGENTP        [📁 FoodDelivery-Loyalty-App]   [✏️ Chế độ 1: Tldraw Phác Thảo]  [👁️ Chế độ 2: Onlook Code Thật]   │
├──────────────────┬──────────────────────────────────────────────────────────────┬───────────────────────────────┤
│ 🌲 CÂY COMPONENT │ 📱 ONLOOK LIVE CANVAS: http://localhost:3000                 │ 🎨 BẢNG STYLE & DESIGN TOKENS │
│ (DOM HIERARCHY)  │ ┌──────────────────────────────────────────────────────────┐ │ ┌───────────────────────────┐ │
│                  │ │ 🛒 Giỏ Hàng Của Bạn (FoodDelivery)            [✖️ Đóng]   │ │ │ 🎨 Bảng Màu (Palette)       │ │
│ ▼ <CartDrawer>   │ │ ──────────────────────────────────────────────────────── │ │ │ • Nền:  [#E0F2FE Sky-100   ]│ │
│   ▼ <Header>     │ │  🍜 Phở Bò Tái Lăn Đặc Biệt               55.000đ  [x1]  │ │ │ • Chữ:  [#0284C7 Sky-600   ]│ │
│     <Title>      │ │  🧋 Trà Sữa Trân Châu Đường Đen           32.000đ  [x2]  │ │ │ • Viền: [#BAE6FD Sky-200   ]│ │
│   ▼ <ItemList>   │ │ ──────────────────────────────────────────────────────── │ │ └───────────────────────────┘ │
│     <CartItem>   │ │ 🏷️ ƯU ĐÃI & VOUCHER                                      │ │                               │
│     <CartItem>   │ │ ┌──────────────────────────────────────────────────────┐ │ │ 📐 Khoảng Cách (Spacing Box) │ │
│   ▼ <VoucherBox> │ │ │ [ NHẬP MÃ GIẢM GIÁ...        ]  ┌──────────────────┐ │ │ │       ┌─── Margin ───┐      │ │
│     <Input>      │ │ │                                 │ [ ÁP DỤNG ] ✏️   │ │ │ │       │   mt: 8px    │      │ │
│   ▶ <ApplyBtn> 🎯│ │ │                                 └──────────────────┘ │ │ │   ┌───┼── Padding ───┼───┐  │ │
│   ▼ <Summary>    │ │ └──────────────────────────────────────────────────────┘ │ │   │ml │ px: 16 py: 8 │ mr│  │ │
│     <TotalRow>   │ │                                                          │ │   └───┴──────────────┴───┘  │ │
│     <PayBtn>     │ │  Tạm tính:  119.000đ  |  Giảm giá Voucher: -20.000đ      │ │                               │
│                  │ │ ════════════════════════════════════════════════════════ │ │ 🔤 Kiểu Chữ (Typography)    │ │
│ 🛠️ CÔNG CỤ       │ │ [ 💳 TIẾN HÀNH THANH TOÁN QR (99.000đ)                 ] │ │ • Font: Inter Semibold 14px │ │
│ [↖️ Chọn DOM]    │ └──────────────────────────────────────────────────────────┘ │ • Text Align: Center          │ │
│ [✋ Kéo Canvas]  │                                                              │ • Rounded: lg (8px)           │ │
│ [📱 Mobile 390px]│ ⚡ Phần tử đang chọn: <button class="bg-sky-600 text-white"> │                               │
│ [💻 Web 1440px]  │ 📍 File nguồn: src/features/cart/VoucherBanner.tsx:42        │ 🌿 KẾT QUẢ ĐỒNG BỘ AST CODE   │
│ [🔄 Reload DOM]  │ [ 🎨 Đổi Màu Nền ] [ 📐 Padding +4px ] [ 🔤 Đổi Font Chữ ]  │ • Modified: VoucherBanner.tsx │
├──────────────────┴──────────────────────────────────────────────────────────────┴───────────────────────────────┤
│ 🟢 AST SYNC STATUS: Đã đồng bộ 100% với mã nguồn thật (src/features/cart/VoucherBanner.tsx)  [💾 Lưu Code] [👁️ Diff]│
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 10.1. Điểm Nhấn Của Trang 9 (Visual UI Studio):
1. **Chuyển Đổi Linh Hoạt 2 Chế Độ (Header Tab Switcher)**:
   * **Tab Tldraw (Bàn phác thảo ý tưởng)**: Không gian vẽ nháp tự do. Bạn và Elena phác thảo sơ đồ màn hình, kéo thả sticky notes.
   * **Tab Onlook (Xưởng sửa code thật)**: Nhúng trực tiếp app đang chạy từ localhost. Cho phép click chọn từng phần tử HTML/Flutter và chỉnh sửa trực tiếp.
2. **Cột Trái (Component & DOM Hierarchy)**:
   * Liệt kê cây phân cấp component trực quan giúp định vị nhanh phần tử lồng nhau phức tạp.
3. **Khung Giữa (Interactive Live Canvas)**:
   * Thước đo pixel thông minh, hiển thị đường viền xanh nước nhạt bao quanh phần tử đang được chọn.
   * Thanh công cụ nổi (Floating Quick Toolbar) cho phép thao tác nhanh: Đổi màu, tăng padding, nhân bản component.
4. **Cột Phải (Visual Style & Design Tokens Inspector)**:
   * Hộp Spacing trực quan điều chỉnh margin/padding không cần gõ số.
   * Thư viện màu định sẵn tuân thủ 100% Light Mode (#E0F2FE, #0284C7, #BAE6FD).
5. **Thanh Chân Trang (AST Bi-directional Code Sync Bar)**:
   * Hiển thị trạng thái đồng bộ mã nguồn theo thời gian thực.
   * Bấm `[💾 Lưu Code]` hoặc `[👁️ Diff]` để kiểm tra code thay đổi trước khi Git commit.

---

## 11. TRANG 10: HỆ THỐNG KANBAN PHẢN ỨNG TỰ ĐỘNG HỢP NHẤT (TRI-MODAL AGENTIC KANBAN STUDIO)

Hợp nhất hoàn hảo **Phương án 1 (Embedded Mini-Kanban)**, **Phương án 2 (Full-Screen Studio)** và **Phương án 3 (Slide-over Drawer `Cmd+B`)** trên cùng một nguồn dữ liệu thời gian thực (`Single Source of Truth`):

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⚡ AGENTP  [📁 FoodDelivery-Loyalty-App]   [💬 Bàn Làm Việc] [📋 Bảng Kanban (Active)] [📁 Quản Lý File] [💻 Code]│
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 🔍 Bộ lọc: [14 Roles ▼]  [Sprint: Sprint 1 ▼]   |   Chế độ xem: (•) Bảng 6 Cột   ( ) Theo Roles   | [Cmd+B: Drawer]│
├──────────────────┬──────────────────┬──────────────────┬──────────────────┬──────────────────┬──────────────────┤
│ 📝 1. BACKLOG (3)│ 📋 2. TO DO (2)  │ 💻 3. CODING (2) │ 🧪 4. TESTING (1)│ 🛑 5. CHECKPOINT │ ✅ 6. DONE (8)   │
├──────────────────┼──────────────────┼──────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────┐ │
│ │#12 Push Notif│ │ │#08 API Auth  │ │ │#04 Cart UI   │ │ │#05 Unit Test │ │ │#03 Schema DB │ │ │#01 Project   │ │
│ │  🪙 Liam     │ │ │  ⚡ Victor   │ │ │  ⚡ Chloe    │ │ │  🪙 Oliver   │ │ │  Chờ Boss ký │ │ │    Launchpad │ │
│ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │ └──────────────┘ │
│ ┌──────────────┐ │                  │ ┌──────────────┐ │                  │                  │ ┌──────────────┐ │
│ │#14 Excel Rep │ │                  │ │#09 Diff View │ │                  │                  │ │#02 CoreDaemon│ │
│ │  🪙 Sophia   │ │                  │ │  🪙 Sam      │ │                  │                  │ │    Daemon OK │ │
│ └──────────────┘ │                  │ └──────────────┘ │                  │                  │ └──────────────┘ │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

### 11.1. Ba Chế Độ Hiển Thị Hợp Nhất (3 Unified View Modes):
1. **Mode A (Embedded Mini-Kanban — Thu gọn tại Trang 2)**:
   * Hiển thị thường trực ở Cột Phải của Bàn Làm Việc. Gồm 4 cột mini (`To Do` $\rightarrow$ `Coding` $\rightarrow$ `Testing` $\rightarrow$ `Done`).
   * Boss không cần rời mắt khỏi dòng hội thoại với Alex nhưng vẫn thấy thẻ task tự động di chuyển.
2. **Mode B (Slide-over Drawer `Cmd+B` — Ngăn kéo trượt mở rộng)**:
   * Đang chat với Alex, Boss chỉ cần nhấn tổ hợp phím `Cmd+B` (hoặc click icon `[📋 Kanban]`).
   * Ngăn kéo 400px trượt êm ái ra từ cạnh phải (hoặc chuyển màn hình sang tỷ lệ 60/40), hiển thị chi tiết tiến độ, agent đang gõ code và mức tiêu hao token.
3. **Mode C (Full-Screen Dedicated Studio — Bảng toàn màn hình)**:
   * Nhấp `[⛶ Toàn Màn Hình]` hoặc click tab `[📋 Bảng Kanban]` trên thanh Menu: Trải rộng thành giao diện 6 cột chuẩn mực quốc tế, hỗ trợ phân làn (Swimlanes) theo Module hoặc theo từng nhân sự trong 14 Roles.

---

## 12. BỘ TỆP TIN THIẾT KẾ ĐẦY ĐỦ CHO TỪNG TRANG (FULL MULTI-SCREEN VECTOR SUITE - 10 SCREENS)

Hệ thống đã kết xuất toàn bộ 10 màn hình riêng biệt thành các tệp tin đồ họa vector sắc nét độc lập:

* 🖼️ **Bản Render Kỹ Thuật Số Toàn Cảnh (3D Master Suite Poster JPG)**:
  👉 [**docs/assets/agentp_master_suite_poster.jpg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/agentp_master_suite_poster.jpg)
* 🖼️ **Bảng Vẽ Tổng Thể Toàn Bộ Màn Hình (Master Showcase Artboard SVG)**:
  👉 [**docs/assets/agentp_master_all_screens_showcase.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/agentp_master_all_screens_showcase.svg)
* 📐 **Trang 1: Onboarding Launchpad (Tạo Project & Đặt tên thông minh)**:
  👉 [**docs/assets/screen_1_onboarding_launchpad.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_1_onboarding_launchpad.svg)
* 📐 **Trang 2: Unified Main Command Workspace (Bàn làm việc Bạn ⇄ Lead/PM)**:
  👉 [**docs/assets/screen_2_main_command_workspace.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_2_main_command_workspace.svg)
* 📐 **Trang 3: Provider Setup & Manual Role Binding (Cơ chế 1:1 agentP Core Daemon)**:
  👉 [**docs/assets/screen_3_provider_connection_modal.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_3_provider_connection_modal.svg)
* 📐 **Trang 4: Remote Mobile Controller (Giao diện điều khiển qua Android)**:
  👉 [**docs/assets/screen_4_mobile_remote_controller.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_4_mobile_remote_controller.svg)
* 📐 **Trang 5: Pre-flight Diagnostics & AVD Controller (Tiền kiểm hệ thống)**:
  👉 [**docs/assets/screen_5_preflight_diagnostics.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_5_preflight_diagnostics.svg)
* 📐 **Trang 6: Project File Explorer & Asset Manager (Khu vực quản lý file)**:
  👉 [**docs/assets/screen_6_project_file_explorer.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_6_project_file_explorer.svg)
* 📐 **Trang 7: Integrated Code Editor & Split Diff (Trình xem/sửa/xóa code)**:
  👉 [**docs/assets/screen_7_integrated_code_editor.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_7_integrated_code_editor.svg)
* 📐 **Trang 8: Project Hub & Modal Sửa/Xóa Dự Án (Chuẩn Antigravity)**:
  👉 [**docs/assets/screen_8_project_hub_edit_delete.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_8_project_hub_edit_delete.svg)
* 📐 **Trang 9: Visual UI/UX Studio (Dual-Mode: Tldraw Ý Tưởng & Onlook Sửa Code Thật)**:
  👉 [**docs/assets/screen_9_visual_ui_studio.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_9_visual_ui_studio.svg)
* 📐 **Trang 10: Unified Agentic Kanban System (Hệ thống Kanban 3 Chế Độ Hợp Nhất)**:
  👉 [**docs/assets/screen_10_unified_kanban_system.svg**](file:///Users/tb3c/Documents/antigravity/fearless-einstein/docs/assets/screen_10_unified_kanban_system.svg)


---

## 13. KIẾN TRÚC GIAO DIỆN MỚI: ANTIGRAVITY ACTIVITY RAIL & HORIZONTAL SWARM TOP RIBBON

Cập nhật chính thức bởi **Elena (Lead UI/UX)** và phê duyệt bởi **Alex (Lead/PM)** theo phản hồi của Bạn:

```
+---------------------------------------------------------------------------------------------------------------+
|  ANTIGRAVITY LEFT SIDEBAR (260px)  |  TOP SWARM RIBBON (52px): Alex Desk | 13 Specialists Chips | Actions    |
|                                    +--------------------------------------------------------------------------+
|  [🔴🟡🟢] [◫] [←] [→] [🔍]          |                                      |                                   |
|  [Fedora Logo] agentP v2.0         |  CENTER CHAT WORKSPACE (Flex 1)      |  EXPANDED LIVE KANBAN (560px)     |
|  [+ New Conversation]              |  - Luồng chat với Alex [SPOC]        |  - Chờ Làm (1)                    |
|  [🕒 Conversation History]         |  - <thinking> reasoning box          |  - Đang Làm ⚡ (1)                 |
|  [⏱️ Automations (3 Active)]        |  - Checkpoint Gate #04 (Amber)       |  - Kiểm Thử 🛑 (1)                 |
|  [🧰 Customizations (30 Skills)]   |  - Thanh nhập lệnh                   |  - Hoàn Tất ✓ (4)                 |
|  --------------------------------- |                                      +-----------------------------------+
|  PROJECTS             [≡] [📁⁺]    |                                      |  BOTTOM TOOLS DOCK                |
|  ▼ 📁 FoodDelivery-Loyalty-App     |                                      |  [Git Staging]  |  [AVD Runner]   |
|    - 🧑‍💼 Bàn Làm Việc Alex (6m)    |                                      |  (+45/-12 lines)|  (Pixel 8 Pro)  |
|    - 🎨 Xưởng Thiết Kế (15m)       |                                      |                                   |
|    - 📋 Bảng Tiến Độ (1h)          |                                      |                                   |
|    - 💻 Mã Nguồn & Diff (3h)       |                                      |                                   |
|    - 💬 Multi-Agent CLI App (6m)   |                                      |                                   |
|  ▶ 📁 vietlot (9h)                 |                                      |                                   |
|  ▶ 📁 TV (22d)                     |                                      |                                   |
|  ▶ 📁 agent (2d)                   |                                      |                                   |
|  --------------------------------- |                                      |                                   |
|  [● Host: 192.168.1.15:8080]       |                                      |                                   |
|  [🪙 42.5k tokens saved via Daemon]|                                      |                                   |
|  [⚙️ Settings & Danger Zone Lock]  |                                      |                                   |
+------------------------------------+--------------------------------------+-----------------------------------+
```

### Điểm Cải Tiến Cốt Lõi:
1. **Thanh Điều Hướng Cánh Trái Chuẩn Google Antigravity 2.0 (Width 260px)**:
   - **Thanh tiêu đề macOS**: Bộ 3 đèn tín hiệu giao thông (🔴 Đỏ `#FF5F56`, 🟡 Vàng `#FFBD2E`, 🟢 Xanh `#27C93F`) kết hợp bộ điều khiển: Thu gọn Sidebar `◫`, Quay lui `←`, Tiến tới `→`, và Tìm kiếm nhanh `🔍`.
   - **Nhận diện thương hiệu agentP**: Nón Fedora Monogram và vạch xanh Alpine Teal (`#0D9488`), huy hiệu `v2.0`.
   - **Nút hành động chính**: Thẻ nút bo tròn toàn chiều rộng `+ New Conversation` (`+ Tạo Cuộc Hội Thoại Mới`).
   - **Bộ liên kết hệ thống cấp cao (Upper Navigation)**:
     - `🕒 Conversation History`: Xem lại lịch sử các phiên thảo luận.
     - `⏱️ Automations`: Lịch trình tự động (Pre-flight Doctor, SQLite WAL sync, Token Guard).
     - `🧰 Customizations`: Mở thư viện 30 Universal Skills & Rules độc lập cho 14 vai trò AI.
   - **Khu vực Quản lý Dự án (Projects Tree)**:
     - Tiêu đề mục `Projects` kèm nút Lọc dự án `≡` và Thêm thư mục `📁⁺`.
     - Cây thư mục lồng nhau (Collapsible Accordion) hiển thị các dự án: `📁 FoodDelivery-Loyalty-App`, `📁 vietlot`, `📁 TV`, `📁 agent`, `📁 Remix Xuân Ý & Hoà...`.
     - Dưới dự án đang hoạt động (`FoodDelivery-Loyalty-App`), hiển thị 4 không gian làm việc cốt lõi kèm mốc thời gian:
       - `🧑‍💼 Bàn Làm Việc Alex (SPOC)` (`6m` trước - Active với dải nền xanh Alpine Teal nhạt `#F0FDFA` và thanh viền `#0D9488`).
       - `🎨 Xưởng Thiết Kế UI/UX` (`15m` trước).
       - `📋 Bảng Tiến Độ Kanban [6 Cột]` (`1h` trước).
       - `💻 Mã Nguồn & Monaco Diff` (`3h` trước).
       - Các phiên hội thoại chi tiết: `💬 Multi-Agent App Project...` (`6m` trước).
   - **Đáy thanh điều hướng (Bottom Fixed Dock)**:
     - Thẻ trạng thái Host: `● Host: 192.168.1.15:8080`.
     - Đồng hồ tiết kiệm Token: `🪙 42.5k saved via Daemon`.
     - Nút `⚙️ Settings`: Kích hoạt Cài đặt Dự án và Khóa An Toàn 2 Lớp (Antigravity Danger Zone Lock).
2. **Ban Kỹ Thuật Đẩy Lên Ngang Phía Trên (Horizontal Swarm Top Ribbon)**:
   - Xóa bỏ hoàn toàn thanh bên trái cũ làm dồn lệch giao diện.
   - Trải 13 chuyên gia (Marcus, Elena, David, Carlos, Lucas, Maya, Viktor, Liam, Sophia...) thành dải chip ngang mượt mà, kèm avatar, status dot và đồng hồ token `⚡`.
   - Alex PM có riêng khối Desk Pill sang trọng bên trái ruy-băng.
   - Nút `⏹️ DỪNG ĐỘT NGỘT (ESC)` và các chỉ báo hệ thống `🩺 7/7 OK`, `🔗 14 Live` được neo gọn gàng bên góc phải ruy-băng.
3. **Phối Màu Giữ Nguyên Clean Light Mode Tuyệt Đối (Theo Yêu Cầu Của Người Dùng)**:
   - Nền sứ Porcelain White (`#FFFFFF` & `#F8FAFC`), đường kẻ viền tinh tế `#E2E8F0`.
   - Màu nhận diện Alpine Teal (`#0D9488`), Tuscan Amber (`#D97706`), nhấn Fedora Brown (`#78350F`).
   - Tuyệt đối không dùng chế độ tối (Dark Mode) hay dải màu neon gây mỏi mắt.
