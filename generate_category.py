from faker import Faker
from connect import connect_db

fake = Faker("en_US")


def generate_categories():
    connection = connect_db()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Kiểm tra số lượng dữ liệu hiện tại
        cursor.execute("SELECT COUNT(*) FROM category")
        current_count = cursor.fetchone()[0]

        if current_count == 25:
            print("Bảng category đã có đủ 25 bản ghi.")
            return

        if current_count > 0:
            print("Bảng category đã có dữ liệu.")
            print("Vui lòng kiểm tra trước khi sinh lại.")
            return

        # 1. Sinh 5 danh mục cha bằng Faker
        parent_categories = []

        for _ in range(5):
            category_name = fake.unique.word().capitalize()
            parent_categories.append(category_name)

        parent_ids = []

        for category_name in parent_categories:
            cursor.execute(
                """
                INSERT INTO category (
                    category_name,
                    parent_category_id,
                    level,
                    created_by
                )
                VALUES (%s, NULL, %s, %s)
                RETURNING category_id
                """,
                (category_name, 1, "system")
            )

            parent_id = cursor.fetchone()[0]
            parent_ids.append(parent_id)

        # 2. Sinh 20 danh mục con bằng Faker
        for _ in range(20):
            category_name = fake.unique.word().capitalize()

            # Chọn ngẫu nhiên một danh mục cha
            parent_id = fake.random_element(elements=parent_ids)

            cursor.execute(
                """
                INSERT INTO category (
                    category_name,
                    parent_category_id,
                    level,
                    created_by
                )
                VALUES (%s, %s, %s, %s)
                """,
                (category_name, parent_id, 2, "system")
            )

        connection.commit()

        print("Đã tạo thành công 25 danh mục.")
        print("Danh mục cha: 5")
        print("Danh mục con: 20")

    except Exception as error:
        connection.rollback()
        print("Có lỗi xảy ra:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    generate_categories()
