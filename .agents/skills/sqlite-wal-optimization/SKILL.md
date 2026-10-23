---
name: "SQLite WAL Engine Optimizer"
id: "sqlite-wal-optimization"
category: "architecture"
description: "Cấu hình Write-Ahead Logging (WAL), foreign keys cascade và giải quyết lock contention dưới 5ms."
tools_required: "sql_runner, pragma_tuner"
universal: true
---

# 🛠️ Skill: SQLite WAL Engine Optimizer

> **Phân loại**: `ARCHITECTURE` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Cấu hình Write-Ahead Logging (WAL), foreign keys cascade và giải quyết lock contention dưới 5ms.

## 2. Công Cụ & MCP Được Kích Hoạt
- `sql_runner, pragma_tuner`

## 3. Quy Trình Thực Thi Chuẩn
1. Bật PRAGMA journal_mode = WAL.
2. Bật PRAGMA foreign_keys = ON.
3. Đặt synchronous = NORMAL và cache_size = -64000 (64MB RAM).
4. Chạy ANALYZE định kỳ để tối ưu hóa query plan.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
