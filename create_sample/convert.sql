
-- convert tables to given schema

insert into Title (select title_basics.tconst as t_id, title_basics.primarytitle as name, title_basics.titletype as type, string_to_array(title_basics.genres, ',',',') as genre, title_basics.startyear as release_year, title_ratings.averagerating as rating, title_ratings.numvotes as rating_count, title_basics.isadult as isadult from title_basics inner join title_ratings on title_basics.tconst = title_ratings.tconst);

insert into Person (select nconst as p_id, primaryName as name from name_basics);

insert into Principals (select tconst as t_id, ordering, nconst as p_id, category, characters from title_principals);