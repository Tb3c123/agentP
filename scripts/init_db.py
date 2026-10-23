import sqlite3
import os
import glob
import re

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '.agents', 'db.sqlite')
ROLES_DIR = os.path.join(os.path.dirname(__file__), '..', '.agents', 'roles')

def init_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. PRAGMAS
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA synchronous = NORMAL;")
    cursor.execute("PRAGMA busy_timeout = 5000;")

    # 2. TABLES DDL
    ddl_statements = """
    CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS projects (
        project_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        slug TEXT NOT NULL UNIQUE,
        workspace_path TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('initializing', 'active', 'paused', 'archived')),
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS project_env_vars (
        var_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
        key_name TEXT NOT NULL,
        encrypted_value TEXT NOT NULL,
        is_secret BOOLEAN NOT NULL DEFAULT 1,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(project_id, key_name)
    );

    CREATE TABLE IF NOT EXISTS agent_roles (
        role_id TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        code_name TEXT NOT NULL UNIQUE,
        category TEXT NOT NULL CHECK(category IN ('management', 'conception', 'architecture', 'engineering', 'qa', 'devops')),
        default_model TEXT NOT NULL,
        persona_summary TEXT NOT NULL,
        system_prompt_template TEXT NOT NULL,
        color_accent TEXT NOT NULL DEFAULT '#0D9488',
        is_active BOOLEAN NOT NULL DEFAULT 1,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS provider_sessions (
        session_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
        role_id TEXT NOT NULL REFERENCES agent_roles(role_id) ON DELETE RESTRICT,
        provider_name TEXT NOT NULL CHECK(provider_name IN ('anthropic', 'openai', 'gemini', 'deepseek', 'local_ollama')),
        assigned_model TEXT NOT NULL,
        router_port INTEGER NOT NULL DEFAULT 9090,
        total_tokens_in INTEGER NOT NULL DEFAULT 0,
        total_tokens_out INTEGER NOT NULL DEFAULT 0,
        total_cost_usd REAL NOT NULL DEFAULT 0.0,
        latency_ms INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'connected' CHECK(status IN ('connected', 'idle', 'error', 'disconnected')),
        last_ping_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(project_id, role_id)
    );

    CREATE TABLE IF NOT EXISTS chat_sessions (
        chat_session_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
        title TEXT NOT NULL DEFAULT 'Hội thoại chính với Lead / PM',
        status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'closed')),
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS chat_messages (
        message_id TEXT PRIMARY KEY,
        chat_session_id TEXT NOT NULL REFERENCES chat_sessions(chat_session_id) ON DELETE CASCADE,
        sender_type TEXT NOT NULL CHECK(sender_type IN ('user', 'pm_agent', 'sub_agent', 'system_event')),
        sender_role_id TEXT REFERENCES agent_roles(role_id) ON DELETE SET NULL,
        sender_name TEXT NOT NULL,
        content TEXT NOT NULL,
        thinking_log TEXT,
        thought_duration_ms INTEGER DEFAULT 0,
        tokens_consumed INTEGER DEFAULT 0,
        is_checkpoint_trigger BOOLEAN NOT NULL DEFAULT 0,
        checkpoint_gate_id TEXT,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS sprints (
        sprint_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
        sprint_number INTEGER NOT NULL,
        name TEXT NOT NULL,
        goal TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'planned' CHECK(status IN ('planned', 'active', 'completed', 'cancelled')),
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(project_id, sprint_number)
    );

    CREATE TABLE IF NOT EXISTS kanban_tasks (
        task_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
        sprint_id TEXT REFERENCES sprints(sprint_id) ON DELETE SET NULL,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL CHECK(category IN ('spec', 'design', 'architecture', 'frontend', 'backend', 'qa', 'devops')),
        column_status TEXT NOT NULL DEFAULT 'backlog' CHECK(
            column_status IN ('backlog', 'conception', 'architecture', 'development', 'quality_gate', 'done')
        ),
        priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
        assigned_role_id TEXT REFERENCES agent_roles(role_id) ON DELETE RESTRICT,
        tokens_spent INTEGER NOT NULL DEFAULT 0,
        estimated_points INTEGER NOT NULL DEFAULT 1,
        git_branch_name TEXT,
        pr_commit_hash TEXT,
        order_index INTEGER NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS task_subtasks (
        subtask_id TEXT PRIMARY KEY,
        task_id TEXT NOT NULL REFERENCES kanban_tasks(task_id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        is_completed BOOLEAN NOT NULL DEFAULT 0,
        completed_at DATETIME,
        order_index INTEGER NOT NULL DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS checkpoint_gates (
        checkpoint_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
        task_id TEXT NOT NULL REFERENCES kanban_tasks(task_id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        diff_stats_files INTEGER NOT NULL DEFAULT 0,
        diff_stats_insertions INTEGER NOT NULL DEFAULT 0,
        diff_stats_deletions INTEGER NOT NULL DEFAULT 0,
        automated_test_passed BOOLEAN NOT NULL DEFAULT 0,
        automated_test_details TEXT,
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected', 'rework_requested')),
        user_feedback TEXT,
        resolved_at DATETIME,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS audit_git_commits (
        commit_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
        task_id TEXT REFERENCES kanban_tasks(task_id) ON DELETE SET NULL,
        checkpoint_id TEXT REFERENCES checkpoint_gates(checkpoint_id) ON DELETE SET NULL,
        commit_hash TEXT NOT NULL UNIQUE,
        branch_name TEXT NOT NULL DEFAULT 'main',
        author_agent_role_id TEXT REFERENCES agent_roles(role_id) ON DELETE SET NULL,
        commit_message TEXT NOT NULL,
        files_changed_count INTEGER NOT NULL DEFAULT 0,
        insertions_count INTEGER NOT NULL DEFAULT 0,
        deletions_count INTEGER NOT NULL DEFAULT 0,
        committed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS ui_design_snapshots (
        snapshot_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
        task_id TEXT REFERENCES kanban_tasks(task_id) ON DELETE SET NULL,
        studio_mode TEXT NOT NULL CHECK(studio_mode IN ('tldraw_whiteboard', 'onlook_dom_editor')),
        component_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        design_data_json TEXT NOT NULL,
        tailwind_classes_json TEXT,
        synced_to_code BOOLEAN NOT NULL DEFAULT 0,
        git_commit_hash TEXT,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.executescript(ddl_statements)

    # 3. TRIGGERS
    triggers_ddl = """
    CREATE TRIGGER IF NOT EXISTS trg_projects_updated_at
    AFTER UPDATE ON projects
    FOR EACH ROW
    BEGIN
        UPDATE projects SET updated_at = CURRENT_TIMESTAMP WHERE project_id = OLD.project_id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_kanban_tasks_updated_at
    AFTER UPDATE ON kanban_tasks
    FOR EACH ROW
    BEGIN
        UPDATE kanban_tasks SET updated_at = CURRENT_TIMESTAMP WHERE task_id = OLD.task_id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_sprints_updated_at
    AFTER UPDATE ON sprints
    FOR EACH ROW
    BEGIN
        UPDATE sprints SET updated_at = CURRENT_TIMESTAMP WHERE sprint_id = OLD.sprint_id;
    END;

    CREATE TRIGGER IF NOT EXISTS trg_checkpoint_approved_to_done
    AFTER UPDATE OF status ON checkpoint_gates
    FOR EACH ROW
    WHEN NEW.status = 'approved' AND OLD.status != 'approved'
    BEGIN
        UPDATE kanban_tasks 
        SET column_status = 'done', updated_at = CURRENT_TIMESTAMP 
        WHERE task_id = NEW.task_id;
    END;
    """
    cursor.executescript(triggers_ddl)

    # 4. INITIAL MIGRATION RECORD
    cursor.execute("""
    INSERT OR IGNORE INTO schema_migrations (version, description)
    VALUES (1, 'Initial Schema v1.0.0 (Tri-Modal Kanban, Checkpoints, 14 Roles, Chat & Tldraw)')
    """)

    # 5. INITIAL PROJECT SEED
    project_id = "proj_food_delivery_01"
    cursor.execute("""
    INSERT OR IGNORE INTO projects (project_id, name, slug, workspace_path, description, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        project_id,
        "FoodDelivery-Loyalty-App",
        "fooddelivery-loyalty-app",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        "Ứng dụng đặt đồ ăn trên Android và Web bằng Flutter & NestJS có giỏ hàng, tích điểm voucher.",
        "active"
    ))

    # 6. SEED 14 AGENT ROLES (from .agents/roles/*.yaml or structured roster)
    roles = [
        ("lead_pm", "Alex (Trưởng Dự Án / Lead PM)", "Alex", "management", "claude-3-5-sonnet",
         "Chịu trách nhiệm tổng thể, tương tác trực tiếp với Bạn, phân chia task và kích hoạt Checkpoint.",
         "Bạn là Alex, Trưởng dự án...", "#0D9488"),
        ("ba_lead", "Marcus (Lead Business Analyst)", "Marcus", "conception", "gpt-4o",
         "Khảo sát nghiệp vụ, viết User Stories và quản trị backlog Sprint.",
         "Bạn là Marcus, BA Lead...", "#10B981"),
        ("ui_ux_designer", "Elena (Chuyên Gia UI/UX)", "Elena", "conception", "claude-3-5-sonnet",
         "Thiết kế giao diện Light Mode chuẩn Alpine Teal & Amber, vẽ Tldraw & style Onlook.",
         "Bạn là Elena, UI/UX Designer...", "#06B6D4"),
        ("system_architect", "Maya (Kiến Trúc Sư Hệ Thống)", "Maya", "architecture", "claude-3-5-sonnet",
         "Thiết kế kiến trúc tổng thể, mô hình SQLite DDL, API contracts.",
         "Bạn là Maya, System Architect...", "#8B5CF6"),
        ("frontend_dev", "David (Kỹ Sư Frontend Flutter)", "David", "engineering", "gemini-2-5-flash",
         "Lập trình Flutter BloC, giao diện reactive và Onlook DOM sync.",
         "Bạn là David, Frontend Dev...", "#3B82F6"),
        ("backend_dev", "Carlos (Kỹ Sư Backend NestJS)", "Carlos", "engineering", "claude-3-5-sonnet",
         "Xây dựng REST API, DTO, TypeORM, 9router daemon integration.",
         "Bạn là Carlos, Backend Dev...", "#6366F1"),
        ("qa_lead", "Viktor (Trưởng Nhóm Kiểm Thử QA)", "Viktor", "qa", "deepseek-r1",
         "Soạn test Jest & Flutter, logic suy luận sâu, thẩm định Checkpoint.",
         "Bạn là Viktor, QA Lead...", "#D97706"),
        ("devops_lead", "Liam (Kỹ Sư DevOps & CI/CD)", "Liam", "devops", "gemini-2-5-flash",
         "Chạy Pre-flight diagnostics, điều khiển máy ảo AVD Pixel 8, WebSocket port 8080.",
         "Bạn là Liam, DevOps Lead...", "#EC4899"),
        ("tech_lead", "Lucas (Senior Code Reviewer)", "Lucas", "engineering", "claude-3-5-sonnet",
         "Rà soát AST parser, tối ưu thuật toán, đảm bảo Clean Architecture.",
         "Bạn là Lucas, Senior Dev...", "#0F766E"),
        ("security_auditor", "Nora (Chuyên Gia Bảo Mật)", "Nora", "qa", "deepseek-r1",
         "Rà soát an toàn SQL, chống rò rỉ secret key, kiểm định xác nhận xóa dự án.",
         "Bạn là Nora, Security Auditor...", "#EF4444"),
        ("perf_tester", "Oliver (Kỹ Sư Hiệu Năng)", "Oliver", "qa", "deepseek-r1",
         "Đo tải hệ thống, benchmark FPS, RAM và tối ưu thời gian khởi động.",
         "Bạn là Oliver, Perf Tester...", "#F59E0B"),
        ("report_specialist", "Sophia (Chuyên Gia Báo Cáo)", "Sophia", "management", "claude-3-5-sonnet",
         "Soạn thảo tài liệu kỹ thuật, xuất file Excel .xlsx đa phong cách.",
         "Bạn là Sophia, Technical Writer...", "#14B8A6"),
        ("fullstack_dev", "Sam (Kỹ Sư Fullstack)", "Sam", "engineering", "gemini-2-5-flash",
         "Phụ trách Monaco Editor, Side-by-Side Diff, và tính năng mở rộng.",
         "Bạn là Sam, Fullstack Dev...", "#64748B"),
        ("git_specialist", "Max (Bậc Thầy Git)", "Max", "devops", "gemini-2-5-flash",
         "Quản lý chiến lược phân nhánh, conflict resolution, Conventional Commits an toàn.",
         "Bạn là Max, Git Specialist...", "#10B981")
    ]

    for role in roles:
        cursor.execute("""
        INSERT OR REPLACE INTO agent_roles (
            role_id, display_name, code_name, category, default_model,
            persona_summary, system_prompt_template, color_accent
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, role)

    # 7. SEED 1:1 PROVIDER SESSIONS
    provider_map = {
        "claude-3-5-sonnet": "anthropic",
        "gpt-4o": "openai",
        "gemini-2-5-flash": "gemini",
        "deepseek-r1": "deepseek"
    }

    for role_id, display_name, code_name, category, model, _, _, _ in roles:
        prov = provider_map.get(model, "anthropic")
        sess_id = f"sess_{code_name.lower()}_01"
        cursor.execute("""
        INSERT OR REPLACE INTO provider_sessions (
            session_id, project_id, role_id, provider_name, assigned_model, router_port, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sess_id, project_id, role_id, prov, model, 9090, "connected"))

    # 8. SEED SPRINT 1
    sprint_id = "sprint_01"
    cursor.execute("""
    INSERT OR REPLACE INTO sprints (
        sprint_id, project_id, sprint_number, name, goal, status, start_date, end_date
    ) VALUES (?, ?, ?, ?, ?, ?, DATE('now'), DATE('now', '+14 days'))
    """, (
        sprint_id, project_id, 1,
        "Sprint 1: Nền Tảng Hạ Tầng & Lõi 9router Local Proxy Daemon",
        "Xây dựng khung ứng dụng, CSDL SQLite cục bộ, Proxy Daemon 1:1 sessions và bộ test tự động",
        "active"
    ))

    # 9. SEED KANBAN TASKS FOR SPRINT 1
    tasks = [
        ("TASK-101", project_id, sprint_id, "Thiết kế & Khởi tạo CSDL SQLite .agents/db.sqlite",
         "Tạo 12 bảng, indexes, foreign keys và triggers tự động hóa", "architecture", "done", "urgent", "system_architect", 1400),
        ("TASK-102", project_id, sprint_id, "Xây dựng 9router Local Daemon (Port 9090)",
         "Hỗ trợ 1:1 session isolation, streaming raw thinking log và fallback failover", "backend", "development", "high", "backend_dev", 2100),
        ("TASK-103", project_id, sprint_id, "Bộ Test Tự Động Hóa (Unit & Integration Tests)",
         "Viết test xác thực WAL mode, foreign keys cascade, và thinking log parser", "qa", "development", "high", "qa_lead", 1850),
        ("TASK-104", project_id, sprint_id, "Thiết lập cấu hình Tauri v2 & Pre-flight Diagnostics",
         "Cấu hình package.json, TypeScript và script tiền kiểm 7 tiêu chí hệ thống", "devops", "conception", "medium", "devops_lead", 950)
    ]

    for task in tasks:
        cursor.execute("""
        INSERT OR REPLACE INTO kanban_tasks (
            task_id, project_id, sprint_id, title, description, category,
            column_status, priority, assigned_role_id, tokens_spent
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, task)

    # 10. SEED INITIAL CHAT SESSION
    chat_sess_id = "chat_main_session_01"
    cursor.execute("""
    INSERT OR REPLACE INTO chat_sessions (chat_session_id, project_id, title, status)
    VALUES (?, ?, ?, ?)
    """, (chat_sess_id, project_id, "Bàn làm việc điều hành với Alex (Lead / PM)", "active"))

    cursor.execute("""
    INSERT OR REPLACE INTO chat_messages (
        message_id, chat_session_id, sender_type, sender_role_id, sender_name,
        content, thinking_log, thought_duration_ms, tokens_consumed
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "msg_init_01", chat_sess_id, "pm_agent", "lead_pm", "Alex (Trưởng Dự Án / Lead PM)",
        "Chào bạn! Tôi là Alex. Toàn bộ ban kỹ thuật 14 nhân sự đã sẵn sàng. Chúng tôi đã chính thức khởi động Sprint 1 với CSDL SQLite và 9router Daemon.",
        "<thinking> Initializing AgentP swarm architecture. Database and proxy ready. </thinking>",
        1250, 420
    ))

    conn.commit()
    conn.close()
    print("✓ SQLite database initialized successfully at:", DB_PATH)

if __name__ == "__main__":
    init_database()
