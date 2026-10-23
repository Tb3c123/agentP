---
name: "Onlook DOM-to-Code Synchronizer"
id: "onlook-dom-to-code"
category: "design"
description: "Click-to-inspect phần tử UI trên giao diện đang chạy và đồng bộ trực tiếp Tailwind CSS vào mã nguồn."
tools_required: "ast_parser, class_updater"
universal: true
---

# 🛠️ Skill: Onlook DOM-to-Code Synchronizer

> **Phân loại**: `DESIGN` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Click-to-inspect phần tử UI trên giao diện đang chạy và đồng bộ trực tiếp Tailwind CSS vào mã nguồn.

## 2. Công Cụ & MCP Được Kích Hoạt
- `ast_parser, class_updater`

## 3. Quy Trình Thực Thi Chuẩn
1. Bắt sự kiện click trên phần tử UI iframe sandbox.
2. Mở thanh inspector hiển thị classes Tailwind hiện tại.
3. Cho phép đổi màu sắc, padding, border radius.
4. Ghi đè vào file .tsx/.dart với độ trễ <50ms.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
