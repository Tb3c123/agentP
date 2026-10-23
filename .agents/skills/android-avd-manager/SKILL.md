---
name: "Android Virtual Device (AVD) Controller"
id: "android-avd-manager"
category: "devops"
description: "Quản lý vòng đời máy ảo Android Pixel 8 Pro: khởi chạy GUI/Headless, cài APK, chụp ảnh màn hình."
tools_required: "emulator_cli, adb_bridge"
universal: true
---

# 🛠️ Skill: Android Virtual Device (AVD) Controller

> **Phân loại**: `DEVOPS` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Quản lý vòng đời máy ảo Android Pixel 8 Pro: khởi chạy GUI/Headless, cài APK, chụp ảnh màn hình.

## 2. Công Cụ & MCP Được Kích Hoạt
- `emulator_cli, adb_bridge`

## 3. Quy Trình Thực Thi Chuẩn
1. Kiểm tra danh sách AVD có sẵn qua lệnh `emulator -list-avds`.
2. Khởi chạy máy ảo tại port 5554.
3. Chụp ảnh màn hình qua adb và lưu vào docs/assets/.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
