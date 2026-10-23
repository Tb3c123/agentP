---
name: "C4 Architecture Modeler"
id: "c4-architecture-modeling"
category: "architecture"
description: "Thiết kế và xuất sơ đồ kiến trúc 4 cấp độ: Context, Container, Component, Code dạng Mermaid."
tools_required: "mermaid_gen, arch_validator"
universal: true
---

# 🛠️ Skill: C4 Architecture Modeler

> **Phân loại**: `ARCHITECTURE` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Thiết kế và xuất sơ đồ kiến trúc 4 cấp độ: Context, Container, Component, Code dạng Mermaid.

## 2. Công Cụ & MCP Được Kích Hoạt
- `mermaid_gen, arch_validator`

## 3. Quy Trình Thực Thi Chuẩn
1. Vẽ sơ đồ Context mô tả tương tác giữa User và hệ thống.
2. Vẽ Container cho Tauri Desktop, Core Daemon và SQLite.
3. Mô tả chi tiết component và giao tiếp cổng Adapter.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
