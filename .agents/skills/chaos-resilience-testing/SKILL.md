---
name: "Chaos & Process Crash Recovery"
id: "chaos-resilience-testing"
category: "qa"
description: "Kiểm thử tắt ứng dụng đột ngột (kill -9) để chứng minh SQLite WAL không bị hỏng dữ liệu."
tools_required: "process_killer, integrity_checker"
universal: true
---

# 🛠️ Skill: Chaos & Process Crash Recovery

> **Phân loại**: `QA` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Kiểm thử tắt ứng dụng đột ngột (kill -9) để chứng minh SQLite WAL không bị hỏng dữ liệu.

## 2. Công Cụ & MCP Được Kích Hoạt
- `process_killer, integrity_checker`

## 3. Quy Trình Thực Thi Chuẩn
1. Đang ghi dữ liệu vào SQLite -> Ngắt tiến trình đột ngột.
2. Mở lại ứng dụng và chạy PRAGMA integrity_check.
3. Chứng minh toàn bộ transaction đã commit được bảo toàn 100%.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
