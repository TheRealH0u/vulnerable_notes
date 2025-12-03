-- Drop existing tables (if any) to ensure this script can be re-run during initialization
DROP TABLE IF EXISTS note CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(30) UNIQUE NOT NULL,
  email VARCHAR(60) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

-- Create note table
CREATE TABLE note (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(100) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- #ThisIsSomeLongAssPasswordThatYouWillNeverGetBecauseItsSoLong123!!!!!

-- Seed users
INSERT INTO users (id, username, email, password) VALUES
  (1, 'admin', 'ctf{You_Found_The_Flag!!!}', 'scrypt:32768:8:1$6fpkMvCmXTlYHJCD$afd81d0209d969644e726bb75588c299fe8f467803657ca7859a8a3544ed78039da7048f840ebe554ccdebf4ef5abfb811b72ad2cc6352eb6982bde22f5e4723'),
  (2, 'bob', 'bob@example.com', 'scrypt:32768:8:1$ozw5RB3IdFJ9Y76C$ed59f1109d58722a4b0588d2baf335a55cae9fa873133faac1c22bb52421c2d284fe736102598fe55ba3e8b8bc7e4b6538e3b845152e9b51fe2238b9b6d4cf5e'),
  (3, 'alice', 'alice@example.com', 'scrypt:32768:8:1$PtYYMWfrdXL0onsx$951e61f80a6358bbbe3d2b16297e5a890f28680d49aefa3780f2d3ccc96df167f5f52c58b9e71af81d49364fc45f0ebac0fc795cf4aa0ff6ef78fad56f83f88d');

-- Reset users sequence
SELECT setval(pg_get_serial_sequence('users','id'), (SELECT COALESCE(MAX(id),0) FROM users));

-- Seed notes
INSERT INTO note (id, user_id, title, content, created_at, updated_at) VALUES
  (1, 3, 'Alice Note 1', 'This is Alice''''s note #1.', NOW(), NOW()),
  (2, 3, 'Alice Note 2', 'This is Alice''''s note #2.', NOW(), NOW()),
  (3, 3, 'Alice Note 3', 'This is Alice''''s note #3.', NOW(), NOW()),
  (4, 3, 'Alice Note 4', 'This is Alice''''s note #4.', NOW(), NOW()),
  (5, 3, 'Alice Note 5', 'This is Alice''''s note #5.', NOW(), NOW()),
  (6, 1, 'Admin Special Note', 'This note belongs to admin.', NOW(), NOW()),
  (7, 2, 'Bob Note 1', 'This is Bob''''s note #1.', NOW(), NOW()),
  (8, 2, 'Bob Note 2', 'This is Bob''''s note #2.', NOW(), NOW()),
  (9, 2, 'Bob Note 3', 'This is Bob''''s note #3.', NOW(), NOW()),
  (10, 2, 'Bob Note 4', 'This is Bob''''s note #4.', NOW(), NOW()),
  (11, 2, 'Bob Note 5', 'This is Bob''''s note #5.', NOW(), NOW());

-- Reset note sequence
SELECT setval(pg_get_serial_sequence('note','id'), (SELECT COALESCE(MAX(id),0) FROM note));