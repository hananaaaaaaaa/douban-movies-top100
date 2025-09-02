

DB_SCHEMA = {
    "table_name": "douban_movies_top100",
    "fields": [
        {"name": "id", "type": "INTEGER", "primary_key": True, "autoincrement": True},
        {"name": "ranking", "type": "INTEGER", "not_null": True, "description": "排名 (1-100)"},
        {"name": "title", "type": "VARCHAR(255)", "not_null": True, "description": "电影名称"},
        {"name": "rating", "type": "DECIMAL(2,1)", "not_null": True, "description": "评分 (0.0-10.0)"},
        {"name": "rating_count", "type": "INTEGER", "description": "评分人数"},
        {"name": "release_year", "type": "INTEGER", "description": "上映年份"},
        {"name": "genres", "type": "VARCHAR(100)", "description": "类型 (多个用逗号分隔)"},
        {"name": "country", "type": "VARCHAR(100)", "description": "国家/地区"},
        {"name": "directors", "type": "VARCHAR(255)", "description": "导演 (多个用逗号分隔)"},
        {"name": "casts", "type": "VARCHAR(500)", "description": "主演 (多个用逗号分隔)"},
        {"name": "douban_url", "type": "VARCHAR(500)", "description": "豆瓣链接"},
        {"name": "created_time", "type": "DATETIME", "default": "CURRENT_TIMESTAMP", "description": "创建时间"}
    ],
    "visualization_support": {
        "rating_distribution": ["rating"],
        "year_distribution": ["release_year"],
        "country_distribution": ["country"],
        "genre_distribution": ["genres"],
        "rating_vs_popularity": ["rating", "rating_count"],
        "director_analysis": ["directors", "rating"],
        "actor_analysis": ["casts", "rating"]
    }
}

def get_create_table_sql():
    """生成创建表的SQL语句"""
    fields_sql = []
    for field in DB_SCHEMA["fields"]:
        field_sql = f"{field['name']} {field['type']}"
        if field.get('primary_key'):
            field_sql += " PRIMARY KEY"
        if field.get('autoincrement'):
            field_sql += " AUTOINCREMENT"
        if field.get('not_null'):
            field_sql += " NOT NULL"
        if field.get('default'):
            field_sql += f" DEFAULT {field['default']}"
        fields_sql.append(field_sql)
    
    return f"CREATE TABLE IF NOT EXISTS {DB_SCHEMA['table_name']} (\n    " + ",\n    ".join(fields_sql) + "\n)"

if __name__ == "__main__":
    print("豆瓣电影Top100数据库设计")
    print("=" * 50)
    print(get_create_table_sql())
    print("\n支持的视觉化分析:")
    for viz_type, fields in DB_SCHEMA["visualization_support"].items():
        print(f"- {viz_type}: {', '.join(fields)}")
