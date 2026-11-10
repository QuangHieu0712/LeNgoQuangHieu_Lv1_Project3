from faker import Faker
from connect import connect_db

fake = Faker("en_US")


def generate_brands():
    connection = connect_db()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Kiểm tra số lượng brand hiện có
        cursor.execute("SELECT COUNT(*) FROM brand")
        current_count = cursor.fetchone()[0]

        # Chỉ tạo thêm nếu chưa đủ 20 bản ghi
        remaining = 20 - current_count

        if remaining <= 0:
            print("Bảng brand đã có đủ 20 bản ghi.")
            return

        brands = []

        for _ in range(remaining):
            brand_name = fake.unique.company()
            country = fake.country()

            brands.append((
                brand_name,
                country,
                "system"
            ))

        # Thêm dữ liệu vào PostgreSQL
        cursor.executemany(
            """
            INSERT INTO brand (
                brand_name,
                country,
                created_by
            )
            VALUES (%s, %s, %s)
            """,
            brands
        )

        connection.commit()

        print(f"Đã tạo thêm {remaining} thương hiệu.")

    except Exception as error:
        connection.rollback()
        print("Có lỗi xảy ra:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    generate_brands()