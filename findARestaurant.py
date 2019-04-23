# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7


from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "PASTE_YOUR_ID_HERE"
foursquare_client_secret = "YOUR_SECRET_HERE"


def findARestaurant(mealType, location):
		# 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
		geocode = ("%s,%s" % (getGeocodeLocation(location)[0], getGeocodeLocation(location)[1]))

		# 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
		# HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

		client_id = "QJZVRPS4IUK4CRDAPQUQMMCYX5N5OBC22N2J43YZVWZX2RV4"
		client_secret = "GBLKKUNFWF2NSQJ04EXEGHCBE1EEVUO1GTFQOK3EGGDAF1QL"
		meal = mealType.replace(" ", "+")
		url = ("https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s&query=%s" % (
		client_id, client_secret, geocode, meal))

		h = httplib2.Http()
		result = json.loads(h.request(url, 'GET')[1])

		if result['response']['venues']:
			# 3. Grab the first restaurant
			restaurant = result['response']['venues'][0]
			restaurant_name = restaurant['name']
			restaurant_address = restaurant['location']['formattedAddress']
			address = ""
			for item in restaurant_address:
				address += item + " "
			restaurant_address = address
			restaurant_id = restaurant['id']
			# 4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture"
			url = ("https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20130815" % (restaurant_id, client_id, client_secret))
			result = json.loads(h.request(url, 'GET')[1])
			# 5. Grab the first image
			if result["response"]["photos"]["items"]:
				photo = result["response"]["photos"]["items"][0]
				prefix = photo["prefix"]
				suffix = photo["suffix"]
				imgUrl = prefix + "300x300" + suffix
			else:
				# 6. If no image is available, insert default a image url
				imgUrl = (
					"http://www.soidergi.com/wp-content/uploads/ca/thumb-cartoon-fast-food-restaurant-hamburger-vector-element.jpg")
			# 7. Return a dictionary containing the restaurant name, address, and image url
			restaurant_info = {"name": restaurant_name, "address": restaurant_address, "image": imgUrl}
			print "Restaurant Name: %s" % restaurant_info['name']
			print "Restaurant Address: %s " % restaurant_info['address']
			print "Image: %s" % restaurant_info["image"]
			print "\n \n"
			return restaurant_info

		else:
			print "No Restaurant Found for %s" % location
			return "Restaurant not Found"


if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney, Australia")
