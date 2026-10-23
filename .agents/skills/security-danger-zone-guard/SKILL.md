---
name: "Antigravity Danger Zone Safety Lock"
id: "security-danger-zone-guard"
category: "security"
description: "Cơ chế bảo vệ 2 lớp chống mất dữ liệu: bắt buộc gõ chính xác 100% tên dự án để mở khóa nút xóa."
tools_required: "security_guard, string_verifier"
universal: true
---

# 🛠️ Skill: Antigravity Danger Zone Safety Lock

> **Phân loại**: `SECURITY` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Cơ chế bảo vệ 2 lớp chống mất dữ liệu: bắt buộc gõ chính xác 100% tên dự án để mở khóa nút xóa.

## 2. Công Cụ & MCP Được Kích Hoạt
- `security_guard, string_verifier`

## 3. Quy Trình Thực Thi Chuẩn
1. Khóa cứng nút xóa (disabled, con trỏ not-allowed).
2. Bắt sự kiện bàn phím so khớp chính xác từng ký tự hoa/thường.
3. Chỉ mở khóa đỏ khi trùng khớp 100%, yêu cầu popup xác nhận lần 2.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
