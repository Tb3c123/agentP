---
name: "Pre-flight Diagnostics System Doctor"
id: "preflight-system-doctor"
category: "devops"
description: "Tự động kiểm tra 7 tiêu chí hệ thống: SQLite, Node.js, Git, Daemon, Flutter, Android, Swarm."
tools_required: "system_scanner, doctor_cli"
universal: true
---

# 🛠️ Skill: Pre-flight Diagnostics System Doctor

> **Phân loại**: `DEVOPS` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Tự động kiểm tra 7 tiêu chí hệ thống: SQLite, Node.js, Git, Daemon, Flutter, Android, Swarm.

## 2. Công Cụ & MCP Được Kích Hoạt
- `system_scanner, doctor_cli`

## 3. Quy Trình Thực Thi Chuẩn
1. Quét các công cụ CLI trên máy tính của người dùng.
2. Kiểm tra port 9090 và port 8080 xem có bị xung đột không.
3. Xuất báo cáo dạng bảng màu chuẩn mực [✓ ĐẠT CHUẨN].

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
