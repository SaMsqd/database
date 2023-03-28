import sqlite3


class DB:
    def __init__(self, file_name="database.db"):
        self.file_name = file_name
        self.connection = sqlite3.connect(file_name)
        self.cursor = self.connection.cursor()
        self.tables = self.get_tables()

    def get_tables(self):
        table_names = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[1:]
        res = dict()
        for table in table_names:
            res[table[0]] = [{x[1]: x[2]} for x in self.cursor.execute(f"PRAGMA table_info({table[0]})").fetchall()]
        return res

    def get_all_rows(self, table_name, b_print=0):
        self.cursor.execute(f"GET * FROM {table_name}")
        if not b_print:
            print(self.cursor.fetchall())
        return self.cursor.fetchall()

    def get_user_by(self, table_name, value, search_name="id", b_print=0):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {search_name} = {value}")
        if not b_print:
            print(self.cursor.fetchall())
        return self.cursor.fetchall()

    def insert_users(self, table_name, values):
        pass

    def delete_user_by_id(self):
        pass

    def exec_command(self, command):
        try:
            self.cursor.execute(command)
            try:
                data = self.cursor.fetchall()
                print(data)
            except:
                pass
            self.connection.commit()
        except:
            print("Команда не прошла")

    # Удаляет таблицу
    def delete_table(self, table_name):
        self.cursor.execute(f"DROP TABLE {table_name}")
        self.connection.commit()

    # Создаёт таблицу в базе данных. аргументы: название таблицы, **kwargs вида "имя": "колонки её параметры"
    # Пример: create_table(users, {"id": "integer primary key autoincrement", "name": "text"})
    def create_table(self, table_name, columns: dict):
        values = ''
        for key, value in columns.items():
            values += f'{key} {value},'
        values = values[0:-1]
        try:
            self.cursor.execute(f"CREATE TABLE {table_name}({values})")
            self.connection.commit()
            print(f"Таблица {table_name} успешно создана в базе {self.file_name}")
        except:
            if input("Эта таблица уже существует, хотите пересоздать её? y/n").lower() == "y":
                self.delete_table(table_name)
                self.create_table(table_name, columns)
