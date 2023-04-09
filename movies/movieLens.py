# import os
# import csv
# import sys
# import re

# from surprise import Dataset
# from surprise import Reader

from collections import defaultdict
import numpy as np
import pandas as pd
import ast

class MovieLens:

    RATINGS_PATH = '../preprocessing/ratings.csv'
    MOVIES_PATH = '../preprocessing/movies.csv'
    
    # Dictionary to map movies' titles and IDs
    movieID_to_name = {}
    name_to_movieID = {}
    
    # Dataframes
    ratings = pd.DataFrame()
    movies = pd.DataFrame()
    
    # Dictionary that maps movie IDs to lists of genre IDs
    # For each movie, we have a list indicating whether the movie contains each genre or not.  
    movies_genres = defaultdict(list)
    
    # Dictionary that maps genres to their corresponding IDs."
    genre_to_genreID = {}
    
    def __init__(self):
        self.loadData()
        self.mapMovies()
        self.getGenres()
    
    def loadData(self):
        self.ratings = pd.read_csv(self.RATINGS_PATH)
        self.movies = pd.read_csv(self.MOVIES_PATH)
        # self.mapMovies()

    def mapMovies(self):
        for i in range(0,len(self.movies),1):
            movieID = self.movies['movieId'][i]
            movieName = self.movies['title'][i]
            self.movieID_to_name[movieID] = movieName  # add mapping to dictionary
            self.name_to_movieID[movieName] = movieID  # add mapping to dictionary
            
    def getMovieName(self, movieID):
        if movieID in self.movieID_to_name:
            return self.movieID_to_name[movieID]
        else:
            return ""
        
    def getMovieID(self, movieName):
        if movieName in self.name_to_movieID:
            return self.name_to_movieID[movieName]
        else:
            return 0
    
    def getUserRatings(self, userId):
        
        userRatings = []
        
        filtered_df = self.ratings[self.ratings['userId'] == userId]
        
        for i in range(0,len(filtered_df),1):
            movieID = filtered_df['movieId'][i]
            rating = filtered_df['rating'][i]
            userRatings.append((movieID, rating))

        return userRatings

    def getYears(self):
        years = defaultdict(int)
        for i in range(0,len(self.movies),1):
            movieID = self.movies['movieId'][i]
            year = self.movies['year'][i]
            if year:
                years[movieID] = year
        return years
    
#     def getPopularityRanks(self):
#         ratings = defaultdict(int)
#         rankings = defaultdict(int)
#         with open(self.ratingsPath, newline='') as csvfile:
#             ratingReader = csv.reader(csvfile)
#             next(ratingReader)
#             for row in ratingReader:
#                 movieID = int(row[1])
#                 ratings[movieID] += 1
#         rank = 1
#         for movieID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
#             rankings[movieID] = rank
#             rank += 1
#         return rankings
    
    def getGenres(self):
        
        """
        This function is in charge of completing the dictionary that maps movie IDs to lists of genre IDs (movies_genres)
        as well as the dictionary that maps genres to their corresponding IDs (genre_to_genreID)
        
        """
        
        # Assign an ID to the existing genres
        # Keep track of the number of genres
        maxGenreID = 0
        
        # Apply ast.literal_eval to each element of the column genres to transform it into a list
        self.movies['genres'] = self.movies['genres'].apply(ast.literal_eval)

        # Iterate over the rows of the dataframe
        for index, row in self.movies.iterrows():
            # Get the movie ID from the first column of the row
            movieID = row['movieId']
            # Get a list of genre names from the third column of the row
            genreList = row['genres']
            #print(type(genreList))

            # Create a list of genre IDs for the movie
            genreIDList = []
            # Loop over each genre
            for genre in genreList:
                # If we've seen this genre before, use its existing ID
                if genre in self.genre_to_genreID:
                    #print("Existing genre: "+genre)
                    genreID = self.genre_to_genreID[genre]
                    #print(self.genre_to_genreID)
                # Otherwise, create a new genre ID and add it to the dictionary
                else:
                    #print("New genre: "+genre)
                    genreID = maxGenreID
                    self.genre_to_genreID[genre] = genreID
                    maxGenreID += 1

                # Add the genre ID to the list of genre IDs for the movie
                genreIDList.append(genreID)

            # Add the list of genre IDs to the genres dictionary for the movie
            self.movies_genres[movieID] = genreIDList

        # Convert the integer-encoded genre lists to bitfields that we can treat as vectors
        for (movieID, genreIDList) in self.movies_genres.items():
            bitfield = [0] * maxGenreID
            for genreID in genreIDList:
                bitfield[genreID] = 1
                self.movies_genres[movieID] = bitfield   


    
#     def getMiseEnScene(self):
#         mes = defaultdict(list)
#         with open("LLVisualFeatures13K_Log.csv", newline='') as csvfile:
#             mesReader = csv.reader(csvfile)
#             next(mesReader)
#             for row in mesReader:
#                 movieID = int(row[0])
#                 avgShotLength = float(row[1])
#                 meanColorVariance = float(row[2])
#                 stddevColorVariance = float(row[3])
#                 meanMotion = float(row[4])
#                 stddevMotion = float(row[5])
#                 meanLightingKey = float(row[6])
#                 numShots = float(row[7])
#                 mes[movieID] = [avgShotLength, meanColorVariance, stddevColorVariance,
#                    meanMotion, stddevMotion, meanLightingKey, numShots]
#         return mes