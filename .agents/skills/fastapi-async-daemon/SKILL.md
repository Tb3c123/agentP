---
name: "Asynchronous High-Speed Local Daemon"
id: "fastapi-async-daemon"
category: "backend"
description: "Xây dựng REST/WebSocket daemon phản hồi dưới 10ms, tiết kiệm RAM (<45MB) và không phụ thuộc bên ngoài."
tools_required: "socket_builder, async_worker"
universal: true
---

# 🛠️ Skill: Asynchronous High-Speed Local Daemon

> **Phân loại**: `BACKEND` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Xây dựng REST/WebSocket daemon phản hồi dưới 10ms, tiết kiệm RAM (<45MB) và không phụ thuộc bên ngoài.

## 2. Công Cụ & MCP Được Kích Hoạt
- `socket_builder, async_worker`

## 3. Quy Trình Thực Thi Chuẩn
1. Sử dụng non-blocking I/O hoặc luồng sự kiện nhẹ.
2. Định tuyến các endpoint /health, /sessions, /kanban, /chat.
3. Đóng gói binary tự khởi chạy cùng Tauri v2.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
