# 🏛️ NGHIÊN CỨU & KHẢO SÁT DESIGN PATTERNS CHO HỆ THỐNG AGENTP
**Tác giả**: Alex (Project Lead & Research Analyst)  
**Phê duyệt & Lựa chọn**: Marcus (Lead Business Analyst)  
**Đội ngũ thực thi**: Maya (Architect), Carlos (Backend), David (Frontend), Viktor (QA Lead)

---

## 1. TỔNG QUAN BÀI TOÁN KIẾN TRÚC

Hệ thống **agentP** là ứng dụng desktop đa tác nhân (Multi-Agent System) với **14 vai trò chuyên biệt** hoạt động ngầm, phục vụ một người dùng duy nhất (Boss/User) thông qua **Bàn làm việc chỉ huy (Single-Desk Command)**.

Để đảm bảo hệ thống mở rộng tốt, không bị nghẽn cổ chai (bottleneck), không xung đột phiên làm việc và bảo toàn tính toàn vẹn dữ liệu cục bộ, Alex đã nghiên cứu và lập bảng đánh giá **5 Design Patterns kinh điển** trong ngành công nghệ phần mềm:

---

## 2. BẢNG KHẢO SÁT 5 DESIGN PATTERNS CHI TIẾT

```
+---------------------------------------------------------------------------------------------------+
| PATTERN             | MỤC ĐÍCH ỨNG DỤNG TRONG AGENTP             | ĐÁNH GIÁ CỦA ALEX & MAYA       |
+---------------------+--------------------------------------------+--------------------------------+
| 1. Mediator         | Điều phối 14 agent roles không giao tiếp   | ⭐⭐⭐⭐⭐ Xuất sắc cho bài      |
|    Pattern          | chéo hỗn loạn. Alex là trung gian duy nhất.| toán Single-Desk SPOC.         |
|                     |                                            |                                |
| 2. Hexagonal        | Tách biệt nghiệp vụ cốt lõi khỏi SQLite,   | ⭐⭐⭐⭐⭐ Hoàn hảo cho tính     |
|    (Ports & Adapts) | LLM Daemon và giao diện Web/Tauri OS.      | module hóa và thay thế DB/LLM. |
|                     |                                            |                                |
| 3. Observer         | Bắn sự kiện khi Checkpoint được duyệt hoặc | ⭐⭐⭐⭐ Rất tốt cho cập nhật     |
|    (Event-Driven)   | code AST được đồng bộ sang Kanban/AVD.     | thời gian thực (Reactive UI).  |
|                     |                                            |                                |
| 4. Command &        | Đóng gói mọi thao tác thành đối tượng để   | ⭐⭐⭐⭐ Cần thiết cho ESC      |
|    Memento          | hỗ trợ Emergency Stop ESC và Undo thùng rác| Dừng đột ngột và Safe Trash.   |
|                     |                                            |                                |
| 5. State Machine    | Kiểm soát chu trình chuyển đổi 6 cột       | ⭐⭐⭐⭐ Chuẩn hóa quy trình     |
|    Pattern          | Kanban và các trạng thái Checkpoint Gate.  | kiểm duyệt chất lượng DoD.     |
+---------------------+--------------------------------------------+--------------------------------+
```

---

## 3. PHÂN TÍCH CHUYÊN SÂU TỪNG PATTERN

### Pattern 1: Mediator Pattern (Bộ Điều Phối Trung Gian)
- **Vấn đề**: Nếu 14 chuyên gia (BA, UI/UX, FE, BE, QA, DevOps) tự do gọi lẫn nhau, số lượng kênh liên lạc sẽ tăng theo cấp số nhân: $C = \frac{14 \times 13}{2} = 91$ kênh. Điều này gây bão token (token storm), mất đồng bộ context và người dùng không thể kiểm soát.
- **Giải pháp**: Alex đóng vai trò **Mediator**. Mọi chỉ thị từ Boss đều đi qua Alex; Alex phân tích AST/Spec, giao việc cho từng agent chuyên trách và nhận báo cáo về để tổng hợp gửi lại Boss.

### Pattern 2: Hexagonal Architecture (Kiến Trúc Lục Giác / Ports & Adapters)
- **Vấn đề**: Việc viết code SQL trực tiếp trong các controller/daemon khiến logic nghiệp vụ bị trói chặt vào SQLite hoặc HTTP server.
- **Giải pháp**:
  - **Core Domain**: Quản lý nghiệp vụ Sprints, Tasks, Checkpoints, AST Sync, File Tree.
  - **Inbound Ports**: `CommandPort` (Giao tiếp với UI Web/Tauri/Mobile).
  - **Outbound Ports**: `StoragePort` (CSDL SQLite WAL), `LlmGatewayPort` (agentP Core Daemon), `EventBusPort` (Thông báo sự kiện).
  - **Adapters**: Cho phép cắm/rút CSDL hoặc đổi mô hình AI mà không phải sửa 1 dòng code nghiệp vụ nào.

