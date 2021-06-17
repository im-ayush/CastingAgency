import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *

# To configure the order in which tests will be executed
unittest.TestLoader.sortTestMethodsUsing = None

# Bearer Token
# Replace the token string with your own token
token = "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1sYmdQSmhkMU9BejB4dVY2WnhfaCJ9.eyJpc3MiOiJodHRwczovL2F1dGgwdHJpYWxzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGMwMWRkMDhiYzczZDAwNzAwNDhlZDkiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9hdXRoMHRyaWFscy51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjIzNjM3MDcwLCJleHAiOjE2MjM3MjM0NzAsImF6cCI6IjFXdmxIWDJ5dUZZQmtwUkdnU2lVSHFOcjA2YWlUbHBYIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBnZXQ6YWN0b3JzIGdldDptb3ZpZXMgcG9zdDphY3RvcnMgcG9zdDptb3ZpZXMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBkZWxldGU6YWN0b3JzIGRlbGV0ZTptb3ZpZXMiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.aGdNBc5HoC4HJIUqMjr62CFs7PW4GFG-Nd9EFodS2gSv0Ou90PhgWaRuxNGmKCB6WpC6ZWTMebUkd0yxDF5zOBp4ryTSXelHt9ecuCNjx2mvZZI0H6Kh1IaE9qEkhe568etKTi1ved4DV6a1Bzxi6MC2220XJkM3L3Cc9RSKZ7kIDZHhYmPqytJJPHnMexKUCQATnFeY1CMzc0WgZip21bxLHuQI5p7XNsh6D3eDmPdFkmKHy6XNd14h82kvhwfm0Jdn7NG3msC7QL9gwTqWA-p4o5OrThLWr5W_eTVH18aUeP8J8kJnrLqEEx13M9b-In-FXs3vW5JW5UdNITG2WA"

class AgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{user}:{password}@{host}/{database}".format(
                                                                user='postgres',
                                                                password='ayush882',
                                                                host='localhost:5432',
                                                                database=self.database_name,
                                                                )
        setup_db(self.app, self.database_path)
        db.drop_all()
        db.create_all()

        movie = Movie(
        release_date = "2 Jan 2022",
        title = "TM",
        )
        movie.insert()

        actor = Actor(
        age = "23",
        gender = "F",
        name = "TA",
        )
        actor.insert()

        self.new_movie =  {
        "release_date": "2025-06-07",
        "title": "XYZ",
        }

        self.updated_movie_details =  {
        "release_date": "2025-06-07",
        "title": "XYZ Returns"
        }

        self.new_actor = {
        "age": "45",
        "gender": "M",
        "name": "ABCDE"
        }

        self.updated_actor_details = {
        "age": "24",
        "name": "ABCDZ"
        }

        self.invalid_movie =  {
        "release_date": "2025-06-07"
        }

        self.invalid_actor = {
        "name": "ABCDE"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    # Use the token with producer role permissions to test the endpoints
    # Authorization can be tested with seperate Authorization tests
    """
    # -------------------------------------------------------------------------
    # Authorization Tests
    # -------------------------------------------------------------------------
    # def test_auth_assistant(self):
    #     response = self.client().get(
    #                                 '/movies',
    #                                 headers={"Authorization":token}
    #                                 )
    #     data = json.loads(response.data)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #
    # def test_401_auth_assistant(self):
    #     response = self.client().post(
    #                             '/movies',
    #                             json=self.new_movie,
    #                             headers={"Authorization":token}
    #                             )
    #     data = json.loads(response.data)
    #
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #
    # def test_auth_director(self):
    #     response = self.client().post(
    #                             '/actors',
    #                             json=self.new_actor,
    #                             headers={"Authorization":token}
    #                             )
    #     data = json.loads(response.data)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #
    # def test_401_auth_director(self):
    #     response = self.client().post(
    #                             '/movies',
    #                             json=self.new_movie,
    #                             headers={"Authorization":token}
    #                             )
    #     data = json.loads(response.data)
    #
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #
    # def test_auth_producer_post_movie(self):
    #     response = self.client().post(
    #                             '/movies',
    #                             json=self.new_movie,
    #                             headers={"Authorization":token}
    #                             )
    #     data = json.loads(response.data)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #
    # def test_auth_producer_post_actor(self):
    #     response = self.client().post(
    #                             '/actors',
    #                             json=self.new_actor,
    #                             headers={"Authorization":token}
    #                             )
    #     data = json.loads(response.data)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # Endpoints Test (Can be tested using producers' access Token)
    # ------------------------------------------------------------------------

    # ========================================================================
    #  MOVIE Endpoints Tests
    # ========================================================================
    """MOVIES POST"""
    def test_create_movie(self):
        response = self.client().post(
                                '/movies',
                                json=self.new_movie,
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])

    def test_422_create_movie(self):
        response = self.client().post(
                                '/movies',
                                json=self.invalid_movie,
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    """MOVIES GET"""
    def test_get_movies(self):
        response = self.client().get(
                                '/movies',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_404_sent_requesting_invalid_page(self):
        response = self.client().get(
                                '/movies?page=999',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """MOVIES GET (with ID)"""
    def test_get_movie_details(self):
        response = self.client().get(
                                '/movies/1',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        """
        movie might not have actors casted yet
        In such case data['actors'] and data['total_actors'] will be evaluated
        as False
        """
        # self.assertTrue(data['actors'])
        # self.assertTrue(data['total_actors'])

    def test_404_get_movie_details(self):
        response = self.client().get(
                                '/movies/50',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """MOVIES PATCH"""
    def test_update_movie(self):
        response = self.client().patch(
                                '/movies/1',
                                json=self.updated_movie_details,
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])


    def test_404_update_movie(self):
        response = self.client().get(
                                '/movies/2',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """MOVIES DELETE"""
    def test_delete_movie(self):
        response = self.client().delete(
                                '/movies/1',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['total_movies'])
        self.assertTrue(data['deleted'])

    def test_404_delete_invalid_movie(self):
        response = self.client().delete(
                                '/movies/999',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # ========================================================================
    # ACTOR Endpoints Tests
    # ========================================================================

    """ACTORS POST"""
    def test_create_actor(self):
        response = self.client().post(
                                '/actors',
                                json=self.new_actor,
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])

    def test_422_create_actor(self):
        response = self.client().post(
                                '/actors',
                                json=self.invalid_actor,
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    """ACTORS GET"""
    def test_get_actors(self):
        response = self.client().get(
                                '/actors',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_invalid_page(self):
        response = self.client().get(
                                '/actors?page=999',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """ACTORS GET (with ID)"""
    def test_get_actor_details(self):
        response = self.client().get(
                                '/actors/1',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        """
        actor might not have any movie
        In such case data['movies'] and data['total_movies'] will be evaluated
        as False
        """
        # self.assertTrue(data['movies'])
        # self.assertTrue(data['total_movies'])

    def test_404_get_actor_details(self):
        response = self.client().get(
                                '/actors/99',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """ACTORS PATCH"""
    def test_update_actor(self):
        response = self.client().patch(
                                '/actors/1',
                                json=self.updated_actor_details,
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])

    def test_404_update_actor(self):
        response = self.client().get(
                                '/actors/999',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """ACTORS DELETE"""
    def test_delete_actor(self):
        response = self.client().delete(
                                '/actors/1',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['total_actors'])
        self.assertTrue(data['deleted'])

    def test_404_delete_invalid_actor(self):
        response = self.client().delete(
                                '/actors/999',
                                headers={"Authorization":token}
                                )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
