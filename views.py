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

        if restaurant != "No Restaurant Found":
            name = restaurant['name']
            address = restaurant['address']
            image = restaurant['image']

            return newRestaurant(name, address, image)
        else:
            return jsonify({"error":"No Restaurants Found for %s in %s" % (mealType, location)})



@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
        return getRestaurant(id)

    elif request.method == 'PUT':
        name = request.args.get("name", "")
        address = request.args.get("address", "")
        image = request.args.get("image", "")

        return updateRestaurant(id, name, address, image)

    elif request.method == 'DELETE':
        return deleteRestaurant(id)


def getAllRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[i.serialize for i in restaurants])


def newRestaurant(name, address, image):
    restaurant = Restaurant(restaurant_name=name,
                            restaurant_address=address,
                            restaurant_image=image)

    session.add(restaurant)
    session.commit()

    return jsonify(restaurant=restaurant.serialize)


def getRestaurant(id):

    restaurant = session.query(Restaurant).filter_by(id=id).one()

    return jsonify(restaurant=restaurant.serialize)


def updateRestaurant(id, name, address, image):

    restaurant = session.query(Restaurant).filter_by(id=id).one()

    if name:
        restaurant.name = name
    if address:
        restaurant.address = address
    if image:
        restaurant.image = image

    session.commit()

    return jsonify(restaurant=restaurant.serialize)

def deleteRestaurant(id):

    restaurant = session.query(Restaurant).filter_by(id=id).one()

    session.delete(restaurant)
    session.commit()

    return "Restaurant with id %s deleted" % id

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
