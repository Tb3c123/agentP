---
name: "JWT & Role-Based Access Guard"
id: "jwt-rbac-authenticator"
category: "backend"
description: "Bảo mật các endpoint nội bộ với xác thực JSON Web Token và phân quyền vai trò."
tools_required: "jwt_coder, rbac_validator"
universal: true
---

# 🛠️ Skill: JWT & Role-Based Access Guard

> **Phân loại**: `BACKEND` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Bảo mật các endpoint nội bộ với xác thực JSON Web Token và phân quyền vai trò.

## 2. Công Cụ & MCP Được Kích Hoạt
- `jwt_coder, rbac_validator`

## 3. Quy Trình Thực Thi Chuẩn
1. Ký token với thuật toán HMAC-SHA256.
2. Kiểm tra header Authorization: Bearer <token>.
3. Xác minh quyền hạn trước khi cho phép gọi API nhạy cảm.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
