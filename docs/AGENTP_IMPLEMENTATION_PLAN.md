# KẾ HOẠCH TRIỂN KHAI XÂY DỰNG ỨNG DỤNG agentP
## (MASTER IMPLEMENTATION & VERIFIED EXECUTION ROADMAP)

> **Dự án**: Nền Tảng Điều Phối Đa Trí Tuệ Nhân Tạo **agentP**  
> **Chủ nhiệm dự án & Điều phối viên chính**: Alex (Trưởng Dự Án / Lead PM)  
> **Chiến lược sản phẩm & Trợ lý điều phối**: Marcus (Lead Business Analyst)  
> **Kiến trúc trưởng & CSDL**: Maya (Kiến Trúc Sư Hệ Thống) & Viktor (Lead QA)  
> **Chủ nhiệm thiết kế UI/UX**: Elena (Chuyên Gia UI/UX)  
> **Phiên bản kế hoạch**: v2.5.0 (Chính thức phê duyệt — Chuẩn hóa Tri-Modal Kanban & 10 Màn Hình Hợp Nhất)  
> **Mục tiêu cốt lõi**: Xây dựng ứng dụng hoàn chỉnh cho macOS, Windows, Android và Web theo đúng chuẩn 10 Màn hình, CSDL SQLite cục bộ `.agents/db.sqlite`, cơ chế cô lập session 1:1 qua agentP Core Daemon, và luồng làm việc duy nhất qua thanh chat với Alex.

---

## 1. TỔNG QUAN DỰ ÁN & CÔNG NGHỆ MỤC TIÊU (TECH STACK)

| Thành phần | Lựa chọn công nghệ | Lý do kỹ thuật | Phụ trách chính |
| :--- | :--- | :--- | :--- |
| **Desktop Shell** | **Tauri v2 (Rust)** | Khởi động tức thì, dung lượng <30MB, RAM cực nhẹ (<40MB so với Electron >250MB), an toàn, native APIs đa nền tảng. | **Liam** (DevOps) & **Lucas** (Senior Dev) |
| **Frontend UI** | **React 19 + TypeScript + Tailwind CSS** | Render hiệu năng cao, tích hợp mượt mà Monaco Editor, Tldraw và Onlook. | **David** (Frontend) & **Elena** (UI/UX) |
| **Bảng Màu Chính** | **Alpine Teal (`#0D9488`), Tuscan Amber (`#D97706`), Fedora Brown (`#78350F`)** | Chuẩn Clean Light Mode 100%, không neon, mang sắc thái đặc trưng của Agent P tinh tế, trang nhã. | **Elena** (UI/UX) |
| **Local Proxy Lõi** | **Rust / Python Local Daemon (agentP Core Daemon)** | Chạy tại `localhost:9090`, cô lập session 1:1 cho từng agent, tái sử dụng phiên đăng nhập CLI (`claude login`, `gh auth`), tối ưu chi phí. | **Carlos** (Backend) & **Liam** (DevOps) |
| **Whiteboard Engine** | **@tldraw/tldraw (Canvas Vector)** | Nhẹ, 0 setup, chạy offline 100%, hỗ trợ vẽ wireframe, sticky notes, sơ đồ luồng dữ liệu. | **Elena** (UI/UX) & **David** (Frontend) |
| **DOM-to-Code Engine**| **Onlook Core (Babel/PostCSS AST Sync)** | Nhúng trực tiếp dev server đang chạy, visual Tailwind inspector và ghi đè trực tiếp vào file `.tsx`/`.dart`. | **Lucas** (Senior Dev) & **David** (Frontend) |
| **Code Editor** | **Monaco Editor (VS Code core)** | Syntax highlighting đa ngôn ngữ, Side-by-Side Split Diff (Đỏ xóa / Xanh thêm), nút xóa file an toàn. | **Sam** (Fullstack) |
| **Cơ Sở Dữ Liệu** | **SQLite Cục Bộ (`.agents/db.sqlite`)** | WAL mode, foreign keys bật sẵn, lưu trữ projects, roles, sessions, chat history kèm `<thinking>`, Kanban tasks, git audits. | **Maya** (Architect) & **Carlos** (Backend) |
| **Hệ Thống Kanban** | **Tri-Modal System (Mode A, B, C)** | Tích hợp Mini-Kanban trên Bàn làm việc (Mode A), Drawer trượt (Mode B), và Studio 6 cột toàn màn hình (Mode C). | **Marcus** (BA) & **Alex** (Lead PM) |
| **DevOps & Testing**| **Docker, Android ADB Bridge, Jest, Flutter Test**| Tiền kiểm phần cứng, điều khiển máy ảo AVD Pixel 8, chạy test tự động 100% Pass trước khi vào Checkpoint. | **Liam** (DevOps), **Viktor** (QA Lead) & **Oliver** (Perf) |
| **Báo Cáo Nghiệm Thu**| **ExcelJS / SheetJS + Puppeteer PDF** | Xuất báo cáo nghiệm thu Excel `.xlsx` có màu sắc, công thức, định dạng chuẩn doanh nghiệp. | **Sophia** (Docs & Excel) |

