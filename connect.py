import psycopg2
from config import DB_CONFIG


def connect_db():
    try:
        connection = psycopg2.connect(**DB_CONFIG)

        print("Kết nối PostgreSQL thành công!")

        return connection

    except psycopg2.Error as error:
        print("Lỗi kết nối PostgreSQL:", error)

        return None


if __name__ == "__main__":
    connection = connect_db()

    if connection:
        connection.close()
        print("Đã đóng kết nối database.")