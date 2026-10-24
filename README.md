# agentP — Developer Multi-Agent Desktop Suite 🚀

> **Hệ Thống Điều Phối Đa Tác Nhân Trí Tuệ Nhân Tạo (Multi-Agent Swarm Platform)**  
> **Kiến trúc**: Single-Desk Command (Alex Lead/PM làm SPOC duy nhất) + 13 Chuyên Viên Kỹ Thuật Hậu Trường  
> **Phong cách UI/UX**: Google Antigravity 2.0 Navigation Tree + 100% Clean Light Mode (Porcelain White, Alpine Teal, Tuscan Amber, Fedora Brown)  
> **Lõi Giao Thức**: agentP Core Local Protocol Daemon (Chạy độc lập, không phụ thuộc bên ngoài)  
> **Phiên bản hiện tại**: v2.6.0  

---

## 📌 1. TRIẾT LÝ THIẾT KẾ & LUỒNG LÀM VIỆC ĐƠN BÀN (SINGLE-DESK)

Trong **agentP**, người dùng (Chủ dự án / Boss) **chỉ cần tương tác duy nhất với Alex (Trưởng Dự Án / Lead PM)** qua thanh chat. Bạn không cần chuyển tab thủ công hay quản lý 14 cửa sổ chat rời rạc:

```
                            ┌────────────────────────────────────────┐
                            │        BẠN (CHỦ DỰ ÁN / USER)          │
                            └───────────────────┬────────────────────┘
                                                │ 1. Ra lệnh vào thanh chat
                                                │ 4. Phê duyệt tại Cổng Checkpoint
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🧑‍💼 ALEX (TRƯỞNG DỰ ÁN / LEAD PM) — ĐẦU MỐI DUY NHẤT (SPOC)                                   │
│ • Tiếp nhận yêu cầu, suy nghĩ đa chiều trong thẻ <thinking>                                  │
│ • Phân rã bài toán thành các Task kỹ thuật trong SQLite (.agents/db.sqlite)                  │
│ • Điều phối 13 nhân sự hậu trường (Backstage Swarm) theo cơ chế cô lập 1:1                   │
│ • Giám sát tiến độ Live Kanban 6 cột, nhận kết quả kiểm thử tự động từ Viktor QA             │
│ • Trình Cổng Kiểm Duyệt (User Checkpoint Gate #04) màu Hổ Phách lên khung chat               │
└───────────────────────────────────────────────┬─────────────────────────────────────────────┘
                                                │ 2. Ủy thác nhiệm vụ (Session 1:1)
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🐝 BAN KỸ THUẬT HẬU TRƯỜNG (BACKSTAGE SWARM - 13 CHUYÊN GIA)                                │
│                                                                                             │
│  [Marcus - BA]       ──► Phân rã User Stories & Acceptance Criteria (DoD)                    │
│  [Elena - UI/UX]     ──► Vẽ phác thảo Tldraw & Tinh chỉnh CSS Onlook (Rose Pink)            │
│  [Maya - Architect]  ──► Thiết kế CSDL SQLite WAL & Contract API (Cyan Teal)                │
│  [David - FE Dev]    ──► Lập trình Giao diện Flutter & React 19 (Ocean Sky Blue)            │
│  [Carlos - BE Dev]   ──► Xây dựng REST API, Daemon & Repositories (Emerald Green)            │
│  [Lucas - Senior]    ──► Lập trình Lõi Core Engine & AST Sync 2 chiều (Royal Indigo)         │
│  [Viktor - QA Lead]  ──► Kiểm thử tự động E2E, Unit Tests & Coverage >80% (Ruby Crimson)    │
│  [Liam - DevOps]     ──► Đóng gói Bundle, Android AVD Pixel 8 Pro Bridge (Tangerine Orange) │
│  [Frank - SRE]       ──► Độ tin cậy hệ thống & Chống sập tiến trình (Deep Purple)            │
│  [Sophia - Security] ──► Kiểm toán bảo mật & Khóa An Toàn Danger Zone (Gold Bronze)         │
│  [Chloe - Data]      ──► Báo cáo KPI, Xuất Excel .xlsx & Quản trị Token (Mint Teal)          │
│  [Sarah - Docs]      ──► Biên soạn tài liệu kỹ thuật & Keep a Changelog (Slate Gray)         │
│  [Oliver - Perf]     ──► Tối ưu độ trễ render <16.6ms & Bộ nhớ đệm Token (Cobalt Blue)       │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 2. GIAO DIỆN CHUẨN GOOGLE ANTIGRAVITY 2.0 (CLEAN LIGHT MODE)

Giao diện được tái cấu trúc toàn diện theo chuẩn **Google Antigravity 2.0**:

- **Cánh Trái (Width 260px)**:
  - Bộ điều khiển macOS Traffic Lights (🔴 🟡 🟢) kèm các icon thu gọn `◫`, quay lui `←`, tiến tới `→`, và tìm kiếm nhanh `🔍`.
  - Nút bấm `+ New Conversation` (`+ Tạo Cuộc Hội Thoại Mới`).
  - Liên kết cấp cao (Global): `🔌 Kết Nối AI Providers` (Trang kết nối độc lập 9router Hub: OAuth CLI, Free, API Key, Compatible).
  - Cây thư mục dự án (Collapsible Projects Tree): Dưới dự án `📁 FoodDelivery-Loyalty-App` phân nhánh các không gian làm việc chuyên biệt: `🧑‍💼 Bàn Làm Việc Alex`, `🎨 Xưởng Thiết Kế UI/UX`, `📋 Bảng Tiến Độ Kanban`, `💻 Mã Nguồn & Monaco Diff`, `📱 Mobile Pairing & AVD`, `👥 Quản Lý Nhân Sự` (14 AI Specialists & Phân bổ AI Models linh hoạt), `🩺 Tiền Kiểm Hệ Thống` kèm mốc thời gian thực.
  - Chân trang: Đèn mạng `● Host: 192.168.1.15:8080`, đồng hồ `🪙 42.5k saved` và nút `⚙️ Settings` (mở Khóa 2 lớp Antigravity Danger Zone).
- **Ruy-Băng Trên Đỉnh (Top Swarm Ribbon - 52px)**:
  - Xóa bỏ việc dồn ép bên trái, trải 14 chuyên viên kỹ thuật thành dải chip ngang phân màu theo nhóm chuyên môn (Amber, Pink, Blue, Green, Indigo, Red, Orange, Purple...).
  - Alex PM có Desk Pill riêng màu Alpine Teal `#F0FDFA`.
  - Tích hợp nút mở nhanh `🔌 AI Providers Hub`, `📱 Mobile Pairing`, chỉ số tiền kiểm `🩺 7/7 OK`, nhân sự `👥 14 Roles`, và nút khẩn cấp `⏹️ DỪNG ĐỘT NGỘT (ESC)`.