---

## 2. CƠ CHẾ HOẠT ĐỘNG QUA THANH CHAT DUY NHẤT (SINGLE-DESK COMMAND WORKFLOW)

Người dùng (Chủ dự án) **CHỈ CẦN TƯƠNG TÁC QUA THANH CHAT VỚI ALEX**. Bạn không cần mở nhiều cửa sổ hay quản lý thủ công từng agent. Alex đóng vai trò là Tổng chỉ huy trực tiếp nhận lệnh từ bạn và điều phối 13 nhân sự hậu trường.

```
                    ┌────────────────────────────────────────────────────────┐
                    │               BẠN (CHỦ DỰ ÁN / USER)                   │
                    └───────────────────────────┬────────────────────────────┘
                                                │ 1. Nhập chỉ thị vào thanh chat
                                                │ 4. Bấm duyệt tại Checkpoint Gate
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🧑‍💼 ALEX (TRƯỞNG DỰ ÁN / LEAD PM) — ĐẦU MỐI DUY NHẤT                                         │
│ • Nhận lệnh, suy nghĩ sâu trong <thinking>, vạch chiến lược thực thi                        │
│ • Tách yêu cầu thành các Task ghi vào SQLite (.agents/db.sqlite)                            │
│ • Điều động và giao việc cho 13 nhân sự hậu trường (Backstage Swarm)                         │
│ • Theo dõi tiến độ Kanban, tổng hợp kết quả test từ Viktor                                  │
│ • Trình Checkpoint Gate lên chat stream cho Bạn duyệt                                       │
└───────────────────────────────────────────────┬─────────────────────────────────────────────┘
                                                │ 2. Dispatch Task (Session 1:1 qua agentP Core Daemon)
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🐝 ĐỘI NGŨ CHUYÊN VIÊN HẬU TRƯỜNG (BACKSTAGE SWARM - 13 ROLES)                              │
│                                                                                             │
│  [Marcus - BA]       ──► Viết User Stories & AC                  (GPT-4o)                  │
│  [Elena - UI/UX]     ──► Vẽ Wireframe Tldraw & Style Onlook      (Claude 3.5 Sonnet)       │
│  [Maya - Architect]  ──► Thiết kế SQLite DDL & API Contracts     (Claude 3.5 Sonnet)       │
│  [David - FE Dev]    ──► Code Flutter UI, BloC & Onlook Sync     (Gemini 2.5 Flash)        │
│  [Carlos - BE Dev]   ──► Code NestJS API, Service & DB Queries   (Claude 3.5 Sonnet)       │
│  [Viktor - QA Lead]  ──► Viết Unit & E2E Test (Jest/Flutter)     (DeepSeek R1)             │
│  [Liam - DevOps]     ──► Chạy Pre-flight, AVD Runner & Port 8080 (Gemini 2.5 Flash)        │
│  [Lucas - Senior]    ──► Soát lỗi AST & Clean Architecture       (Claude 3.5 Sonnet)       │
│  [Max - Git]         ──► Quản lý Git branch, tạo diff chuẩn      (Gemini 2.5 Flash)        │
│  [Sophia - Reports]  ──► Xuất báo cáo kỹ thuật Excel .xlsx       (Claude 3.5 Sonnet)       │
│  [Sam - Fullstack]   ──► Tích hợp Monaco Editor & Diff Split     (Gemini 2.5 Flash)        │
│  [Nora - Security]   ──► Rà soát lỗ hổng bảo mật & SQL Injection (DeepSeek R1)             │
│  [Oliver - Perf]     ──► Đo tải, benchmark RAM & FPS             (DeepSeek R1)             │
└───────────────────────────────────────────────┬─────────────────────────────────────────────┘
                                                │ 3. Báo cáo kết quả kiểm thử (Pass 100%)
                                                ▼
                               ┌──────────────────────────────────┐
                               │ 🛑 USER CHECKPOINT GATE (CHAT)   │
                               │ [✅ Duyệt & Merge] [📱 Thử AVD]  │
                               └──────────────────────────────────┘
```

