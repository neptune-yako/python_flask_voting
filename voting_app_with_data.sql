-- 创建数据库
CREATE DATABASE IF NOT EXISTS voting_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE voting_app;

-- 创建用户表
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL
);

-- 创建投票表
CREATE TABLE IF NOT EXISTS poll (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    unique_share_id VARCHAR(36) NOT NULL UNIQUE,
    creation_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 创建选项表
CREATE TABLE IF NOT EXISTS `option` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    vote_count INT DEFAULT 0,
    poll_id INT NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES poll(id) ON DELETE CASCADE
);

-- 创建投票记录表
CREATE TABLE IF NOT EXISTS vote_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    poll_id INT NOT NULL,
    option_id INT NOT NULL,
    user_id INT NULL,
    voter_ip_hash VARCHAR(64) NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (poll_id) REFERENCES poll(id) ON DELETE CASCADE,
    FOREIGN KEY (option_id) REFERENCES `option`(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL,
    UNIQUE KEY `_poll_user_uc` (poll_id, user_id)
);

-- 插入测试用户数据
-- 密码均为 'password'，使用Werkzeug生成的哈希值
INSERT INTO user (username, password_hash) VALUES 
('admin', 'pbkdf2:sha256:260000$7tGrwEZzRpYjKMQm$d778ef55e78a580411c3af2f98f92786e5b02c0fdafc1b1b54764cc3c6536d34'),
('user1', 'pbkdf2:sha256:260000$7tGrwEZzRpYjKMQm$d778ef55e78a580411c3af2f98f92786e5b02c0fdafc1b1b54764cc3c6536d34'),
('user2', 'pbkdf2:sha256:260000$7tGrwEZzRpYjKMQm$d778ef55e78a580411c3af2f98f92786e5b02c0fdafc1b1b54764cc3c6536d34'),
('test_user', 'pbkdf2:sha256:260000$7tGrwEZzRpYjKMQm$d778ef55e78a580411c3af2f98f92786e5b02c0fdafc1b1b54764cc3c6536d34');

-- 插入测试投票数据
INSERT INTO poll (question, unique_share_id, user_id) VALUES 
('你最喜欢的编程语言是什么？', 'abc123def456ghi789', 1),
('你最常用的操作系统是？', 'jkl012mno345pqr678', 1),
('你更喜欢在哪里工作？', 'stu901vwx234yz5678', 2),
('你平时最常用的交通工具是？', 'a1b2c3d4e5f6g7h8i9', 3),
('你最喜欢的休闲活动是什么？', 'j0k1l2m3n4o5p6q7r8', 4);

-- 插入测试选项数据
-- 投票1的选项
INSERT INTO `option` (text, poll_id) VALUES 
('Python', 1),
('JavaScript', 1),
('Java', 1),
('C++', 1),
('Go', 1);

-- 投票2的选项
INSERT INTO `option` (text, poll_id) VALUES 
('Windows', 2),
('macOS', 2),
('Linux', 2),
('其他', 2);

-- 投票3的选项
INSERT INTO `option` (text, poll_id) VALUES 
('办公室', 3),
('家里', 3),
('咖啡厅', 3),
('共享工作空间', 3);

-- 投票4的选项
INSERT INTO `option` (text, poll_id) VALUES 
('公共交通', 4),
('私家车', 4),
('自行车', 4),
('步行', 4),
('网约车', 4);

-- 投票5的选项
INSERT INTO `option` (text, poll_id) VALUES 
('看电影', 5),
('阅读', 5),
('运动', 5),
('游戏', 5),
('旅行', 5);

-- 更新选项的投票计数
-- 投票1的投票数据
UPDATE `option` SET vote_count = 15 WHERE id = 1; -- Python
UPDATE `option` SET vote_count = 8 WHERE id = 2;  -- JavaScript
UPDATE `option` SET vote_count = 6 WHERE id = 3;  -- Java
UPDATE `option` SET vote_count = 4 WHERE id = 4;  -- C++
UPDATE `option` SET vote_count = 3 WHERE id = 5;  -- Go

