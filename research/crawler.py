import requests
import json
import sys
from datetime import date
import smtplib
from email.mime.text import MIMEText
sys.path.append('C:\Users\Enrique Cruz\Documents\Columbia\Scalper')
from research.event_location import setup_locations

class Event():

    def __init__(self, date_available, venue_location, venue_name, event_name, url, sale_url, price, genre, sale_start, sale_end, sale_type, country='us'):
        self.date_available = date_available
        self.venue_location = venue_location
        self.venue_name = venue_name
        self.event_name = event_name
        self.price = price
        self.genre = genre
        self.sale_start = sale_start
        self.sale_end = sale_end
        self.sale_type = sale_type
        self.url = url
        self.sale_url = sale_url
        self.country = country

    def is_comming_soon(self, include_today=False):
        #parse current date
        current_date = str(date.today())
        today = current_date.split('-')
        current_year = 12
        #current_year = int(today[0])
        current_month = int(today[1])
        current_day = int(today[2])

        #
        if include_today:
            current_day -= 1
        date_info = self.get_sale_info()
        day = date_info[0]
        month = date_info[1]
        year = date_info[2]   
        
        #compare event date to current date
        if year >= current_year:
            if month > current_month:
                return True
            elif month == current_month:
                if day > current_day:
                   return True
                else:
                   return False
            else:
                return False
        else:
            return False

    def get_sale_type(self):
        if self.sale_type == '1':
            return 'Normal Sale'
        elif self.sale_type == '2':
            return 'Presale'
        else:
            return 'Sale Type Unknown'

    def get_sale_info(self):
        #parse event timestamp
        date_elems = self.sale_start.split('<br>')
        date = date_elems[0]
        time = date_elems[1]
        temp = date.split('/')
        #date month format varies by region
        if self.country=='us' or self.country=='ca':
            month = int(temp[0].split()[1])
            day = int(temp[1])
        else:
            day = int(temp[0].split()[1])
            month = int(temp[1])
        year = int(temp[2])
        return [day, month, year]

    def html_sanitize(self, word):
        sanitized = word.split('&#39;')
        if sanitized.__len__() == 1:
            return word
        else:
            return sanitized[0] + '\'' + sanitized[1]

    def __repr__(self):
        date = self.date_available.split('T')
        sale_date = self.sale_start.split('<br>')
        event_name = self.html_sanitize(self.event_name)
        str_rep =  'EVENT DATE:  ' + date[0] + "\n" 
        str_rep += 'ARTIST:      ' + event_name + "\n" 
        str_rep += 'VENUE:       ' + self.venue_name + "\n" 
        str_rep += 'LOCATION:    ' + self.venue_location + "\n" 
        str_rep += 'PRICE RANGE: ' + self.price + "\n" 
        str_rep += 'GENRE:       ' + self.genre + "\n" 
        str_rep += 'SALE START:  ' + sale_date[0] + ' at ' + sale_date[1] + "\n"
        str_rep += 'SALE TYPE:   ' + self.get_sale_type() + "\n"
        str_rep += 'ARTIST URL:  ' + self.url + "\n"
        str_rep += 'SALE URL:    ' + self.sale_url + "\n\n"
        return str_rep
        #return self.date_release

def get_sale_url(doc):
    minor_genre = doc['MinorGenreId']
    major_genre = doc['MajorGenreId']
    attraction_id = doc['AttractionId']
    event_id = doc['EventId']
    return str(event_id) + '?artistid=' + str(attraction_id[0]) + '&majorcatid=' + str(major_genre[0]) + '&minorcatid=' + str(minor_genre[0])

