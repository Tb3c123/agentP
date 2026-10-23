---
name: "Contract-First API Designer"
id: "api-contract-first"
category: "architecture"
description: "Soạn thảo đặc tả OpenAPI 3.1 và JSON Schema cho các endpoint REST trước khi code."
tools_required: "openapi_validator, schema_linter"
universal: true
---

# 🛠️ Skill: Contract-First API Designer

> **Phân loại**: `ARCHITECTURE` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Soạn thảo đặc tả OpenAPI 3.1 và JSON Schema cho các endpoint REST trước khi code.

## 2. Công Cụ & MCP Được Kích Hoạt
- `openapi_validator, schema_linter`

## 3. Quy Trình Thực Thi Chuẩn
1. Định nghĩa Data Transfer Object (DTO) cho Request và Response.
2. Khai báo status code chuẩn (200, 201, 400, 404, 500).
3. Tự động sinh client types cho TypeScript và Dart.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