### 2.1. Quy Trình Vận Hành Từng Bước (Step-by-Step Flow)
1. **Bước 1 — Tiếp Nhận Chỉ Thị**: Bạn gõ yêu cầu vào thanh chat (ví dụ: *"Hãy tạo module Giỏ hàng có áp mã voucher giảm giá"*).
2. **Bước 2 — Suy Nghĩ & Phân Tách Nhiệm Vụ**: Alex phân tích bài toán, hiển thị hộp `💭 RAW MODEL THINKING LOG` (`<thinking>`), sau đó ghi các thẻ công việc vào bảng `kanban_tasks` trong SQLite:
   - `TASK-099`: Marcus viết User Story.
   - `TASK-100`: Elena dựng wireframe giỏ hàng trên Tldraw.
   - `TASK-098`: Maya thiết kế DDL bảng voucher.
   - `TASK-102`: David code Flutter BloC.
   - `TASK-103`: Carlos code NestJS controller.
   - `TASK-101`: Viktor viết bộ test tự động.
3. **Bước 3 — Điều Động Độc Lập**: Alex gọi các agent thực hiện nhiệm vụ qua các session 1:1 của agentP Core Daemon. Thẻ Mini-Kanban trên cột phải tự động chuyển từ **To Do** sang **Coding**.
4. **Bước 4 — Kiểm Thử Tự Động Gắt Gao**: Viktor (QA Lead) chạy test suites. Nếu fail, tự động yêu cầu David hoặc Carlos sửa lại cho đến khi pass 100%. Task chuyển sang cột **QA Gate**.
5. **Bước 5 — Trình Checkpoint Gate**: Alex gửi thông báo chốt chặn màu hổ phách (`#FFFBEB`) ngay trên luồng chat kèm tóm tắt diff (+45 / -12 lines) và kết quả 8/8 test pass.
6. **Bước 6 — Phê Duyệt An Toàn**: Bạn bấm **"✅ Duyệt & Merge Git"** (hoặc duyệt từ xa qua điện thoại). Task tự động nhảy sang **Done**, Git commit được ghi nhận an toàn vào SQLite và repo.

---

## 3. DANH BẠ 14 NHÂN SỰ CHUYÊN TRÁCH CỦA agentP

