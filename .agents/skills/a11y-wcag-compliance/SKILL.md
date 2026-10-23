---
name: "A11y WCAG 2.2 Auditor"
id: "a11y-wcag-compliance"
category: "design"
description: "Kiểm tra độ tương phản màu sắc (tối thiểu 4.5:1), ARIA labels, focus ring và phím tắt trợ năng."
tools_required: "contrast_checker, aria_linter"
universal: true
---

# 🛠️ Skill: A11y WCAG 2.2 Auditor

> **Phân loại**: `DESIGN` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Kiểm tra độ tương phản màu sắc (tối thiểu 4.5:1), ARIA labels, focus ring và phím tắt trợ năng.

## 2. Công Cụ & MCP Được Kích Hoạt
- `contrast_checker, aria_linter`

## 3. Quy Trình Thực Thi Chuẩn
1. Quét toàn bộ button và input xem đã có aria-label chưa.
2. Kiểm tra độ tương phản văn bản so với màu nền.
3. Đảm bảo hỗ trợ điều hướng hoàn toàn bằng phím Tab và Enter.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