-- 投票2的投票数据
UPDATE `option` SET vote_count = 12 WHERE id = 6; -- Windows
UPDATE `option` SET vote_count = 9 WHERE id = 7;  -- macOS
UPDATE `option` SET vote_count = 10 WHERE id = 8; -- Linux
UPDATE `option` SET vote_count = 1 WHERE id = 9;  -- 其他

-- 投票3的投票数据
UPDATE `option` SET vote_count = 5 WHERE id = 10; -- 办公室
UPDATE `option` SET vote_count = 18 WHERE id = 11; -- 家里
UPDATE `option` SET vote_count = 7 WHERE id = 12; -- 咖啡厅
UPDATE `option` SET vote_count = 3 WHERE id = 13; -- 共享工作空间

-- 投票4的投票数据
UPDATE `option` SET vote_count = 8 WHERE id = 14; -- 公共交通
UPDATE `option` SET vote_count = 14 WHERE id = 15; -- 私家车
UPDATE `option` SET vote_count = 6 WHERE id = 16; -- 自行车
UPDATE `option` SET vote_count = 4 WHERE id = 17; -- 步行
UPDATE `option` SET vote_count = 5 WHERE id = 18; -- 网约车

-- 投票5的投票数据
UPDATE `option` SET vote_count = 12 WHERE id = 19; -- 看电影
UPDATE `option` SET vote_count = 8 WHERE id = 20;  -- 阅读
UPDATE `option` SET vote_count = 10 WHERE id = 21; -- 运动
UPDATE `option` SET vote_count = 15 WHERE id = 22; -- 游戏
UPDATE `option` SET vote_count = 20 WHERE id = 23; -- 旅行

-- 插入一些投票记录
-- 为简化，只插入部分记录，实际应与vote_count一致
INSERT INTO vote_record (poll_id, option_id, user_id, voter_ip_hash) VALUES
(1, 1, 2, NULL),  -- user1 投票给 Python
(1, 2, 3, NULL),  -- user2 投票给 JavaScript
(1, 1, 4, NULL),  -- test_user 投票给 Python
(2, 8, 2, NULL),  -- user1 投票给 Linux
(2, 6, 3, NULL),  -- user2 投票给 Windows
(3, 11, 1, NULL), -- admin 投票给 家里
(3, 10, 3, NULL), -- user2 投票给 办公室
(4, 15, 1, NULL), -- admin 投票给 私家车
(4, 14, 2, NULL), -- user1 投票给 公共交通
(5, 23, 1, NULL), -- admin 投票给 旅行
(5, 22, 2, NULL); -- user1 投票给 游戏

-- 添加一些匿名用户的投票记录
INSERT INTO vote_record (poll_id, option_id, user_id, voter_ip_hash) VALUES
(1, 1, NULL, 'f86e2423f9e2dfc0c3b1e9385b9c8289f9a65e3f156e9bd0f82a17315a4ce8dc'),
(1, 3, NULL, 'a3d8e36eb57411894e572c2f7ad2a8b86d2c7d1ca9860e7b7aad4b6c4f72b08e'),
(2, 7, NULL, 'b8c37e33defde51cf91e1e03e51657da2d45552dc10a6e5d8e4b1494c6d5c863'),
(3, 11, NULL, 'c5f8422c7254acdb5d3c5dba9077ba9b1526114f5c0a5c0e4da0fe1a5e34b05e'),
(4, 15, NULL, 'd7e37e33defde51cf91e1e03e51657da2d45552dc10a6e5d8e4b1494c6d5c863'),
(5, 23, NULL, 'e8c422c7254acdb5d3c5dba9077ba9b1526114f5c0a5c0e4da0fe1a5e34b05e'); 