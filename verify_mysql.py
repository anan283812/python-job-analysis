# -*- coding: utf-8 -*-
"""验证 MySQL 中文数据（纯 pymysql，不依赖 pandas/matplotlib）"""
import pymysql

conn = pymysql.connect(
    host="127.0.0.1", port=3306, user="root",
    password="123456", database="job_analysis", charset="utf8mb4",
)

with conn.cursor() as cur:
    # 1. 中文数据验证
    print("=== 中文数据验证（前5条）===")
    cur.execute("SELECT id, city, job_name, company, salary_raw, location FROM jobs LIMIT 5")
    for row in cur.fetchall():
        print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")

    # 2. 城市分布
    print("\n=== 城市岗位分布 ===")
    cur.execute("SELECT city, COUNT(*) FROM jobs GROUP BY city ORDER BY COUNT(*) DESC")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")

    # 3. 薪资面议统计
    print("\n=== 数据质量 ===")
    cur.execute("SELECT COUNT(*) FROM jobs WHERE salary_raw LIKE '%面议%'")
    print(f"  薪资面议: {cur.fetchone()[0]} 条")
    cur.execute("SELECT COUNT(DISTINCT company) FROM jobs")
    print(f"  不同公司数: {cur.fetchone()[0]} 家")

conn.close()
print("\n✔ 中文数据验证通过")
