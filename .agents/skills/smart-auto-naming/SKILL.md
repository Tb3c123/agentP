---
name: "Smart Auto-Naming & Taxonomy"
id: "smart-auto-naming"
category: "management"
description: "Thuật toán ngôn ngữ tự động phát hiện ngữ cảnh bài toán và sinh tên dự án chuẩn kebab-case."
tools_required: "text_analyzer, regex_parser"
universal: true
---

# 🛠️ Skill: Smart Auto-Naming & Taxonomy

> **Phân loại**: `MANAGEMENT` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Thuật toán ngôn ngữ tự động phát hiện ngữ cảnh bài toán và sinh tên dự án chuẩn kebab-case.

## 2. Công Cụ & MCP Được Kích Hoạt
- `text_analyzer, regex_parser`

## 3. Quy Trình Thực Thi Chuẩn
1. Phân tích chuỗi mô tả tiếng Việt/tiếng Anh.
2. Trích xuất Domain (Food, ECommerce, SaaS, AI).
3. Trích xuất Core Function & Tech Stack.
4. Xuất 3 biến thể tên chuẩn mực.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
