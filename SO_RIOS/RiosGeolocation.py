#from picamera import PiCamera,Color
#import httplib2 as http
#from urlparse import urlparse
import googlemaps
#from googlemaps import GoogleMaps


import json


class RiosGeolocation:

 def getGeolocation(self, address):


  gmaps = googlemaps.Client(key='AIzaSyC8RayL0qVmqFu9NFttSCT5FTEexBdCavQ')
  #gmaps = GoogleMaps('AIzaSyC8RayL0qVmqFu9NFttSCT5FTEexBdCavQ')


# Geocoding an address
  geocode_result = gmaps.geocode(address)
  #lat, lng = gmaps.address_to_latlng('1600 Amphitheatre Parkway, Mountain View, CA')
  #print lat, lng
  #headers = {
  #  'Content-Type': 'application/json'
  #}
  #url = "https://www.googleapis.com"
  #path = "/geolocation/v1/geolocate?key=AIzaSyBlDkJ8pIalNaVG339XB7jDIi8XM-T5_iU"
  #path = "/maps/api/geocode/json?sensor=false&address=" + address

  #target = urlparse(url+path)
  #method = 'GET'
  #body = ''
  
  #print target.geturl()

  #h = http.Http()

  #response, content = h.request(
  #      target.geturl(),
  #      method,
  #      body,
  #      headers)

# assume that content is a json reply
# parse content with the json module
  #data = json.loads(content)
  lat = geocode_result[0]['geometry']['location']['lat']
  lng = geocode_result[0]['geometry']['location']['lng']
  
  #print data
  #djson = json.loads(data)
  print lat
  print lng 
  return lat, lng #['coord']
