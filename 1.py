import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# 要爬取的城市列表
cities = {
    "010000": "北京",
    "020000": "上海",
    "040000": "深圳",
    "030200": "广州",
    "080200": "杭州",
    "150200": "合肥",
}

with open("jobs.csv", "w", encoding="UTF-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["城市", "岗位名称", "公司名称", "薪资", "地点"])

    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    for city_code, city_name in cities.items():
        for page in range(1, 6):
            if page == 1:
                url = f"https://we.51job.com/pc/search?keyword=Python&jobArea={city_code}"
            else:
                url = f"https://we.51job.com/pc/search?keyword=Python&jobArea={city_code}&currentPage={page}"

            driver.get(url)
            time.sleep(3)

            jobs = driver.find_elements(By.CSS_SELECTOR, ".joblist-item-job")
            print(f"{city_name} 第{page}页，找到{len(jobs)}个岗位")

            for i, job in enumerate(jobs):
                title = job.find_element(By.CSS_SELECTOR, ".jname").get_attribute("title")
                company = job.find_element(By.CSS_SELECTOR, ".cname").get_attribute("title")
                salary_list = job.find_elements(By.CSS_SELECTOR, ".sal")
                salary = salary_list[0].text if salary_list else "薪资面议"
                location_list = job.find_elements(By.CSS_SELECTOR, ".area")
                location = location_list[0].text if location_list else "未知"
                writer.writerow([city_name, title, company, salary, location])
                print(f"  {city_name} 第{page}页 岗位{i+1}: {title}, 公司:{company}, 薪资:{salary}")

    print("爬取完成，正在关闭浏览器...")
    driver.quit()

print("数据已保存到 jobs.csv")
# -*- coding: utf-8 -*-
"""
51job Python岗位数据分析
功能：读取爬取的数据，进行薪资分析、城市分布、公司排行，生成可视化图表
"""
import csv
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体，防止中文乱码
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False


# ========== 第1步：读取数据 ==========
print("=" * 50)
print("正在读取数据...")
print("=" * 50)

df = pd.read_csv("jobs.csv", encoding="UTF-8")
# 删除岗位名称为空的行（空行/无效数据）
df = df.dropna(subset=["岗位名称"])
print(f"总共读取到 {len(df)} 条有效岗位数据\n")
print(df.head())  # 打印前5行看看
print()


# ========== 第2步：数据清洗 - 解析薪资 ==========
def parse_salary(salary_str):
    """
    解析薪资字符串，返回平均薪资（元/月）
    支持的格式：
      "7-9千·13薪" → 8000
      "9千-1.5万" → 12000
      "1-2万" → 15000
      "8千-1.2万" → 10000
      "面议" → None
    """
    if pd.isna(salary_str) or salary_str == "薪资面议":
        return None

    salary_str = str(salary_str).strip()

    # 去掉 ·13薪 这种后缀，只保留薪资范围部分
    salary_str = salary_str.split("·")[0]

    # 格式1: "7-9千" 或 "7.5-9千"（单位在后面，只出现一次）
    pattern1 = r'^([\d.]+)-([\d.]+)([万千])'
    match1 = re.match(pattern1, salary_str)
    if match1:
        low = float(match1.group(1))
        high = float(match1.group(2))
        unit = match1.group(3)
        if unit == "万":
            low *= 10000
            high *= 10000
        elif unit == "千":
            low *= 1000
            high *= 1000
        return (low + high) / 2

    # 格式2: "9千-1.5万"（每个数字后面都有单位）
    pattern2 = r'^([\d.]+)([万千])-([\d.]+)([万千])'
    match2 = re.match(pattern2, salary_str)
    if match2:
        low = float(match2.group(1))
        unit1 = match2.group(2)
        high = float(match2.group(3))
        unit2 = match2.group(4)
        if unit1 == "万":
            low *= 10000
        elif unit1 == "千":
            low *= 1000
        if unit2 == "万":
            high *= 10000
        elif unit2 == "千":
            high *= 1000
        return (low + high) / 2

    # 格式3: "1.5万" 单独一个值
    pattern3 = r'^([\d.]+)([万千])$'
    match3 = re.match(pattern3, salary_str)
    if match3:
        val = float(match3.group(1))
        unit = match3.group(2)
        if unit == "万":
            val *= 10000
        elif unit == "千":
            val *= 1000
        return val

    return None


print("=" * 50)
print("正在解析薪资数据...")
print("=" * 50)

df["平均薪资"] = df["薪资"].apply(parse_salary)

# 统计有多少有效薪资数据
valid_salary = df["平均薪资"].notna().sum()
print(f"有效薪资数据：{valid_salary} 条，薪资面议或无法解析：{len(df) - valid_salary} 条\n")


# ========== 第3步：提取城市 ==========
def extract_city(location):
    """从地点中提取城市名，例如 '合肥·高新区' → '合肥'"""
    if pd.isna(location):
        return "未知"
    location = str(location).strip()
    # 按·分割，取第一部分就是城市
    city = location.split("·")[0]
    return city


df["城市"] = df["地点"].apply(extract_city)


# ========== 第4步：数据分析 ==========
print("=" * 50)
print("数据分析结果")
print("=" * 50)

# 分析1：城市分布
print("\n【岗位城市分布 TOP10】")
city_count = df["城市"].value_counts().head(10)
print(city_count)
print()

# 分析2：薪资统计
print("【薪资统计】")
salary_data = df[df["平均薪资"].notna()]["平均薪资"]
if len(salary_data) > 0:
    print(f"平均薪资：{salary_data.mean():.0f} 元/月")
    print(f"中位数：{salary_data.median():.0f} 元/月")
    print(f"最高薪资：{salary_data.max():.0f} 元/月")
    print(f"最低薪资：{salary_data.min():.0f} 元/月")
print()

# 分析3：薪资区间分布
print("【薪资区间分布】")
if len(salary_data) > 0:
    bins = [0, 5000, 10000, 15000, 20000, 30000, 50000]
    labels = ["5K以下", "5K-10K", "10K-15K", "15K-20K", "20K-30K", "30K以上"]
    df.loc[df["平均薪资"].notna(), "薪资区间"] = pd.cut(
        df.loc[df["平均薪资"].notna(), "平均薪资"], bins=bins, labels=labels
    )
    salary_range = df["薪资区间"].value_counts().sort_index()
    print(salary_range)
print()

# 分析4：招聘数量最多的公司
print("【招聘数量最多的公司 TOP10】")
company_count = df["公司名称"].value_counts().head(10)
print(company_count)
print()


# ========== 第5步：可视化图表 ==========
print("=" * 50)
print("正在生成图表...")
print("=" * 50)

# 创建一个 2x2 的画布
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("51job Python岗位数据分析", fontsize=20, fontweight="bold")

# 图1：城市分布柱状图
axes[0, 0].bar(city_count.index, city_count.values, color="#4A90D9")
axes[0, 0].set_title("岗位城市分布 TOP10", fontsize=14)
axes[0, 0].set_xlabel("城市")
axes[0, 0].set_ylabel("岗位数量")
axes[0, 0].tick_params(axis='x', rotation=45)
# 在柱子上标数字
for i, v in enumerate(city_count.values):
    axes[0, 0].text(i, v + 0.5, str(v), ha='center', fontsize=10)

# 图2：薪资区间分布饼图
if len(salary_data) > 0:
    axes[0, 1].pie(salary_range.values, labels=salary_range.index, autopct='%1.1f%%',
                   colors=["#5B9BD5", "#70AD47", "#FFC000", "#ED7D31", "#FF0000", "#7030A0"])
    axes[0, 1].set_title("薪资区间分布", fontsize=14)

# 图3：招聘数量最多的公司
axes[1, 0].barh(company_count.index[::-1], company_count.values[::-1], color="#70AD47")
axes[1, 0].set_title("招聘数量最多的公司 TOP10", fontsize=14)
axes[1, 0].set_xlabel("岗位数量")

# 图4：各城市平均薪资
if len(salary_data) > 0:
    city_salary = df[df["平均薪资"].notna()].groupby("城市")["平均薪资"].mean().sort_values(ascending=False).head(10)
    axes[1, 1].bar(city_salary.index, city_salary.values, color="#ED7D31")
    axes[1, 1].set_title("各城市平均薪资 TOP10", fontsize=14)
    axes[1, 1].set_xlabel("城市")
    axes[1, 1].set_ylabel("平均薪资（元/月）")
    axes[1, 1].tick_params(axis='x', rotation=45)
    for i, v in enumerate(city_salary.values):
        axes[1, 1].text(i, v + 500, f"{v:.0f}", ha='center', fontsize=9)

plt.tight_layout()
plt.savefig("jobs_analysis.png", dpi=150, bbox_inches="tight")
print("图表已保存为 jobs_analysis.png")

# 单独画一个薪资直方图
plt.figure(figsize=(10, 6))
if len(salary_data) > 0:
    plt.hist(salary_data, bins=20, color="#4A90D9", edgecolor="white")
    plt.title("Python岗位薪资分布直方图", fontsize=16)
    plt.xlabel("薪资（元/月）")
    plt.ylabel("岗位数量")
    plt.axvline(salary_data.mean(), color="red", linestyle="--", label=f"平均薪资: {salary_data.mean():.0f}")
    plt.axvline(salary_data.median(), color="green", linestyle="--", label=f"中位数: {salary_data.median():.0f}")
    plt.legend()
    plt.tight_layout()
    plt.savefig("salary_distribution.png", dpi=150, bbox_inches="tight")
    print("薪资分布图已保存为 salary_distribution.png")

print("\n分析完成！")
print("生成的文件：")
print("  1. jobs_analysis.png - 综合分析图表（4合1）")
print("  2. salary_distribution.png - 薪资分布直方图")









