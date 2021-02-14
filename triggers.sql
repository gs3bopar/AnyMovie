-- File containing triggers and their associated functions

-- Changing the movie rating when a user review is added
CREATE OR REPLACE FUNCTION add_movie_rating()
RETURNS TRIGGER AS
$BODY$
DECLARE
   movie record;
   new_rating float;
   new_count int;
BEGIN
    -- Only make changes to a movie's rating if the new review has a rating
    IF NEW.rating IS NOT NULL THEN
        SELECT rating, rating_count INTO STRICT movie FROM title WHERE t_id = NEW.t_id;
        -- Set 0 as default if the movie is missing count or rating
        IF movie.rating_count IS NULL THEN
            movie.rating_count := 0;
        END IF;
        IF movie.rating IS NULL THEN
            movie.rating := 0;
        END IF;
        -- Increase the amount of ratings by 1
        new_count := movie.rating_count + 1;
        -- Find the sum of all the ratings, add the new rating, and divide by the new count
        new_rating := (movie.rating_count * movie.rating + NEW.rating) / new_count;
        UPDATE title
            SET rating = new_rating, rating_count = new_count
            WHERE t_id = NEW.t_id;
    END IF;

    RETURN new;
END;
$BODY$
language plpgsql;


CREATE TRIGGER AddRating
AFTER INSERT on review
FOR EACH ROW
EXECUTE PROCEDURE add_movie_rating();


-- Changing the movie rating when a user review is edited
CREATE OR REPLACE FUNCTION update_movie_rating()
RETURNS TRIGGER AS
$BODY$
DECLARE
   movie record;
   new_rating float;
   new_count int;
BEGIN
    SELECT rating, rating_count INTO STRICT movie FROM title WHERE t_id = NEW.t_id;
    -- Set 0 as default if the movie is missing count or rating
    IF movie.rating_count IS NULL THEN
        movie.rating_count := 0;
    END IF;
    IF movie.rating IS NULL THEN
        movie.rating := 0;
    END IF;
    -- There are 4 cases for this update. This update depends on whether or not
    -- the review had a rating and whether or not the new review has a rating
    -- Case 1: No Rating -> Rating
    IF OLD.rating IS NULL AND NEW.rating IS NOT NULL THEN
        new_count := movie.rating_count + 1;
        -- factor in new rating into the overall movie rating
        new_rating := (movie.rating_count * movie.rating + NEW.rating) / new_count;
        UPDATE title
            SET rating = new_rating, rating_count = new_count
            WHERE t_id = NEW.t_id;
    -- Case 2: Rating -> No Rating
    ELSIF OLD.rating IS NOT NULL AND NEW.rating IS NULL THEN
        new_count := movie.rating_count - 1;
        -- Set the movie rating to NULL if the amount of ratings is 0
        IF new_count = 0 THEN
            new_rating := NULL;
        ELSE
            -- remove old rating from the overall movie rating
            new_rating := (movie.rating_count * movie.rating - OLD.rating) / new_count;
        END IF;
        UPDATE title
            SET rating = new_rating, rating_count = new_count
            WHERE t_id = NEW.t_id;
    -- Case 3: Rating -> Rating
    -- the amount of ratings does not change in this case
    ELSIF OLD.rating IS NOT NULL AND NEW.rating IS NOT NULL THEN
        new_rating := (movie.rating_count * movie.rating - OLD.rating + NEW.rating) / movie.rating_count;
        UPDATE title
            SET rating = new_rating
            WHERE t_id = NEW.t_id;
    END IF;
    -- Case 4: No Rating -> No Rating (No changes occur to the title's ratings)

    RETURN new;
END;
$BODY$
language plpgsql;


CREATE TRIGGER UpdateRating
AFTER UPDATE OF rating on review
FOR EACH ROW
EXECUTE PROCEDURE update_movie_rating();


-- Changing the movie rating when a user review is removed
CREATE OR REPLACE FUNCTION remove_movie_rating()
RETURNS TRIGGER AS
$BODY$
DECLARE
   movie record;
   new_rating float;
   new_count int;
BEGIN
    SELECT rating, rating_count INTO STRICT movie FROM title WHERE t_id = OLD.t_id;
    -- Only change the movie rating if the review had a rating
    IF OLD.rating IS NOT NULL THEN
        -- Since there was a rating, we don't need to set defaults for the movie rating and count
        new_count := movie.rating_count - 1;
        -- Set the movie rating to NULL if the amount of ratings is 0
        IF new_count = 0 THEN
            new_rating := NULL;
        ELSE
            -- remove old rating from the overall movie rating
            new_rating := (movie.rating_count * movie.rating - OLD.rating) / new_count;
        END IF;
        UPDATE title
            SET rating = new_rating, rating_count = new_count
            WHERE t_id = OLD.t_id;
    END IF;

    RETURN new;
END;
$BODY$
language plpgsql;


CREATE TRIGGER RemoveRating
AFTER DELETE on review
FOR EACH ROW
EXECUTE PROCEDURE remove_movie_rating();