| STT | Mã Vai Trò | Nhân Sự | Chuyên Môn / Trách Nhiệm | Model Chỉ Định |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `lead_pm` | 🧑‍💼 **Alex** | **Trưởng Dự Án (Lead/PM)**: Đầu mối duy nhất trao đổi với Bạn, phân chia task, kích hoạt checkpoint. | Claude 3.5 Sonnet |
| 2 | `ba_lead` | 📋 **Marcus** | **Lead Business Analyst**: Khảo sát nghiệp vụ, viết User Stories, quản trị Sprint backlog. | GPT-4o |
| 3 | `ui_ux_designer` | 🎨 **Elena** | **Chuyên Gia UI/UX**: Thiết kế Light Mode chuẩn Alpine Teal & Amber, vẽ Tldraw & style Onlook. | Claude 3.5 Sonnet |
| 4 | `system_architect`| 🏛️ **Maya** | **Kiến Trúc Sư Hệ Thống**: Thiết kế mô hình SQLite, quan hệ bảng, API contract và module flow. | Claude 3.5 Sonnet |
| 5 | `frontend_dev` | 💻 **David** | **Kỹ Sư Frontend Flutter**: Lập trình giao diện, BloC state, tích hợp visual DOM sync qua Onlook. | Gemini 2.5 Flash |
| 6 | `backend_dev` | ⚙️ **Carlos** | **Kỹ Sư Backend NestJS**: Lập trình REST API, TypeORM, logic nghiệp vụ, đồng bộ agentP Core Daemon. | Claude 3.5 Sonnet |
| 7 | `qa_lead` | 🔍 **Viktor** | **Trưởng Nhóm Kiểm Thử QA**: Soạn test Jest/Flutter, logic suy luận sâu, bảo đảm 100% Pass trước Checkpoint. | DeepSeek R1 |
| 8 | `devops_lead` | 🛡️ **Liam** | **Kỹ Sư DevOps & CI/CD**: Chạy Pre-flight diagnostics, điều khiển máy ảo AVD Pixel 8, WebSocket port 8080. | Gemini 2.5 Flash |
| 9 | `tech_lead` | 🔬 **Lucas** | **Senior Code Reviewer**: Rà soát AST parser, tối ưu thuật toán, đảm bảo Clean Architecture. | Claude 3.5 Sonnet |
| 10 | `security_auditor`| 🔒 **Nora** | **Chuyên Gia Bảo Mật**: Kiểm tra an toàn SQL, chống rò rỉ secret key, kiểm định xác nhận xóa dự án. | DeepSeek R1 |
| 11 | `perf_tester` | ⚡ **Oliver** | **Kỹ Sư Hiệu Năng**: Đo tải hệ thống, benchmark FPS, bộ nhớ RAM và tối ưu hóa thời gian khởi động. | DeepSeek R1 |
| 12 | `report_specialist`| 📊 **Sophia** | **Chuyên Gia Báo Cáo & Docs**: Soạn tài liệu kỹ thuật, xuất file Excel `.xlsx` đa phong cách. | Claude 3.5 Sonnet |
| 13 | `fullstack_dev` | 🚀 **Sam** | **Kỹ Sư Fullstack Tổng Hợp**: Phụ trách Monaco Editor, Side-by-Side Diff, và tính năng mở rộng. | Gemini 2.5 Flash |
| 14 | `git_specialist` | 🌿 **Max** | **Bậc Thầy Git**: Quản lý chiến lược phân nhánh, conflict resolution, Conventional Commits an toàn. | Gemini 2.5 Flash |

---

## 4. BỘ 10 MÀN HÌNH HỢP NHẤT TOÀN DIỆN (OFFICIAL 10-SCREEN SUITE)

Mọi màn hình đều đã được hoàn thiện dạng SVG chuẩn mực tại `docs/assets/`, sử dụng bảng màu **Alpine Teal (`#0D9488`)**, **Tuscan Amber (`#D97706`)**, **Porcelain White (`#F8FAFC`)** và huy hiệu **Fedora Brown (`#78350F`)**:

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │ BỘ 10 MÀN HÌNH HỢP NHẤT AGENTP (Tất cả file lưu tại docs/assets/)     │
 ├────────────────────────────────────────────────────────────────────────┤
 │ 1. screen_1_onboarding_launchpad.svg        (Khởi tạo ý tưởng ban đầu) │
 │ 2. screen_2_main_command_workspace.svg      (Chat + Mode A Mini-Kanban)│
 │ 3. screen_3_provider_connection_modal.svg   (Quản lý 1:1 sessions agentP Daemon)│
 │ 4. screen_4_mobile_remote_controller.svg    (Điều khiển từ xa Web/Phone)│
 │ 5. screen_5_preflight_diagnostics.svg       (Tiền kiểm 7 tiêu chí 100%)│
 │ 6. screen_6_project_file_explorer.svg       (Cây thư mục & Xuất Excel) │
 │ 7. screen_7_integrated_code_editor.svg      (Monaco Split Diff Đỏ/Xanh)│
 │ 8. screen_8_project_hub_edit_delete.svg     (Cài đặt & Xác nhận xóa)   │
 │ 9. screen_9_visual_ui_studio.svg            (Studio kép Tldraw+Onlook) │
 │ 10. screen_10_unified_kanban_system.svg     (Hệ thống Tri-Modal Kanban)│
 │ ── agentp_master_all_screens_showcase.svg   (Showcase tổng thể 10 hình)│
 └────────────────────────────────────────────────────────────────────────┘
