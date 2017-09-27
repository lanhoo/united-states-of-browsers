import os

from pprint import pprint
from pathlib import Path
from typing import (Union,
                    Optional,
                    Iterable,
                    AnyStr,
                    Type,
                    TypeVar,
                    )


debug = 0


def _choose_browser_paths(browser_ref: Union[str, Path]) -> Union[str, Path]:
	'''
	Accepts a browser name or a directory path pointing to the profile location of the browser.
	Returns the browser profile location.
	'''
	path_crumbs = {'firefox': ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles'],
					'chrome': ['~', 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default',
								'History'],
					}
	return os.path.expanduser(Path(*path_crumbs.get(browser_ref, [browser_ref])))


def _profile_dir(profile_loc: Path, *, profiles: Optional[Union[str, Iterable[AnyStr]]]=None) -> Iterable[Path]:
	'''
	Creates paths for all profile directories in profile_loc (default), or for specified profiles.
	
	profile_loc: Root path of directory with all profile directories
	profile_name: All profiles are included by default, can accept name of single profile or list of profiles.
	:return: Profile path or list of profile paths
	'''
	get_profile_name = lambda profile_dir: (profile_dir[profile_dir.find('.') + 1:])
	if profiles is None:  # Returns all the profile paths if no profiles specified
		return {get_profile_name(dir_.name): dir_ for dir_ in Path(profile_loc).iterdir() if
		        dir_.is_dir()}
	
	if isinstance(profiles, str):
		profiles = [profiles]
	return {get_profile_name(dir_.name): dir_ for profile_ in profiles
	        for dir_ in Path(profile_loc).iterdir()
	        if get_profile_name(dir_.name) == profile_}


def setup_profile_paths(*, browser_ref, profiles):
	"""
	Sets up the directory path for sqlite database files.
	Returns path to sqlite file's copy stored in project directory.
	:return: root directory
	:rtype: str/path-like object
	"""
	profile_loc = _choose_browser_paths(browser_ref=browser_ref)
	
	profile_paths = _profile_dir(profile_loc, profiles=profiles)
	return profile_paths


def _db_files(profile_paths: Path, ext: Optional[AnyStr]='.sqlite') -> Iterable[Path]:
	'''
	Returns a list of file in the specified directory (not subdirectories) with a specified (or no) extension.
	
	profile_paths: Path to directory with the files
	:param ext: Extension for the file. (Default: .sqlite)
	:return: list of files with the specified extension.
	'''
	try:
		for curr_dir, subdirs, files in os.walk(profile_paths):
			break
	except TypeError:
		print("ERROR: Path can not be None")
	else:
		ext = ext[1:] if ext[0] == '.' else ext
		return [file_ for file_ in files if file_.rfind(ext) == len(file_) - len(ext)]


def db_filepath(profile_paths, filenames=None, ext='sqlite'):
	"""
	Yields the path for the next database file.
	By default, these are sqlite file. (used by browsers to store history, bookmarks etc)

	Usage:
		filepath_generator = _filepath(root, filenames, ext)
		next_sqlite_databse_filepath = next(filepath_generator)

	:param profile_paths: Directory path containing the database files.
		Default: <project_root>/tinker/data/firefox_regular_surfing/
	:type profile_paths: str/path-like object
	:param filenames: List of database filenames in the root directory.
		Default: ['places', 'storage']
	:type filenames: list[str]
	:param ext: Extension of the databse file.
		Default: sqlite
	:type ext: str
		Default: sqlite
	:return: yields path of the database file.
	:rtype: str/path-like object
	"""
	try:
		ext_joiner = '' if ext[0] in {os.extsep,
									  '.'} else os.extsep  # if a . in ext arg, doesn't add another
	except (
	TypeError, IndexError):  #  if file doesn't have an ext, ext arg is empty, doesn't add the .
		ext_joiner = ''
		ext = ''
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
	
