"""
agentP - Providers Repository
Manages global AI provider credentials, connection status, latency and endpoints in SQLite WAL.
Author: Carlos (Backend Dev) & Alex (PM)
"""

import sqlite3
import os
from typing import Dict, Any, List, Optional
try:
    from .base_repo import BaseRepository
except ImportError:
    from base_repo import BaseRepository

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.agents', 'db.sqlite'))

class ProvidersRepository(BaseRepository):
    """Manages global AI provider settings and failover configurations."""

    @classmethod
    def ensure_table(cls):
        """Creates the global_providers table if it does not exist."""
        conn = cls.get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS global_providers (
                    provider_id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    category TEXT NOT NULL CHECK(category IN ('oauth', 'free', 'api', 'compat')),
                    icon TEXT NOT NULL,
                    base_url TEXT NOT NULL,
                    api_key TEXT,
                    is_enabled INTEGER DEFAULT 1,
                    models_supported TEXT DEFAULT '',
                    latency_ms INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'configured',
                    failover_priority INTEGER DEFAULT 10,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            cls._seed_defaults(conn)
        finally:
            conn.close()

    @classmethod
    def _seed_defaults(cls, conn: sqlite3.Connection):
        """Seeds initial 9router providers if table is empty."""
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM global_providers;")
        if cursor.fetchone()[0] > 0:
            return

        defaults = [
            # OAuth Providers
            ('claude_code', 'Claude Code CLI', 'oauth', '🤖', 'http://127.0.0.1:9090', '', 1, 'claude-3-5-sonnet,claude-3-7-sonnet', 98, 'connected', 1),
            ('cursor', 'Cursor IDE Bridge', 'oauth', '⚡', 'http://127.0.0.1:9090/v1', '', 1, 'claude-3-5-sonnet,gpt-4o', 115, 'connected', 2),
            ('codex', 'Codex CLI', 'oauth', '💻', 'http://127.0.0.1:9090/v1', '', 1, 'gpt-4o,o3-mini', 130, 'connected', 3),
            ('gemini_cli', 'Gemini CLI Tool', 'oauth', '✨', 'http://127.0.0.1:9090', '', 1, 'gemini-2-5-pro,gemini-2-5-flash', 88, 'connected', 4),

            # Free Providers
            ('antigravity', 'Antigravity Core Free', 'free', '🚀', 'http://127.0.0.1:9090/v1', '', 1, 'gemini-2-5-flash,claude-3-5-haiku', 64, 'connected', 5),
            ('qwen_code', 'Qwen 2.5 Coder Free', 'free', '🐉', 'https://api.qwen.ai/v1', '', 1, 'qwen-2-5-coder', 142, 'connected', 6),
            ('kimi', 'Kimi Moonshot Free', 'free', '🌙', 'https://api.moonshot.cn/v1', '', 1, 'kimi-v1', 185, 'connected', 7),
            ('glm', 'GLM-4 Free', 'free', '🔮', 'https://api.zhipuai.cn/v1', '', 1, 'glm-4', 190, 'connected', 8),

            # API Key Providers
            ('openrouter', 'OpenRouter', 'api', '🧭', 'https://openrouter.ai/api/v1', '', 1, 'claude-3-7-sonnet,deepseek-r1,gpt-4o', 110, 'connected', 1),
            ('deepseek', 'DeepSeek Official', 'api', '🐳', 'https://api.deepseek.com/v1', '', 1, 'deepseek-r1,deepseek-v3', 125, 'connected', 2),
            ('anthropic', 'Anthropic Direct', 'api', '🎭', 'https://api.anthropic.com/v1', '', 1, 'claude-3-5-sonnet,claude-3-7-sonnet', 95, 'connected', 3),
            ('openai', 'OpenAI Direct', 'api', '🧠', 'https://api.openai.com/v1', '', 1, 'gpt-4o,gpt-4o-mini,o3-mini', 105, 'connected', 4),
            ('groq', 'Groq Ultra-Fast LPU', 'api', '⚡', 'https://api.groq.com/openai/v1', '', 1, 'llama-3.3-70b', 45, 'connected', 5),
            ('cerebras', 'Cerebras Fast', 'api', '🧠', 'https://api.cerebras.ai/v1', '', 0, 'llama-3.1-70b', 0, 'disconnected', 9),
            ('cohere', 'Cohere Command', 'api', '🔗', 'https://api.cohere.com/v1', '', 0, 'command-r-plus', 0, 'disconnected', 10),

            # Compatible Providers
            ('alibaba_compat', 'Alibaba Custom Compatible', 'compat', '🈹', 'https://dashscope.aliyuncs.com/compatible-mode/v1', '', 1, 'qwen-plus', 160, 'connected', 6),
        ]

        cursor.executemany("""
            INSERT INTO global_providers (
                provider_id, display_name, category, icon, base_url, api_key, is_enabled, models_supported, latency_ms, status, failover_priority
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, defaults)
        conn.commit()

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        cls.ensure_table()
        conn = cls.get_connection()
        try:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM global_providers ORDER BY category, failover_priority;").fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @classmethod
    def get_by_category(cls) -> Dict[str, List[Dict[str, Any]]]:
        all_provs = cls.get_all()
        grouped = {
            'oauth': [],
            'free': [],
            'api': [],
            'compat': []
        }
        for p in all_provs:
            cat = p.get('category', 'api')
            if cat in grouped:
                grouped[cat].append(p)
        return grouped

    @classmethod
    def get_by_id(cls, provider_id: str) -> Optional[Dict[str, Any]]:
        cls.ensure_table()
        conn = cls.get_connection()
        try:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM global_providers WHERE provider_id = ?;", (provider_id,)).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @classmethod
    def update_config(cls, provider_id: str, data: Dict[str, Any]) -> bool:
        cls.ensure_table()
        conn = cls.get_connection()
        try:
            base_url = data.get('base_url')
            api_key = data.get('api_key')
            models = data.get('models_supported')
            is_enabled = data.get('is_enabled', 1)
            status = 'connected' if (api_key or 'free' in provider_id or 'oauth' in provider_id) else 'configured'

            conn.execute("""
                UPDATE global_providers
                SET base_url = COALESCE(?, base_url),
                    api_key = COALESCE(?, api_key),
                    models_supported = COALESCE(?, models_supported),
                    is_enabled = COALESCE(?, is_enabled),
                    status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE provider_id = ?;
            """, (base_url, api_key, models, is_enabled, status, provider_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @classmethod
    def update_latency(cls, provider_id: str, latency_ms: int, status: str = 'connected'):
        cls.ensure_table()
        conn = cls.get_connection()
        try:
            conn.execute("""
                UPDATE global_providers
                SET latency_ms = ?, status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE provider_id = ?;
            """, (latency_ms, status, provider_id))
            conn.commit()
        finally:
            conn.close()
