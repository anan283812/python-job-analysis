# 51job Python岗位数据分析项目

## 项目简介

通过爬取前程无忧（51job）招聘网站的 Python 相关岗位数据，对多个城市的 Python 岗位进行薪资分析、城市分布分析和企业招聘需求分析，并通过可视化图表展示分析结果。

## 项目功能

- **数据采集**：使用 Selenium 自动化爬取 51job 上 5 个城市（北京、上海、深圳、广州、杭州）的 Python 岗位信息，包括岗位名称、公司名称、薪资、地点
- **数据存储**：数据先保存为 CSV，再设计 MySQL 表结构（DDL）建库建表，通过 pymysql 批量导入数据库
- **数据分析**：使用 SQL（DQL）编写分组聚合查询，统计岗位城市分布、薪资区间分布、企业招聘数量排行、岗位方向分布
- **数据可视化**：使用 matplotlib 生成综合分析图表和薪资分布直方图

## 技术栈

| 模块 | 技术 |
|---|---|
| 数据采集 | Selenium + ChromeDriver |
| 数据存储 | MySQL 8.0 + pymysql（含 CSV 中间格式） |
| 数据库设计 | DDL（CREATE DATABASE / CREATE TABLE / 约束 / 字段类型） |
| 数据查询 | DQL（SELECT / GROUP BY / ORDER BY / 聚合函数 / CASE WHEN） |
| 数据清洗 | pandas + re（正则表达式） |
| 数据可视化 | matplotlib |

## 项目结构

```
├── 1.py                   # 爬虫脚本，采集51job岗位数据
├── analysis.py            # pandas 数据分析与可视化脚本
├── import_to_mysql.py     # CSV 数据导入 MySQL 脚本（pymysql）
├── verify_mysql.py        # MySQL 中文数据验证脚本
├── sql/
│   ├── 01_create_tables.sql    # DDL 建库建表脚本
│   └── 02_analysis_queries.sql # SQL 分析查询（DQL）
├── jobs.csv               # 爬取的岗位数据（460条）
├── jobs_analysis.png      # 综合分析图表（4合1）
├── salary_distribution.png # 薪资分布直方图
├── chromedriver.exe       # Chrome浏览器驱动
└── README.md              # 项目说明文档
```

## 运行方式

### 1. 安装依赖

```bash
pip install selenium pandas matplotlib pymysql
```

### 2. 爬取数据

```bash
python 1.py
```

爬虫会自动打开 Chrome 浏览器，依次爬取 5 个城市的 Python 岗位数据（每个城市最多 5 页），爬取完成后自动关闭浏览器，数据保存到 jobs.csv。

### 3. 导入 MySQL

先执行 DDL 建库建表（需先启动 MySQL 服务）：

```sql
source sql/01_create_tables.sql;
```

再运行导入脚本：

```bash
python import_to_mysql.py
```

脚本会读取 jobs.csv，通过 pymysql 批量插入 460 条数据到 MySQL 的 job_analysis.jobs 表。

### 4. SQL 数据分析

```sql
source sql/02_analysis_queries.sql;
```

包含以下分析维度：
- 岗位城市分布（GROUP BY + COUNT）
- 招聘公司排行 TOP10
- 薪资区间分布（CASE WHEN 分级）
- 岗位方向分析（LIKE 模糊匹配分类）
- 各城市招聘最多公司（子查询 + 窗口函数）

### 5. 数据可视化

```bash
python analysis.py
```

脚本读取 jobs.csv，进行数据清洗和分析，生成两张图表。

## 分析结果（基于 460 条数据）

- 城市分布：北京/上海/深圳各 100 条，广州/杭州各 80 条
- 薪资档次：中等(1-2万) 304 条，高薪(2万+) 146 条，低薪(1万以下) 10 条
- 岗位方向：开发 268，爬虫/采集 83，AI/算法 63
- 不同公司：98 家

## 数据库设计

### 表结构（jobs 表）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT UNSIGNED AUTO_INCREMENT | 主键 |
| city | VARCHAR(20) | 城市 |
| job_name | VARCHAR(100) | 岗位名称 |
| company | VARCHAR(100) | 公司名称 |
| salary_raw | VARCHAR(50) | 原始薪资文本（如"1.5-2万"） |
| location | VARCHAR(100) | 工作地点 |
| created_at | TIMESTAMP | 插入时间 |

### 设计说明

- 薪资存原始文本而非解析后的数值，便于后续用 SQL 灵活处理
- 所有字段 NOT NULL，主键自增
- 使用 utf8mb4 字符集支持中文
- InnoDB 存储引擎支持事务

## 数据说明

- 数据来源：前程无忧（51job）招聘网站
- 采集范围：北京、上海、深圳、广州、杭州（共 460 条）
- 采集字段：城市、岗位名称、公司名称、薪资、地点
- 薪资解析：支持"7-9千·13薪"、"9千-1.5万"、"1-2万"等多种格式
