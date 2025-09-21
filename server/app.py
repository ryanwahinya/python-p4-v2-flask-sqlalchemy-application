# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
# set up to point to our existing database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#avoid building up too much unhelpful data in memory when our application is running.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app) #connects our database to our application before it runs.

@app.route('/') #determines which resources are available at which URLs and saves them to the application's URL map
def index():
    response = make_response(
        '<h1>Welcome to the pet directory!</h1>',
        200
    ) 
    return response
#Responses are what we return to the client after a request and make_response helps us with that. 
# It is a function that allows you to create an HTTP response object that you can customize before returning it to the client.
# It's a useful tool for building more complex responses, especially when you need to set custom headers, cookies, or other response attributes.
# The included response has a status code of 200, which means that the resource exists and is accessible at the provided URL.

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
       response_body = f'<p>{pet.name} {pet.species}</p>'
       response_status = 200

    else:
        response_body = f'<p>Pet {id} not found</p>'
        response_status = 404

    response = make_response(response_body, response_status)
    return response

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = Pet.query.filter_by(species=species).all() 
    #The species before the equal sign refers to the table column,
    #  while species after the equal sign refers to the route parameter.

    size = len(pets)
    response_body = f'<h2>There are {size} {species}s</h2>'
    for pet in pets:
        response_body += f'<p>{pet.name}</p>'
    response = make_response(response_body, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)