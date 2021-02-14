from django.http import HttpResponse
from django.db import connections

def gen_name_query(name):
	ans = 'SELECT * FROM ' + 'title' + ' WHERE lower(name) LIKE \'%%{0}%%\';'.format(name.lower())
	print(ans)
	return ans

def gen_query_search(name, year, genre, rating):
	ans = 'select * from title where '
	if (name != None and name != ""):
		ans = ans + 'to_tsvector(\'english\', name) @@ to_tsquery(\'english\',\'{0}\') and '.format(name.lower())
	else: 
		ans = ans + 'false and '

	if (year != None and year != ""):
		ans = ans + 'release_year = \'{0}\' and '.format(year)
	if (genre != None and genre != ""):
		ans = ans + '\'{0}\' = ANY(lower(genre::text)::text[]) and '.format(genre.lower())
	if (rating != None and rating != ""):
		ans = ans + 'rating >= \'{0}\' and '.format(rating)
	ans = ans + 'true;'
	print(ans)
	return ans
	
def gen_query(name, year, isadult):
	ans = 'select * from title where '
	if (name != None):
		ans = ans + 'name ILIKE \'%%{0}%%\' and '.format(name.lower())
	if (year != None):
		ans = ans + 'release_year = \'{0}\' and '.format(year)
	if (isadult != None):
		ans = ans + 'isadult = \'{0}\' and '.format(isadult)
		
	ans = ans + 'true limit 100;'
	print(ans)
	return ans
	
# def query():

#gen_name_query('star wars')
#gen_query(name='New Movie', year='1998', isadult=None)