import re

KEYWORD_MAP = [
    (r"(đặt đồ ăn|giao đồ ăn|food delivery|thức ăn|quán ăn)", "FoodDelivery"),
    (r"(tích điểm|thành viên|voucher|khuyến mãi|loyalty|reward)", "Loyalty"),
    (r"(thương mại điện tử|bán hàng|shop|mua sắm|ecommerce|e-commerce)", "ECommerce"),
    (r"(thanh toán|ví điện tử|qr code|vnpay|momo|payment)", "Payment"),
    (r"(nhắn tin|chat|tin nhắn|messaging|chat app)", "ChatApp"),
    (r"(trí tuệ nhân tạo|ai agent|bot|llm|agent)", "AIAgent"),
    (r"(quản lý dự án|công việc|kanban|task|project)", "TaskMaster"),
    (r"(quản lý kho|inventory|kho bãi|vật tư)", "Inventory"),
    (r"(sức khỏe|y tế|bệnh viện|phòng khám|healthcare|fitness)", "HealthCare"),
    (r"(học trực tuyến|giáo dục|khóa học|lms|education)", "EduLearn"),
    (r"(mạng xã hội|social|cộng đồng|community)", "SocialNetwork"),
    (r"(tài chính|kế toán|tiết kiệm|finance|budget)", "FinanceBudget")
]

TECH_TAG_MAP = [
    (r"(flutter|dart)", "Flutter"),
    (r"(react|nextjs|next\.js)", "React"),
    (r"(nestjs|nest\.js|node)", "NestJS"),
    (r"(python|fastapi|django)", "Python"),
    (r"(android|avd|kotlin)", "Android"),
    (r"(ios|swift)", "iOS")
]

def generate_project_names(description: str):
    """
    Marcus (BA Lead) Smart Auto-Naming Algorithm:
    Phân tích từ khóa mô tả ý tưởng và sinh tên đề xuất chuẩn PascalCase-Kebab.
    """
    desc_lower = description.lower()
    detected_domains = []
    
    for pattern, label in KEYWORD_MAP:
        if re.search(pattern, desc_lower):
            detected_domains.append(label)

    detected_tech = []
    for pattern, tag in TECH_TAG_MAP:
        if re.search(pattern, desc_lower):
            detected_tech.append(tag)

    if not detected_domains:
        detected_domains = ["CustomCore"]

    primary_name = "-".join(detected_domains[:2]) + "-App"
    concise_name = detected_domains[0] + "Hub"
    tech_name = f"{detected_domains[0]}-" + (detected_tech[0] if detected_tech else "Suite")

    return {
        "primary": primary_name,
        "concise": concise_name,
        "tech_variant": tech_name,
        "detected_domains": detected_domains,
        "detected_tech": detected_tech,
        "suggested_path": f"~/Projects/{primary_name}"
    }

if __name__ == '__main__':
    sample = "Tôi muốn làm ứng dụng đặt đồ ăn trên Android và Web bằng Flutter & NestJS, có giỏ hàng, tích điểm voucher thành viên và thanh toán quét mã QR."
    print("Marcus Auto-Namer Test Output:")
    print(generate_project_names(sample))
