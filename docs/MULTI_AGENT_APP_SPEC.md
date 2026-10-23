# TÀI LIỆU ĐẶC TẢ KIẾN TRÚC & YÊU CẦU DỰ ÁN TOÀN DIỆN (MASTER PRD & SYSTEM SPECIFICATION)
## DỰ ÁN: NỀN TẢNG ĐIỀU PHỐI ĐA TRÍ TUỆ NHÂN TẠO agentP

> **Phiên bản**: v3.5.0 (Master Comprehensive Edition — Tích Hợp Hệ Thống Kanban Đa Tầng Hợp Nhất: Mini-Kanban, Drawer & Full-Board)  
> **Chủ nhiệm dự án & Điều phối tổng thể**: Alex (Project Lead & Research Analyst)  
> **Chiến lược sản phẩm & Trợ lý điều hành**: Marcus (Product Strategist & Assistant)  
> **Thiết kế UI/UX & Sáng tạo**: Elena (UI/UX & Creative Designer)  
> **Trạng thái**: Đã phê duyệt chính thức — Đang tích hợp hệ thống Kanban phản ứng tự động

---

## MỤC LỤC TỔNG QUAN

1. [Tầm Nhìn & 8 Trụ Cột Cốt Lõi](#1-tầm-nhìn--8-trụ-cột-cốt-lõi)
2. [Hệ Thống 14 Vai Trò Chuyên Biệt (Roles & Skill Matrix)](#2-hệ-thống-14-vai-trò-chuyên-biệt-roles--skill-matrix)
3. [Lõi Provider 1:1 agentP Core Daemon & Gán Model Thủ Công](#3-lõi-provider-11-agentp-core-daemon--gán-model-thủ-công)
4. [Mô Hình Phối Hợp: Bàn Làm Việc Duy Nhất & Đội Ngũ Kỹ Thuật Ngầm](#4-mô-hình-phối-hợp-bàn-làm-việc-duy-nhất--đội-ngũ-kỹ-thuật-ngầm)
5. [Thu Thập Luồng Suy Nghĩ Nguyên Bản (Raw Model Thinking Log)](#5-thu-thập-luồng-suy-nghĩ-nguyên-bản-raw-model-thinking-log)
6. [Hệ Thống Đo Lường Token Theo Role (Token Load Icons & Live Meter)](#6-hệ-thống-đo-lường-token-theo-role-token-load-icons--live-meter)
7. [Bộ Điều Khiển Tương Tác: Dừng Khẩn Cấp, Revert & CRUD Chat](#7-bộ-điều-khiển-tương-tác-dừng-khẩn-cấp-revert--crud-chat)
8. [Quản Lý Đa Dự Án & Ngữ Cảnh Độc Lập (Context Architecture)](#8-quản-lý-đa-dự-án--ngữ-cảnh-độc-lập-context-architecture)
9. [Khu Vực Quản Lý File Dự Án (Project File Manager)](#9-khu-vực-quản-lý-file-dự-án-project-file-manager--asset-explorer)
10. [Trang Trình Soạn Thảo & Xem/Sửa/Xóa Code (Integrated Code Editor)](#10-trang-trình-soạn-thảo--xemsửaxóa-code-integrated-code-editor--diff-viewer)
11. [Hệ Sinh Thái Thiết Kế UI/UX Kép: Tldraw + Onlook (Dual-Engine Studio)](#11-hệ-sinh-thái-thiết-kế-uiux-kép-tldraw--onlook-dual-engine-design-studio)
12. [Hệ Thống Kanban Phản Ứng Tự Động Hợp Nhất (Tri-Modal Kanban System)](#12-hệ-thống-kanban-phản-ứng-tự-động-hợp-nhất-tri-modal-agentic-kanban-system)
13. [Hạ Tầng Đa Nền Tảng, Remote Host & DevOps Tiền Kiểm](#13-hạ-tầng-đa-nền-tảng-remote-host--devops-tiền-kiểm)
14. [Lộ Trình Tương Lai: Tự Chuyển Model Thông Minh Khi Hết Token](#14-lộ-trình-tương-lai-tự-chuyển-model-thông-minh-khi-hết-token)

---

## 1. TẦM NHÌN & 8 TRỤ CỘT CỐT LÕI

Dự án xây dựng một **Nền tảng Điều phối Đa Trí Tuệ Nhân Tạo Đa Nền Tảng (macOS, Windows, Android, Web)** cho phép một cá nhân duy nhất (Bạn/Chủ dự án) vận hành cả một phòng ban phát triển phần mềm chuyên môn hóa cao.

### 8 Trụ Cột Kiến Trúc Vững Chắc:
1. **Trang Khởi Tạo Thông Minh (Smart Onboarding Launchpad)**: Bắt đầu bằng câu hỏi tối giản *"Bạn muốn tạo project gì?"*, phân tích mô tả sơ bộ để tự động sinh tên project chuẩn (kebab-case), khởi tạo workspace và đưa người dùng vào việc ngay lập tức.
2. **Lõi Provider 1:1 agentP Core Daemon**: Đóng vai trò Local Reverse Proxy Daemon nội bộ. Ưu tiên tối đa việc tái sử dụng tài khoản/phiên đăng nhập có sẵn trên máy (như `claude login`, `cursor`, `gh auth/copilot`, session tokens) thay vì bắt buộc dùng API key trả phí.
3. **Gán Model Thủ Công Sau Khi Kết Nối (Dynamic Model Binding)**: Quét danh sách model khả dụng từ các profile đã kết nối thành công, cho phép người dùng tự tay chỉ định model tối ưu cho từng Role.
4. **Bàn Làm Việc Điều Hành Duy Nhất (Single Point of Contact - SPOC)**: Người dùng chỉ trao đổi trực tiếp với **Trưởng dự án (Lead/PM)**. Toàn bộ 13 role kỹ thuật còn lại (BA, UI/UX, Architect, Dev, QA, DevOps, Docs/Excel Specialist) hoạt động dưới dạng **Đội ngũ Kỹ thuật Ngầm (Backstage Swarm)**, triệt tiêu hoàn toàn gánh nặng phải vào từng phòng chat.
5. **Nhật Ký Suy Nghĩ Nguyên Bản (Raw Model Thinking Log)**: Trích xuất 100% token suy nghĩ thực tế từ payload của các model thế hệ mới (`<thinking>`, `reasoning_content`, `thought`), không giả lập hay biên soạn lại.
6. **Kiểm Soát Tương Tác Toàn Năng**: Trang bị nút Dừng đột ngột (Emergency Stop), khả năng quay lui thời gian (Time-travel Revert), chạy lại (Rerun) và Thêm/Xóa/Sửa bất kỳ tin nhắn nào trong lịch sử để tinh lọc ngữ cảnh.
7. **Hạ Tầng Đa Nền Tảng, Remote Host & DevOps Toàn Diện**: Chạy native trên máy tính, có khả năng làm Host Server để điện thoại Android hoặc Web kết nối điều khiển từ xa. Tích hợp tiền kiểm hạ tầng (ổ đĩa, RAM, ảo hóa, cổng mạng) và quản lý máy ảo Android (AVD).
8. **Hệ Sinh Thái Thiết Kế UI/UX Kép Tldraw + Onlook**: Kết hợp hoàn hảo giữa bàn phác thảo ý tưởng tự do (Tldraw Whiteboard / Make Real) và studio trực tiếp chỉnh sửa mã nguồn thật (Onlook DOM-to-Code WYSIWYG), xóa bỏ hoàn toàn rào cản và độ trễ chuyển giao giữa bản vẽ và code thật.

---

## 2. HỆ THỐNG 14 VAI TRÒ CHUYÊN BIỆT (ROLES & SKILL MATRIX)

Hệ thống phân tách rạch ròi 14 chuyên môn, mỗi role được nạp bộ System Prompt chuyên biệt và quyền truy cập vào các công cụ MCP (Model Context Protocol) tương ứng:

```
                                  ┌───────────────────────────┐
                                  │      BẠN (USER / BOSS)    │
                                  └─────────────┬─────────────┘
                                                │ (Chỉ đạo & Duyệt Checkpoint)
                                                ▼
                                  ┌───────────────────────────┐
                                  │     PROJECT LEAD / PM     │
                                  │  (Kèm Trợ lý Runner)      │
                                  └─────────────┬─────────────┘
                                                │
         ┌──────────────────────────────────────┼──────────────────────────────────────┐
         ▼                                      ▼                                      ▼
┌─────────────────────────┐            ┌─────────────────────────┐            ┌─────────────────────────┐
│     PRODUCT & DOCS      │            │  TECH & ARCHITECTURE    │            │   DEV, TEST & RELEASE   │
│ • BA (Business Analyst) │            │ • Tech Lead             │            │ • Frontend Dev          │
│ • UI/UX Designer        │            │ • System Architect      │            │ • Backend Dev           │
│ • Docs & Excel Reporter │            │                         │            │ • Fullstack Dev         │
│                         │            │                         │            │ • QA Specialist (Manual)│
│                         │            │                         │            │ • Automation Tester     │
│                         │            │                         │            │ • Git Specialist        │
│                         │            │                         │            │ • DevOps Specialist     │
└─────────────────────────┘            └─────────────────────────┘            └─────────────────────────┘
```

### Bảng Ma Trận 14 Nhân Sự Chuyên Môn & Kỹ Năng Chi Tiết (agentP Swarm Roster):

| STT | Nhân sự & Vai trò | Trách nhiệm chi tiết | Bộ Skill / MCP Tools tích hợp | Tiêu chí Nghiệm thu Bàn giao (Hand-off Gate) |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Alex**<br>`(Project Lead / PM)` | Đầu mối duy nhất trao đổi trực tiếp với Bạn; rã task, điều phối đội ngũ ngầm, tổng hợp nghiệm thu. **Có quyền chạy trực tiếp: Build dự án, Push Git, tạo task Jira** hoặc giao việc cho Marcus. | `jira_mcp`, `git_direct`, `terminal_exec`, `task_matrix`, `report_gen` | Bạn (User) ký duyệt tại Checkpoint Gate. |
| **2** | **Marcus**<br>`(Assistant & Runner)` | Trợ lý chiến lược & thực thi tác vụ phụ trợ ngoài luồng: dọn dẹp thư mục rác, tải tài liệu tham khảo, đồng bộ Jira ticket, cập nhật changelog thô, điều phối luồng sprint. | `terminal_exec`, `jira_mcp`, `file_ops`, `web_fetch` | Alex xác nhận task phụ đã hoàn thành. |
| **3** | **Liam**<br>`(Business Analyst)` | Phân tích nghiệp vụ sâu, viết User Stories và Tiêu chí nghiệm thu (Acceptance Criteria - AC), phản biện tính khả dụng cùng Elena và Lucas. | `prd_writer`, `user_flow_doc`, `spec_diff_analyzer` | Đồng thuận 100% với Elena và Lucas. |
| **4** | **Elena**<br>`(UI/UX Designer)` | Thiết kế Wireframe trên **Tldraw** (Whiteboard tự do / Make Real), xây dựng Design System (Light Mode), quản trị Design Tokens (`colors`, `spacing`), và trực tiếp tinh chỉnh UI trên mã nguồn thật thông qua **Onlook** (DOM-to-Code AST Sync). | `tldraw_canvas_mcp`, `onlook_ast_sync`, `design_tokens`, `svg_previewer`, `theme_builder` | Liam và Bạn nghiệm thu giao diện trên Onlook Live Studio. |
| **5** | **Lucas**<br>`(Tech Lead)` | Nhạc trưởng kỹ thuật: Review code, gỡ vướng mắc logic phức tạp, định hướng giải pháp kỹ thuật, kiểm soát chuẩn Clean Code và kiến trúc phần mềm. | `code_review_tool`, `ast_navigator`, `dependency_auditor` | Code đáp ứng tiêu chuẩn trước khi chuyển sang Nora & Oliver. |
| **6** | **Maya**<br>`(System Architect)` | Thiết kế kiến trúc tổng thể, mô hình thực thể dữ liệu (Database Schema), API Contract (OpenAPI/gRPC), phân tách ranh giới module. | `db_schema_gen`, `openapi_spec`, `system_diagram_mermaid` | Lucas và Victor nhất trí phương án kỹ thuật. |
| **7** | **Chloe**<br>`(Frontend Developer)` | Lập trình giao diện (React, Tailwind, Flutter), quản lý State phía client, tích hợp API, đảm bảo độ mượt mà và tương thích màn hình. | `file_editor`, `package_manager`, `component_preview`, `linter` | Giao diện chạy đúng spec, bàn giao cho Nora & Oliver. |
| **8** | **Victor**<br>`(Backend Developer)` | Viết API Endpoints, xử lý Business Logic, tối ưu truy vấn Database PostgreSQL, phân quyền xác thực và an toàn dữ liệu. | `file_editor`, `sql_runner`, `api_tester`, `linter` | API phản hồi chuẩn 100%, bàn giao cho Nora & Oliver. |
| **9** | **Sam**<br>`(Fullstack Developer)` | Đảm nhiệm các tính năng khép kín (end-to-end), các module độc lập hoặc dựng nhanh các bản mẫu Proof-of-Concept (PoC). | `file_editor`, `terminal_exec`, `fullstack_templates` | Hoàn thành cả UI và API của module. |
| **10**| **Nora**<br>`(QA Specialist - Manual)`| Thiết kế kịch bản kiểm thử (Test Cases), kiểm tra kịch bản biên (Edge-cases), lập Bug Report chi tiết trả về cho Chloe & Victor. | `test_case_manager`, `bug_tracker`, `diff_inspector` | Không còn lỗi nghiêm trọng (Critical/Major). |
| **11**| **Oliver**<br>`(Automation Tester)` | Viết và chạy suite Unit Test, E2E Test, Integration Test tự động trên môi trường Web và Android giả lập, đo độ phủ code. | `run_terminal_command`, `jest_pytest_runner`, `coverage_checker` | Tỷ lệ Pass đạt 100%, Coverage tối thiểu 80%. |
| **12**| **Max**<br>`(Git Specialist)` | Quản lý nhánh (Branching Strategy), giải quyết Conflict, kiểm tra chuẩn Conventional Commits, tạo PR sạch sẽ. | `git_visual_manager`, `conflict_resolver`, `changelog_gen` | Nhánh sạch, sẵn sàng merge mà không xung đột. |
| **13**| **Leo**<br>`(DevOps Specialist)` | Quản trị hạ tầng: Docker, **chạy máy ảo giả lập Android (AVD) GUI/Headless**, chạy tiền kiểm phần cứng (Pre-flight), mạng, cổng, CI/CD. | `system_diagnostics_mcp`, `android_sdk_mcp`, `docker_mcp`, `ci_cd_validator`, `env_guard`, `port_checker` | Môi trường xanh, không bị lỗi phần cứng/bảo mật. |
| **14**| **Sophia**<br>`(Docs & Excel Specialist)`| Chuyên trách soạn thảo tài liệu (API Docs, Technical Specs, User Manual, Release Notes) và **lập báo cáo số liệu chuyên nghiệp (Excel `.xlsx` chuẩn doanh nghiệp có công thức/định dạng màu, CSV, PDF, Markdown)**. **Tự động biến chuyển phong cách theo môi trường làm việc**: Môi trường Doanh nghiệp/Khách hàng (Formal, Excel KPI/Chi phí/Tiến độ, bảng biểu rõ ràng); Môi trường Startup/Tech (Docusaurus, GitBook, Notion Markdown); Môi trường Open Source (CONTRIBUTING, README, Wiki). | `excel_generator_mcp`, `markdown_docs_mcp`, `pdf_exporter`, `data_aggregator`, `i18n_translator` | File Excel/Docs định dạng chuẩn chỉnh, số liệu chính xác 100%. |

---

## 3. LÕI PROVIDER 1:1 AGENTP CORE DAEMON & GÁN MODEL THỦ CÔNG

### 3.1. Cơ Chế Reverse Proxy Cục Bộ (Tái Sử Dụng Phiên Đăng Nhập):
Lõi daemon nội bộ `agentp-core-daemon`: Đại đa số người dùng đã có gói thuê bao (Claude Pro/Team, Cursor Pro, ChatGPT Plus, GitHub Copilot). Bắt người dùng trả thêm tiền API là rào cản lớn. Do đó agentP tự động nhận diện và tái sử dụng các phiên đăng nhập sẵn có.
* Hệ thống khởi chạy một **Local Daemon** (`localhost:PORT`).
* Hỗ trợ trích xuất phiên đăng nhập trực tiếp từ:
  * `claude login` (Claude CLI Session).
  * `gh auth login` (GitHub Copilot CLI).
  * Session token từ trình duyệt hoặc Cursor credentials.
  * Local Ollama API (chạy offline miễn phí 100%).
* Lõi Proxy thực hiện giả lập header và đóng gói request gửi đi, biến mọi tài khoản thành một endpoint chuẩn OpenAI-compatible nội bộ.

### 3.2. Quy Tắc Gán Model Thủ Công (Manual Binding Rule):
* Hệ thống **tuyệt đối không gán cứng model** cho bất kỳ role nào.
* Sau khi Bạn bấm kết nối thành công một Profile, hệ thống sẽ truy vấn danh sách model mà Profile đó được quyền dùng.
* Tại bảng cài đặt Role, menu thả xuống chỉ hiển thị đúng các model khả dụng để Bạn tự do lựa chọn (ví dụ: gán Claude 3.7 Sonnet cho Lead/PM, DeepSeek R1 cho Dev, Gemini Flash cho QA).

---

## 4. MÔ HÌNH PHỐI HỢP: BÀN LÀM VIỆC DUY NHẤT & ĐỘI NGŨ KỸ THUẬT NGẦM

### 4.1. Khái Niệm Bàn Làm Việc Duy Nhất (Single-Desk Command):
* Bạn chỉ nhìn thấy **1 Bàn làm việc chính với Trưởng dự án (Lead/PM)**.
* Mọi đề tài, chỉ đạo chiến lược đều được trao đổi trực tiếp với PM.
* Bạn không phải quản lý từng phòng họp lẻ tẻ, không phải chuyển tab liên tục.

### 4.2. Cơ Chế Điều Phối Ngầm (Backstage Swarm & Dynamic Looping):
Khi Bạn giao một yêu cầu, PM sẽ kích hoạt quy trình điều phối ngầm tự động:
1. **Khảo sát & Thiết kế**: PM giao BA viết User Story $\rightarrow$ BA tự động hội thảo với UI/UX để vẽ Wireframe $\rightarrow$ Tech Lead phản biện tính khả thi.
2. **Kiến trúc Dữ liệu**: System Architect thiết kế bảng dữ liệu (DB Schema) và API Contract $\rightarrow$ Backend Dev rà soát.
3. **Lập trình & Tự sửa lỗi Khép kín (Dev-QA Loop)**:
   * Frontend & Backend Dev viết code.
   * Ngay khi viết xong, task tự động chuyển cho Automation Tester chạy test suite.
   * Nếu test fail, QA gửi log lỗi trả lại cho Dev sửa ngay tại chỗ (tối đa 3 vòng lặp). Chỉ khi Pass 100%, task mới được chuyển tiếp.
4. **Đóng gói & Trình Checkpoint**: Git Specialist chuẩn bị commit sạch, DevOps kiểm tra build thành công $\rightarrow$ PM tổng hợp toàn bộ kết quả trình lên **Cổng Phê Duyệt (User Checkpoint Gate)** để Bạn nghiệm thu.

---

## 5. THU THẬP LUỒNG SUY NGHĨ NGUYÊN BẢN (RAW MODEL THINKING LOG)

Hệ thống cam kết tính trung thực và minh bạch tuyệt đối, **không dùng suy nghĩ giả lập**:
* Bắt trọn vẹn luồng token suy nghĩ gốc từ nhà cung cấp:
  * Khối `<thinking>...</thinking>` của **Claude 3.7 Sonnet (Thinking Enabled)**.
  * Trường `reasoning_content` của **DeepSeek R1** và **OpenAI o1/o3**.
  * Luồng `thought` chunks của **Gemini 2.0 Thinking**.
* Trên giao diện, khối suy nghĩ được hiển thị dạng Accordion thanh nhã:
  * Hiển thị thời gian suy nghĩ và số lượng token tiêu thụ: `💭 RAW THINKING LOG: Thought for 8.4s (1,248 tokens) [▲]`.
  * Cho phép Bạn mở ra đọc toàn bộ quá trình model tự vấn, lập luận các phương án loại trừ và tự sửa sai trước khi chốt phương án.

---

## 6. HỆ THỐNG ĐO LƯỜNG TOKEN THEO ROLE (TOKEN LOAD ICONS & LIVE METER)

Nhằm giúp Bạn kiểm soát chặt chẽ ngân sách và mức độ tiêu hao tài nguyên của từng thành viên AI:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 👥 ĐỘI NGŨ KỸ THUẬT NGẦM (SWARM LIVE MONITOR)                          │
├────────────────────────────────────────────────────────────────────────┤
│ • 🧑‍💼 Lead / PM        : 🟢 Sẵn sàng    │ 🪙 12.4k tk  (Claude 3.7)     │
│ • 📋 Business Analyst  : 🟢 Xong Specs   │ 🪙  3.2k tk  (Claude 3.5)     │
│ • 🏛️ System Architect  : 🟢 Xong Schema  │ 🪙  5.1k tk  (Claude 3.7)     │
│ • 💻 Frontend Dev      : 🔵 Đang code    │ ⚡ 18.6k tk  (DeepSeek R1)    │
│ • ⚙️ Backend Dev       : 🔵 Đang code    │ ⚡ 14.2k tk  (DeepSeek R1)    │
│ • 🧪 Automation QA     : 🟡 Chờ test     │ 🪙  2.8k tk  (Haiku 3.5)      │
│ • 🚀 DevOps Specialist : 🟢 Build Sẵn    │ 🪙  1.9k tk  (Claude 3.5)     │
└────────────────────────────────────────────────────────────────────────┘
```

* **Biểu tượng Token (Token Load Icon)**:
  * Biểu tượng `🪙` (Coin) cho các model tính token tiêu chuẩn.
  * Biểu tượng `⚡` (Bolt) cho các model suy nghĩ sâu (Reasoning models như DeepSeek R1).
* **Đồng hồ đo trực tiếp (Real-time Token Counter)**: Nhảy số theo thời gian thực khi từng role đang stream phản hồi.
* **Cảnh báo tải (Load Threshold Warning)**: Đổi màu từ Xanh $\rightarrow$ Vàng khi một role tiêu tốn vượt quá định mức (ví dụ trên 50,000 tokens trong một task) để Bạn chủ động kiểm tra.

---

## 7. BỘ ĐIỀU KHIỂN TƯƠNG TÁC: DỪNG KHẨN CẤP, REVERT & CRUD CHAT

* ⏹️ **Nút Dừng Khẩn Cấp (Emergency Stop - Phím tắt `Esc`)**:
  * Khi các Agent đang stream chữ, gọi tool MCP hoặc chạy lệnh terminal, nút Gửi sẽ tự động chuyển thành **Nút Dừng Đột Ngột màu đỏ**.
  * Bấm nút này: Ngắt ngay lập tức kết nối socket/stream, hủy lệnh tiến trình terminal và đóng băng trạng thái hiện tại an toàn.
* ↩️ **Quay Lui Thời Gian (Time-Travel Revert)**:
  * Cho phép Bạn quay ngược toàn bộ dự án (lịch sử chat + trạng thái mã nguồn Git) về đúng thời điểm trước một tin nhắn chỉ định. Giúp Bạn thử nghiệm hướng đi khác mà không lo hỏng code.
* 🔄 **Chạy Lại (Rerun)**:
  * Gọi lại model cho một tin nhắn nhất định (ví dụ: đổi sang model khác hoặc bổ sung thêm lưu ý).
* ✏️ **Chỉnh Sửa & Xóa Tin Nhắn (CRUD Chat History)**:
  * Bạn có quyền sửa lại câu hỏi của mình, xóa bỏ các tin nhắn rác hoặc đoạn chat lỗi để làm sạch Context Window, giúp các role hoạt động chính xác và tiết kiệm token tối đa.

---

## 8. QUẢN LÝ ĐA DỰ ÁN & NGỮ CẢNH ĐỘC LẬP (CONTEXT ARCHITECTURE)

```
[PROJECT WORKSPACE ROOT]
│
├── .agents/
│   ├── project.yaml             # Cấu hình project, role mapping & model profile
│   ├── shared_knowledge/        # BỘ NHỚ CHUNG CỦA DỰ ÁN (Project Knowledge Bank)
│   │   ├── prd_specs.md         # Yêu cầu nghiệp vụ đã chốt từ BA
│   │   ├── design_tokens.json   # Hệ thống màu sắc, font, spacing từ UI/UX
│   │   ├── architecture.md      # Cấu trúc thư mục, API Contract từ Architect
│   │   └── changelog.md         # Lịch sử thay đổi code từ Git Specialist
│   │
│   ├── context_vector.db        # Vector DB cục bộ (SQLite/LanceDB) phục vụ tìm kiếm ngữ cảnh
│   └── sessions/                # CÁC PHIÊN LÀM VIỆC ĐỘC LẬP
│       ├── session_cart.json    # Phiên làm chức năng Giỏ hàng
│       └── session_auth.json    # Phiên làm chức năng Đăng nhập
```

* **Quy tắc phân vùng Context**: Mỗi Session chỉ lưu lịch sử hội thoại của chính nó để tránh phình token.
* **Bộ nhớ dùng chung (Selective Shared Knowledge)**: Các role khi cần dữ liệu nền tảng sẽ dùng công cụ `read_shared_context` để trích xuất đúng tài liệu liên quan trong `shared_knowledge/`.

### 8.2. Cơ Chế Quản Lý, Sửa & Xóa Dự Án Toàn Năng (Chuẩn Antigravity Workspace Manager):
Tương tự như cơ chế quản trị Workspace trong Google Antigravity, người dùng có toàn quyền kiểm soát vòng đời của mọi dự án:

1. **Chỉnh Sửa Dự Án (Edit Project Metadata & Directives)**:
   * **Đổi tên dự án**: Cập nhật Display Name và thư mục Slug.
   * **Chỉnh sửa Mô tả & Chỉ đạo cốt lõi (Project System Directives)**: Cập nhật lại yêu cầu bài toán hoặc bổ sung quy chuẩn code riêng cho dự án này để Lead/PM và các Sub-agent luôn tuân thủ.
   * **Thay đổi Đường dẫn Thư mục (Relocate Workspace Path)**: Di chuyển hoặc trỏ lại thư mục mã nguồn sang ổ đĩa khác.
   * **Cấu hình lại Model Role**: Tinh chỉnh lại danh sách model phân công cho từng Role cụ thể trong file `.agents/project.yaml`.
   * **Quản trị Biến môi trường (`.env` Editor)**: Xem và sửa các API keys bí mật, biến môi trường của dự án với chế độ ẩn/hiện an toàn.

2. **Xóa & Gỡ Bỏ Dự Án An Toàn (Delete / Unlink Workspace với 2 Chế độ)**:
   * **Lựa chọn 1: Chỉ gỡ bỏ khỏi Ứng dụng (Unlink / Remove from App)**:
     * Giữ nguyên 100% tệp tin mã nguồn, lịch sử git trên ổ cứng của bạn.
     * Chỉ xóa dự án khỏi bảng danh sách điều hành của agentP. Có thể Import lại bất kỳ lúc nào.
   * **Lựa chọn 2: Xóa hoàn toàn khỏi Ổ cứng (Permanent Disk Delete)**:
     * Xóa sạch toàn bộ thư mục dự án và dữ liệu context trên máy tính.
     * **Cổng xác nhận an toàn (Safety Gate)**: Bắt buộc người dùng phải gõ chính xác tên dự án (ví dụ: nhập đúng dòng chữ `FoodDelivery-Loyalty-App`) thì nút *Xóa Vĩnh Viễn* màu đỏ mới sáng lên, triệt tiêu hoàn toàn nguy cơ bấm nhầm.

3. **Bộ Chuyển Đổi Workspace Nhanh (Fast Project Switcher)**:
   * Menu xổ xuống tại Header cho phép chuyển đổi tức thì giữa các dự án mà không cần khởi động lại ứng dụng.
   * Các Agent đang chạy ngầm ở dự án cũ vẫn tiếp tục thực thi không bị ngắt quãng.

---

## 9. KHU VỰC QUẢN LÝ FILE DỰ ÁN (PROJECT FILE MANAGER & ASSET EXPLORER)

Nhằm giúp người dùng nắm bắt cấu trúc toàn diện và quản lý tài nguyên của dự án mà không cần mở File Explorer hệ điều hành:

### 9.1. Tính Năng Quản Trị File Cốt Lõi:
* **Cây Thư Mục Trực Quan (Interactive Folder Tree)**: Xem phân cấp toàn bộ thư mục mã nguồn (`src/`, `lib/`, `tests/`), tài liệu (`docs/`), và cấu hình (`.agents/`).
* **Hành Động File Toàn Năng (CRUD Operations)**:
  * ➕ Tạo file / thư mục mới ngay trên giao diện.
  * ✏️ Đổi tên (Rename) an toàn kèm cảnh báo nếu file đang được tham chiếu bởi các module khác.
  * 🗑️ Xóa file / thư mục (chuyển vào Thùng rác dự án `.agents/trash/` trước khi xóa vĩnh viễn để chống mất dữ liệu).
  * 📤 Upload / Kéo thả tệp tin từ máy tính vào trực tiếp dự án (hỗ trợ file ảnh asset, file excel dữ liệu, file schema `.sql`).
  * 📥 Tải xuống / Export file hoặc nén toàn bộ project thành file `.zip`.
* **Phân Loại Tệp Thông Minh (Smart File Badging)**:
  * Icon nhận diện tự động theo ngôn ngữ: TypeScript/Dart, Markdown, JSON, YAML, SQL, Excel (`.xlsx`), SVG/PNG.
  * Đánh dấu màu các file vừa được Agent chỉnh sửa gần nhất (Modified by Swarm).

---

## 10. TRANG TRÌNH SOẠN THẢO & XEM/SỬA/XÓA CODE (INTEGRATED CODE EDITOR & DIFF VIEWER)

Không cần bắt buộc phải mở IDE ngoài như VSCode/Cursor khi cần xem nhanh hoặc sửa một vài dòng code:

### 10.1. Trình Soạn Thảo Code Tích Hợp (Monaco / Native Code Editor):
* **Hỗ trợ Đa ngôn ngữ Đầy đủ**: Syntax Highlighting, thụt đầu dòng tự động, hiển thị số dòng (Line Numbers), Mini-map cuộn trang cho TypeScript, JavaScript, Python, Dart/Flutter, Rust, Go, HTML/CSS, SQL, JSON, YAML.
* **Thanh Tab Đa Nhiệm**: Cho phép mở cùng lúc nhiều file code theo dạng thẻ (Tabs).
* **Trực tiếp Chỉnh Sửa & Lưu Code**: Người dùng có thể tự tay gõ sửa code, bấm `Ctrl+S` / `Cmd+S` để lưu file tức thì.
* **Xóa Dòng & Xóa File Nhanh**: Tích hợp nút `🗑️ Xóa File` trên thanh công cụ code và tính năng xóa hàng loạt.

### 10.2. Chế Độ So Sánh Thay Đổi (Split-View Diff Viewer):
* Khi các Developer Agent vừa code xong một tính năng, người dùng có thể bật chế độ **Side-by-Side Diff**:
  * Cột bên trái: Code cũ trước khi sửa (Đánh dấu đỏ những dòng bị xóa).
  * Cột bên phải: Code mới sau khi Agent sửa (Đánh dấu xanh những dòng được thêm vào).
* Hỗ trợ nút **"Revert Dòng này"** hoặc **"Chấp nhận Thay đổi"** trực tiếp trên từng block diff.

### 10.3. Tích Hợp Trợ Lý Code Trực Tiếp (Inline AI Code Assistant):
* Bôi đen bất kỳ đoạn code nào $\rightarrow$ Bấm chuột phải hoặc nhấn `Cmd+K`:
  * *"Giải thích đoạn code này"*
  * *"Nhờ Backend Dev tối ưu đoạn truy vấn này"*
  * *"Viết unit test cho hàm này"*
* Lệnh được chuyển tiếp trực tiếp vào luồng của Agent tương ứng mà không cần copy paste qua lại.

---

## 11. HỆ SINH THÁI THIẾT KẾ UI/UX KÉP: TLDRAW + ONLOOK (DUAL-ENGINE DESIGN STUDIO)

Để giải quyết triệt để bài toán: **Làm sao để AI tự thiết kế, tự lấy source đó để lập trình và cho phép người dùng can thiệp trực quan mà không bị lệch chuẩn (Design-to-Code Gap)**, agentP tích hợp bộ đôi công nghệ mã nguồn mở hàng đầu:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                            VÒNG ĐỜI THIẾT KẾ & HIỆN THỰC HÓA GIAO DIỆN                      │
├──────────────────────────────────────────────┬──────────────────────────────────────────────┤
│    GIAI ĐOẠN 0 ➔ 1: Ý TƯỞNG & PHÁC THẢO      │    GIAI ĐOẠN 2 ➔ 3: PRODUCTION & CODE THẬT   │
│            🎨 TLDRAW WHITEBOARD              │             👁️ ONLOOK LIVE STUDIO            │
│  (Bàn vẽ nháp vô hạn, Napkin Wireframe)      │  (Soạn thảo trực quan trên DOM & Code thật)  │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ • Không gian sáng tạo tự do cùng Elena & Bạn │ • Nhúng trực tiếp app đang chạy (Vite/NextJS)│
│ • Vẽ box, thả sticky notes, vẽ sơ đồ luồng   │ • Click chọn phần tử trên màn hình           │
│ • Make Real: Phân tích Vision ➔ User Stories │ • Kéo chỉnh padding, đổi màu pale blue       │
│ • Lưu trữ: `.agents/designs/concept.tldr`    │ • AST Sync: Ghi thẳng vào file `.tsx`/`.dart`│
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

### 11.1. Phân Hệ 1: Tldraw — Bàn Phác Thảo Ý Tưởng Vô Hạn (Ideation & Napkin Canvas):
* **Bản chất công nghệ**: Nhúng lõi canvas vector mã nguồn mở `@tldraw/tldraw` siêu nhẹ, không phụ thuộc internet.
* **Quy trình hoạt động giữa Bạn và Elena (UI/UX Designer)**:
  1. Khi khởi tạo đề tài tại Trang 1 Launchpad, bạn có thể chuyển sang Tab **Tldraw** để vẽ nhanh bố cục mong muốn (vẽ tay khung màn hình mobile, kéo các ô vuông đại diện cho Voucher, giỏ hàng, ghi chú yêu cầu).
  2. Elena (UI/UX) và BA phân tích bản vẽ thông qua cơ chế Multi-modal Vision & Tldraw JSON AST:
     * Tự động nhận diện cấu trúc layout (Header, Hero Banner, Product Card Grid, Sticky Checkout Button).
     * Xuất ra bản đặc tả chi tiết (UI Component Hierarchy) chuyển thẳng sang cho Tech Lead và Frontend Dev.
* **Lợi ích**: Cực kỳ tự do, không bị gò bó bởi quy tắc CSS phức tạp trong giai đoạn thai nghén ý tưởng.

### 11.2. Phân Hệ 2: Onlook — Xưởng Soạn Thảo Trực Tiếp Trên Mã Nguồn Thật (DOM-to-Code WYSIWYG):
* **Bản chất công nghệ**: Tích hợp lõi `onlook-dev/onlook` (Next-gen visual editor cho React/Tailwind/Flutter Web).
* **Cơ chế Đồng Bộ Cây Cú Pháp Trừu Tượng (AST Bi-directional Synchronization)**:
  * Khác với Figma chỉ là bản vẽ tĩnh, Onlook nhúng trực tiếp **bản build đang chạy thực tế** của ứng dụng thông qua Dev Server nội bộ (`localhost:3000`).
  * Khi bạn hoặc Elena nhấp chuột vào bất kỳ phần tử nào trên giao diện (ví dụ: Nút *"Áp Dụng Voucher"*):
    * Thanh công cụ Visual Inspector hiển thị đầy đủ thuộc tính: Màu sắc (Color Palette định sẵn theo chuẩn Pale Water Blue `#E0F2FE`, `#0284C7`), Căn chỉnh Spacing (Margin/Padding bằng thanh trượt trực quan), Flexbox/Grid alignment, Typography, Border-radius.
    * Khi bạn kéo thay đổi thông số, Onlook sử dụng bộ phân tích cú pháp (Babel/PostCSS AST) để **ghi đè chính xác dòng code tương ứng trong file nguồn (`src/features/cart/VoucherBanner.tsx`)**.
* **Độ trễ bằng 0**: Thay đổi có hiệu lực ngay lập tức, file được lưu vào Git working directory, triệt tiêu hoàn toàn công đoạn "nhìn ảnh Figma rồi gõ lại CSS".

### 11.3. Sự Phối Hợp Nhịp Nhàng Giữa 14 Roles và Bộ Đôi Tldraw + Onlook:
1. **Bạn & Elena**: Phác thảo nhanh luồng người dùng trên **Tldraw**.
2. **BA & System Architect**: Dựa vào bản vẽ Tldraw để chốt User Stories và cấu trúc Props/State.
3. **Frontend & Fullstack Dev**: Dựng khung code sơ bộ (`.tsx`/`.dart`) theo Design System.
4. **Elena & Bạn**: Mở **Onlook Studio**, nhìn thấy ứng dụng đang chạy thật, dùng chuột click-and-edit để tinh chỉnh giao diện hoàn hảo đến từng pixel.
5. **Git Specialist & Automation QA**: Commit các file code đã được Onlook cập nhật sạch sẽ và chạy bộ test kiểm thử tự động.

---

## 12. HỆ THỐNG KANBAN PHẢN ỨNG TỰ ĐỘNG HỢP NHẤT (TRI-MODAL AGENTIC KANBAN SYSTEM)

Nhằm đáp ứng yêu cầu kiểm soát tiến độ trực quan tối đa mà không làm phân tán trải nghiệm điều hành trực tiếp qua khung chat, agentP tích hợp **Hệ thống Kanban 3 Chế độ Hợp nhất (Tri-Modal Kanban)** cùng chia sẻ 1 nguồn dữ liệu thời gian thực (Single Source of Truth tại `.agents/db.sqlite`):

### 12.1. Ba Chế Độ Hiển Thị Hợp Nhất (3 Seamless View Modes):
1. **Mode A: Embedded Mini-Kanban (Widget Tinh Gọn Tại Cột Phải Bàn Làm Việc)**:
   * Nằm thường trực tại Cột Inspector bên phải Trang 2 (Bàn làm việc Bạn ⇄ Alex).
   * Gồm 4 cột rút gọn: `📋 Backlog` ➔ `🔄 Swarm Coding` ➔ `🛑 Checkpoint Gate` ➔ `✅ Done`.
   * Giúp Bạn vừa trao đổi với Alex vừa liếc thấy nhịp đập của 14 Roles mà không cần rời mắt khỏi khung chat.
2. **Mode B: Slide-Over Drawer / Split-Screen (Ngăn Kéo Trượt Mở Rộng `Cmd+B`)**:
   * Khi cần xem sâu hơn danh sách task hoặc kiểm tra log commit mà vẫn muốn giữ luồng chat, Bạn chỉ cần bấm `Cmd+B` hoặc click icon `[📋 Mở Rộng]`.
   * Một Drawer 400px trượt êm ái ra từ cạnh phải (hoặc chuyển sang chế độ chia đôi 50/50), hiển thị chi tiết assignees, live token meter `🪙`/`⚡` và diff code của từng thẻ.
3. **Mode C: Full-Screen Dedicated Board (Trang Bảng Kanban Toàn Màn Hình Chuẩn Enterprise)**:
   * Nhấp nút `[⛶ Toàn Màn Hình]` hoặc chọn tab `[📋 Bảng Kanban]` trên thanh điều hướng để mở rộng thành bàn điều phối toàn cảnh 6 cột chuẩn mực quốc tế (`Backlog`, `To Do`, `In Progress`, `Code Review`, `User Checkpoint Gate`, `Done`).
   * Hỗ trợ Swimlanes (phân làn theo Module tính năng hoặc theo 14 Roles), quản lý WIP limits và thống kê velocity của từng Sprint.

### 12.2. Cơ Chế Phản Ứng Tự Động Theo Vòng Đời Tác Tử (Agentic Reactive Lifecycle):
Không giống Kanban truyền thống (Jira/Trello) bắt con người phải kéo thả thủ công:
* 🎯 **Tự động sinh Task**: Khi Bạn yêu cầu một tính năng, Liam (BA) tự động rã task con và thả vào cột `Backlog` / `To Do`.
* ⚡ **Tự động vào `In Progress`**: Khi Chloe (Frontend) hoặc Victor (Backend) bắt đầu gõ code, thẻ tự động nhảy sang `In Progress` kèm avatar của Agent và nhãn đo token `⚡`.
* 🧪 **Tự động vào `Code Review & Testing`**: Khi code xong, Lucas kiểm duyệt AST và Oliver chạy Unit test, thẻ tự động chuyển sang cột `Testing`.
* 🛑 **Tự động vào `User Checkpoint Gate`**: Khi test pass 100%, thẻ tự động khóa tại cột Checkpoint Gate màu hổ phách `#FFFBEB` và phát thông báo cho Bạn.
* ✅ **Tự động sang `Done`**: Ngay khi Bạn bấm duyệt hoặc gõ *"Duyệt"* trong chat, Max (Git) tự động commit code và đẩy thẻ sang `Done`!

---

## 13. HẠ TẦNG ĐA NỀN TẢNG, REMOTE HOST & DEVOPS TIỀN KIỂM

### 13.1. Khung Ứng Dụng Native & Remote Host:
* Xây dựng bằng **Tauri v2 (Rust)** hoặc **Flutter Desktop/Mobile**: Siêu nhẹ (<30MB), khởi động tức thì, hỗ trợ biên dịch 100% native cho **macOS, Windows, Android và Web**.
* Tính năng **"Run as Host"**: Máy tính cá nhân biến thành một máy chủ điều khiển an toàn. Bạn có thể dùng điện thoại Android quét mã QR để theo dõi tiến độ, xem demo và bấm duyệt Checkpoint khi đang ở bên ngoài.

### 13.2. Năng Lực Toàn Diện Của DevOps Specialist:
* **Bộ Tiền Kiểm Hệ Thống (Pre-flight System Diagnostics)**:
  * 💾 *Dung lượng ổ đĩa*: Cảnh báo nếu ổ cứng trống dưới mức cần thiết (ví dụ: cần 16GB để cài đặt Android SDK).
  * 🧠 *RAM & Ảo hóa CPU*: Kiểm tra tính khả dụng của VT-x/AMD-V, KVM/Hyper-V để đảm bảo chạy mượt mà máy ảo.
  * 🔌 *Quét xung đột cổng mạng*: Kiểm tra port ADB 5037, port Web 3000/8080 trước khi khởi chạy.
  * 🛡️ *Tường lửa & Proxy*: Phát hiện môi trường mạng doanh nghiệp chặn tải Gradle/Docker/NPM.
* **Quản Trị Giả Lập Android (AVD Lifecycle)**: Khởi chạy máy ảo Pixel 8 Pro ở chế độ có giao diện (GUI) hoặc chế độ chạy ngầm nhẹ (Headless) phục vụ kiểm thử E2E tự động.

---

## 14. LỘ TRÌNH TƯƠNG LAI: TỰ CHUYỂN MODEL THÔNG MINH KHI HẾT TOKEN

> 📌 **Ghi chú tính năng chiến lược cho các phiên bản tiếp theo (Roadmap Phase 2):**

### Cơ Chế Tự Động Failover Khi Hết Hạn Mức Token (Intelligent Token Auto-Failover):
* **Bối cảnh thực tế**: Khi một Role đang thực thi tác vụ nặng mà Model được gán bị cạn kiệt Token (đụng trần Context Window, hết Quota gói tài khoản trong ngày, hoặc gặp lỗi Rate Limit HTTP 429).
* **Cơ chế Tự Chuyển Thông Minh (Smart Failover Engine)**:
  1. **Phát hiện tức thời (Instant Quota Breach Detection)**: Lõi Proxy nội bộ lập tức bắt mã lỗi 429 hoặc cảnh báo `context_length_exceeded`.
  2. **Chuỗi Dự Phòng Phân Cấp (Hierarchical Fallback Chain)**:
     * *Ví dụ cho Coder Role*: `Claude 3.7 Sonnet` $\xrightarrow{\text{hết quota}}$ `DeepSeek R1` $\xrightarrow{\text{hết quota}}$ `Claude 3.5 Sonnet` $\xrightarrow{\text{hết quota}}$ `Local Qwen 2.5 Coder (Ollama)`.
  3. **Tự động Nén & Chuyển Giao Ngữ Cảnh (Context Hand-off)**: Nén nhanh 20 lượt chat gần nhất thành một bản tóm tắt súc tích và nạp trực tiếp vào model dự phòng.
  4. **Tiếp nối Trơn tru Không Ngắt Quãng**: Tiến trình của Agent tiếp tục chạy mà không làm đứt mạch pipeline, đồng thời gửi một thông báo nhẹ (Toast Notification) cho Bạn biết: *"Role Frontend Dev đã tự động chuyển từ Claude 3.7 sang DeepSeek R1 do hết quota."*
