---
name: "Docker Multi-Stage Lightweight Bundle"
id: "docker-multistage-bundle"
category: "devops"
description: "Viết Dockerfile đa giai đoạn tạo image kích thước siêu nhẹ (<80MB) để triển khai nhanh."
tools_required: "docker_cli, image_optimizer"
universal: true
---

# 🛠️ Skill: Docker Multi-Stage Lightweight Bundle

> **Phân loại**: `DEVOPS` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Viết Dockerfile đa giai đoạn tạo image kích thước siêu nhẹ (<80MB) để triển khai nhanh.

## 2. Công Cụ & MCP Được Kích Hoạt
- `docker_cli, image_optimizer`

## 3. Quy Trình Thực Thi Chuẩn
1. Giai đoạn 1 (Builder): Biên dịch source code và cài dependencies.
2. Giai đoạn 2 (Runner): Chỉ chép file build và binary sang base Alpine Linux.
3. Cấu hình người dùng non-root để đảm bảo an toàn.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
