from datetime import datetime
from faker import Faker
from database.connect import connect_db

fake = Faker("en_US")


def generate_customers():
    connection = connect_db()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Kiểm tra số lượng khách hàng hiện tại
        cursor.execute("SELECT COUNT(*) FROM customer")
        current_count = cursor.fetchone()[0]

        if current_count == 30000:
            print("Bảng customer đã có đủ 30.000 bản ghi.")
            return

        if current_count > 0:
            print(f"Bảng customer hiện có {current_count} bản ghi.")
            print("Vui lòng kiểm tra dữ liệu trước khi sinh thêm.")
            return

        customers = []

        # Sinh 30.000 khách hàng
        for i in range(30000):
            customer_name = fake.name()
            email = fake.unique.email()

            # Sinh số điện thoại gồm 10 chữ số
            phone = fake.unique.numerify(text="09########")

            gender = fake.random_element(
                elements=("Male", "Female")
            )

            address = fake.address().replace("\n", ", ")
            city = fake.city()

            # Thời gian đăng ký từ tháng 1 đến tháng 5 năm 2025
            created_at = fake.date_time_between(
                start_date=datetime(2025, 1, 1),
                end_date=datetime(2025, 5, 31, 23, 59, 59)
            )

            customers.append((
                customer_name,
                email,
                phone,
                gender,
                address,
                city,
                created_at,
                "system"
            ))

            # Mỗi 1.000 khách hàng thì ghi vào database
            if len(customers) == 1000:
                cursor.executemany(
                    """
                    INSERT INTO customer (
                        customer_name,
                        email,
                        phone,
                        gender,
                        address,
                        city,
                        created_at,
                        created_by
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    customers
                )

                connection.commit()
                print(f"Đã tạo {i + 1:,} khách hàng.")

                customers = []

        # Ghi những bản ghi còn lại
        if customers:
            cursor.executemany(
                """
                INSERT INTO customer (
                    customer_name,
                    email,
                    phone,
                    gender,
                    address,
                    city,
                    created_at,
                    created_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                customers
            )

            connection.commit()

        print("Đã tạo thành công 30.000 khách hàng!")

    except Exception as error:
        connection.rollback()
        print("Có lỗi xảy ra:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    generate_customers()
