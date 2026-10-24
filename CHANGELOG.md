# Changelog 📜
All notable changes to **agentP** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.7.0] - 2026-10-24 (Sprint 8)

### 🚀 Added
- Automated Git Engine with Conventional Commits validation (`feat:`, `fix:`, `refactor:`)
- Automated Keep a Changelog generator service (`CHANGELOG.md`)
- Chaos & Process Crash Resilience Guard with SQLite WAL snapshots
- Local Daemon JWT Authenticator and Role-Based Access Control (RBAC)

### 🔄 Changed
- Enhanced UI Workspace with Changelog modal viewer and Git Staging diff tool
- Updated full documentation manual in `docs/AGENTP_MASTER_ARCHITECTURE.md`

### 🛠️ Fixed
- Prevented flex-direction squishing across full-width views (`.personnel-view`, `.providers-hub-view`)
- Fixed header collapse on smaller viewports with full-width enforcement

### 🛡️ Security
- Added token-based authorization for daemon management endpoints
- Reinforced 2-step Antigravity Danger Zone deletion safety lock

## [2.6.0] - 2026-10-24 (Sprint 7)

### 🚀 Added
- Dynamic Agent Summoning protocol between peer specialists
- Real-time Event-Driven Pub-Sub Bus (`/api/swarm/events`)
- Multi-Turn Swarm Execution Runner connecting PM -> BA -> Dev -> QA -> Checkpoint
- Cost & Token Consumption Guard with 1:1 prompt caching calculation

### 🔄 Changed
- Transformed README.md into high-impact executive product showcase

### 🛠️ Fixed
- Resolved horizontal layout bug on Providers Hub and Personnel views

## [2.5.0] - 2026-10-24 (Sprint 6)

### 🚀 Added
- In-house 9router Core Engine with zero external Node.js/Docker dependencies
- Developer CLI Bridge for Claude Code (`/v1/messages`) and Cursor (`/v1/chat/completions`)
- Automated failover fallback when upstream provider latency exceeds threshold
