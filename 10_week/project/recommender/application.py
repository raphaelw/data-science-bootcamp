from flask import Flask, render_template, request, send_from_directory, g
import os.path
from recommender import RecommenderCossim

app = Flask(__name__)
# here we construct a Flask object and __name__ sets the script to the root

def get_recommender():
    if 'recommender' not in g:
        g.recommender = RecommenderCossim()
    
    return g.recommender

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#@ symbol for decorator
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommender')
def recommender():
    title = request.args.getlist('movie_title')
    rating = request.args.getlist('movie_rating')

    #rating = request.args['movie_rating'] # to grab value using key from URL 
    user_ratings = dict(zip(title, rating))
    print(user_ratings)

    matched_movies, recommendations = get_recommender().recommend_from_ratings(user_ratings, k=5)

    return render_template('recommender.html', recommendations=recommendations, matched_movies=matched_movies)


if __name__ == "__main__":
    # init classifier in g-object
    # -> https://flask.palletsprojects.com/en/2.0.x/appcontext/#storing-data
    
    # runs app and debuging=True ensures that  we make changes when the web server restarts.
    app.run(debug=True, port=5000)

