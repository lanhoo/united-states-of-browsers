# -*- encoding: utf-8 -*-
"""
Setups the path to browser database files.

Available functions:
 - setup_profile_paths: Returns the profile directory path for each firefox profile.
 - db_filepaths: Returns paths to firefox database files for each profile returned by setup_profile_paths().
	
"""
import os

from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge import helpers

from united_states_of_browsers.db_merge.imported_annotations import *


debug = 0

appdata_path = Path(__file__).parents[1].joinpath('appdata')
app_inf_path = str(appdata_path.joinpath('app_inf.json'))

def _choose_browser_paths(browser_ref: Union[str, PathLike]) -> Union[PathLike, Dict[str, PathLike]]:
	""" Accepts a browser name or a directory path pointing to the profile location of the browser.
	Returns the browser profile location.
	"""
	path_crumbs = {'firefox': ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles'],
					'chrome': ['~', 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default',
								'History'],
					}
	# if browser_ref not in path_crumbs, returns browser_ref as list of profile path.
	return str(Path(*path_crumbs.get(browser_ref, [browser_ref])).expanduser())


def _profile_dir(profile_loc: PathLike, *, profiles: Optional[Union[str, Iterable[AnyStr]]]=None) -> Iterable[PathLike]:
	""" Returns paths for all profile directories in profile_loc (default),
	or for the profile name specified in profiles.
	"""
	get_profile_name = lambda profile_dir: (profile_dir[profile_dir.find('.') + 1:])
	if profiles is None:  # Returns all the profile paths if no profiles specified
		return {get_profile_name(dir_.name): dir_ for dir_ in Path(profile_loc).iterdir() if
		        dir_.is_dir()}
	
	if isinstance(profiles, str):
		profiles = [profiles]
	return {get_profile_name(dir_.name): dir_ for profile_ in profiles
	        for dir_ in Path(profile_loc).iterdir()
	        if get_profile_name(dir_.name) == profile_}


def setup_profile_paths(*, browser_ref: Union[str, PathLike], profiles: Optional[str]):
	""" Returns the directory path for sqlite database files for each profile.
	"""
	profile_loc = _choose_browser_paths(browser_ref=browser_ref)
	
	profile_paths = _profile_dir(profile_loc, profiles=profiles)
	return profile_paths


def _db_files(profile_paths: PathInfo, ext: Optional[AnyStr]='.sqlite') -> Iterable[PathLike]:
	""" Returns a list of file in the specified directory (not subdirectories) with a specified (or no) extension.
	
	profile_paths: Path to directory with the files
	ext: Extension for the file. (Default: .sqlite)
	
	returns: list of files with the specified extension.
	"""
	try:
		for curr_dir, subdirs, files in os.walk(profile_paths):
			break
	except TypeError:
		print("ERROR: Path can not be None")
	else:
		ext = ext[1:] if ext[0] == '.' else ext
		return [file_ for file_ in files if file_.rfind(ext) == len(file_) - len(ext)]


def db_filepath(profile_paths: Dict[str, PathLike], filenames: str='places', ext='sqlite') -> Dict[str, PathLike]:
	""" Yields the path for the next database file.
	Exits program if browser info or profile directory path are invalid.
	
	Accepts profile directory path.
	Optional: file name(s), extensions (default is sqlite)
	"""
	try:
		ext_joiner = '' if ext[0] in {os.extsep, '.'} else os.extsep  # if a . in ext arg, doesn't add another
	except (TypeError, IndexError):  #  if file doesn't have an ext, ext arg is empty, doesn't add the `.`
		ext_joiner, ext = ('', '')
	if filenames is None:
		filenames = _db_files(profile_paths=profile_paths, ext=ext)
	filenames = [filenames]
	file_names = [ext_joiner.join([file_, ext]) for file_ in filenames]
	try:
		return {profile_name: os.path.join(profile_path_, file_name_) for
				profile_name, profile_path_ in profile_paths.items() for file_name_ in file_names}
	except TypeError as excep:
		print('Missing value: browser name or profile path', excep, sep='\n')
		if debug: raise excep
		os.sys.exit()
	

def setup_output_db_paths(db_filename: Optional[Text]) -> [PathInfo, PathInfo]:
	""" Returns paths for the database file and the file with record of processed record's hashes.
	 Accepts filename for the sqlite database file to be written to.
	"""

	appdata_path.mkdir(exist_ok=True)
	if db_filename:
		db_filename = helpers.query_sanitizer(query=db_filename, allowed_chars=['_', '-', ' '])
		sink_db_path = str(appdata_path.joinpath(f'{db_filename}.sqlite'))
		url_hash_log_path = str(appdata_path .joinpath(f'{db_filename}_url_hashes.bin'))
	else:
		import datetime
		this_moment = str(datetime.datetime.now()).split('.')[0]
		for replacee, replacer in zip(['-', ':', ' '], ['', '', '_']):
			this_moment = this_moment.replace(replacee, replacer)
		url_hash_log_path = str(appdata_path.joinpath(f'url_hash_log_{this_moment}.bin'))
		sink_db_path = None
	return appdata_path, sink_db_path, url_hash_log_path


if __name__ == '__main__':
	pprint(setup_profile_paths(browser_ref='firefox', profiles=None))
	print('\n' * 3)
	pprint(setup_profile_paths(browser_ref='firefox', profiles='RegularSurfing'))
	print('\n' * 3)
	pprint(setup_profile_paths(browser_ref='firefox', profiles=['default', 'RegularSurfing']))
	print('\n' * 3)
	pprint(setup_profile_paths(browser_ref='firefox', profiles='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing'))
	print('\n' * 3)
	print(setup_profile_paths(
		browser_ref='~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing', profiles=None))