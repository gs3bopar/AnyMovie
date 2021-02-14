import psycopg2
from psycopg2 import Error
import time

def load(connection, cursor, create_table_query, table_name, file_path):
	print("Loading...\n")
	cursor.execute(create_table_query)
	connection.commit()
	
	'''f = open(file_path, 'r')
	print(f.read())
	f.close()'''
	f = open(file_path, 'r', encoding='UTF-8')
	cursor.copy_from(f, table_name, sep='\t')
	f.close()
	connection.commit()

def load_imdb_data_sample(connection, cursor):
	
	create_table_query = 'drop table if exists sample_title_ratings; create table sample_title_ratings(tconst varchar(255) not null, averageRating float not null, numVotes integer not null, primary key(tconst));'
	table_name = 'sample_title_ratings'
	file_path = r'title.ratings.sample.tsv'
	load(connection, cursor, create_table_query, table_name, file_path)
	
	create_table_query = 'drop table if exists sample_title_basics; create table sample_title_basics(tconst varchar(10) not null, titleType varchar(20) not null, primaryTitle varchar(500) not null, originalTitle varchar(500) not null, isAdult boolean not null, startYear integer, endYear integer, runtimeMinites varchar(10), genres varchar(100), primary key(tconst));'
	table_name = 'sample_title_basics'
	file_path = r'title.basics.sample.tsv'
	load(connection, cursor, create_table_query, table_name, file_path)
	
	create_table_query = 'drop table if exists sample_name_basics; create table sample_name_basics(nconst varchar(10) not null, primaryName varchar(200) not null, birthYear integer, deathYear varchar(10), primaryProfession varchar(100), knownForTitles varchar(200), primary key(nconst));'
	table_name = 'sample_name_basics'
	file_path = r'name.basics.sample.tsv'
	load(connection, cursor, create_table_query, table_name, file_path)
	
	create_table_query = 'drop table if exists sample_title_principals; create table sample_title_principals(tconst varchar(10) not null, ordering integer not null, nconst varchar(10) not null, category varchar(30) not null, job varchar(300), characters varchar(500), primary key(tconst, ordering));'
	table_name = 'sample_title_principals'
	file_path = r'title.principals.sample.tsv'
	load(connection, cursor, create_table_query, table_name, file_path)
	
def load_imdb_data(connection, cursor):
	
	create_table_query = 'drop table if exists title_ratings; create table title_ratings(tconst varchar(255) not null, averageRating float not null, numVotes int not null, primary key(tconst));'
	table_name = 'title_ratings'
	file_path = r'title.ratings.tsv'
	load(connection, cursor, create_table_query, table_name, file_path)
	
	create_table_query = 'drop table if exists title_basics; create table title_basics(tconst varchar(10) not null, titleType varchar(20) not null, primaryTitle varchar(500) not null, originalTitle varchar(500) not null, isAdult boolean not null, startYear integer, endYear integer, runtimeMinites varchar(10), genres varchar(100), primary key(tconst));'
	table_name = 'title_basics'
	file_path = r'title.basics.tsv'
	load(connection, cursor, create_table_query, table_name, file_path)
	
	create_table_query = 'drop table if exists name_basics; create table name_basics(nconst varchar(10) not null, primaryName varchar(200) not null, birthYear integer, deathYear varchar(10), primaryProfession varchar(100), knownForTitles varchar(200), primary key(nconst));'
	table_name = 'name_basics'
	file_path = r'name.basics.tsv'
	load(connection, cursor, create_table_query, table_name, file_path)
	
	create_table_query = 'drop table if exists title_principals; create table title_principals(tconst varchar(10) not null, ordering integer not null, nconst varchar(10) not null, category varchar(30) not null, job varchar(300), characters varchar(500), primary key(tconst, ordering));'
	table_name = 'title_principals'
	file_path = r'title.principals.tsv'
	load(connection, cursor, create_table_query, table_name, file_path)
	
	
def main():
	start = time.time()
	print (time.time() - start)

	connection = psycopg2.connect(user = "postgres", password = "password", host = "34.68.71.161", port = "5432", database = "postgres")	
	cursor = connection.cursor()
	
	cursor.execute(open("droptables-custom.sql", "r").read())
	cursor.execute(open("createtables.sql", "r").read())
	
	connection.commit()
	
	load_imdb_data(connection, cursor)
	
	connection.commit()
	
	title = 'insert into Title (select title_basics.tconst as t_id, title_basics.primarytitle as name, title_basics.titletype as type, string_to_array(title_basics.genres, \',\') as genre, title_basics.startyear as release_year, title_ratings.averagerating as rating, title_ratings.numvotes as rating_count, title_basics.isadult as isadult from title_basics left join title_ratings on title_basics.tconst = title_ratings.tconst);'
	
	person = 'insert into Person (select nconst as p_id, primaryName as name from name_basics);'
	
	principals = 'insert into Principals (select tconst as t_id, ordering, nconst as p_id, category, characters from title_principals);'
	
	print (time.time() - start)

	cursor.execute(title)
	connection.commit()
	print('title done')
	cursor.execute(person)
	connection.commit()
	print('person done')
	
	#Remove invalid data from title_principals
	
	#create_index = 'create index nid on title_principals (nconst)'
	
	clean_principals = 'delete from title_principals where nconst in (select distinct nconst from title_principals except select nconst from name_basics); delete from title_principals where tconst in (select distinct tconst from title_principals except select tconst from title_basics);'
	cursor.execute(clean_principals)
	connection.commit()
	
	cursor.execute(principals)
	connection.commit()
	print('principals done')

	cursor.execute(open("createindex.sql", "r").read())
	
	print (time.time() - start)
	
	connection.commit()
	connection.close()
	

main()