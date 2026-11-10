from faker import Faker
from database.connect import connect_db
from datetime import datetime

fake = Faker("en_US")


def generate_promotion_products():
    connection = connect_db()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Kiểm tra số lượng hiện tại
        cursor.execute("SELECT COUNT(*) FROM promotion_product")
        current_count = cursor.fetchone()[0]

        if current_count == 500:
            print("Bảng promotion_product đã có đủ 500 bản ghi.")
            return

        if current_count > 0:
            print(f"Bảng promotion_product hiện có {current_count} bản ghi.")
            print("Vui lòng kiểm tra dữ liệu trước khi sinh lại.")
            return

        # Lấy ID từ bảng promotion
        cursor.execute("SELECT promotion_id FROM promotion")
        promotion_ids = [row[0] for row in cursor.fetchall()]

        # Lấy ID từ bảng product
        cursor.execute("SELECT product_id FROM product")
        product_ids = [row[0] for row in cursor.fetchall()]

        if not promotion_ids or not product_ids:
            raise ValueError(
                "Bảng promotion hoặc product chưa có dữ liệu."
            )

        # Tạo 500 cặp promotion_id và product_id không trùng nhau
        all_pairs = [
            (promotion_id, product_id)
            for promotion_id in promotion_ids
            for product_id in product_ids
        ]

        selected_pairs = fake.random_elements(
            elements=all_pairs,
            length=500,
            unique=True
        )

        promotion_products = []

        for promotion_id, product_id in selected_pairs:
            created_at = fake.date_time_between(
                start_date=datetime(2025, 1, 1),
                end_date=datetime(2025, 5, 31, 23, 59, 59)
            )

            promotion_products.append((
                promotion_id,
                product_id,
                created_at,
                "system"
            ))

        # Chèn dữ liệu vào PostgreSQL
        cursor.executemany(
            """
            INSERT INTO promotion_product (
                promotion_id,
                product_id,
                created_at,
                created_by
            )
            VALUES (%s, %s, %s, %s)
            """,
            promotion_products
        )

        connection.commit()

        print("Đã tạo thành công 500 liên kết promotion_product!")

    except Exception as error:
        connection.rollback()
        print("Có lỗi xảy ra:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    generate_promotion_products()