### Pattern 3: Observer / Event-Driven Pub-Sub
- Cho phép các thành phần UI như Live Kanban, Git Staging Diff và AVD Runner tự động cập nhật khi có sự kiện `CheckpointApprovedEvent` hoặc `AstSyncedEvent` mà không cần polling liên tục.

### Pattern 4: Command & Memento Pattern
- Đóng gói thao tác thành `ExecuteTaskCommand` và `RevertDiffCommand`. Nút **Emergency Stop (ESC)** chỉ cần hủy lệnh đang thực thi trong hàng đợi Command Queue với độ trễ <15ms.

### Pattern 5: State Machine Pattern
- Định nghĩa các trạng thái hợp lệ của một Task trong Kanban:
  $$\text{Backlog} \longrightarrow \text{Spec/Design} \longrightarrow \text{Development} \longrightarrow \text{Review} \longrightarrow \text{Quality Gate} \longrightarrow \text{Done}$$
- Chặn đứng việc nhảy cóc (ví dụ: từ Backlog nhảy thẳng sang Done mà chưa qua Quality Gate của Viktor QA).

---

## 4. QUYẾT ĐỊNH CỦA MARCUS (LEAD BA) VÀ LỘ TRÌNH REFACTOR

Sau khi nghiên cứu kỹ đề xuất của Alex, **Marcus đã lựa chọn mô hình kết hợp tối ưu nhất**:

> **QUYẾT ĐỊNH CHÍNH THỨC CỦA MARCUS**:  
> Chúng ta sẽ áp dụng **Mô Hình Kết Hợp: Mediator Pattern + Hexagonal Architecture (Ports & Adapters)**.  
> - **Alex** là Mediator trung tâm điều phối toàn bộ Swarm 14 vai trò và tiếp nhận lệnh từ User.  
> - **Hexagonal Architecture** tạo ra ranh giới module rõ ràng, phân định rạch ròi giữa Domain, Ports và Adapters.

---

## 5. CẤU TRÚC THƯ MỤC SAU KHI REFACTOR

```
src/
├── core/                        <-- DOMAIN CORE (Pure Business Logic)
│   ├── mediator.py              <-- AlexMediator (Mediator Pattern)
│   ├── ports.py                 <-- Abstract Ports (Storage, Gateway, Events)
│   ├── state_machine.py         <-- Kanban State Machine Transitions
│   └── dispatcher.py            <-- RequestDispatcher (Front Controller Pattern)
├── controllers/                 <-- HTTP ROUTE CONTROLLERS (Single Responsibility)
│   ├── base_controller.py       <-- BaseController interface & JSON responder
│   ├── workspace_controller.py  <-- Chat, Swarm Roles & Checkpoint Gate
│   ├── kanban_controller.py     <-- 6-column Kanban & Task status transitions
│   ├── code_controller.py       <-- File Tree, Content & Safe Trash
│   ├── project_controller.py    <-- Auto-Naming, Settings & Danger Zone
│   ├── skills_controller.py     <-- 30 Universal Skills querying & filtering
│   └── static_controller.py     <-- Static assets & HTML serving
├── repositories/                <-- REPOSITORY PATTERN (Database Decoupling)
│   ├── base_repo.py             <-- SQLite WAL Connection Manager
│   ├── kanban_repo.py           <-- Kanban Tasks persistence
│   ├── skills_repo.py           <-- Agent Skills querying
│   └── sessions_repo.py         <-- Provider Sessions & Role tracking
├── adapters/                    <-- ADAPTERS (External Integrations)
│   ├── sqlite_adapter.py        <-- SQLiteStorageAdapter (StoragePort)
│   └── daemon_adapter.py        <-- AgentPDaemonAdapter (LlmGatewayPort)
├── services/                    <-- APPLICATION SERVICES
│   ├── auto_namer.py            <-- Smart Auto-Naming
│   ├── ast_sync.py              <-- AST 2-way Synchronization
│   ├── diff_strategy.py         <-- Monaco Split Diff Strategy Engine
│   ├── project_manager.py       <-- File Explorer, Safe Trash & Danger Zone
│   └── command_workspace.py     <-- Command Workspace Facade
├── daemon/
│   └── router.py                <-- Lightweight HTTP Daemon Entrypoint (<90 lines)
└── web/                         <-- PRESENTATION LAYER
    ├── index.html               <-- Left Nav Rail (Antigravity 2.0 Hierarchy)
    ├── style.css                <-- Clean Light Mode CSS + Role Domain Colors
    └── app.js                   <-- Modular Reactive Client
```

---

