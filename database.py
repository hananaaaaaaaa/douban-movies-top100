import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="douban_top100.db"):
        self.db_name = f"data/{db_name}"
        self.init_database()
    
    def init_database(self):
        """初始化数据库和表"""
        os.makedirs('data', exist_ok=True)
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ranking INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            rating DECIMAL(2,1) NOT NULL,
            rating_count INTEGER,
            release_year INTEGER,
            genres VARCHAR(100),
            country VARCHAR(100),
            directors VARCHAR(255),
            casts VARCHAR(500),
            douban_url VARCHAR(500),
            created_time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_movies(self, movies):
        """保存电影数据到数据库"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # 清空现有数据
        cursor.execute('DELETE FROM movies')
        
        for movie in movies:
            cursor.execute('''
            INSERT INTO movies 
            (ranking, title, rating, rating_count, release_year, genres, country, directors, casts, douban_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                movie['ranking'],
                movie['title'],
                movie['rating'],
                movie['rating_count'],
                movie['release_year'],
                movie['genres'],
                movie['country'],
                movie['directors'],
                movie['casts'],
                movie['douban_url']
            ))
        
        conn.commit()
        conn.close()
    
    def get_movies(self):
        """从数据库获取电影数据"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM movies ORDER BY ranking')
        columns = [description[0] for description in cursor.description]
        movies = []
        
        for row in cursor.fetchall():
            movies.append(dict(zip(columns, row)))
        
        conn.close()
        return movies
