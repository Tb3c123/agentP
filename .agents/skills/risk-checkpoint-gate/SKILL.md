---
name: "Risk Assessor & Checkpoint Gatekeeper"
id: "risk-checkpoint-gate"
category: "management"
description: "Đánh giá mức độ rủi ro của thay đổi mã nguồn và tự động kích hoạt Cổng nghiệm thu Checkpoint."
tools_required: "diff_analyzer, test_runner"
universal: true
---

# 🛠️ Skill: Risk Assessor & Checkpoint Gatekeeper

> **Phân loại**: `MANAGEMENT` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Đánh giá mức độ rủi ro của thay đổi mã nguồn và tự động kích hoạt Cổng nghiệm thu Checkpoint.

## 2. Công Cụ & MCP Được Kích Hoạt
- `diff_analyzer, test_runner`

## 3. Quy Trình Thực Thi Chuẩn
1. Kiểm tra số file sửa đổi và tỷ lệ xóa code.
2. Nếu chạm vào schema database hoặc auth -> Khóa lại và yêu cầu User bấm duyệt.
3. Sinh bản tóm tắt thay đổi dễ hiểu cho User.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
