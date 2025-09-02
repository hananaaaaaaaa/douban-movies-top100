import requests
from bs4 import BeautifulSoup
import re
import time
from database import DatabaseManager

class DoubanSpider:
    def __init__(self):
        self.base_url = "https://movie.douban.com/top250"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.db = DatabaseManager()
    
    def get_html(self, url):
        """获取网页内容"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except:
            return None
    
    def parse_movie(self, item, ranking):
        """解析单个电影信息"""
        # 标题和链接
        title_elem = item.find('span', class_='title')
        title = title_elem.text.strip() if title_elem else ""
        link = item.find('a')['href'] if item.find('a') else ""
        
        # 评分
        rating_elem = item.find('span', class_='rating_num')
        rating = float(rating_elem.text.strip()) if rating_elem else 0.0
        
        # 评分人数
        rating_count_elem = item.find('div', class_='star').find_all('span')[-1]
        rating_count_text = rating_count_elem.text.replace('人评价', '').replace(',', '').strip()
        rating_count = int(rating_count_text) if rating_count_text else 0
        
        # 其他信息
        info_text = item.find('div', class_='bd').find('p', class_='').text.strip()
        info_lines = info_text.split('\n')
        
        # 导演和演员
        director_cast = info_lines[0].strip() if info_lines else ""
        directors, casts = self.parse_people(director_cast)
        
        # 年份、国家、类型
        year, country, genres = None, "", ""
        if len(info_lines) > 1:
            detail_info = info_lines[1].strip()
            year, country, genres = self.parse_details(detail_info)
        
        return {
            'ranking': ranking,
            'title': title,
            'rating': rating,
            'rating_count': rating_count,
            'release_year': year,
            'country': country,
            'genres': genres,
            'directors': directors,
            'casts': casts,
            'douban_url': link
        }
    
    def parse_people(self, text):
        """解析导演和演员信息"""
        directors, casts = "", ""
        if '导演:' in text:
            if '主演:' in text:
                directors = text.split('导演:')[1].split('主演:')[0].strip()
                casts = text.split('主演:')[1].strip()
            else:
                directors = text.split('导演:')[1].strip()
        return directors, casts
    
    def parse_details(self, text):
        """解析年份、国家、类型信息"""
        year, country, genres = None, "", ""
        
        # 提取年份
        year_match = re.search(r'(\d{4})', text)
        if year_match:
            year = int(year_match.group(1))
        
        # 分割信息
        parts = re.split(r'\s*/\s*', text)
        if len(parts) >= 3:
            country = parts[1].strip()
            genres = parts[2].strip()
        elif len(parts) == 2:
            country = parts[1].strip()
        
        return year, country, genres
    
    def run(self):
        """运行爬虫"""
        movies = []
        
        for start in range(0, 100, 25):
            url = f"{self.base_url}?start={start}"
            html = self.get_html(url)
            
            if not html:
                continue
                
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find_all('div', class_='item')
            
            for item in items:
                if len(movies) >= 100:
                    break
                    
                movie = self.parse_movie(item, len(movies) + 1)
                movies.append(movie)
                print(f"爬取: #{movie['ranking']} {movie['title']}")
            
            time.sleep(2)
        
        # 保存到数据库
        self.db.save_movies(movies)
        print(f"完成! 共爬取 {len(movies)} 部电影")

if __name__ == "__main__":
    spider = DoubanSpider()
    spider.run()
