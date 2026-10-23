---
name: "Flutter BLoC/Cubit State Machine"
id: "flutter-bloc-state-machine"
category: "frontend"
description: "Xây dựng kiến trúc BLoC cho ứng dụng Flutter di động, phân tách Event, State và UI."
tools_required: "flutter_gen, dart_analyzer"
universal: true
---

# 🛠️ Skill: Flutter BLoC/Cubit State Machine

> **Phân loại**: `FRONTEND` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Xây dựng kiến trúc BLoC cho ứng dụng Flutter di động, phân tách Event, State và UI.

## 2. Công Cụ & MCP Được Kích Hoạt
- `flutter_gen, dart_analyzer`

## 3. Quy Trình Thực Thi Chuẩn
1. Định nghĩa sealed class cho CartState: Initial, Loading, Loaded, Error.
2. Xử lý các sự kiện: AddToCart, ApplyVoucher, Checkout.
3. Đảm bảo render lại UI với blocBuilder mà không gây giật lag (60 FPS).

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
