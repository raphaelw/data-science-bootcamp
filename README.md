# Data Science Bootcamp
My notebooks, learnings and results from a 12 week Data Science course at Spiced Academy


## Week 1: Data Wrangling

- __Machine Learning Workflow__: Steps how to approach a new dataset
- **Data wrangling** (pandas)
- Technical and design aspects of **plotting data** (matplotlib, seaborn)
- Descriptive statistics
- Pivoting / Wide and narrow data (pandas)

[**Project**](01_week/weekly_project/): Recreation of the famous animated scatterplot by Hans Rosling.

[**Presentation**](01_week/fizzbuzz_cleancode.ipynb): Essentials of clean code inspired by Uncle Bob (Robert C. Martin).


## Week 2: Classification Problem

- __Data exploration__, __cleaning__, __imputation__
- __Feature enginerring__
    - Encoding strategies e.g. one-hot, ordinal, etc
    - Polynomial and interaction terms
- Designing preprocessing __pipelines__ (sklearn)
- __Logistic regression__ in math and application (sklearn)
- __Evaluation__ of classifiers: Cross-Validation, Precision, Recall, F1-score

[**Project**](02_week/project/titanic_survival_prediction.ipynb): Titanic survival prediction ([kaggle competition](https://www.kaggle.com/c/titanic)) using basic feature engineering and logistic regression.

[**Presentation**](02_week/project/correlations.ipynb): About the different kinds of **correlations** (pearson, kendall & spearman).


## Week 3: Regression Problem

- Math and implementation of __gradient descent__ algorithm for linear regression.
- __Linear regression__
    - __Regularization__ strategies: Lasso (L1), Ridge (L2), ElasticNet
    - Model __evaluation__: R2 score
- Feature expansion
- __Hyperparameter optimization__ (sklearn)

[**Project**](03_week/project/bike_sharing_demand_kaggle.ipynb): Prediction of bike sharing demand ([kaggle competition](https://www.kaggle.com/c/bike-sharing-demand/)). Submission to kaggle.

[**Presentation**](03_week/project/loss_function_3d_plot.png): 3D surface plot using matplotlib to get an intuition on loss functions and the gradient descent approach.


## Week 4: Naive Bayes Classification and NLP

- __Naive Bayes__ classification
    - Theory
    - Application (sklearn)
- Natural Language Processing (NLP)
    - Vectorization of text: Bag-of-words, __TF-IDF__
- __Class balancing__ strategies
- Web scraping, parsing, regular expressions, scrapy

[**Project**](04_week/project/nlp_lyrics_classification.ipynb): Classification (Multinomial Naive Bayes) of a text phrase to a musical artist based on their lyrics.

[**Presentation**](04_week/lightning_talk/talk.ipynb): How I gathered lyrics data with an own [scraper](04_week/project/lyrics_scraping) based on scrapy.


## Week 5: Dashboards, Cloud & Databases

- Relational databases (__PostreSQL__), Data modeling, SQL (Python SQLAlchemy)
- __Cloud computing__ on AWS
    - Unix administration basics
    - Setup PostgreSQL on AWS
    - Setup Metabase dashboard on  AWS (EC2)

[**Project**](05_week/project/metabase_aws_hosted.png): Metabase dashboard deployed on AWS.

[**Presentation**](05_week/project/lyrics_graph.ipynb): Used lyrics data from week 4 to create a clustered [map](05_week/project/lyrics_map.pdf) of songs using the ForceAtlas2 algorithm available in Gephi. It uses physical modelling of masses and springs to visualize a graph. The approach failed most likely due to curse of dimensionality.


## Week 6: ETL Pipeline, Sentiment Analysis of Tweets

- Basics of __Sentiment Analysis__ (NLP)
- __ETL (Extract, Transform, Load)__ pipeline with __Docker Compose__
     - MongoDB NoSQL database
     - Web APIs (Twitter, Slack)

[**Project**](06_week/project): Processing pipeline fetching tweets in real time from Twitter for a given Keyword and perform a sentiment analysis on them. Pipeline: Fetch (_Extract_) tweets -> Store in MongoDB -> _Load_ new tweets -> Perform sentiment analysis (_Transform_) -> Store tweet along with sentiment score in PostgreSQL.

[**Presentation**](06_week/project): Debugging. What challenges I faced during the project and how I solved them.


## Week 7: Time Series

- __ARIMA__ Model, (Partial) autocorrelation function
- Evaluating Forecasts
- Statistical distribution functions

[**Project**](07_week/project/time_series_weather.ipynb): Manual step-by-step ARIMA modelling of weather data. Frequency analysis using signal processing techniques (Fourier transform).

[**Presentation**](07_week/project/time_series_weather.ipynb): Introduction to sonification of time series data.


## Week 8: Markov Chain Monte Carlo (MCMC)

- __Markov Chains__ & Monte Carlo simulations
- Linear Algebra
- __OpenCV__
- Software Design, OOP & Code Style

[**Project**](08_week/project): Simulation of an average day in a supermarket based on the data analysis of its customer data. Animated visualization using OpenCV of simulated customers.

[**Presentation**](08_week/project): Software design of the project.


## Week 9: Artificial Neural Networks & Deep Learning

- Feed-Forward Neural Networks
- Convolutional Neural Networks for Image Processing
- Backpropagation
- Transfer Learning
- Recurrent Neural Networks
- __Keras__ (TensorFlow Interface)

[**Project**](09_week): Image classification using transfer learning on a pretrained network (MobileNetV2).

[**Presentation**](09_week/exercises/backpropagation_thoughts.pdf): Understanding the backpropagation algorithm by using a graph approach of the chain rule.


## Week 10: Unsupervised Learning & Recommender Systems

- __Principal Component Analysis__ (PCA)
- t-SNE
- Non-negative Matrix Factorization (NMF)
- Nearest neighbour approaches
    - Clustering
    - Cosine similarity
- Web App
    - Python Flask, Jinja & Bootstrap
    - Deployment on Heroku

[**Project**](10_week/project/recommender): Movie recommender based on cosine similarity approach and a movie rating data set. See deployed web app at [mega-movie-recommender.herokuapp.com](https://mega-movie-recommender.herokuapp.com/)

[**Presentation**](10_week/project/cosine_similarity_recommendation.ipynb): Details of my approach for the movie recommender. 


## Week 11-12: Final Project

Topic Modelling on Bundestag Speeches (German Parliament). See [github.com/raphaelw/nlp-bundestag](https://github.com/raphaelw/nlp-bundestag)