## 6. BỔ SUNG THIẾT KẾ DESIGN PATTERNS CHO MÃ NGUỒN DEV (CODE BREAKDOWN)
Theo chỉ thị của chủ dự án về việc rã nhỏ (break down) các file mã nguồn quá dài để code gọn gàng, dễ xem, dễ bảo trì và dễ truy xuất, **Alex** đã nghiên cứu và **Marcus** phê duyệt kế hoạch áp dụng thêm 4 Design Patterns chuyên biệt cho Dev:

### Pattern 6: Front Controller & Action Dispatcher Pattern (Web Architecture)
- **Vấn đề**: File `src/daemon/router.py` phình to lên >420 dòng với hàng chục khối `if path == ... elif path == ...` lồng nhau phức tạp, nhồi nhét cả logic database và định dạng dữ liệu trực tiếp trong phương thức `do_GET` và `do_POST`.
- **Giải pháp**: Xây dựng `RequestDispatcher` (`src/core/dispatcher.py`). Chia tách các endpoint thành các **Controller độc lập** (`src/controllers/`):
  1. `WorkspaceController`: Quản lý `/api/workspace`, chat Bạn ⇄ Alex, phản hồi Checkpoint.
  2. `KanbanController`: Quản lý `/api/kanban/all`, kéo thả task giữa 6 cột.
  3. `CodeController`: Quản lý cây file `/api/files/tree`, diff Monaco `/api/code/diff`, xóa file `/api/files/delete`.
  4. `ProjectController`: Quản lý sinh tên tự động `/api/auto-name`, `/api/project/settings`, xác thực 2 lớp xóa dự án `/api/project/verify-delete`.
  5. `SkillsController`: Quản lý tra cứu 30 Universal Skills `/api/skills`.
  6. `StaticController`: Phục vụ tệp tĩnh HTML/CSS/JS/Assets.
- **Hiệu quả**: `router.py` rút gọn từ 424 dòng xuống còn dưới 90 dòng, chỉ đóng vai trò khởi tạo server và giao việc cho Dispatcher.

### Pattern 7: Repository Pattern (Data Access Decoupling)
- **Vấn đề**: Các câu lệnh SQL thô (`SELECT`, `INSERT`, `UPDATE`) nằm rải rác trong `router.py` và các handler, gây khó khăn khi viết Unit Test và dễ rò rỉ kết nối SQLite WAL.
- **Giải pháp**: Tạo tầng `src/repositories/` chuyên trách:
  - `BaseRepository`: Đóng gói kết nối SQLite WAL, bật `foreign_keys = ON`.
  - `KanbanRepository`: Chuyên trách truy vấn và cập nhật 6 cột Kanban.
  - `SkillsRepository`: Chuyên trách nạp và lọc 30 bộ kỹ năng chuyên biệt.
  - `SessionsRepository`: Chuyên trách 14 phiên cô lập và định mức tiêu thụ token.
- **Hiệu quả**: Tách biệt hoàn toàn tầng dữ liệu khỏi tầng HTTP, mỗi file repository dưới 80 dòng, dễ dàng mock trong kiểm thử.

### Pattern 8: Strategy Pattern cho Thuật Toán So Sánh Mã Nguồn (Diff Engine)
- **Vấn đề**: Hàm `compute_monaco_split_diff` trong `project_manager.py` xử lý logic phức tạp (tách dòng, đánh dấu added/deleted/context lines) chiếm dung lượng lớn.
- **Giải pháp**: Đóng gói thuật toán sinh diff vào `src/services/diff_strategy.py` theo giao diện `DiffStrategyInterface`.
- **Hiệu quả**: `project_manager.py` trở nên nhẹ nhàng, tập trung đúng nghiệp vụ file explorer và thùng rác an toàn.

---

## 7. CHỈ ĐẠO CỦA MARCUS (LEAD BA) GỬI ĐỘI DEV THỰC THI (DoD)
1. **Tiêu chí nghiệm thu (DoD)**:
   - Tất cả các file controller mới trong `src/controllers/` phải dưới 120 dòng code.
   - File `src/daemon/router.py` phải dưới 100 dòng code.
   - Không được làm gián đoạn bất kỳ endpoint API nào đang phục vụ frontend.
   - Toàn bộ 29/29 test suites hiện có phải vượt qua 100%.
   - Bổ sung unit tests cho Dispatcher và Controller mới.
2. **Phân công thực thi**:
   - **Carlos (Backend Dev)**: Xây dựng `src/core/dispatcher.py` và các Controller trong `src/controllers/`.
   - **Maya (Architect)**: Xây dựng tầng `src/repositories/` chuẩn hóa truy xuất SQLite WAL.
   - **Lucas (Senior Dev)**: Trích xuất `src/services/diff_strategy.py`.
   - **Viktor (QA Lead)**: Viết test suite `test/test_modular_controllers.py` kiểm định tính đúng đắn.
