-- create tables of original data

create table sample_title_basics(tconst varchar(10) not null, titleType varchar(20) not null, primaryTitle varchar(500) not null, originalTitle varchar(500) not null, isAdult boolean not null, startYear integer, endYear integer, runtimeMinites varchar(10), genres varchar(100), primary key(tconst));

create table sample_name_basics(nconst varchar(10) not null, primaryName varchar(200) not null, birthYear integer, deathYear varchar(10), primaryProfession varchar(100), knownForTitles varchar(100), primary key(nconst));

create table sample_title_principals(tconst varchar(10) not null, ordering integer not null, nconst varchar(10) not null, category varchar(30) not null, job varchar(300), characters varchar(500), primary key(tconst, ordering));

create table sample_title_ratings(tconst varchar(255) not null, averageRating float not null, numVotes integer not null, primary key(tconst));

-- convert tables to given schema

insert into Title (select sample_title_basics.tconst as t_id, sample_title_basics.primarytitle as name, sample_title_basics.titletype as type, string_to_array(sample_title_basics.genres, ',',',') as genre, sample_title_basics.startyear as release_year, sample_title_ratings.averagerating as rating, sample_title_ratings.numvotes as rating_count, sample_title_basics.isadult as isadult from sample_title_basics inner join sample_title_ratings on sample_title_basics.tconst = sample_title_ratings.tconst);

insert into Person (select nconst as p_id, primaryName as name from sample_name_basics);

insert into Principals (select tconst as t_id, ordering, nconst as p_id, category, characters from sample_title_principals);