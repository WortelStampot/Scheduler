DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS staff;

Create Table staff (
    id INTEGER PRIMARY KEY
    name TEXT NOT NULL
    );


CREATE TABLE role (
id INTEGER PRIMARY KEY
name TEXT NOT NULL
callTime TEXT NOT NULL
-- calltime text stored in HH:MM:SS format
    );

