---
name: "Bi-directional AST Sync Engine"
id: "ast-sync-bidirectional"
category: "backend"
description: "Phân tích cú pháp Abstract Syntax Tree và sửa đổi file code thật với độ trễ <50ms."
tools_required: "ast_engine, file_patcher"
universal: true
---

# 🛠️ Skill: Bi-directional AST Sync Engine

> **Phân loại**: `BACKEND` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Phân tích cú pháp Abstract Syntax Tree và sửa đổi file code thật với độ trễ <50ms.

## 2. Công Cụ & MCP Được Kích Hoạt
- `ast_engine, file_patcher`

## 3. Quy Trình Thực Thi Chuẩn
1. Đọc nội dung file TypeScript/Dart và xác định vị trí thẻ JSX/Widget.
2. Cập nhật chuỗi className hoặc styling properties.
3. Lưu bản snapshot dự phòng vào CSDL trước khi ghi file.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
