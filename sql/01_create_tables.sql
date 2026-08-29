-- ============================================================
-- 51job Python岗位数据 - DDL 建库建表脚本
-- 知识点：CREATE DATABASE / CREATE TABLE / 字段类型 / 约束
-- 对应黑马 MySQL 基础篇：DDL-数据库操作、DDL-表操作
-- ============================================================

-- 第1步：建库（若不存在则创建）
-- DEFAULT CHARACTER SET utf8mb4：支持中文和 emoji
-- DEFAULT COLLATE utf8mb4_unicode_ci：排序规则（ci = case insensitive 不区分大小写）
CREATE DATABASE IF NOT EXISTS job_analysis
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

-- 切换到目标库
USE job_analysis;

-- 第2步：建表（若不存在则创建）
-- 字段设计说明：
--   id        主键，自增，无符号整数
--   city      城市名，最长的"哈尔滨"等 3-4 字，VARCHAR(20) 足够
--   job_name  岗位名称，如"高级python开发工程师"，VARCHAR(100)
--   company   公司名称，最长的公司名可能 30-40 字，VARCHAR(100)
--   salary_raw 原始薪资文本，如"1.5-2万""6-9千""薪资面议"，VARCHAR(50)
--   location  工作地点，如"北京·丰台区"，VARCHAR(100)
--   created_at 记录插入时间，默认当前时间（DEFAULT CURRENT_TIMESTAMP）
--
-- 约束：
--   NOT NULL        非空约束（5个核心字段都有值）
--   AUTO_INCREMENT  自增
--   PRIMARY KEY     主键约束（唯一标识一行）
CREATE TABLE IF NOT EXISTS jobs (
  id         INT UNSIGNED  NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  city       VARCHAR(20)   NOT NULL COMMENT '城市',
  job_name   VARCHAR(100)  NOT NULL COMMENT '岗位名称',
  company    VARCHAR(100)  NOT NULL COMMENT '公司名称',
  salary_raw VARCHAR(50)   NOT NULL COMMENT '原始薪资文本',
  location   VARCHAR(100)  NOT NULL COMMENT '工作地点',
  created_at TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '51job爬取Python岗位表';

-- 第3步：验证
-- SHOW DATABASES;              -- 查看所有数据库
-- SHOW TABLES;                 -- 查看当前库的表
-- DESC jobs;                   -- 查看表结构（DESCRIBE 简写）
-- SHOW CREATE TABLE jobs;      -- 查看建表语句

-- 第4步：注意
-- 如果表结构设计错了要改，用 ALTER TABLE：
--   ALTER TABLE jobs ADD COLUMN xxx VARCHAR(50) COMMENT '新增字段';
--   ALTER TABLE jobs MODIFY COLUMN salary_raw VARCHAR(80) COMMENT '改字段长度';
--   ALTER TABLE jobs DROP COLUMN xxx;
--   DROP TABLE jobs;           -- 删表（慎用，会连数据一起删）
