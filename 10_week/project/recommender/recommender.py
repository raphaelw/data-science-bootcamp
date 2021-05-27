"""
Contains recommondation implementation
"""

import os.path
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
from random import sample as random_sample

WEB_APP_DATA_ROOT = os.path.join(os.path.dirname(__file__),"data")

def clamp(x,mn,mx):
    """ clamp x to range of [mn,mx] """
    return min(max(mn,x),mx)

class RecommenderCossim:
    def __init__(self, movie_vecs_path=os.path.join(WEB_APP_DATA_ROOT,'movie_vectors.json')):
        movie_vectors = pd.read_json(movie_vecs_path)
        self.movie_similarities = pd.DataFrame(data=cosine_similarity(movie_vectors),
                                               columns=movie_vectors.index,
                                               index=movie_vectors.index)
        
    def recommend(self, raw_title, k=20, random_n=None):
        """
        Recommendation based on cosine similarity neighbours.

        Parameters
        ----------
        movie_similarities : pandas.DataFrame
            Cosine similarity matrix. Square shape. Columns and index are movie title strings.
        raw_title : str
            Movie title as raw user input. Matched with fuzzywuzzy.
        k : int
            How many of the most similar movies to consider.

        Returns
        -------
        matched_title, recommendations : str , list
        """
        matched_title = process.extractOne(raw_title, self.movie_similarities.index)[0]
        recommendations = self.movie_similarities[matched_title].sort_values(ascending=False)[1:k+1]
        if random_n is not None:
            recommendations = recommendations.sample(n=random_n)
        return matched_title, list(recommendations.index)

    def recommend_from_ratings(self, ratings, k=5):
        """
        ratings : dict
            Key is a raw movie title, value is a rating in range [1,5]
        k : int
            Number of recommendations

        Returns
        -------
        matched_movies, recommendations : dict, list
            matched_movies is like ratings dict
        """
        recommendation_pool = set()
        matched_movie_titles = {}
        for raw_movie_title, rating in ratings.items():
            rating_ = float(rating)
            rating = round(clamp(rating_, 1, 5))
            matched_title, recommendations = self.recommend(raw_movie_title, k=10)
            matched_movie_titles[matched_title] = rating_

            weight = clamp(rating*3, 1, len(recommendations))
            recommendation_pool.update( random_sample(recommendations, k=weight) )
        
        #print(recommendation_pool)
        recommendations = random_sample(recommendation_pool, k=k)
        return matched_movie_titles, recommendations
