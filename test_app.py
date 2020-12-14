import os
import json
import unittest
import datetime
from models import Actor, Movie, setup_db, db
from app import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.producer = os.environ['PRODUCER']
        self.assistant = os.environ['ASSISTANT']
        self.director = os.environ['DIRECTOR']
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {
            "title": "New Movie",
            "release_date": datetime.date(2020, 10, 13)
        }

        self.new_bad_movie = {"release_date": datetime.date(2020, 10, 13)}

        self.new_bad_actor = {"age": 22, "gender": "female"}

        self.new_actor = {
            "name": "Updated Actor",
            "age": 22,
            "gender": "female"
        }

        self.updated_movie = {
            "title": "Updated Movie",
            "release_date": datetime.date(2020, 10, 14)
        }

        self.updated_actor = {
            "name": "Updated Actor",
            "age": 22,
            "gender": "female"
        }
        self.latest_movie = 0
        self.latest_actor = 0
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors_no_token(self):

        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Authorization header is expected.")

    def test_get_movies_no_token(self):

        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Authorization header is expected.")

    def test_get_actors(self):

        res = self.client().get(
            '/actors',
            headers={'Authorization': "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["actors"])
        self.assertTrue(len(data["actors"]))

    def test_get_movies(self):

        res = self.client().get(
            '/movies',
            headers={'Authorization': "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["movies"])
        self.assertTrue(len(data["movies"]))

    def test_assistant_post_movies(self):

        res = self.client().post(
            '/movies',
            headers={'Authorization': "Bearer {}".format(self.assistant)},
            json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "Unauthorized")
        self.assertEqual(data["description"], "No Permission")

    def test_assistant_post_actors(self):

        res = self.client().post(
            '/actors',
            headers={'Authorization': "Bearer {}".format(self.assistant)},
            json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "Unauthorized")
        self.assertEqual(data["description"], "No Permission")

    def test_assistant_delete_movies(self):

        res = self.client().delete(
            '/movies/1',
            headers={'Authorization': "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "Unauthorized")
        self.assertEqual(data["description"], "No Permission")

    def test_assistant_delete_actors(self):

        res = self.client().delete(
            '/actors/1',
            headers={'Authorization': "Bearer {}".format(self.assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "Unauthorized")
        self.assertEqual(data["description"], "No Permission")

    def test_assistant_update_movies(self):

        res = self.client().patch(
            '/movies/1',
            headers={'Authorization': "Bearer {}".format(self.assistant)},
            json=self.updated_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "Unauthorized")
        self.assertEqual(data["description"], "No Permission")

    def test_assistant_update_actors(self):

        res = self.client().patch(
            '/actors/1',
            headers={'Authorization': "Bearer {}".format(self.assistant)},
            json=self.updated_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "Unauthorized")
        self.assertEqual(data["description"], "No Permission")

# director

    def test_director_post_movies(self):  #should be unauthorized

        res = self.client().post(
            '/movies',
            headers={'Authorization': "Bearer {}".format(self.director)},
            json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "Unauthorized")
        self.assertEqual(data["description"], "No Permission")

    def test_director_post_actors(self):

        res = self.client().post(
            '/actors',
            headers={'Authorization': "Bearer {}".format(self.director)},
            json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["actors"])
        self.assertTrue(len(data["actors"]))

    def test_director_update_movies(self):

        res = self.client().patch(
            '/movies/1',
            headers={'Authorization': "Bearer {}".format(self.director)},
            json=self.updated_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_director_update_actors(self):

        res = self.client().patch(
            '/actors/2',
            headers={'Authorization': "Bearer {}".format(self.director)},
            json=self.updated_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_director_delete_movies(self):  #should be unauthorized

        res = self.client().delete(
            '/movies/1',
            headers={'Authorization': "Bearer {}".format(self.director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "Unauthorized")
        self.assertEqual(data["description"], "No Permission")

    def test_director_delete_actors(self):

        res = self.client().delete(
            '/actors/1',
            headers={'Authorization': "Bearer {}".format(self.director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

# producer

    def test_producer_post_movies(self):

        res = self.client().post(
            '/movies',
            headers={'Authorization': "Bearer {}".format(self.producer)},
            json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["movies"])
        self.assertTrue(len(data["movies"]))

    def test_producer_post_actors(self):

        res = self.client().post(
            '/actors',
            headers={'Authorization': "Bearer {}".format(self.producer)},
            json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["actors"])
        self.assertTrue(len(data["actors"]))

    def test_producer_update_movies(self):

        res = self.client().patch(
            '/movies/2',
            headers={'Authorization': "Bearer {}".format(self.producer)},
            json=self.updated_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_producer_update_actors(self):

        res = self.client().patch(
            '/actors/2',
            headers={'Authorization': "Bearer {}".format(self.producer)},
            json=self.updated_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_producer_delete_movies(self):

        res = self.client().delete(
            '/movies/3',
            headers={'Authorization': "Bearer {}".format(self.producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_producer_delete_actors(self):

        res = self.client().delete(
            '/actors/3',
            headers={'Authorization': "Bearer {}".format(self.producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_producer_post_bad_movies(self):

        res = self.client().post(
            '/movies',
            headers={'Authorization': "Bearer {}".format(self.producer)},
            json=self.new_bad_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])

    def test_producer_post_bad_actors(self):

        res = self.client().post(
            '/actors',
            headers={'Authorization': "Bearer {}".format(self.producer)},
            json=self.new_bad_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()