- **Hệ Màu Clean Light Mode 100%**:
  - Porcelain White (`#FFFFFF`), Slate Canvas (`#F8FAFC`).
  - Alpine Teal (`#0D9488`), Tuscan Amber (`#D97706`), Fedora Brown (`#78350F`).
  - Tuyệt đối không dùng Dark Mode hoặc màu neon gây mỏi mắt.

---

## 🏛️ 3. HỆ THỐNG DESIGN PATTERNS ĐÃ ÁP DỤNG TRONG CODEBASE

Dự án tuân thủ nghiêm ngặt các mẫu thiết kế hướng đối tượng kinh điển (GoF) và kiến trúc doanh nghiệp:

1. **Mediator Pattern**: Alex PM đóng vai trò Mediator duy nhất tiếp nhận lệnh và điều phối 13 vai trò kỹ thuật, ngăn chặn bão token và liên lạc chéo hỗn loạn.
2. **Hexagonal Architecture (Ports & Adapters)**: Tách biệt lõi Domain khỏi CSDL SQLite, Local Daemon và giao diện Web.
3. **Front Controller & Action Dispatcher Pattern**: File `src/daemon/router.py` được tinh gọn xuống **<90 dòng**, chuyển giao toàn bộ yêu cầu HTTP cho `RequestDispatcher` (`src/core/dispatcher.py`) điều phối đến các Controller chuyên biệt.
4. **Repository Pattern**: Tách biệt toàn bộ câu lệnh SQL thô ra khỏi controller, đóng gói vào tầng `src/repositories/` (`KanbanRepository`, `SkillsRepository`, `SessionsRepository`).
5. **Strategy Pattern**: Thuật toán tính toán dòng so sánh split diff được đóng gói vào `src/services/diff_strategy.py` theo giao diện `DiffStrategyInterface`.
6. **State Machine Pattern**: Kiểm soát chu trình chuyển đổi nghiêm ngặt của thẻ công việc qua 6 cột Kanban: `Backlog ➔ Spec/Design ➔ Development ➔ Review ➔ Quality Gate ➔ Done`.
7. **Observer Pattern**: Phát và bắt sự kiện tự động cập nhật Live Kanban, Git Staging và AVD Runner.
8. **Command & Memento Pattern**: Hỗ trợ nút Emergency Stop ESC hủy tiến trình trong <15ms và cơ chế hoàn tác thùng rác an toàn.

---

## 📂 4. CẤU TRÚC THƯ MỤC CHUẨN HÓA (DIRECTORY MAP)

