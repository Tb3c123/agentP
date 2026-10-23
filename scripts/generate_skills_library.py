"""
Skills Library Generator & SQLite Seeder for agentP
Generates 30 specialized skill packages in .agents/skills/ and registers them in .agents/db.sqlite.
All skills are modular and universally usable by ANY role on demand.
"""

import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(BASE_DIR, ".agents", "skills")
DB_PATH = os.path.join(BASE_DIR, ".agents", "db.sqlite")

os.makedirs(SKILLS_DIR, exist_ok=True)

SKILLS_DEFINITIONS = [
    # 1. Management & BA
    {
        "id": "agile-sprint-breakdown",
        "name": "Agile Sprint Story Breakdown",
        "category": "management",
        "description": "Rã nhỏ user story thành subtask kỹ thuật, gán story points và xác định tiêu chí nghiệm thu (DoD).",
        "tools": "task_matrix, jira_mcp",
        "instructions": "1. Phân tích bài toán tổng quát từ User.\n2. Rã thành 3-5 nhiệm vụ cụ thể cho từng role.\n3. Gán điểm độ phức tạp (1, 2, 3, 5, 8 story points).\n4. Thiết lập Checkpoint Gate nghiệm thu."
    },
    {
        "id": "smart-auto-naming",
        "name": "Smart Auto-Naming & Taxonomy",
        "category": "management",
        "description": "Thuật toán ngôn ngữ tự động phát hiện ngữ cảnh bài toán và sinh tên dự án chuẩn kebab-case.",
        "tools": "text_analyzer, regex_parser",
        "instructions": "1. Phân tích chuỗi mô tả tiếng Việt/tiếng Anh.\n2. Trích xuất Domain (Food, ECommerce, SaaS, AI).\n3. Trích xuất Core Function & Tech Stack.\n4. Xuất 3 biến thể tên chuẩn mực."
    },
    {
        "id": "cost-token-guard",
        "name": "Cost & Token Consumption Guard",
        "category": "management",
        "description": "Giám sát ngân sách token, cảnh báo ngưỡng vượt định mức và tối ưu prompt caching 1:1.",
        "tools": "token_meter, cache_optimizer",
        "instructions": "1. Đọc số token tiêu thụ từ bảng provider_sessions.\n2. Tính toán tỷ lệ tiết kiệm (Tokens Saved).\n3. Tối ưu prompt nén và cắt tỉa ngữ cảnh dư thừa."
    },
    {
        "id": "risk-checkpoint-gate",
        "name": "Risk Assessor & Checkpoint Gatekeeper",
        "category": "management",
        "description": "Đánh giá mức độ rủi ro của thay đổi mã nguồn và tự động kích hoạt Cổng nghiệm thu Checkpoint.",
        "tools": "diff_analyzer, test_runner",
        "instructions": "1. Kiểm tra số file sửa đổi và tỷ lệ xóa code.\n2. Nếu chạm vào schema database hoặc auth -> Khóa lại và yêu cầu User bấm duyệt.\n3. Sinh bản tóm tắt thay đổi dễ hiểu cho User."
    },

    # 2. Architecture & Database
    {
        "id": "sqlite-wal-optimization",
        "name": "SQLite WAL Engine Optimizer",
        "category": "architecture",
        "description": "Cấu hình Write-Ahead Logging (WAL), foreign keys cascade và giải quyết lock contention dưới 5ms.",
        "tools": "sql_runner, pragma_tuner",
        "instructions": "1. Bật PRAGMA journal_mode = WAL.\n2. Bật PRAGMA foreign_keys = ON.\n3. Đặt synchronous = NORMAL và cache_size = -64000 (64MB RAM).\n4. Chạy ANALYZE định kỳ để tối ưu hóa query plan."
    },
    {
        "id": "c4-architecture-modeling",
        "name": "C4 Architecture Modeler",
        "category": "architecture",
        "description": "Thiết kế và xuất sơ đồ kiến trúc 4 cấp độ: Context, Container, Component, Code dạng Mermaid.",
        "tools": "mermaid_gen, arch_validator",
        "instructions": "1. Vẽ sơ đồ Context mô tả tương tác giữa User và hệ thống.\n2. Vẽ Container cho Tauri Desktop, Core Daemon và SQLite.\n3. Mô tả chi tiết component và giao tiếp cổng Adapter."
    },
    {
        "id": "event-driven-pubsub",
        "name": "Event-Driven Pub-Sub Bus",
        "category": "architecture",
        "description": "Thiết lập bus sự kiện đồng bộ/bất đồng bộ giữa Alex và 13 agent roles ngầm.",
        "tools": "event_dispatcher, queue_manager",
        "instructions": "1. Đăng ký subscriber cho các sự kiện: TaskCreated, CodeDiffReady, CheckpointApproved.\n2. Đảm bảo xử lý lỗi độc lập không làm treo daemon.\n3. Ghi log sự kiện vào SQLite audit trail."
    },
    {
        "id": "api-contract-first",
        "name": "Contract-First API Designer",
        "category": "architecture",
        "description": "Soạn thảo đặc tả OpenAPI 3.1 và JSON Schema cho các endpoint REST trước khi code.",
        "tools": "openapi_validator, schema_linter",
        "instructions": "1. Định nghĩa Data Transfer Object (DTO) cho Request và Response.\n2. Khai báo status code chuẩn (200, 201, 400, 404, 500).\n3. Tự động sinh client types cho TypeScript và Dart."
    },

    # 3. UI/UX Design
    {
        "id": "tldraw-canvas-wireframing",
        "name": "Tldraw Infinite Canvas Wireframing",
        "category": "design",
        "description": "Vẽ phác thảo UI/UX vector, sticky notes, liên kết flow màn hình và xuất file .tldr.",
        "tools": "tldraw_ast, vector_exporter",
        "instructions": "1. Tạo khung màn hình di động 390x844 (iPhone) hoặc 412x915 (Android Pixel).\n2. Kéo thả các hình khối: Header, Card, Button, Input.\n3. Gắn nhãn màu sắc Alpine Teal & Tuscan Amber.\n4. Lưu bản vẽ vào .agents/designs/."
    },
    {
        "id": "onlook-dom-to-code",
        "name": "Onlook DOM-to-Code Synchronizer",
        "category": "design",
        "description": "Click-to-inspect phần tử UI trên giao diện đang chạy và đồng bộ trực tiếp Tailwind CSS vào mã nguồn.",
        "tools": "ast_parser, class_updater",
        "instructions": "1. Bắt sự kiện click trên phần tử UI iframe sandbox.\n2. Mở thanh inspector hiển thị classes Tailwind hiện tại.\n3. Cho phép đổi màu sắc, padding, border radius.\n4. Ghi đè vào file .tsx/.dart với độ trễ <50ms."
    },
    {
        "id": "design-tokens-crafting",
        "name": "Design Tokens & Clean Light Palette",
        "category": "design",
        "description": "Chuẩn hóa hệ màu Clean Light Mode: Porcelain White, Alpine Teal, Tuscan Amber, Fedora Brown.",
        "tools": "color_tuner, token_exporter",
        "instructions": "1. Enforce 100% Clean Light Mode (Slate-50 #F8FAFC canvas, Pure White #FFFFFF panels).\n2. Cấm hoàn toàn màu neon và dark mode u tối.\n3. Xuất CSS Variables và Tailwind configuration."
    },
    {
        "id": "a11y-wcag-compliance",
        "name": "A11y WCAG 2.2 Auditor",
        "category": "design",
        "description": "Kiểm tra độ tương phản màu sắc (tối thiểu 4.5:1), ARIA labels, focus ring và phím tắt trợ năng.",
        "tools": "contrast_checker, aria_linter",
        "instructions": "1. Quét toàn bộ button và input xem đã có aria-label chưa.\n2. Kiểm tra độ tương phản văn bản so với màu nền.\n3. Đảm bảo hỗ trợ điều hướng hoàn toàn bằng phím Tab và Enter."
    },

    # 4. Frontend & Mobile Development
    {
        "id": "flutter-bloc-state-machine",
        "name": "Flutter BLoC/Cubit State Machine",
        "category": "frontend",
        "description": "Xây dựng kiến trúc BLoC cho ứng dụng Flutter di động, phân tách Event, State và UI.",
        "tools": "flutter_gen, dart_analyzer",
        "instructions": "1. Định nghĩa sealed class cho CartState: Initial, Loading, Loaded, Error.\n2. Xử lý các sự kiện: AddToCart, ApplyVoucher, Checkout.\n3. Đảm bảo render lại UI với blocBuilder mà không gây giật lag (60 FPS)."
    },
    {
        "id": "react-tailwind-components",
        "name": "React 19 Functional UI Components",
        "category": "frontend",
        "description": "Lập trình component React 19 tối ưu, hỗ trợ Server Actions, Tailwind CSS và TypeScript nghiêm ngặt.",
        "tools": "tsx_builder, prettier_linter",
        "instructions": "1. Viết component dạng functional thuần khiết với generic TypeScript props.\n2. Áp dụng utility classes của Tailwind CSS.\n3. Tránh re-render không cần thiết bằng useMemo và useCallback."
    },
    {
        "id": "responsive-layout-builder",
        "name": "Responsive Multi-Form Factor Layout",
        "category": "frontend",
        "description": "Thiết kế layout co giãn thích ứng mượt mà trên Desktop (1440px), Tablet (1024px) và Mobile (390px).",
        "tools": "media_query_helper, grid_tuner",
        "instructions": "1. Áp dụng CSS Grid và Flexbox linh hoạt.\n2. Xếp dọc thanh bên trên màn hình nhỏ và mở rộng khi trên desktop.\n3. Ngăn ngừa tràn khung hình (RenderFlex overflow)."
    },
    {
        "id": "hot-reload-diagnostics",
        "name": "Live Hot Reload & Layout Fixer",
        "category": "frontend",
        "description": "Kết nối Flutter DevTools và Chrome Inspector để phát hiện và sửa tức thời lỗi layout overflow.",
        "tools": "hot_reload_bridge, stack_tracer",
        "instructions": "1. Lắng nghe thông báo lỗi 'RenderFlex overflowed by X pixels'.\n2. Thay thế Column không giới hạn bằng SingleChildScrollView hoặc Expanded.\n3. Gửi tín hiệu Hot Reload (phím r) để kiểm tra kết quả ngay lập tức."
    },

    # 5. Backend & Core Systems
    {
        "id": "fastapi-async-daemon",
        "name": "Asynchronous High-Speed Local Daemon",
        "category": "backend",
        "description": "Xây dựng REST/WebSocket daemon phản hồi dưới 10ms, tiết kiệm RAM (<45MB) và không phụ thuộc bên ngoài.",
        "tools": "socket_builder, async_worker",
        "instructions": "1. Sử dụng non-blocking I/O hoặc luồng sự kiện nhẹ.\n2. Định tuyến các endpoint /health, /sessions, /kanban, /chat.\n3. Đóng gói binary tự khởi chạy cùng Tauri v2."
    },
    {
        "id": "jwt-rbac-authenticator",
        "name": "JWT & Role-Based Access Guard",
        "category": "backend",
        "description": "Bảo mật các endpoint nội bộ với xác thực JSON Web Token và phân quyền vai trò.",
        "tools": "jwt_coder, rbac_validator",
        "instructions": "1. Ký token với thuật toán HMAC-SHA256.\n2. Kiểm tra header Authorization: Bearer <token>.\n3. Xác minh quyền hạn trước khi cho phép gọi API nhạy cảm."
    },
    {
        "id": "session-isolation-protocol",
        "name": "1:1 AI Model Session Isolation",
        "category": "backend",
        "description": "Cô lập hoàn toàn context lịch sử và luồng suy nghĩ giữa 14 AI specialist models không bị nhiễm chéo.",
        "tools": "session_jail, memory_scrubber",
        "instructions": "1. Cấp phát session_id và context window riêng biệt cho từng role_id.\n2. Tái sử dụng phiên đăng nhập Claude CLI, Cursor hoặc gh auth.\n3. Tách biệt token quota và lưu riêng vào CSDL SQLite."
    },
    {
        "id": "ast-sync-bidirectional",
        "name": "Bi-directional AST Sync Engine",
        "category": "backend",
        "description": "Phân tích cú pháp Abstract Syntax Tree và sửa đổi file code thật với độ trễ <50ms.",
        "tools": "ast_engine, file_patcher",
        "instructions": "1. Đọc nội dung file TypeScript/Dart và xác định vị trí thẻ JSX/Widget.\n2. Cập nhật chuỗi className hoặc styling properties.\n3. Lưu bản snapshot dự phòng vào CSDL trước khi ghi file."
    },

    # 6. QA, Testing & Security
    {
        "id": "e2e-playwright-automation",
        "name": "Playwright E2E UI Automation",
        "category": "qa",
        "description": "Viết và chạy kịch bản kiểm thử giao diện đầu cuối: click nút, gõ phím, duyệt Checkpoint.",
        "tools": "playwright_cli, visual_differ",
        "instructions": "1. Khởi chạy trình duyệt headless.\n2. Thực hiện thao tác người dùng: Nhập mô tả -> Bấm khởi tạo -> Chat với Alex.\n3. Chụp ảnh màn hình đối chiếu và xác minh kết quả."
    },
    {
        "id": "security-danger-zone-guard",
        "name": "Antigravity Danger Zone Safety Lock",
        "category": "security",
        "description": "Cơ chế bảo vệ 2 lớp chống mất dữ liệu: bắt buộc gõ chính xác 100% tên dự án để mở khóa nút xóa.",
        "tools": "security_guard, string_verifier",
        "instructions": "1. Khóa cứng nút xóa (disabled, con trỏ not-allowed).\n2. Bắt sự kiện bàn phím so khớp chính xác từng ký tự hoa/thường.\n3. Chỉ mở khóa đỏ khi trùng khớp 100%, yêu cầu popup xác nhận lần 2."
    },
    {
        "id": "chaos-resilience-testing",
        "name": "Chaos & Process Crash Recovery",
        "category": "qa",
        "description": "Kiểm thử tắt ứng dụng đột ngột (kill -9) để chứng minh SQLite WAL không bị hỏng dữ liệu.",
        "tools": "process_killer, integrity_checker",
        "instructions": "1. Đang ghi dữ liệu vào SQLite -> Ngắt tiến trình đột ngột.\n2. Mở lại ứng dụng và chạy PRAGMA integrity_check.\n3. Chứng minh toàn bộ transaction đã commit được bảo toàn 100%."
    },
    {
        "id": "unit-test-coverage-enforcer",
        "name": "Unit Test Coverage Enforcer",
        "category": "qa",
        "description": "Đo lường độ bao phủ mã nguồn (Code Coverage) và chặn commit nếu dưới 80%.",
        "tools": "coverage_lcov, test_runner",
        "instructions": "1. Chạy toàn bộ test suites với cờ --coverage.\n2. Xuất báo cáo LCOV và phân tích độ phủ từng file.\n3. Xác nhận đạt 100% Pass trước khi cho phép đóng Sprint."
    },

    # 7. DevOps & Infrastructure
    {
        "id": "android-avd-manager",
        "name": "Android Virtual Device (AVD) Controller",
        "category": "devops",
        "description": "Quản lý vòng đời máy ảo Android Pixel 8 Pro: khởi chạy GUI/Headless, cài APK, chụp ảnh màn hình.",
        "tools": "emulator_cli, adb_bridge",
        "instructions": "1. Kiểm tra danh sách AVD có sẵn qua lệnh `emulator -list-avds`.\n2. Khởi chạy máy ảo tại port 5554.\n3. Chụp ảnh màn hình qua adb và lưu vào docs/assets/."
    },
    {
        "id": "preflight-system-doctor",
        "name": "Pre-flight Diagnostics System Doctor",
        "category": "devops",
        "description": "Tự động kiểm tra 7 tiêu chí hệ thống: SQLite, Node.js, Git, Daemon, Flutter, Android, Swarm.",
        "tools": "system_scanner, doctor_cli",
        "instructions": "1. Quét các công cụ CLI trên máy tính của người dùng.\n2. Kiểm tra port 9090 và port 8080 xem có bị xung đột không.\n3. Xuất báo cáo dạng bảng màu chuẩn mực [✓ ĐẠT CHUẨN]."
    },
    {
        "id": "docker-multistage-bundle",
        "name": "Docker Multi-Stage Lightweight Bundle",
        "category": "devops",
        "description": "Viết Dockerfile đa giai đoạn tạo image kích thước siêu nhẹ (<80MB) để triển khai nhanh.",
        "tools": "docker_cli, image_optimizer",
        "instructions": "1. Giai đoạn 1 (Builder): Biên dịch source code và cài dependencies.\n2. Giai đoạn 2 (Runner): Chỉ chép file build và binary sang base Alpine Linux.\n3. Cấu hình người dùng non-root để đảm bảo an toàn."
    },
    {
        "id": "git-branching-conventional",
        "name": "Git Branching & Conventional Commits",
        "category": "devops",
        "description": "Quản lý chiến lược nhánh feature/*, hotfix/* và chuẩn hóa thông điệp commit feat/fix/refactor.",
        "tools": "git_cli, commit_linter",
        "instructions": "1. Tạo nhánh tính năng cô lập từ main: feature/<tên-tính-năng>.\n2. Soạn thông điệp commit theo chuẩn: type(scope): description.\n3. Kiểm tra git status sạch sẽ trước khi tạo Pull Request."
    },

    # 8. Docs & Enterprise Reporting
    {
        "id": "excel-corporate-reporter",
        "name": "Enterprise Excel Data & KPI Reporter",
        "category": "docs",
        "description": "Tự động tạo bảng tính Excel .xlsx chuyên nghiệp có màu thương hiệu, công thức và phân bổ token.",
        "tools": "excel_writer, openpyxl_helper",
        "instructions": "1. Tổng hợp số liệu: danh sách file, dòng code, token tiêu thụ của 14 vai trò.\n2. Tô màu tiêu đề Alpine Teal (#0D9488) và viền bảng sắc nét.\n3. Thêm công thức tính tổng SUM, AVERAGE và tỷ lệ tiết kiệm chi phí."
    },
    {
        "id": "changelog-release-notes",
        "name": "Automated Changelog & Release Notes Generator",
        "category": "docs",
        "description": "Tự động trích xuất git commit history và phân loại theo Sprint để tạo CHANGELOG.md chuẩn Keep a Changelog.",
        "tools": "git_log_parser, markdown_writer",
        "instructions": "1. Đọc lịch sử commit giữa các tag phát hành.\n2. Nhóm thành các mục: Added, Changed, Fixed, Security.\n3. Xuất tài liệu Markdown đẹp mắt phục vụ bàn giao dự án."
    }
]