def get_events_data(event_list, event_location):
    #dict(cookies_are='working')
    reply = requests.get(event_location.url, cookies=event_location.cookies)
    json_contents = reply.content
    contents = json.loads(json_contents)
    response = contents['response']
    docs =  response['docs']
    #print docs[0].keys()
    
    for doc in docs:
        date_available = doc['OnsaleOn']
        location = doc['VenueCityState']
        venue = doc['VenueName'] 
        url = event_location.get_base_url() + doc['AttractionSEOLink'][0]
        sale_url = event_location.get_base_sale_url() +  get_sale_url(doc)
        event_name = doc['EventName']
        if doc.has_key('PriceRange'):
            price = doc['PriceRange']
        else:
            price = 'Unavailable'
        genre = doc['Genre'][0]

        #Try to fix the parsing error and eliminate the try catch block
        try:
            onsale_interval =  doc['PostProcessedData']['Onsales']['onsales'][0]['interval']
            start = onsale_interval['start']
            end = onsale_interval['end']
            sale_type = str(doc['PostProcessedData']['Onsales']['onsales'][0]['onsale_type'])
            event = Event(date_available, location, venue, event_name, url, sale_url, price, genre, start, end, sale_type, event_location.country)
            if event.is_comming_soon():
                event_list.append(event)

        except Exception as e:
            #print e
            None

def collect_upcomming_sales(output_file):
    locations = setup_locations()
    events = []
    for location in locations:
        get_events_data(events, location)

    output = open(output_file, 'w')
    output.write(str('UPCOMING SALES INFO\n\n'))
    output.write('TOTAL UPCOMIG SALES: ' + str(events.__len__()) + '\n\n')
    for e in events:
        try:
            output.write(str(e))
        except Exception as e:
                print e
                None
    print events.__len__()
    output.close()

def send_data_by_email(data_file):
    info = open(data_file, 'rb')
    email = MIMEText(info.read())
    info.close()
    #Compose the email
    today = str(date.today())
    sender = 'battistelcruzenrique@gmail.com'
    recipient_group = 'ssc-tickets@googlegroups.com'
    recipient1 = 'battistelcruzenrique@gmail.com'
    #recipient2 = 'msher09@gmail.com'
    #recipient3 = 'tylermsilver@gmail.com'
    email['Subject'] = '--' + today + '-- Upcoming Sales Info' 
    email['From'] = sender
    email['To'] = recipient_group
    #email['To'] = recipient1
    #Send Message
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    username = 'battistelcruzenrique'
    password = 'cowboyratman8'
    server.login(username,password)
    #for more recipients simply add to array
    #OFFICIAL ADRESS
    server.sendmail(sender, [recipient_group], email.as_string())
    #TESTING ADDRESS
    #server.sendmail(sender, [recipient1], email.as_string())
    server.quit()

if __name__ == "__main__":
    collect_upcomming_sales('./Upcoming_sales.txt')
    send_data_by_email('./Upcoming_sales.txt')

#POSIBLE USABLE FIELDS FOR EVENTS

    #doc['VenueCityState'] --> "Morgantown, WV",
    #doc['AttractionSEOLink'] --> [  "/Leon-Fleisher-tickets/artist/1072238" ],
    #doc['Type'] --> [ "Event" ],
    #doc['PurchaseDomain'] --> "1",
    #doc['DMAId'] --> [ 233,244,252,271,307,356,360,413 ],
    #doc['SearchableUntil'] --> "2012-07-06T03:59:59Z",
    #doc['EventStatus'] --> "3",
    #doc['Host'] --> """CH6",
    #doc['EventInternetRelease'] --> "2012-05-09T16:33:00Z",
    #doc['PostProcessedData']['Onsales']['unmodified_epdate'] --> null
    #doc['PostProcessedData']['Onsales']['expire'] --> "Thu, 07/05/12<br>07:00 PM"
    #doc['PostProcessedData']['Onsales']['event_date']['event_date_type'] --> 5
    #doc['PostProcessedData']['Onsales']['event_date']['date'] --> "Thu, 07/05/12<br>07:00 PM"
    #doc['PostProcessedData']['Onsales']['event_date']['date_range'] --> null
    #doc['PostProcessedData']['Onsales']['event_date']['suppress_time'] --> 0
    #doc['PostProcessedData']['Onsales']['event_date']['onsale_status'] --> "1"                                    
