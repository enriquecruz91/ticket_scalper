import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

BASE_DESCRIPTION = '''Artist: {artist}
URL:
Sale Type: {sale_type}
Password: {password}
Buyer:
Buy Guidelines: {buy_guidelines}
Sell Guidelines: Immediately upload to StubHub; price it competitively but still above the lowest price for similar seats (based on section and row) unless margins are sufficiently high (>=70% over the break even price)
StubHub account info: silvertix@gmail.com, tsilver91'
'''

def user_OAuth2():
	# Set up a Flow object to be used if we need to authenticate. This
	# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
	# the information it needs to authenticate. Note that it is called
	# the Web Server Flow, but it can also handle the flow for native
	# applications
	# The client_id and client_secret are copied from the API Access tab on
	# the Google APIs Console
	FLOW = OAuth2WebServerFlow(
	    client_id='543969079784-4m945i6c1s5c9jmplabpsc4o2s29i4om.apps.googleusercontent.com',
	    client_secret='VF-_9Y47aNjZR7jCjKr42Cz1',
	    scope='https://www.googleapis.com/auth/calendar',
	    user_agent='SSC-0.2')

	# To disable the local server feature, uncomment the following line:
	# FLAGS.auth_local_webserver = False

	# If the Credentials don't exist or are invalid, run through the native client
	# flow. The Storage object will ensure that if successful the good
	# Credentials will get written back to a file.
	storage = Storage('calendar.dat')
	credentials = storage.get()
	if credentials is None or credentials.invalid == True:
	  credentials = run(FLOW, storage)

	# Create an httplib2.Http object to handle our HTTP requests and authorize it
	# with our good Credentials.
	http = httplib2.Http()
	http = credentials.authorize(http)

	# Build a service object for interacting with the API. Visit
	# the Google APIs Console
	# to get a developerKey for your own application.
	service = build(serviceName='calendar', version='v3', http=http,
	       developerKey='AIzaSyD4CyU_Y0ydHzD5zjMGmV7QjpwwHj62XUY')
	return service

def create_calendar_event(api_service, date, artist='', location ='', sale_type='', buy_guidelines=''):
	password = get_password(sale_type)
	event = {
	  'summary': '{artist} {location} - {sale_type}'.format(artist=artist, sale_type=sale_type, location=location),
	  'location': '{location}'.format(location=location),
	  'start': {
	    'dateTime': date,
	    "timeZone": "America/New_York"
	  },
	  'end': {
	    'dateTime': date,
	    "timeZone": "America/New_York"
	  },
	  'description': BASE_DESCRIPTION.format(artist=artist, sale_type=sale_type, password=password, 
	  		buy_guidelines=buy_guidelines)
	}

	return api_service.events().insert(
	  calendarId='0fktvjbc0obq8trsvnkfg9ql24@group.calendar.google.com', 
	  body=event).execute()

def get_password(sale_type):
	if 'sale_type' == 'General Sale':
		password = 'N/A'
	else:
		password = '?'
	return password

def test():
	print create_calendar_event(user_OAuth2(), '2012-28-08T10:00:00', 'enrique', 'here', 'General Sale')