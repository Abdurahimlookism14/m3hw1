import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS survey_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER,
                        gender TEXT,
                        genre TEXT
                    )
                """
            )
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS genres (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT
                    )
                """
            )
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS books(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        author TEXT,
                        price INTEGER,
                        genre TEXT 
                        genre_id INTEGER,
                        FOREIGN KEY (genre_id) REFERENCES genres(id)
                    )
                """
            )
            conn.commit()

    def execute(self, query: str, params: tuple):
        with sqlite3.connect(self.path) as conn:
            conn.execute(query, params)
            conn.commit()

    def fetch(self, query: str, params: tuple = None):
        with sqlite3.connect(self.path) as conn:
            if not params:
                params = tuple()
            result = conn.execute(query, params)
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(r) for r in data]



# conn = sqlite3.connect("database.sqlite")
# cursor = conn.cursor()

# conn.execute("""
#     CREATE TABLE IF NOT EXISTS survey_results (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         age INTEGER,
#         gender TEXT,
#         genre TEXT
#     )
# """)


import sqlite3

class Database:
    def init(self, db_name="reviews.db"):
        self.db_name = db_name

    def execute(self, query, params=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def create_tables(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            visit_date TEXT NOT NULL,
            food_rating INTEGER NOT NULL,
            cleanliness_rating INTEGER NOT NULL,
            extra_comments TEXT
        );
        '''
        self.execute(create_table_query)


import sqlite3

class Database:
    def init(self, db_name="reviews.db"):
        self.db_name = db_name

    def execute(self, query, params=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def create_tables(self):
        create_reviews_table_query = '''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            visit_date TEXT NOT NULL,
            food_rating INTEGER NOT NULL,
            cleanliness_rating INTEGER NOT NULL,
            extra_comments TEXT
        );
        '''
        self.execute(create_reviews_table_query)

        create_dishes_table_query = '''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL
        );
        '''
        self.execute(create_dishes_table_query)



import sqlite3

class Database:
    def init(self, db_name="reviews.db"):
        self.db_name = db_name

    def execute(self, query, params=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def create_tables(self):
        create_categories_table_query = '''
        CREATE TABLE IF NOT EXISTS dish_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL
        );
        '''
        self.execute(create_categories_table_query)

        create_dishes_table_query = '''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES dish_categories(id)
        );
        '''
        self.execute(create_dishes_table_query)