from faker import Faker
from connect import connect_db
from decimal import Decimal

fake = Faker("en_US")


def generate_sellers():
    connection = connect_db()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Kiểm tra số lượng dữ liệu hiện tại
        cursor.execute("SELECT COUNT(*) FROM seller")
        current_count = cursor.fetchone()[0]

        remaining = 50 - current_count

        if remaining <= 0:
            print("Bảng seller đã có đủ 50 bản ghi.")
            return

        if current_count > 0:
            print(f"Bảng seller hiện có {current_count} bản ghi.")
            print("Vui lòng kiểm tra dữ liệu trước khi sinh thêm.")
            return

        sellers = []

        # Sinh dữ liệu bằng Faker
        for _ in range(remaining):
            seller_name = fake.unique.company()
            join_date = fake.date_between(
                start_date="-5y",
                end_date="today"
            )

            seller_type = fake.random_element(
                elements=("Official", "Marketplace")
            )

            rating = Decimal(
                fake.random_int(min=0, max=50)
            ) / Decimal("10")

            country = "Vietnam"

            sellers.append((
                seller_name,
                join_date,
                seller_type,
                rating,
                country,
                "system"
            ))

        # Thêm dữ liệu vào PostgreSQL
        cursor.executemany(
            """
            INSERT INTO seller (
                seller_name,
                join_date,
                seller_type,
                rating,
                country,
                created_by
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            sellers
        )

        connection.commit()

        print(f"Đã tạo thành công {remaining} người bán.")

    except Exception as error:
        connection.rollback()
        print("Có lỗi xảy ra:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    generate_sellers()
