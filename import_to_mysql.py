# -*- coding: utf-8 -*-
"""
CSV 数据导入 MySQL 脚本
功能：读取 jobs.csv，批量插入到 MySQL 的 jobs 表
知识点：pymysql 连接数据库、参数化 SQL、批量插入 executemany

用法：python import_to_mysql.py
"""
import csv
import pymysql

# ========== 数据库连接配置 ==========
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "job_analysis",
    "charset": "utf8mb4",
}

CSV_FILE = "jobs.csv"


def main():
    # 1. 读取 CSV
    print("=" * 50)
    print("正在读取 jobs.csv ...")
    with open(CSV_FILE, encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        rows = [(row["城市"], row["岗位名称"], row["公司名称"], row["薪资"], row["地点"]) for row in reader]
    print(f"读取到 {len(rows)} 条数据")

    # 2. 连接数据库
    print("正在连接 MySQL ...")
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            # 3. 清空旧数据（防止重复导入，学习环境用 TRUNCATE）
            cursor.execute("TRUNCATE TABLE jobs")
            print("已清空 jobs 表旧数据")

            # 4. 批量插入（executemany 一次插入所有行）
            sql = """
                INSERT INTO jobs (city, job_name, company, salary_raw, location)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(sql, rows)
            print(f"已插入 {cursor.rowcount} 条数据")

        # 5. 提交事务
        conn.commit()
        print("事务已提交")

        # 6. 验证：查询总数
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM jobs")
            count = cursor.fetchone()[0]
            cursor.execute("SELECT city, job_name, salary_raw FROM jobs LIMIT 5")
            sample = cursor.fetchall()
        print(f"\n验证：jobs 表共有 {count} 条数据")
        print("前5条样例：")
        for row in sample:
            print("  ", row)

    finally:
        conn.close()
        print("\n数据库连接已关闭")


if __name__ == "__main__":
    main()
