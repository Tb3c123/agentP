---
name: "Event-Driven Pub-Sub Bus"
id: "event-driven-pubsub"
category: "architecture"
description: "Thiết lập bus sự kiện đồng bộ/bất đồng bộ giữa Alex và 13 agent roles ngầm."
tools_required: "event_dispatcher, queue_manager"
universal: true
---

# 🛠️ Skill: Event-Driven Pub-Sub Bus

> **Phân loại**: `ARCHITECTURE` | **Tính khả dụng**: Toàn bộ 14 vai trò Swarm (Universal)

## 1. Mô Tả Nhiệm Vụ
Thiết lập bus sự kiện đồng bộ/bất đồng bộ giữa Alex và 13 agent roles ngầm.

## 2. Công Cụ & MCP Được Kích Hoạt
- `event_dispatcher, queue_manager`

## 3. Quy Trình Thực Thi Chuẩn
1. Đăng ký subscriber cho các sự kiện: TaskCreated, CodeDiffReady, CheckpointApproved.
2. Đảm bảo xử lý lỗi độc lập không làm treo daemon.
3. Ghi log sự kiện vào SQLite audit trail.

## 4. Tiêu Chuẩn Nghiệm Thu (Definition of Done)
- Thực hiện hoàn tất không có cảnh báo lỗi.
- Ghi nhận nhật ký suy nghĩ và cập nhật trạng thái vào CSDL SQLite `.agents/db.sqlite`.
