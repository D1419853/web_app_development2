-- 追劇推薦系統資料庫 Schema (SQLite)

-- 1. 劇集表
CREATE TABLE IF NOT EXISTS drama (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    rating REAL DEFAULT 0.0,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 演員表
CREATE TABLE IF NOT EXISTS actor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image_url TEXT
);

-- 3. 劇集-演員關聯表 (多對多)
CREATE TABLE IF NOT EXISTS drama_actor (
    drama_id INTEGER NOT NULL,
    actor_id INTEGER NOT NULL,
    PRIMARY KEY (drama_id, actor_id),
    FOREIGN KEY (drama_id) REFERENCES drama(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actor(id) ON DELETE CASCADE
);

-- 4. 個人收藏清單
CREATE TABLE IF NOT EXISTS collection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drama_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drama_id) REFERENCES drama(id) ON DELETE CASCADE
);

-- 預填一些範例資料
INSERT INTO drama (title, description, category, rating, image_url) VALUES 
('黑暗榮耀', '描述一位高中時期遭受校園暴力的女子，在多年後展開縝密復仇的故事。', '懸疑復仇', 9.5, 'https://example.com/glory.jpg'),
('機智醫生生活', '講述五位好友醫生在醫院裡的日常與溫馨故事。', '醫療生活', 9.8, 'https://example.com/hospital.jpg'),
('愛的迫降', '韓國財閥繼承人因滑翔傘事故迫降北韓，與軍官展開跨越國界的愛情。', '浪漫愛情', 9.2, 'https://example.com/crash.jpg');

INSERT INTO actor (name, image_url) VALUES 
('宋慧喬', 'https://example.com/song.jpg'),
('曹政奭', 'https://example.com/cho.jpg'),
('玄彬', 'https://example.com/hyun.jpg'),
('孫藝真', 'https://example.com/son.jpg');

INSERT INTO drama_actor (drama_id, actor_id) VALUES 
(1, 1), -- 黑暗榮耀 - 宋慧喬
(2, 2), -- 機智醫生生活 - 曹政奭
(3, 3), -- 愛的迫降 - 玄彬
(3, 4); -- 愛的迫降 - 孫藝真
