# -*- coding: utf-8 -*-
#!/usr/bin/env python27

from findARestaurant import findARestaurant
from database_setup import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

reload(sys)
sys.setdefaultencoding('utf8')


foursquare_client_id = 'QJZVRPS4IUK4CRDAPQUQMMCYX5N5OBC22N2J43YZVWZX2RV4'
foursquare_client_secret = 'GBLKKUNFWF2NSQJ04EXEGHCBE1EEVUO1GTFQOK3EGGDAF1QL'
google_api_key = 'AIzaSyApIVwdVD88sZsq2ePBgN5U-u0f8piwnCw'

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/restaurants', methods=['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        return getAllRestaurants()

    elif request.method == 'POST':
        mealType = request.args.get('mealType', '')
        location = request.args.get('location', '')

        restaurant = findARestaurant(mealType, location)

        name = restaurant['name']
        address = restaurant['address']
        image = restaurant['image']

        return newRestaurant(name, address, image)



@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
        pass
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass



def getAllRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])

def newRestaurant(name, address, image):
    restaurant = Restaurant(restaurant_name=name,
                            restaurant_address=address,
                            restaurant_image=image)

    session.add(restaurant)
    session.commit()

    return jsonify(Restaurant=restaurant.serialize)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