```
agentP/
├── docs/                                  <-- TÀI LIỆU HỆ THỐNG & ĐẶC TẢ CHI TIẾT
│   ├── UI_UX_DESIGN_SYSTEM.md             <-- Đặc tả 10 màn hình, Token màu, Antigravity Sidebar
│   ├── DESIGN_PATTERNS_RESEARCH.md        <-- Nghiên cứu 8 Design Patterns & Quyết định của Marcus
│   ├── AGENTP_IMPLEMENTATION_PLAN.md      <-- Kế hoạch tổng thể 5 Sprints & Lộ trình thực thi
│   ├── DATABASE_SCHEMA_SPEC.md            <-- Cấu trúc 16 bảng SQLite WAL & Triggers
│   ├── MULTI_AGENT_APP_SPEC.md            <-- Đặc tả 14 Agent Roles, Persona & Sessions 1:1
│   └── assets/                            <-- Bản vẽ Vector Artboards (.svg) & Mockups
├── src/
│   ├── core/                              <-- DOMAIN CORE & DISPATCHER
│   │   ├── mediator.py                    <-- AlexMediator (Mediator Pattern)
│   │   ├── ports.py                       <-- Inbound & Outbound Ports
│   │   ├── state_machine.py               <-- Kanban State Machine Transitions
│   │   └── dispatcher.py                  <-- RequestDispatcher (Front Controller)
│   ├── controllers/                       <-- MODULAR HTTP CONTROLLERS (<100 lines/file)
│   │   ├── base_controller.py             <-- BaseController & JSON responders
│   │   ├── workspace_controller.py        <-- Chat Bạn ⇄ Alex, Checkpoint Gate
│   │   ├── kanban_controller.py           <-- 6 cột Kanban & Move task
│   │   ├── studio_controller.py           <-- Dual-Mode UI Studio & AST Sync
│   │   ├── code_controller.py             <-- File Tree, Monaco Split Diff, Trash
│   │   ├── project_controller.py          <-- Auto-Naming, Settings, Danger Zone
│   │   ├── skills_controller.py           <-- 30 Universal Skills API
│   │   ├── protocol_controller.py         <-- Health, Sessions 1:1, Thinking Stream
│   │   ├── devops_controller.py           <-- AVD Pixel 8 Pro, Remote Pairing, Excel Export
│   │   └── static_controller.py           <-- Phục vụ tệp tĩnh Web & Assets
│   ├── repositories/                      <-- REPOSITORY PATTERN (Data Layer)
│   │   ├── base_repo.py                   <-- SQLite WAL Connection Manager
│   │   ├── kanban_repo.py                 <-- Truy vấn & Cập nhật Kanban tasks
│   │   ├── skills_repo.py                 <-- Nạp & Lọc 30 Universal Skills
│   │   └── sessions_repo.py               <-- Quản lý 14 Sessions & Token Metrics
│   ├── adapters/                          <-- HEXAGONAL ADAPTERS
│   │   ├── sqlite_adapter.py              <-- SQLiteStorageAdapter
│   │   └── daemon_adapter.py              <-- AgentPDaemonAdapter
│   ├── services/                          <-- APPLICATION SERVICES
│   │   ├── auto_namer.py                  <-- Thuật toán sinh tên dự án tự động
│   │   ├── ast_sync.py                    <-- AST Sync Engine 2 chiều (<50ms)
│   │   ├── diff_strategy.py               <-- Monaco Split Diff Strategy
│   │   ├── project_manager.py             <-- File Explorer, Safe Trash, Danger Zone
│   │   ├── avd_controller.py              <-- AVD Pixel 8 Pro, Hot Reload & Screenshot
│   │   ├── remote_controller.py           <-- Mobile Remote Pairing & WebSocket Host
│   │   ├── preflight_service.py           <-- Pre-flight Diagnostics 7 Criteria Service
│   │   ├── excel_reporter.py              <-- Corporate Acceptance Excel/CSV Reporter
│   │   └── command_workspace.py           <-- Workspace Facade
│   ├── daemon/
│   │   └── router.py                      <-- agentP Core Local Daemon (<95 lines)
│   └── web/                               <-- GIAO DIỆN FRONTEND
│       ├── index.html                     <-- Antigravity 2.0 Sidebar & 8 Full Views (All 10 Screens)
│       ├── style.css                      <-- Clean Light Mode CSS + Role Domain Colors
│       └── app.js                         <-- Client SPA Script điều khiển tương tác
├── .agents/
│   ├── db.sqlite                          <-- CSDL Cục Bộ SQLite WAL Mode
│   ├── skills/                            <-- 30 Bộ Kỹ Năng Độc Lập (.agents/skills/*/SKILL.md)
│   └── trash/                             <-- Thùng rác nội bộ an toàn (Safe Trash)
├── reports/                               <-- BÁO CÁO NGHIỆM THU DOANH NGHIỆP
│   └── agentp_acceptance_report.csv       <-- Báo cáo số liệu kỹ thuật, token & chi phí
├── scripts/
│   └── preflight.py                       <-- Bác Sĩ Tiền Kiểm 7 Tiêu Chí (Pre-flight Doctor)
└── test/                                  <-- TOÀN BỘ BỘ TEST TỰ ĐỘNG (48/48 PASS)
    ├── test_sprint5_devops_reports.py     <-- Test AVD, Remote Pairing, Preflight & Excel
    ├── test_modular_controllers.py        <-- Test Dispatcher, Repositories & Controllers
    ├── test_design_patterns.py            <-- Test Mediator, Hexagonal & State Machine
    ├── test_agentp_protocol.py            <-- Test Health, Sessions 1:1, Thinking Log
    ├── test_sqlite_architecture.py        <-- Test WAL, Foreign Keys & 16 Bảng
    ├── test_workspace_command.py          <-- Test Chat stream & Checkpoint Gate
    ├── test_smart_autoname.py             <-- Test Auto-Naming regex & heuristics
    ├── test_studio_ast_sync.py            <-- Test Đồng bộ AST 2 chiều
    └── test_file_explorer_danger_zone.py  <-- Test Safe Trash & Danger Zone Lock
```

