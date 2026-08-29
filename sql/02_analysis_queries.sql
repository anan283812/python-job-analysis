-- ============================================================
-- 51job Python岗位数据 - SQL 分析查询
-- 知识点：DQL 查询（SELECT / GROUP BY / ORDER BY / 聚合函数）
-- 对应黑马 MySQL 基础篇：DQL-基础查询 ~ DQL-分组查询
-- ============================================================

USE job_analysis;

-- ============================================================
-- 分析1：岗位城市分布（GROUP BY + COUNT + ORDER BY）
-- 哪个城市 Python 岗位最多
-- ============================================================
SELECT
    city            AS 城市,
    COUNT(*)        AS 岗位数量
FROM jobs
GROUP BY city
ORDER BY 岗位数量 DESC;

-- ============================================================
-- 分析2：招聘公司排行 TOP10（GROUP BY + ORDER BY + LIMIT）
-- 哪些公司招聘 Python 岗位最多
-- ============================================================
SELECT
    company         AS 公司名称,
    COUNT(*)        AS 招聘数量
FROM jobs
GROUP BY company
ORDER BY 招聘数量 DESC
LIMIT 10;

-- ============================================================
-- 分析3：薪资区间分布
-- 用 CASE WHEN 把原始薪资文本归为"高/中/低"三档
-- 知识点：CASE WHEN（黑马 DQL 进阶内容，先了解）
-- ============================================================
SELECT
    CASE
        WHEN salary_raw LIKE '%万' AND CAST(SUBSTRING_INDEX(salary_raw, '-', -1) AS DECIMAL(4,1)) >= 2 THEN '高薪(2万以上)'
        WHEN salary_raw LIKE '%千' AND CAST(SUBSTRING_INDEX(salary_raw, '-', -1) AS DECIMAL(4,1)) < 10 THEN '低薪(1万以下)'
        ELSE '中等(1-2万)'
    END             AS 薪资档次,
    COUNT(*)        AS 岗位数量
FROM jobs
WHERE salary_raw NOT LIKE '%面议%'
GROUP BY 薪资档次
ORDER BY 岗位数量 DESC;

-- ============================================================
-- 分析4：岗位名称关键词分析（哪些方向最火）
-- 知识点：LIKE 模糊查询 + GROUP BY
-- ============================================================
SELECT
    CASE
        WHEN job_name LIKE '%算法%' OR job_name LIKE '%AI%' OR job_name LIKE '%智能%' THEN 'AI/算法'
        WHEN job_name LIKE '%爬虫%' OR job_name LIKE '%采集%' THEN '爬虫/采集'
        WHEN job_name LIKE '%大数据%' OR job_name LIKE '%数据%' THEN '大数据/数据'
        WHEN job_name LIKE '%后端%' OR job_name LIKE '%服务%' OR job_name LIKE '%开发%' THEN '开发'
        WHEN job_name LIKE '%测试%' THEN '测试'
        WHEN job_name LIKE '%运维%' THEN '运维'
        ELSE '其他'
    END             AS 岗位方向,
    COUNT(*)        AS 岗位数量
FROM jobs
GROUP BY 岗位方向
ORDER BY 岗位数量 DESC;

-- ============================================================
-- 分析5：城市 + 公司维度（每个城市招聘最多的公司）
-- 知识点：多表/子查询（先了解，黑马 DQL 进阶内容）
-- ============================================================
SELECT city, company, cnt AS 招聘数量
FROM (
    SELECT
        city,
        company,
        COUNT(*) AS cnt,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY COUNT(*) DESC) AS rn
    FROM jobs
    GROUP BY city, company
) t
WHERE rn = 1
ORDER BY 招聘数量 DESC;

-- ============================================================
-- 面试常问：数据质量检查
-- ============================================================
-- 有多少条"薪资面议"（无薪资数据）
SELECT COUNT(*) AS 面议数量 FROM jobs WHERE salary_raw LIKE '%面议%';
-- 公司名重复检查
SELECT COUNT(*) - COUNT(DISTINCT company) AS 重复公司名数量 FROM jobs;
