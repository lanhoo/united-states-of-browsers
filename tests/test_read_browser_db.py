import pytest

from united_states_of_browsers.db_merge import read_browser_db
from tests.data import test_read_browser_db_data as rbd_data


@pytest.mark.parametrize('test_case', [test_case for test_case in rbd_data.firefox_testdata['defaults']])
def test_firefox_defaults(test_case):
	actual_output = read_browser_db.firefox()
	assert test_case.expected == actual_output

@pytest.mark.parametrize('test_case', [test_case for test_case in rbd_data.firefox_testdata['values']])
def test_firefox_values(test_case):
	actual_output = read_browser_db.firefox(profiles=test_case.profiles)
	assert test_case.expected == actual_output

@pytest.mark.parametrize('test_case', [test_case for test_case in rbd_data.firefox_testdata['exceps']])
def test_firefox_excep(test_case):
	with pytest.raises(test_case.expected) as excinfo:
		actual_output = read_browser_db.firefox(profiles=test_case.profiles)