```

---

## 5. LỘ TRÌNH 5 SPRINT TRIỂN KHAI CHI TIẾT (SPRINT ROADMAP)

```
[ SPRINT 1 ] ───► [ SPRINT 2 ] ───► [ SPRINT 3 ] ───► [ SPRINT 4 ] ───► [ SPRINT 5 ]
Lõi Hạ Tầng &      Onboarding &        Studio Kép UI/UX    Editor, File &      DevOps, Remote &
agentP Daemon      Workspace + Kanban  Tldraw + Onlook     Project Hub         Báo Cáo Nghiệm Thu
(Liam, Carlos)     (David, Alex)       (Elena, David)      (Sam, Lucas)        (Liam, Sophia, Viktor)
```

### SPRINT 1: NỀN TẢNG HẠ TẦNG & LÕI AGENTP CORE LOCAL DAEMON PROTOCOL
* **Mục tiêu**: Thiết lập khung dự án Tauri v2, cơ sở dữ liệu SQLite cục bộ `.agents/db.sqlite` và daemon proxy agentP Core Daemon cô lập session 1:1.
* **Nhân sự thực thi**: Liam (DevOps), Carlos (Backend), Maya (Architect), Lucas (Senior Dev).
* **Nhiệm vụ cụ thể**:
  1. *Maya & Carlos*: Khởi tạo file `.agents/db.sqlite` theo đúng đặc tả `docs/DATABASE_SCHEMA_SPEC.md` với đầy đủ 12 bảng, index và trigger đồng bộ Kanban khi duyệt Checkpoint.
  2. *Carlos*: Xây dựng Local Proxy Daemon tại `localhost:9090` hỗ trợ cô lập phiên 1:1 cho 14 agent roles, quản lý token usage và fallback failover.
  3. *Lucas & Carlos*: Xây dựng bộ bắt luồng token suy nghĩ thô (Raw Thinking Stream) cho Claude 3.5/3.7 (`<thinking>`), DeepSeek R1 (`reasoning_content`) và Gemini 2.5 (`thought`).
  4. *Liam*: Dựng khung dự án Tauri v2 (Rust + React 19 Shell), cấu hình bundle cho macOS và Windows.
* **Nghiệm thu (DoD)**: Proxy khởi chạy thành công, gọi thử nghiệm 14 model độc lập không xung đột context, stream được raw thinking log ra terminal.

---

### SPRINT 2: ONBOARDING, BÀN LÀM VIỆC ĐIỀU HÀNH & MINI-KANBAN LIVE
* **Mục tiêu**: Hiện thực hóa trải nghiệm cốt lõi: Bạn chỉ nói chuyện với Alex trên Bàn làm việc, Backstage Swarm chạy ngầm, và widget Mini-Kanban Live (Mode A) cập nhật thời gian thực.
* **Nhân sự thực thi**: David (Frontend), Alex (Lead/PM), Marcus (BA Lead), Viktor (QA Lead).
* **Nhiệm vụ cụ thể**:
  1. *Marcus & Alex*: Thuật toán phân tích mô tả đề tài để tự động sinh tên project chuẩn (Smart Auto-Naming).
  2. *David*: Lập trình Trang 1 Onboarding Launchpad (Clean Light Mode, thẻ nhập mô tả, nút khởi tạo dự án).
  3. *David & Alex*: Lập trình Trang 2 Main Command Workspace:
     - Cột trái: Bàn làm việc với Alex, danh sách 14 vai trò ngầm kèm đồng hồ đo Token (`🪙` và `⚡`), nút Dừng Đột Ngột (`ESC`).
     - Khung giữa: Luồng chat Bạn ⇄ Alex, Hộp Raw Model Thinking mở/gập, Cổng Checkpoint Gate màu hổ phách `#FFFBEB` với 3 nút bấm chuẩn.
     - **Cột phải (Mode A: Embedded Mini-Kanban Live Widget)**: 4 cột thu gọn (To Do, Coding, QA, Done), task card có badge agent, tóm tắt Git diff (+45/-12 lines) và bộ điều khiển AVD Pixel 8.
  4. *Viktor*: Viết bộ test kiểm tra phản hồi của nút Emergency Stop bảo đảm hủy tiến trình Agent dưới 100ms.
