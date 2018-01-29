from collections import namedtuple

from united_states_of_browsers.oops.table import Table

TableData = namedtuple('TableData','table, path, browser, file, profile')

firefox_profile_path = 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
chrome_profile_path = 'C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\'
init_testdata_input = (
	TableData(table='moz_places',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	TableData(table='moz_bookmarks',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	TableData(table='moz_places',
	          path=firefox_profile_path+'udd5sttq.test_profile2\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile2',
	          ),
	TableData(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	TableData(table='urls',
	          path=chrome_profile_path+'Profile 1\\History',
	          browser='chrome',
	          file='history',
	          profile='Profile 1',
	          ),
	)

init_testdata_expected = [
	Table(table='moz_places',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	Table(table='moz_bookmarks',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	Table(table='moz_places',
	          path=firefox_profile_path+'udd5sttq.test_profile2\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile2',
	          ),
	Table(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	Table(table='urls',
	          path=chrome_profile_path+'Profile 1\\History',
	          browser='chrome',
	          file='history',
	          profile='Profile 1',
	          ),
	]

make_records_testdata_input = [
	Table(table='moz_places',
		path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
		browser='firefox',
		file='places.sqlite',
		profile='test_profile1',
		),
	Table(table='urls',
		path=chrome_profile_path+'Profile 1\\History',
		browser='chrome',
		file='history',
		profile='Profile 1',
		),
	]
make_records_testdata_expected = (
	set(['place:sort=8&maxResults=10',
	'place:type=6&sort=14&maxResults=10',
	'https://www.mozilla.org/privacy/firefox/',
	'https://www.nytimes.com/2017/10/20/opinion/sunday/to-complain-is-to-truly-be-alive.html',
	'https://www.wired.com/story/google-sidewalk-labs-toronto-quayside/',
	'https://www.outsideonline.com/2243621/appalachian-hustle',
	'place:type=3&sort=4',
	'place:transition=7&sort=4',
	'place:type=6&sort=1',
	'place:folder=TOOLBAR',
	'place:folder=BOOKMARKS_MENU',
	'place:folder=UNFILED_BOOKMARKS',
	    ]),
	set(['https://www.google.com/search?q=test&oq=test&aqs=chrome..69i57j0l5.789j0j7&sourceid=chrome&ie=UTF-8',
	'http://www.gmail.com/',
	'https://www.gmail.com/',
	'https://www.google.com/gmail/',
	'https://mail.google.com/mail/',
	'https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#',
	'https://mail.google.com/intl/en/mail/help/about.html#',
	'https://www.google.com/intl/en/mail/help/about.html#',
	'https://www.google.com/gmail/about/#',
	'https://www.google.com/search?q=village+dental+nyc&oq=village+dental+nyc&aqs=chrome..69i57j0l5.2878j0j7&sourceid=chrome&ie=UTF-8',
	'http://www.villagedentalnyc.com/',
	'https://www.ident.ws/template_include/new_patient_sign_in.do?site=10679&practiceId=37810',
	'https://www.ident.ws/template_include/new_patient_forms.do?FirstName=Kshitij&MI=&LastName=Chawla&apptDate=12%2F12%2F2017',
	'https://www.ident.ws/template_include/questionnaire_form.do?id=2785850972',
	'http://www.yahoo.com/',
	'https://www.yahoo.com/',
	'https://www.ident.ws/template_include/cal.jsp?format=MM%2FDD%2FYYYY&datefield=document.forms.signInForm.apptDate',
	'https://coderpad.io/ZARYRHRP',
	'https://mail.google.com/mail/u/0/#inbox',
	'https://accounts.google.com/AccountChooser?service=mail&continue=https://mail.google.com/mail/',
	'https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1',
	'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin',
	    ]),
	)
