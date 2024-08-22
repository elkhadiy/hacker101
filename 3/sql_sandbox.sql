-- INIT database
CREATE TABLE admins (
  adminID INT AUTO_INCREMENT KEY,
  username VARCHAR(255),
  password VARCHAR(255)
);

INSERT INTO admins(username, password) VALUES ('john', 'freedom123');
INSERT INTO admins(username, password) VALUES ('Robert', 'ilikegolf73');
INSERT INTO admins(username, password) VALUES ('Mohammed', 'messy83');

-- QUERY database

SELECT username FROM admins WHERE username = 'someone' OR SUBSTRING((SELECT username FROM admins LIMIT 1), 1, 1) > 'z';

SELECT password FROM admins WHERE username = 'someone' OR '1'='1';
