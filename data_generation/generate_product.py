from faker import Faker
from database.connect import connect_db
from datetime import datetime
from decimal import Decimal

fake = Faker("en_US")


def generate_products():
    connection = connect_db()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Kiểm tra số lượng sản phẩm hiện tại
        cursor.execute("SELECT COUNT(*) FROM product")
        current_count = cursor.fetchone()[0]

        if current_count == 3000:
            print("Bảng product đã có đủ 3.000 sản phẩm.")
            return

        if current_count > 0:
            print(f"Bảng product hiện có {current_count} bản ghi.")
            print("Vui lòng kiểm tra dữ liệu trước khi sinh lại.")
            return

        # Lấy ID từ các bảng liên quan
        cursor.execute("SELECT brand_id FROM brand")
        brand_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT category_id FROM category")
        category_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT seller_id FROM seller")
        seller_ids = [row[0] for row in cursor.fetchall()]

        if not brand_ids or not category_ids or not seller_ids:
            raise ValueError(
                "Các bảng brand, category hoặc seller chưa có dữ liệu."
            )

        products = []

        # Sinh 3.000 sản phẩm
        for i in range(3000):
            product_name = fake.catch_phrase()

            # Chọn ID có sẵn để đảm bảo khóa ngoại hợp lệ
            category_id = fake.random_element(elements=category_ids)
            brand_id = fake.random_element(elements=brand_ids)
            seller_id = fake.random_element(elements=seller_ids)

            price = Decimal(
                fake.random_int(min=100000, max=50000000)
            )

            stock_qty = fake.random_int(min=0, max=500)

            rating = Decimal(
                fake.random_int(min=0, max=50)
            ) / Decimal("10")

            created_at = fake.date_time_between(
                start_date=datetime(2025, 1, 1),
                end_date=datetime(2025, 5, 31, 23, 59, 59)
            )

            is_active = fake.boolean(chance_of_getting_true=80)

            products.append((
                product_name,
                category_id,
                brand_id,
                seller_id,
                price,
                stock_qty,
                rating,
                created_at,
                is_active,
                "system"
            ))

            # Insert mỗi 500 sản phẩm
            if len(products) == 500:
                cursor.executemany(
                    """
                    INSERT INTO product (
                        product_name,
                        category_id,
                        brand_id,
                        seller_id,
                        price,
                        stock_qty,
                        rating,
                        created_at,
                        is_active,
                        created_by
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                    """,
                    products
                )

                connection.commit()

                print(f"Đã tạo {i + 1:,} sản phẩm.")

                products = []

        # Insert số sản phẩm còn lại
        if products:
            cursor.executemany(
                """
                INSERT INTO product (
                    product_name,
                    category_id,
                    brand_id,
                    seller_id,
                    price,
                    stock_qty,
                    rating,
                    created_at,
                    is_active,
                    created_by
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                """,
                products
            )

            connection.commit()

        print("Đã tạo thành công 3.000 sản phẩm!")

    except Exception as error:
        connection.rollback()
        print("Có lỗi xảy ra:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    generate_products()
