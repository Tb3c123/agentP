---
name: "Cost & Token Consumption Guard"
id: "cost-token-guard"
category: "management"
description: "Giám sát ngân sách token, cảnh báo ngưỡng vượt định mức và tối ưu prompt caching 1:1."
tools_required: "token_meter, cache_optimizer"
universal: true
---

# 🛠️ Skill: Cost & Token Consumption Guard

> **Phân loại**: `MANAGEMENT` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Giám sát ngân sách token, cảnh báo ngưỡng vượt định mức và tối ưu prompt caching 1:1.

## 2. Công Cụ & MCP Được Kích Hoạt
- `token_meter, cache_optimizer`

## 3. Quy Trình Thực Thi Chuẩn
1. Đọc số token tiêu thụ từ bảng provider_sessions.
2. Tính toán tỷ lệ tiết kiệm (Tokens Saved).
3. Tối ưu prompt nén và cắt tỉa ngữ cảnh dư thừa.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
