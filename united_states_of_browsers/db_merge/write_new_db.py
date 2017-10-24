# -*- encoding: utf-8 -*-
import os

from array import array
from bisect import insort
from collections import OrderedDict as odict

from united_states_of_browsers.db_merge import show
from united_states_of_browsers.db_merge import helpers

from united_states_of_browsers.db_merge.imported_annotations import *


def merge_databases(source_record_yielder: Generator,
                    sink_db_info: Union[Dict, bool],
                    start_from: int=0,
                    show_records: Union[bool, int]=False
                    ) -> [Sequence[int], [Sequence[int], Dict[int, Dict]]]:
	'''
	Creates a new database by merging data from multiple databases.
	Accepts a generator to yield source databases records, dict of info for target database.
	Optional: Accepts the number of initial records to skip, and to print the records as they are processed.
	Returns array of url_hashes of website addresses.
	'''
	all_records = odict()
	url_hashes = array('Q')
	each_time = int(show_records)
	for count, record in enumerate(source_record_yielder):
		if count < start_from and start_from:
			continue
		curr_record_hash = list(record.keys())[0]
		
		if curr_record_hash not in set(url_hashes):
			if sink_db_info:
				curr_record_hash = write_to_db(record=record, sink_db_info=sink_db_info, table='moz_places')
				show.show_record_(record=record, record_count=count, each_time=each_time)
				insort(url_hashes, curr_record_hash)
				all_records = None
			else:
				curr_record_hash = list(record.keys())[0]
				all_records.update(record)
				insort(url_hashes, curr_record_hash)
	
	hash_key_mismatches = [hash_in_key
	                         for hash_in_key, record in all_records.items()
	                         if hash_in_key != record['url_hash']
	                         ]
	try:
		if hash_key_mismatches:
			raise Exception("In variable all_records(dict), url_hash_in_key != record['url_hash']\n"
			                "URL hash in key does not match URL hash in record.")
	except:
		return hash_key_mismatches
	else:
		return url_hashes, all_records


def setup_output_db_paths(output_db):
	try:
		output_db, output_ext = output_db.split(os.extsep)
	except ValueError:
		output_ext = 'sqlite'
		
	sink_db_path = helpers.filepath_from_another(os.extsep.join([output_db, output_ext]))
	
	url_hash_log_filename = '_'.join([os.path.splitext(output_db)[0], 'url_hash_log.bin'])
	url_hash_log_file = helpers.filepath_from_another(url_hash_log_filename)
	return sink_db_path, url_hash_log_file


def write_to_db(record: Dict, sink_db_info: Dict, table: Text='moz_places') -> int:
	'''
	Writes a record to a database.
	Accepts a record and target database info
	Optional: database table name else uses default 'moz_places'.
	Returns the url_hash of the written record.'''
	curr_record_hash = list(record.keys())[0]
	try:
		field_names_string
	except NameError:
		field_names_string, data = helpers.get_record_info(record)
		queries = helpers.make_queries(table=table, field_names=field_names_string)
		helpers.create_table(cursor=sink_db_info['cursor'], query=queries['create'])
	
	data = list(record[curr_record_hash].values())
	helpers.insert_record(connection=sink_db_info['connection'],
	                      cursor=sink_db_info['cursor'],
	                      query=queries['insert'],
	                      data=data
	                      )
	return curr_record_hash

	
def write_to_json(json_path, record_yielder):
	'''Deprecated'''
	import jsonlines
	
	with jsonlines.open(json_path, 'w') as json_records_obj:
		for record in record_yielder:
			json_records_obj.write(record)


if __name__ == '__main__':
	test_records = (
		{47356370932282: odict(
				[('id', 1), ('url', 'https://www.mozilla.org/en-US/firefox/central/'),
				 ('title', None), ('rev_host', 'gro.allizom.www.'), ('visit_count', 0),
				 ('hidden', 0), ('typed', 0), ('favicon_id', None), ('frecency', 74),
				 ('last_visit_date', None), ('guid', 'NNqZA_f2KHI1'), ('foreign_count', 1),
				 ('url_hash', 47356370932282), ('description', None), ('preview_image_url', None)])},
		{47357795150914: dict(odict(
				[('id', 2), ('url', 'https://support.mozilla.org/en-US/products/firefox'),
				 ('title', None), ('rev_host', 'gro.allizom.troppus.'), ('visit_count', 0),
				 ('hidden', 0), ('typed', 0), ('favicon_id', None), ('frecency', 74),
				 ('last_visit_date', None), ('guid', '4xhwpotXndUs'), ('foreign_count', 1),
				 ('url_hash', 47357795150914), ('description', None), ('preview_image_url', None)]))},
		)
	import jsonlines
	# for record in test_records:
		# write_to_json('example_json.jsonl', record)
	with jsonlines.open('example_json.jsonl', 'w') as json_records_obj:
		for record in test_records:
			json_records_obj.write(record)
