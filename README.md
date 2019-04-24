
Guess what you like - Steam Game Recommender System

* Sample : Contain all the data (User id, playtime 2 weeks and playtime forever) we crawled from steam using steamAPI;

* Collaborate_Filtering.py：We use three methods to convert user playtime to rating for each specific game. The algorithm we used for computing and prediction user favourite game is user-based collaborate filter.
(There is no need for special environment setting if you already have python3 installed)

* Result.csv: The website is just a simple demo, so we did not build any back-end. Hence, to achieve ideal function on the front-end, we compute all the possible combinations of user game selection and generate the results

The website demo: https://hfaltgg.github.io/SteamGameRecommender.github.io/
