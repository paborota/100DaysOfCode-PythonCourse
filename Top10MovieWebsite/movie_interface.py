import requests


class MovieDBInterface:

    API_KEY = ""
    DB_URL = "https://api.themoviedb.org/3/"

    def query_movie_name(self, movie_name):

        url = self.DB_URL + "search/movie/"
        response = requests.get(url, params={'api_key': self.API_KEY, 'query': movie_name})

        return response.json()['results']

    def find_movie(self, movie_id):

        url = self.DB_URL + f"movie/{movie_id}"
        response = requests.get(url, params={'api_key': self.API_KEY})

        return response.json()