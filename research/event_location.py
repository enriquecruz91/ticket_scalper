#sys.path.append('C:\Users\Enrique Cruz\Documents\Columbia\Scalper')
from research import location_settings

#COUNTRY URLS
base_uk = 'http://www.ticketmaster.co.uk'
base_us = 'http://www.ticketmaster.com'
base_ca = 'http://www.ticketmaster.ca'
base_ir = 'http://www.ticketmaster.ie'
base_au = 'http://www.ticketmaster.com.au'
base_nz = 'http://www.ticketmaster.co.nz'
uk = 'http://www.ticketmaster.co.uk/json/browse/music?select=n93'
us = 'http://www.ticketmaster.com/json/browse/music?select=n93.json'
ca = 'http://www.ticketmaster.ca/json/browse/music?select=n93'
ir = 'http://www.ticketmaster.ie/json/browse/music?select=n93'
au = 'http://www.ticketmaster.com.au/json/browse/music?select=n93'
nz = 'http://www.ticketmaster.co.nz/json/browse/music?select=n93'

class US_Location():
    #location_settings = ['MARKET_NAME', 'MARKET_ID', 'NDMA']
    def __init__(self, location_settings, language='en-us'):
        self.country = 'us'
        self.url = 'http://www.ticketmaster.com/json/browse/music?select=n93'
        self.cookies = dict(
            MARKET_NAME=location_settings[0],
            MARKET_ID=location_settings[1],
            NDMA=location_settings[2],
            LANGUAGE=language
            ) 

    def get_base_url(self):
        return base_us

    def get_base_sale_url(self):
        return base_us + '/event/'


class Int_Location():

    def __init__(self, country, country_url, ndma):
        self.country = country
        self.url = country_url
        self.cookies = dict(NDMA=ndma)

    def get_base_url(self):
        if self.country == 'uk':
            return base_uk
        elif self.country == 'ca':
            return base_ca
        elif self.country == 'ir':
            return base_ir
        elif self.country == 'au':
            return base_au
        elif self.country == 'nz':
            return base_nz
        else:
            return '-- unsuported location --'
    
    def get_base_sale_url(self):
        if self.country == 'uk':
            return base_uk + '/event/'
        elif self.country == 'ca':
            return base_ca + '/event/'
        elif self.country == 'ir':
            return base_ir + '/event/'
        elif self.country == 'au':
            return base_au + '/event/'
        elif self.country == 'nz':
            return base_nz + '/event/'
        else:
            return '-- unsuported location --'

def setup_locations():
    #US LOCATIONS
    locations = []
    locations.append(US_Location(location_settings.los_angeles))
    locations.append(US_Location(location_settings.san_francisco))
    locations.append(US_Location(location_settings.NY_tristate))
    locations.append(US_Location(location_settings.philadelphia))
    locations.append(US_Location(location_settings.pittsburgh))
    locations.append(US_Location(location_settings.phoenix))
    locations.append(US_Location(location_settings.san_diego))
    locations.append(US_Location(location_settings.chicago))
    locations.append(US_Location(location_settings.indianapolis))
    locations.append(US_Location(location_settings.kansas_city))
    locations.append(US_Location(location_settings.new_orleans))
    locations.append(US_Location(location_settings.baltimore))
    locations.append(US_Location(location_settings.DC))
    locations.append(US_Location(location_settings.boston))
    locations.append(US_Location(location_settings.detroit))
    locations.append(US_Location(location_settings.saint_louis))
    locations.append(US_Location(location_settings.nebraska))
    locations.append(US_Location(location_settings.las_vegas))
    locations.append(US_Location(location_settings.charlotte))
    locations.append(US_Location(location_settings.cleveland))
    locations.append(US_Location(location_settings.columbus))
    locations.append(US_Location(location_settings.portland))
    locations.append(US_Location(location_settings.dallas))
    locations.append(US_Location(location_settings.houston))
    locations.append(US_Location(location_settings.austin))
    locations.append(US_Location(location_settings.san_antonio))
    locations.append(US_Location(location_settings.seattle))
    locations.append(US_Location(location_settings.milwaukee))
    #INTERNATIONAL LOCATIONS
    #locations.append(Int_Location('uk', uk, '99999')) #United Kingdom
    #locations.append(Int_Location('ir', ir, '345')) #Ireland
    locations.append(Int_Location('ca', ca, '527')) #Canada: Toronto, Hamilton & Southwestern Ontario
    locations.append(Int_Location('ca', ca, '522')) #Canada: Montreal and Surrounding Area
    locations.append(Int_Location('ca', ca, '519')) #Canada: Ottawa-Gatineau & Eastern Ontario
    locations.append(Int_Location('ca', ca, '505')) #Canada: Calgary & Southern Alberta
    locations.append(Int_Location('ca', ca, '528')) #Canada: B.C. Lower Mainland & Vancouver Island
    #locations.append(Int_Location('au', au, '705')) #Australia: Victoria/Tasmania
    #locations.append(Int_Location('au', au, '702')) #Australia: New South Wales/Australian Capital Territory
    #locations.append(Int_Location('au', au, '703')) #Australia: Queensland
    #locations.append(Int_Location('au', au, '704')) #Australia: Western Australia
    #locations.append(Int_Location('nz', nz, '751')) #New Zealand: North Island
    #locations.append(Int_Location('nz', nz, '752')) #New Zealand: South Island

    return locations