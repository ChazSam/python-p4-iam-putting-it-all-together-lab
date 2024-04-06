#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        password = request.get_json().get('password')

        user = User(
        username = request.get_json().get('username'),
        image_url = request.get_json().get('image_url'),
        bio = request.get_json().get('bio')
        )

        user.password_hash = password 

        try:
            session['user_id'] = user.id
            db.session.add(user)
            db.session.commit()

            return user.to_dict(), 201

        except:
            return {'message': "Unprocessable Entity"}, 422

class CheckSession(Resource):
    
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return {'message': '401: Not Authorized'}, 401

class Login(Resource):
    
    def post(self):
        user = User.query.filter(
            User.username == request.get_json()['username']
        ).first()

        if not user:
            return {'error': 'Unauthorized'}, 401
        
        session['user_id'] = user.id
        return user.to_dict()


class Logout(Resource):

    def delete(self): 

        if not session['user_id']:
            return {'error': 'Unauthorized'}, 401

        session['user_id'] = None
        return {'message': '204: No Content'}, 204

class RecipeIndex(Resource):
    def get(self):

        if session['user_id']:
            user = User.query.filter(User.id == session['user_id']).first()


            recipe = [recipe.to_dict() for recipe in user.recipes]
            return recipe, 200

        return {'error': 'Unauthorized'}, 401


    def post(self):
        
        recipe = Recipe(
    
        title = request.get_json()['title'],
        instructions = request.get_json()['instructions'],
        minutes_to_complete = request.get_json()['minutes_to_complete'],
        user_id = session['user_id']   
            )
        
        try:
            db.session.add(recipe)
            db.session.commit()

            return recipe.to_dict(), 201

        except:
            return {'message': "Unprocessable Entity"}, 422

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)