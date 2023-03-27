import sqlite3


def create_table():
    connection = sqlite3.connect("test.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text);
    """)
    connection.commit()
    return connection, cursor


def add_user(cursor, connection, data):
    cursor.execute("INSERT INTO users(name) values(?)", (data,))
    connection.commit()


def get_user_by_id(cursor, id):
    try:
        cursor.execute(f"SELECT * FROM users WHERE id = {id}")
        return cursor.fetchall()
    except:
        print("Ошибка! Пользователя с таким id не существует!")


connection, cursor = create_table()
print(get_user_by_id(cursor, 1))
