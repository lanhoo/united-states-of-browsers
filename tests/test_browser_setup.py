#  encoding -*-utf8-*-
"""
/UnitedStatesOfBrowsers$ pip install -e . (sudo) after setting up the packages and setup.py seems to
have ameliorated the import difficulties.
"""

import pytest

from united_states_of_browsers.db_merge import browser_setup
from tests.data import test_browser_setup_data as bs_data


collected_tests = []

@pytest.mark.parametrize(('test_case'), [test_case for test_case in bs_data.setup_profile_paths_values_testdata])
def test_setup_profile_paths_values(test_case):
	global collected_tests
	actual_output = browser_setup.setup_profile_paths(browser_ref=test_case.browser_ref,
	                                                  profiles=test_case.profiles)
	assert test_case.expected == actual_output
	collected_tests.append((test_case),)


@pytest.mark.parametrize(('test_case'), [test_case for test_case in bs_data.setup_profile_paths_excep_testdata])
def test_setup_profile_paths_excep(test_case):
	with pytest.raises(test_case.expected) as excinfo:
		actual = browser_setup.setup_profile_paths(browser_ref=test_case.browser_ref,
		                                           profiles=test_case.profiles)

@pytest.mark.parametrize(('test_case'), [test_case for test_case in bs_data.db_filepaths_values_testdata])
def test_db_filepath_values(test_case):
	actual_output = browser_setup.db_filepath(profile_paths=test_case.profile_paths,
	                                          filenames=test_case.filenames,
	                                          ext=test_case.ext)
	assert test_case.expected == actual_output
	
	
@pytest.mark.parametrize(('test_case'), [test_case for test_case in bs_data.db_filepaths_excep_testdata])
def test_db_filepath_excep(test_case):
	with pytest.raises(test_case.expected) as excinfo:
		actual_output = browser_setup.db_filepath(profile_paths=test_case.profile_paths,
		                                          filenames=test_case.filenames,
		                                          ext=test_case.ext)
		
	
	
	
if __name__ == '__main__':
	pytest.main()

