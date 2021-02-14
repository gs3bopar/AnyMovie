--Query 1, We use two SQL queries to check email validation and add entry to custom_user table these are run when user hits signup
INSERT INTO custom_user (u_id, email, password, username) VALUES('50', 'testing@gmail.com', 'testpassword', 'tesing');
SELECT count(*) FROM custom_user WHERE email = 'testing@gmail.com';

--Query 2, Search for movies based on name, genre, rating, director, actors, language (display all matches)
SELECT * FROM title WHERE name ILIKE '%godfather%' and rating >= 7 and true limit 100;

--Query 3, Accessing detailed movie informationc
  -- get movie details
    SELECT * FROM title WHERE t_id = 'tt0642397';

  -- get movie principals (eg. actor, director)
    SELECT t_id, category, name, characters FROM principals NATURAL JOIN person WHERE t_id = 'tt0642397';
    
  -- get movie reviews
    SELECT u_id, username, rating, comment, time FROM review as r NATURAL JOIN custom_user WHERE t_id = 'tt0642397' ORDER BY time DESC LIMIT 10;