---

## 🧰 5. THƯ VIỆN 30 KỸ NĂNG & QUY TẮC CHUYÊN BIỆT (30 UNIVERSAL SKILLS)

Tất cả 14 chuyên viên AI được nạp sẵn 30 kỹ năng độc lập tại `.agents/skills/`:
- **Quản Trị & Yêu Cầu (4)**: `agile-sprint-breakdown`, `smart-auto-naming`, `risk-checkpoint-gate`, `cost-token-guard`.
- **Kiến Trúc & CSDL (4)**: `sqlite-wal-optimization`, `fastapi-async-daemon`, `api-contract-first`, `c4-architecture-modeling`.
- **Thiết Kế UI/UX (4)**: `design-tokens-crafting`, `tldraw-canvas-wireframing`, `onlook-dom-to-code`, `responsive-layout-builder`.
- **Lập Trình Frontend (4)**: `react-tailwind-components`, `flutter-bloc-state-machine`, `ast-sync-bidirectional`, `hot-reload-diagnostics`.
- **Lập Trình Backend (4)**: `event-driven-pubsub`, `session-isolation-protocol`, `jwt-rbac-authenticator`, `chaos-resilience-testing`.
- **Kiểm Thử & QA (4)**: `unit-test-coverage-enforcer`, `e2e-playwright-automation`, `a11y-wcag-compliance`, `preflight-system-doctor`.
- **DevOps & Bảo Mật (4)**: `android-avd-manager`, `docker-multistage-bundle`, `git-branching-conventional`, `security-danger-zone-guard`.
- **Tài Liệu & Báo Cáo (2)**: `excel-corporate-reporter`, `changelog-release-notes`.

---

## 🩺 6. HƯỚNG DẪN KHỞI CHẠY & KIỂM ĐỊNH CHẤT LƯỢNG

### Bước 1: Chạy Bác Sĩ Tiền Kiểm Hệ Thống (7 Tiêu chí)
```bash
python3 scripts/preflight.py
```
*Kết quả chuẩn: 7/7 tiêu chí hoàn toàn sẵn sàng (100%).*

### Bước 2: Chạy Toàn Bộ Test Suites Tự Động (56 tests)
```bash
python3 -m unittest discover -s test
```
*Kết quả chuẩn: 56/56 tests PASS trong <0.15s (Sprint 1 -> Sprint 6).*

### Bước 3: Khởi Chạy agentP Core Daemon
```bash
python3 src/daemon/router.py
```
*Truy cập giao diện tại: [http://127.0.0.1:9090](http://127.0.0.1:9090)*

---

## 📜 7. NGUYÊN TẮC BẢO TOÀN VÀ ĐỒNG BỘ TÀI LIỆU (DOCUMENTATION INTEGRITY PROTOCOL)

> **CHỈ THỊ CỐT LÕI TỪ ALEX (LEAD PM)**:  
> Mọi thay đổi về mã nguồn (Dev), cơ sở dữ liệu (Maya), quy trình (Marcus) hay giao diện (Elena) **BẮT BUỘC PHẢI CẬP NHẬT ĐỒNG THỜI VÀO TÀI LIỆU TƯƠNG ỨNG TRONG THƯ MỤC `docs/` VÀ `README.md`**. Tuyệt đối không để xảy ra tình trạng tài liệu lỗi thời (outdated) so với mã nguồn thực tế.
