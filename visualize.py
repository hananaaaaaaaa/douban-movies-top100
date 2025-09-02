import matplotlib.pyplot as plt
from database import DatabaseManager

def visualize_data():
    """生成可视化图表"""
    db = DatabaseManager()
    movies = db.get_movies()
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 1. 评分分布
    ratings = [m['rating'] for m in movies]
    plt.figure(figsize=(10, 6))
    plt.hist(ratings, bins=10, edgecolor='black', alpha=0.7)
    plt.title('电影评分分布')
    plt.xlabel('评分')
    plt.ylabel('数量')
    plt.savefig('rating_distribution.png')
    plt.close()
    
    # 2. 年份分布
    years = [m['release_year'] for m in movies if m['release_year']]
    year_counts = {}
    for year in years:
        year_counts[year] = year_counts.get(year, 0) + 1
    
    plt.figure(figsize=(12, 6))
    plt.bar(year_counts.keys(), year_counts.values())
    plt.title('电影年份分布')
    plt.xlabel('年份')
    plt.ylabel('数量')
    plt.xticks(rotation=45)
    plt.savefig('year_distribution.png')
    plt.close()
    
    # 3. 评分vs热度
    ratings = [m['rating'] for m in movies]
    counts = [m['rating_count'] for m in movies]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(ratings, counts, alpha=0.6)
    plt.title('评分 vs 评分人数')
    plt.xlabel('评分')
    plt.ylabel('评分人数')
    plt.savefig('rating_vs_popularity.png')
    plt.close()
    
    print("生成3个可视化图表: rating_distribution.png, year_distribution.png, rating_vs_popularity.png")

if __name__ == "__main__":
    visualize_data()
