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
│   └── state_machine.py         <-- Kanban State Machine Transitions
├── adapters/                    <-- ADAPTERS (External Integrations)
│   ├── sqlite_adapter.py        <-- SQLiteStorageAdapter (StoragePort)
│   └── daemon_adapter.py        <-- AgentPDaemonAdapter (LlmGatewayPort)
├── services/                    <-- APPLICATION SERVICES
│   ├── auto_namer.py            <-- Smart Auto-Naming
│   ├── ast_sync.py              <-- AST 2-way Synchronization
│   ├── project_manager.py       <-- File Explorer, Safe Trash & Danger Zone
│   └── command_workspace.py     <-- Command Workspace Facade
├── daemon/
│   └── router.py                <-- agentP Core Local Daemon
└── web/                         <-- PRESENTATION LAYER
    ├── index.html               <-- Left Nav Rail (Antigravity Style)
    ├── style.css                <-- Clean Light Mode CSS
    └── app.js                   <-- Reactive Client Logic
```
