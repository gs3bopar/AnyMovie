CREATE TABLE Custom_User
(
  u_id          DECIMAL(9, 0) NOT NULL PRIMARY KEY,
  email         VARCHAR(50) UNIQUE NOT NULL,
  password      VARCHAR(50) NOT NULL,
  username      VARCHAR(10) NOT NULL
);

CREATE TABLE Title
(
  t_id          VARCHAR(10) NOT NULL PRIMARY KEY,
  name          VARCHAR(500) NOT NULL,
  type          VARCHAR(20),
  genre         VARCHAR(20) ARRAY,
  release_year  INTEGER,
  rating        FLOAT,
  rating_count  INTEGER,
  isAdult       BOOLEAN
);

CREATE TABLE Person
(
  p_id          VARCHAR(10) NOT NULL PRIMARY KEY,
  name          VARCHAR(200) NOT NULL
);

CREATE TABLE Review
(
  u_id          DECIMAL(9, 0) NOT NULL REFERENCES Custom_User(u_id),
  t_id          VARCHAR(10) NOT NULL REFERENCES Title(t_id),
  time          TIMESTAMP NOT NULL,
  rating        FLOAT,
  comment       VARCHAR(255),
  PRIMARY KEY(u_id, t_id, time)
);

CREATE TABLE Favourite
(
  u_id          DECIMAL(9, 0) NOT NULL REFERENCES Custom_User(u_id),
  t_id          VARCHAR(10) NOT NULL REFERENCES Title(t_id),
  PRIMARY KEY(u_id, t_id)
);

CREATE TABLE History
(
  u_id          DECIMAL(9, 0) NOT NULL REFERENCES Custom_User(u_id),
  t_id          VARCHAR(10) NOT NULL REFERENCES Title(t_id),
  time          TIMESTAMP NOT NULL,
  PRIMARY KEY(u_id, t_id)
);

CREATE TABLE Principals
(
  t_id          VARCHAR(10) NOT NULL REFERENCES Title(t_id),
  ordering      INTEGER NOT NULL,
  p_id          VARCHAR(10) NOT NULL REFERENCES Person(p_id),
  category      VARCHAR(30) NOT NULL,
  characters    VARCHAR(500),       
  PRIMARY KEY(t_id, ordering)
);
