from collections import namedtuple
from typing import Text, Sequence, Dict, Union, Iterable


def make_queries(tablename: Text, primary_key_name: Text, fieldnames: Sequence[Text]) -> Dict:
	""" Constructs the queries necessary for specific purposes.
	Returns them as dict['purpose': 'query']
	"""
	fieldnames_str = ', '.join(fieldnames)
	query_placeholder = '?, ' * len(fieldnames)
	queries = {'create': f'''CREATE TABLE IF NOT EXISTS {tablename} ({primary_key_name} integer PRIMARY KEY, {fieldnames_str[:]})'''}
	queries.update({'insert': f"INSERT INTO {tablename}({fieldnames_str}) VALUES ({query_placeholder[:-2]})"})
	return queries


def query_sanitizer(query: str, allowed_chars: Union[str, Iterable]='_') -> str:
	""" Removes non-alphanumeric characters from a query.
	Retains characters passed in via `allowed_chars`. (Default: '_')
	Returns a string.
	"""
	allowed_chars = set(allowed_chars)
	return ''.join([char for char in query if char.isalnum() or char in allowed_chars])  #, '?', '(', ')', ','}])


def define_non_null_fields(table_obj):
	BrowserFileTableFields = namedtuple('BrowserFileTable', 'browser file table')
	non_null_fields_info = {
		BrowserFileTableFields(browser='firefox', file='places.sqlite', table='moz_places'): ('title', 'last_visit_date'),
		BrowserFileTableFields(browser='chrome', file='history', table='urls'): ('title', 'last_visit_time'),
		}
	query = BrowserFileTableFields(table_obj['browser'], table_obj['file'], table_obj['table'])
	return non_null_fields_info.get(query, None)