---
name: "Unit Test Coverage Enforcer"
id: "unit-test-coverage-enforcer"
category: "qa"
description: "Đo lường độ bao phủ mã nguồn (Code Coverage) và chặn commit nếu dưới 80%."
tools_required: "coverage_lcov, test_runner"
universal: true
---

# 🛠️ Skill: Unit Test Coverage Enforcer

> **Phân loại**: `QA` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Đo lường độ bao phủ mã nguồn (Code Coverage) và chặn commit nếu dưới 80%.

## 2. Công Cụ & MCP Được Kích Hoạt
- `coverage_lcov, test_runner`

## 3. Quy Trình Thực Thi Chuẩn
1. Chạy toàn bộ test suites với cờ --coverage.
2. Xuất báo cáo LCOV và phân tích độ phủ từng file.
3. Xác nhận đạt 100% Pass trước khi cho phép đóng Sprint.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