def main():
    print(f"Bắt đầu khởi tạo thư viện {len(SKILLS_DEFINITIONS)} bộ Skills chuyên biệt cho agentP...")

    # 1. Tạo thư mục và file SKILL.md
    for s in SKILLS_DEFINITIONS:
        s_dir = os.path.join(SKILLS_DIR, s["id"])
        os.makedirs(s_dir, exist_ok=True)
        skill_md_path = os.path.join(s_dir, "SKILL.md")

        content = f"""---
name: "{s['name']}"
id: "{s['id']}"
category: "{s['category']}"
description: "{s['description']}"
tools_required: "{s['tools']}"
universal: true
---

# 🛠️ Skill: {s['name']}

> **Phân loại**: `{s['category'].upper()}` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
{s['description']}

## 2. Công Cụ & MCP Được Kích Hoạt
- `{s['tools']}`

## 3. Quy Trình Thực Thi Chuẩn
{s['instructions']}

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
"""
        with open(skill_md_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"✓ Đã sinh thành công {len(SKILLS_DEFINITIONS)} file SKILL.md trong .agents/skills/")

    # 2. Cập nhật CSDL SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_skills (
        skill_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        tools_required TEXT,
        is_universal INTEGER DEFAULT 1,
        file_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS role_skill_assignments (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_id TEXT NOT NULL,
        skill_id TEXT NOT NULL,
        proficiency_level TEXT DEFAULT 'expert',
        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (role_id) REFERENCES agent_roles(role_id) ON DELETE CASCADE,
        FOREIGN KEY (skill_id) REFERENCES agent_skills(skill_id) ON DELETE CASCADE,
        UNIQUE(role_id, skill_id)
    );
    """)

    for s in SKILLS_DEFINITIONS:
        rel_path = f".agents/skills/{s['id']}/SKILL.md"
        cursor.execute("""
        INSERT OR REPLACE INTO agent_skills 
        (skill_id, name, category, description, tools_required, is_universal, file_path)
        VALUES (?, ?, ?, ?, ?, 1, ?)
        """, (s["id"], s["name"], s["category"], s["description"], s["tools"], rel_path))

    # Gán kỹ năng mặc định cho các role (và bất kỳ role nào cũng có thể mượn)
    roles = cursor.execute("SELECT role_id FROM agent_roles").fetchall()
    for (r_id,) in roles:
        # Mỗi role được cấp tối thiểu 5 kỹ năng chính và có thể truy cập toàn bộ 30 kỹ năng
        for s in SKILLS_DEFINITIONS[:5]:
            cursor.execute("""
            INSERT OR IGNORE INTO role_skill_assignments (role_id, skill_id, proficiency_level)
            VALUES (?, ?, 'expert')
            """, (r_id, s["id"]))

    conn.commit()
    count_skills = cursor.execute("SELECT COUNT(*) FROM agent_skills").fetchone()[0]
    conn.close()

    print(f"✓ Đã nạp thành công {count_skills} bộ Skills vào bảng `agent_skills` trong SQLite!")

if __name__ == "__main__":
    main()
