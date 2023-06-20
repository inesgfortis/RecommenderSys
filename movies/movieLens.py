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

    RATINGS_PATH = '../preprocessing/small-dataset/ratings.csv'
    MOVIES_PATH = '../preprocessing/small-dataset/movies.csv'
    
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

    
    def getMostRated(self):
        """
        This function calculates the rankings of movies based on the number of ratings they have received.

        Returns:
            dict: A dictionary containing movie rankings based on the number of ratings received.
        """

        ratings = {}  # Dictionary to store the count of ratings for each movie
        rankings = {}  # Dictionary to store the rankings of movies

        # Count the number of times each movie has been rated
        for i in range(len(self.ratings)):
            movieID = self.ratings['movieId'][i]
            if movieID in ratings:
                ratings[movieID] += 1
            else:
                ratings[movieID] = 1

        # Sort the movies according to the number of ratings received
        rank = 1
        for movieID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[movieID] = rank
            rank += 1

        return rankings
  
    
    def getYears(self):
        years = defaultdict(int)
        for i in range(0,len(self.movies),1):
            movieID = self.movies['movieId'][i]
            year = self.movies['year'][i]
            if year:
                years[movieID] = year
        return years
    
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
 

    def filterMoviesByGenres(self,movie_title):
        
        # Determine which are the genres associated to the reference movie
        movie_id = self.name_to_movieID[movie_title]
        desired_genre_ids = self.movies_genres[movie_id]

        # Filter the dataframe to include only the movies that contain at least one of the desired genres
        mask = [any(self.movies_genres[int(movie_id)][gid] for gid in desired_genre_ids) 
                for movie_id in self.movies['movieId'].astype(int)]
        filtered_df = self.movies[mask]

        return filtered_df

    

    def getPreferences(self, userId, k):
        """
        Get the top k movies with the highest ratings and the bottom k movies with the lowest ratings for a given userId.

        Args:
            userId (int): The ID of the user.
            k (int): The number of top and bottom movies to retrieve.

        Returns:
            top_movies (pandas.DataFrame): The DataFrame with the top k movies with highest ratings, including movie names.
            bottom_movies (pandas.DataFrame): The DataFrame with the bottom k movies with lowest ratings, including movie names.
        """

        # Filter ratings for the specified userId
        user_ratings = self.ratings[self.ratings['userId'] == userId].copy()
        
        # Add columns 'title' and 'genres' and remvove columns 'year' and 'timestamp'
        user_ratings = pd.merge(user_ratings,self.movies, on='movieId')
        user_ratings = user_ratings.drop(columns=['year', 'timestamp'])
        
        # Reorder the columns
        user_ratings = user_ratings[['userId','movieId','title','rating','genres']]

        # Sort movies by rating in descending order
        sorted_movies = user_ratings.sort_values(by='rating', ascending=False)

        # Get the top k movies with highest and lowest ratings
        top_movies = sorted_movies.head(k).copy()
        bottom_movies = sorted_movies.tail(k).copy()  

        return top_movies, bottom_movies

