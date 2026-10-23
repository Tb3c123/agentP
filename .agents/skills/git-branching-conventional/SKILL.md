---
name: "Git Branching & Conventional Commits"
id: "git-branching-conventional"
category: "devops"
description: "Quản lý chiến lược nhánh feature/*, hotfix/* và chuẩn hóa thông điệp commit feat/fix/refactor."
tools_required: "git_cli, commit_linter"
universal: true
---

# 🛠️ Skill: Git Branching & Conventional Commits

> **Phân loại**: `DEVOPS` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Quản lý chiến lược nhánh feature/*, hotfix/* và chuẩn hóa thông điệp commit feat/fix/refactor.

## 2. Công Cụ & MCP Được Kích Hoạt
- `git_cli, commit_linter`

## 3. Quy Trình Thực Thi Chuẩn
1. Tạo nhánh tính năng cô lập từ main: feature/<tên-tính-năng>.
2. Soạn thông điệp commit theo chuẩn: type(scope): description.
3. Kiểm tra git status sạch sẽ trước khi tạo Pull Request.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
