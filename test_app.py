#This test unit was build to code the API Endpoint, it doesn't work with the Authorization
#There is a Postman collection to test the coded endpoints with Authentication

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""
    
    new_actor = {
        "name": "Leonardo Di Caprio",
        "age": 50,
        "gender": "male"
    }

    bad_actor = {
        "name": "Leonardo Di Caprio",
        "age": 50
    }

    new_movie = {
        "title": "Titanic",
        "release_date": 1993
    }

    bad_movie = {
        "title": "Titanic"
    }

    patch_bad_movie = {
    
    }

    patch_bad_actor = {
        
    }



    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres"
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        #binds the app to the current context

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    

    def test_patch_actor(self):
        first_actor = Actor.query.first().id
        
        res = self.client().patch('/actors/' + str(first_actor), json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_error(self):
        first_actor = Actor.query.first().id
        res = self.client().patch('/actors/' + str(first_actor), json=self.patch_bad_actor)
        
        self.assertEqual(res.status_code, 422)


    def test_patch_movie(self):
        first_movie = Movie.query.first().id
        res = self.client().patch('/movies/' + str(first_movie), json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie_error(self):
        first_movie = Movie.query.first().id
        res = self.client().patch('/movies/' + str(first_movie), json=self.patch_bad_movie)
        
        self.assertEqual(res.status_code, 422)


    def test_post_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_post_actor_error(self):
        res = self.client().post('/actors', json=self.bad_actor)
        self.assertEqual(res.status_code, 422)


    def test_post_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_post_movie_error(self):
        res = self.client().post('/movies', json=self.bad_movie)
        self.assertEqual(res.status_code, 422)

    def test_delete_actor(self):
        first_actor = Actor.query.first()

        res = self.client().delete('/actors/' + str(first_actor.id))
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == first_actor.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], first_actor.id)
        self.assertEqual(actor, None)

        self.client().post('/actors', json=self.new_actor)



    def test_delete_actor_error(self):
        res = self.client().delete('/actors/10000')

        self.assertEqual(res.status_code, 404)

    def test_delete_movie(self):
        first_movie = Movie.query.first()
        

        res = self.client().delete('/movies/' + str(first_movie.id))
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == first_movie.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], first_movie.id)
        self.assertEqual(movie, None)

        self.client().post('/movies', json=self.new_movie)
        

    def test_delete_movie_error(self):
        res = self.client().delete('/movies/10000')

        self.assertEqual(res.status_code, 404)

#TODO Two tests of RBAC for each role


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()