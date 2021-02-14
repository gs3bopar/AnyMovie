-- create tables of original data

create table title_basics(tconst varchar(10) not null, titleType varchar(20) not null, primaryTitle varchar(500) not null, originalTitle varchar(500) not null, isAdult boolean not null, startYear integer, endYear integer, runtimeMinites varchar(10), genres varchar(100), primary key(tconst));

create table name_basics(nconst varchar(10) not null, primaryName varchar(200) not null, birthYear integer, deathYear varchar(10), primaryProfession varchar(100), knownForTitles varchar(100), primary key(nconst));

create table title_principals(tconst varchar(10) not null, ordering integer not null, nconst varchar(10) not null, category varchar(30) not null, job varchar(300), characters varchar(500), primary key(tconst, ordering));

create table title_ratings(tconst varchar(255) not null, averageRating float not null, numVotes integer not null, primary key(tconst));