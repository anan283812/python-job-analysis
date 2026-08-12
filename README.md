51job Python岗位数据分析项目
项目简介
本项目通过爬取前程无忧（51job）招聘网站的 Python 相关岗位数据，对多个城市的 Python 岗位进行薪资分析、城市分布分析和企业招聘需求分析，并通过可视化图表展示分析结果。

项目功能
数据采集：使用 Selenium 自动化爬取 51job 上 6 个城市（北京、上海、深圳、广州、杭州、合肥）的 Python 岗位信息，包括岗位名称、公司名称、薪资、地点
数据清洗：使用 pandas 对原始数据进行清洗，解析薪资字符串（如"7-9千·13薪"），转换为数值型薪资数据
数据分析：统计岗位城市分布、薪资区间分布、企业招聘数量排行、各城市平均薪资对比
数据可视化：使用 matplotlib 生成综合分析图表和薪资分布直方图
技术栈
模块	技术
数据采集	Selenium + ChromeDriver
数据存储	CSV
数据清洗	pandas + re（正则表达式）
数据分析	pandas
数据可视化	matplotlib
项目结构
TEXT
复制
├── 1.py                # 爬虫脚本，采集51job岗位数据
├── analysis.py         # 数据分析与可视化脚本
├── jobs.csv            # 爬取的岗位数据
├── jobs_analysis.png   # 综合分析图表（4合1）
├── salary_distribution.png  # 薪资分布直方图
├── chromedriver.exe    # Chrome浏览器驱动
└── README.md           # 项目说明文档
运行方式
1. 安装依赖
BASH
复制
pip install selenium pandas matplotlib
2. 爬取数据
BASH
复制
python 1.py
爬虫会自动打开 Chrome 浏览器，依次爬取 6 个城市的 Python 岗位数据（每个城市 5 页），爬取完成后自动关闭浏览器，数据保存到 jobs.csv。

3. 数据分析与可视化
BASH
复制
python analysis.py
脚本会自动读取 jobs.csv，进行数据清洗和分析，生成两张图表：

jobs_analysis.png：综合分析图表（城市分布、薪资区间、公司排行、城市薪资对比）
salary_distribution.png：薪资分布直方图
分析维度
岗位城市分布：统计各城市的 Python 岗位数量，了解需求集中地
薪资区间分布：将薪资划分为 6 个区间（5K以下、5K-10K、10K-15K、15K-20K、20K-30K、30K以上），分析市场薪资水平
企业招聘排行：统计招聘数量最多的企业 TOP10
城市薪资对比：对比各城市的平均薪资水平
数据说明
数据来源：前程无忧（51job）招聘网站
采集范围：北京、上海、深圳、广州、杭州、合肥
采集字段：城市、岗位名称、公司名称、薪资、地点
薪资解析：支持"7-9千·13薪"、"9千-1.5万"、"1-2万"等多种格式