* **Nghiệm thu (DoD)**: Nhập bài toán $\rightarrow$ Vào thẳng bàn làm việc $\rightarrow$ Chat với Alex $\rightarrow$ Thẻ Kanban bên phải tự động nhảy trạng thái khi agent viết code và test.

---

### SPRINT 3: TRANG 9 STUDIO THIẾT KẾ UI/UX KÉP (TLDRAW + ONLOOK)
* **Mục tiêu**: Xóa bỏ khoảng cách giữa thiết kế và mã nguồn thực tế với 2 tab tương tác: Tldraw Whiteboard và Onlook DOM-to-Code.
* **Nhân sự thực thi**: Elena (UI/UX), David (Frontend), Lucas (Senior Dev), Carlos (Backend).
* **Nhiệm vụ cụ thể**:
  1. *Elena & David*: Nhúng thư viện `@tldraw/tldraw` vào Tab 1, hỗ trợ vẽ wireframe vector, sticky notes, liên kết flow màn hình và xuất file `.agents/designs/concept_board.tldr`.
  2. *Lucas & David*: Tích hợp lõi Onlook AST Synchronizer vào Tab 2:
     - Nhúng ứng dụng Flutter/React đang chạy qua iframe sandbox.
     - Click-to-inspect phần tử UI, thanh Tailwind CSS inspector, điều chỉnh màu sắc sang Alpine Teal & Tuscan Amber.
  3. *Lucas & Carlos*: Cơ chế đồng bộ AST 2 chiều: Khi chỉnh sửa trên Onlook, tự động cập nhật trực tiếp vào file source code trong thư mục dự án với độ trễ dưới 50ms.
* **Nghiệm thu (DoD)**: Vẽ nháp trên Tldraw $\rightarrow$ Dev sinh code $\rightarrow$ Mở Onlook click đổi màu nút bấm $\rightarrow$ File code thật cập nhật ngay lập tức.

---

### SPRINT 4: FILE EXPLORER, MONACO SPLIT DIFF & PROJECT HUB CHUẨN ANTIGRAVITY
* **Mục tiêu**: Hoàn thiện bộ công cụ quản lý tệp tin, xem/sửa code dạng split diff và kiểm soát an toàn vòng đời dự án.
* **Nhân sự thực thi**: Sam (Fullstack), Max (Git), Nora (Security), Viktor (QA Lead).
* **Nhiệm vụ cụ thể**:
  1. *Sam*: Lập trình Trang 6 File Explorer: Cây thư mục, nhãn agent đảm nhiệm từng file, banner xuất báo cáo Excel, thùng rác an toàn `.agents/trash/`.
  2. *Sam & Max*: Lập trình Trang 7 Integrated Code Editor (Monaco Editor):
     - Syntax highlighting đa ngôn ngữ, chế độ Side-by-Side Split Diff (Đỏ xóa / Xanh thêm).
     - Nút xóa file an toàn, nút phục hồi commit cũ và chấp nhận diff.
  3. *Sam & Nora*: Lập trình Trang 8 Project Hub & Modal Cài Đặt / Xóa Dự Án:
     - Modal sửa cấu hình, metadata và biến môi trường.
     - Vùng nguy hiểm: Cơ chế xác nhận xóa 2 lớp kiểu Antigravity, bắt buộc gõ chính xác tên dự án để mở khóa nút xóa vĩnh viễn.
  4. *Viktor*: Test tự động bảo đảm nút Xóa Vĩnh Viễn bị khóa 100% nếu gõ sai dù chỉ 1 ký tự.
