---
name: "Live Hot Reload & Layout Fixer"
id: "hot-reload-diagnostics"
category: "frontend"
description: "Kết nối Flutter DevTools và Chrome Inspector để phát hiện và sửa tức thời lỗi layout overflow."
tools_required: "hot_reload_bridge, stack_tracer"
universal: true
---

# 🛠️ Skill: Live Hot Reload & Layout Fixer

> **Phân loại**: `FRONTEND` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Kết nối Flutter DevTools và Chrome Inspector để phát hiện và sửa tức thời lỗi layout overflow.

## 2. Công Cụ & MCP Được Kích Hoạt
- `hot_reload_bridge, stack_tracer`

## 3. Quy Trình Thực Thi Chuẩn
1. Lắng nghe thông báo lỗi 'RenderFlex overflowed by X pixels'.
2. Thay thế Column không giới hạn bằng SingleChildScrollView hoặc Expanded.
3. Gửi tín hiệu Hot Reload (phím r) để kiểm tra kết quả ngay lập tức.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
