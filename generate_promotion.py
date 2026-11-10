from faker import Faker
from connect import connect_db
from datetime import datetime, timedelta
from decimal import Decimal

fake = Faker("vi_VN")


def generate_promotions():
    connection = connect_db()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Kiểm tra số lượng promotion hiện tại
        cursor.execute("SELECT COUNT(*) FROM promotion")
        current_count = cursor.fetchone()[0]

        if current_count == 30:
            print("Bảng promotion đã có đủ 30 bản ghi.")
            return

        if current_count > 0:
            print(f"Bảng promotion hiện có {current_count} bản ghi.")
            print("Vui lòng kiểm tra dữ liệu trước khi sinh lại.")
            return

        promotions = []

        for i in range(30):

            # Sinh ngày bắt đầu trong khoảng tháng 1 - tháng 5/2025
            start_date = fake.date_between(
                start_date=datetime(2025, 1, 1).date(),
                end_date=datetime(2025, 5, 31).date()
            )

            # Ngày tạo phải nhỏ hơn hoặc bằng ngày bắt đầu
            created_at = fake.date_time_between(
                start_date=datetime(2024, 12, 1),
                end_date=datetime.combine(start_date, datetime.max.time())
            )

            # Ngày kết thúc sau ngày bắt đầu từ 30 - 50 ngày
            end_date = start_date + timedelta(
                days=fake.random_int(min=30, max=50)
            )

            promotion_name = fake.catch_phrase()

            promotion_type = fake.random_element(
                elements=(
                    "product",
                    "category",
                    "seller",
                    "flash_sale"
                )
            )

            discount_type = fake.random_element(
                elements=("percentage", "fixed_amount")
            )

            if discount_type == "percentage":
                discount_value = Decimal(
                    fake.random_int(min=1, max=100)
                )
            else:
                discount_value = Decimal(
                    fake.random_int(min=10000, max=500000)
                )

            promotions.append((
                promotion_name,
                promotion_type,
                discount_type,
                discount_value,
                start_date,
                end_date,
                created_at,
                "system"
            ))

        # Chèn dữ liệu vào PostgreSQL
        cursor.executemany(
            """
            INSERT INTO promotion (
                promotion_name,
                promotion_type,
                discount_type,
                discount_value,
                start_date,
                end_date,
                created_at,
                created_by
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            promotions
        )

        connection.commit()

        print("Đã tạo thành công 30 chương trình khuyến mãi!")

    except Exception as error:
        connection.rollback()
        print("Có lỗi xảy ra:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    generate_promotions()
