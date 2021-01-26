""" 
Function to reutun geocoded location cordinates from google geocoding API 
"""
import googlemaps


gmaps = googlemaps.Client(key)


def get_cord(addy):
	geocode_result = gmaps.geocode(addy)
	location = (geocode_result[0]['geometry']['location'])
	return (location.get("lat"), location.get('lng'))