* **Nghiệm thu (DoD)**: Mọi thao tác File, Code Diff và Xóa/Sửa dự án hoạt động an toàn, không có nguy cơ mất dữ liệu ngoài ý muốn.

---

### SPRINT 5: DEVOPS TIỀN KIỂM, MOBILE REMOTE CONTROLLER & BÁO CÁO NGHIỆM THU DOANH NGHIỆP
* **Mục tiêu**: Triển khai hạ tầng điều khiển từ xa qua di động, quản lý máy ảo Android và xuất báo cáo số liệu chuẩn mực.
* **Nhân sự thực thi**: Liam (DevOps), Sophia (Docs/Excel), Oliver (Perf), Viktor (QA Lead).
* **Nhiệm vụ cụ thể**:
  1. *Liam*: Lập trình Trang 5 Pre-flight System Diagnostics:
     - Quét và kiểm tra 7 tiêu chí: Flutter SDK, Android Studio & AVD, Node.js 20, Git, SQLite engine, agentP Core Daemon, và port 8080.
     - Quản lý vòng đời AVD: Tạo, khởi chạy Pixel 8 Pro ở chế độ Cửa sổ GUI hoặc Headless ngầm.
  2. *Liam & David*: Lập trình Trang 4 Mobile Remote Controller:
     - Khởi chạy WebSocket Server trên máy tính (Host Online port 8080).
     - Tạo mã QR Pairing để điện thoại Android/iOS kết nối qua Wi-Fi cục bộ, xem tiến độ và bấm duyệt Checkpoint từ xa.
  3. *Sophia*: Xây dựng module xuất báo cáo số liệu kỹ thuật tự động:
     - Kết xuất file Excel `.xlsx` chuyên nghiệp gồm danh sách file, số dòng code, phân bổ token từng role, chi phí tiết kiệm được, định dạng chuẩn màu sắc doanh nghiệp.
  4. *Viktor & Oliver*: Chạy tổng kiểm thử toàn diện E2E Test Suite trên cả Web và Android AVD thật, benchmark thời gian khởi động dưới 2 giây.
* **Nghiệm thu (DoD)**: Điện thoại quét mã duyệt được Checkpoint, máy ảo Android chạy mượt mà, Sophia xuất được file Excel nghiệm thu chuẩn chỉ 100%.

---

## 6. TIÊU CHUẨN NGHIỆM THU CHẤT LƯỢNG (DEFINITION OF DONE - DOD)

Mọi tính năng của **agentP** chỉ được coi là hoàn tất khi thỏa mãn 5 điều kiện ngặt nghèo:
1. **Giao Diện Chuẩn Xác**: Tuân thủ 100% phong cách Clean Minimalist Light Mode, sắc xanh Alpine Teal `#0D9488`, hổ phách Tuscan Amber `#D97706` và điểm nhấn Fedora Brown `#78350F`, tuyệt đối không có màu neon.
2. **Hiệu Năng & Độ Trễ**: Thời gian khởi động ứng dụng <2 giây, RAM nền <45MB, thời gian phản hồi thao tác visual <16ms (60 FPS).
3. **An Toàn Dữ Liệu**: Cơ sở dữ liệu SQLite cục bộ bảo toàn dữ liệu khi tắt đột ngột (WAL mode), mọi hành động xóa code hoặc xóa project đều qua cổng xác nhận an toàn hoặc chuyển vào thùng rác nội bộ.
4. **Kiểm Thử Toàn Diện**: Suite Unit & Integration Tests đạt tỷ lệ Pass 100%, độ bao phủ Code Coverage tối thiểu 85%.
5. **Đồng Thuận Của Bạn (User Checkpoint)**: Chỉ bàn giao và đóng sprint khi Bạn (User) trực tiếp bấm duyệt tại Checkpoint Gate trên màn hình chat hoặc trên điện thoại di động.

---
*Tài liệu được cập nhật và bảo chứng thực thi bởi Alex (Trưởng Dự Án), Marcus (Lead BA), Maya (Architect), Elena (UI/UX) và Viktor (QA Lead).*
