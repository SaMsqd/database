import sqlite3


# Класс для взаимодействия с базами данных
class DB:
    def __init__(self, file_name="database.db"):
        self.file_name = file_name  # Запоминаем имя файла
        self.connection = sqlite3.connect(file_name)    # Создаём соединение
        self.cursor = self.connection.cursor()  # Создаём курсор
        self.tables = self.__get_tables()     # Запоминаем все колонки в каждой таблице в виде списка

    # Нужен только для __init__ возвращает словарь {имя таблицы: [колонка1], [колонка2]}
    def __get_tables(self):
        table_names = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[1:]
        res = dict()
        for table in table_names:
            res[table[0]] = [{x[1]: x[2]} for x in self.cursor.execute(f"PRAGMA table_info({table[0]})").fetchall()]
        return res

    # Получает инфу о всех пользователях. Аргументы: имя таблицы, распечатать результат? по дефолоту 0
    def get_all_rows(self, table_name, b_print=0):
        self.cursor.execute(f"GET * FROM {table_name}")
        if not b_print:
            print(self.cursor.fetchall())
        return self.cursor.fetchall()

    # Получает инфу о пользователе. Аргументы: имя таблицы, колонка(по чему мы будем искать), её значение,
    # распечатать результат? по дефолту 0
    def get_user_by(self, table_name, value, search_name="id", b_print=0):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {search_name} = {value}")
        if not b_print:
            print(self.cursor.fetchall())
        return self.cursor.fetchall()

    # Внести в таблицу 1 пользователя. Аргументы: название таблицы, значения
    # Если внести на одно значение меньше, то будет заноситься всё, кроме айди. Чтобы сработало,
    # айди нужен автоинкрементированный
    def insert_user(self, table_name, *values):
        if len(values) == len(self.tables[table_name]):
            value = " ".join([f'"{x}",' for x in values])[0:-1]     # Да-да, куча говнокода
            print(value)
            print(f"INSERT INTO {table_name} VALUES({value})")
            self.cursor.execute(f"INSERT INTO {table_name} VALUES({value})")
            self.connection.commit()
        elif len(values) == len(self.tables[table_name])-1:
            value = " ".join([f'"{x}",' for x in values])[0:-1]
            columns = ", ".join([list(key.keys())[0] for key in self.tables[table_name]][1:])
            self.cursor.execute(f"INSERT INTO {table_name}({columns}) VALUES({value})")
            self.connection.commit()

    # Вставляет в таблицу сразу несоклько пользователей. Лень пока что реализовывать
    def insert_users(self):
        pass

    # Удаляет пользователя по его id. Аргументы: имя таблицы, id пользователя
    def delete_user_by_id(self, table_name, id):
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id={id}")
            self.connection.commit()
        except:
            print("Ошибка, пользователя с таким id не существует")

    # Выполняет sql запрос и пытается его распечатать. Аргументы: команда
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
