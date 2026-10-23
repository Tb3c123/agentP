---
name: "1:1 AI Model Session Isolation"
id: "session-isolation-protocol"
category: "backend"
description: "Cô lập hoàn toàn context lịch sử và luồng suy nghĩ giữa 14 AI specialist models không bị nhiễm chéo."
tools_required: "session_jail, memory_scrubber"
universal: true
---

# 🛠️ Skill: 1:1 AI Model Session Isolation

> **Phân loại**: `BACKEND` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Cô lập hoàn toàn context lịch sử và luồng suy nghĩ giữa 14 AI specialist models không bị nhiễm chéo.

## 2. Công Cụ & MCP Được Kích Hoạt
- `session_jail, memory_scrubber`

## 3. Quy Trình Thực Thi Chuẩn
1. Cấp phát session_id và context window riêng biệt cho từng role_id.
2. Tái sử dụng phiên đăng nhập Claude CLI, Cursor hoặc gh auth.
3. Tách biệt token quota và lưu riêng vào CSDL SQLite.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
