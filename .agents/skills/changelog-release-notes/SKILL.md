---
name: "Automated Changelog & Release Notes Generator"
id: "changelog-release-notes"
category: "docs"
description: "Tự động trích xuất git commit history và phân loại theo Sprint để tạo CHANGELOG.md chuẩn Keep a Changelog."
tools_required: "git_log_parser, markdown_writer"
universal: true
---

# 🛠️ Skill: Automated Changelog & Release Notes Generator

> **Phân loại**: `DOCS` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Tự động trích xuất git commit history và phân loại theo Sprint để tạo CHANGELOG.md chuẩn Keep a Changelog.

## 2. Công Cụ & MCP Được Kích Hoạt
- `git_log_parser, markdown_writer`

## 3. Quy Trình Thực Thi Chuẩn
1. Đọc lịch sử commit giữa các tag phát hành.
2. Nhóm thành các mục: Added, Changed, Fixed, Security.
3. Xuất tài liệu Markdown đẹp mắt phục vụ bàn giao dự án.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
