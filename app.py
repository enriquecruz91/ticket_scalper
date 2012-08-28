import os, sys
#sys.path.append('C:\Python27\Lib\site-packages\\flask-0.9-py2.7.egg')
#sys.path.append('C:\Python27\Lib\site-packages\\requests-0.13.1-py2.7.egg')

#print sys.version
import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
import requests
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from research import crawler, google_API


# CONFIGURATIONS
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
FLOW = OAuth2WebServerFlow(
    client_id='543969079784-lngogo23fltd477geejt005q8h35plb0.apps.googleusercontent.com',
    client_secret='gqDbB6ciBkgc6Vci_qvJaUPR',
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://morning-mesa-6317.herokuapp.com/auth',
    user_agent='SSC-0.2')

@app.route("/")
def landing():
    return render_template('landing.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/research")
def research():
    return render_template('research.html')

@app.route("/search")
def search():
    search_query = request.args['search_query']
    search_target = request.args['search_target']
    if search_target == 'ticketmaster':
        return render_template('iframe_search.html', search_query=search_query, ticketmaster=True)
    else:
        return render_template('iframe_search.html', search_query=search_query, stubhub=True)

@app.route("/research/send_email")
def send_email():
    crawler.collect_upcomming_sales('./Upcoming_sales.txt')
    crawler.send_data_by_email('./Upcoming_sales.txt') 
    response = { 'status' : '200'} 
    return jsonify(response)


@app.route("/calendar", methods=['GET', 'POST'])
def calendar():
    if request.method == 'GET':
        return render_template('calendar.html')
    elif request.method == 'POST':
        if is_google_auth():
            http = get_credentials()
            service = build(serviceName='calendar', version='v3', http=http,
               developerKey='AIzaSyD4CyU_Y0ydHzD5zjMGmV7QjpwwHj62XUY')
            date = request.form['date']
            artist = request.form['artist']
            location = request.form['location']
            sale_type = request.form['sale_type']
            #print date + '-' + artist + '-' + location + '-' + sale_type
            google_API.create_calendar_event(service, date, artist, location, sale_type)
            return 'Done'
        else:
            return authenticate()
    else:
        return "Method not supported"

@app.route("/tickets/data")
def data(): 
    return render_template('data.html')

@app.route("/tickets/buy")
def buy():
    return render_template('buy.html')

### METHODS FOR API AUTHENTICATIONS
@app.route("/auth")
def calendar_auth():
    authenticate(request.args)
    return 'BOOOM CHAKALAKA'

#### UTILITY METHODS ####
def is_google_auth():
    storage = Storage('googleAPI.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        return None
    else:
        return True

def get_credentials():
    storage = Storage('googleAPI.dat')
    credentials = storage.get()
    http = httplib2.Http()
    http = credentials.authorize(http)
    return http


def authenticate(code=None):
    if code:
        credentials = FLOW.step2_exchange(code)
        store_credentials(credentials)
    else:
        auth_uri = FLOW.step1_get_authorize_url()
        return auth_uri

def store_credentials(credentials):
    storage = Storage('googleAPI.dat')
    storage.put(credentials)



#####################################################################################################################

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run()