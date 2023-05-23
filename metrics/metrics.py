
from collections import defaultdict
import pandas as pd
import numpy as np

class evaluationMetrics:

    
    def __init__(self):
        pass
    
    
    def getTopN(self, predictions, n=10, minimumRating=4.0):
        """Returns the top N recommended movies for each user based on estimated ratings.

        Args:
            predictions (list of tuples): A list of predictions where each tuple contains a user ID,
                a movie ID, an actual rating, an estimated rating, and some additional information.
            n (int, optional): The number of top recommended movies to return for each user.
                Defaults to 10.
            minimumRating (float, optional): The minimum estimated rating for a movie to be considered
                a top recommendation. Defaults to 4.0.

        Returns:
            defaultdict: A defaultdict where the keys are user IDs and the values are lists of tuples,
                where each tuple contains a movie ID and its estimated rating. The length of each list
                is equal to the specified value of `n` or less if there are not enough movies that meet
                the minimum rating threshold.
        """
        topN = defaultdict(list)

        for userID, movieID, actualRating, estimatedRating, _ in predictions:
            if (estimatedRating >= minimumRating):
                topN[int(userID)].append((int(movieID), estimatedRating))

        for userID, ratings in topN.items():
            ratings.sort(key=lambda x: x[1], reverse=True)
            topN[int(userID)] = ratings[:n]

        return topN
    
    
    def getPrecision(self,predictions, k=10, threshold=3.5):
        """Returns precision at k metric for each user

        Args:
        predictions: list of tuples (uid, iid, true_r, est, _)
        k: int, the maximum number of recommended items to consider for each user
        threshold: float, the minimum estimated rating for an item to be considered relevant

        Returns:
        precisions: dict, a dictionary where each key is a user ID and the value is the precision@k score for that user
        """
        # First map the predictions to each user.
        user_est_true = defaultdict(list)
        for uid, _, true_r, est, _ in predictions:
            user_est_true[uid].append((est, true_r))

        precisions = dict()
        for uid, user_ratings in user_est_true.items():

            # Sort user ratings by estimated value
            user_ratings.sort(key=lambda x: x[0], reverse=True)

            # Number of recommended items in top k
            n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

            # Number of relevant and recommended items in top k
            n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                                  for (est, true_r) in user_ratings[:k])

            # Precision@K: Proportion of recommended items that are relevant
            # When n_rec_k is 0, Precision is undefined. We here set it to 0.

            precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0

        return precisions
    
    
    def getRecall(self,predictions, k=10, threshold=3.5):
        """Return recall at k metric for each user

        Args:
        predictions: list of tuples (uid, iid, true_r, est, _)
        k: int, the maximum number of recommended items to consider for each user
        threshold: float, the minimum estimated rating for an item to be considered relevant

        Returns:
        recalls: dict, a dictionary where each key is a user ID and the value is the recall@k score for that user
        """
        
        # First map the predictions to each user.
        user_est_true = defaultdict(list)
        for uid, _, true_r, est, _ in predictions:
            user_est_true[uid].append((est, true_r))

        recalls = dict()
        for uid, user_ratings in user_est_true.items():

            # Number of relevant items
            n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

            # Number of recommended items in top k
            n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

            # Number of relevant and recommended items in top k
            n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                                  for (est, true_r) in user_ratings[:k])

            # Recall@K: Proportion of relevant items that are recommended
            # When n_rel is 0, Recall is undefined. We here set it to 0.

            recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 0

        return recalls
    
    
    def predictionsToDataframe(self,predictions):
        """
        Convert a list of predictions into a pandas dataframe.

        Args:
        - predictions: a list of tuples (user_id, item_id, actual_rating, predicted_rating, _)

        Returns:
        - a pandas dataframe with columns "user_id", "item_id", "rating", "prediction", sorted by user_id and prediction
        """
        
        data = []
        for uid, iid, true_r, est_r, _ in predictions:
            data.append([uid,iid,true_r,est_r])

        df = pd.DataFrame(data, columns = ["user_id", "item_id","rating","prediction"])
        df.sort_values(["user_id","prediction"],inplace = True, ascending = [True,False])

        return df

    
    def getNDCG(self,predictions, k):
        """
        Compute the Normalized Discounted Cumulative Gain (NDCG) at k for each user in a pandas dataframe.

        Args:
        - df: a pandas dataframe with columns "user_id", "item_id", "rating", "prediction", sorted by user_id and prediction
        - k: the number of items to consider for computing the NDCG

        Returns:
        - a tuple (ndcgs, mean_ndcg), where:
          - ndcgs is a list of NDCGs (one for each user)
          - mean_ndcg is the average NDCG over all users
        """
        
        # Adapt the format of the model prediction output to df
        df_test = self.predictionsToDataframe(predictions)
        
        grouped = df_test.groupby('user_id')
        ndcgs = []
        for _, group in grouped:
            group = group.head(k)
            group.reset_index(inplace = True, drop = True)
            dcg = (group['rating'] / np.log2(group.index + 2)).sum()
            ideal = group.sort_values(by='rating', ascending=False)
            ideal.reset_index(inplace = True, drop = True)
            idcg = (ideal['rating'] / np.log2(ideal.index + 2)).sum()
            ndcgs.append(dcg / idcg)
            
        return ndcgs, np.mean(ndcgs)
    

    def getCoverage(self,topNrec, total_items, users):
        """
        Compute the item coverage of the recommendations.

        Args:
            topNrec (dict): A dictionary containing top-N recommendations for each user.
            total_items (int): Total number of unique items in the dataset.
            users (list): List of user IDs for whom the recommendations are generated.

        Returns:
            The item coverage of the recommendations as a ratio of unique recommended items to total items.
        """
        rec_items = []

        for user in users:
            rec_items += [pred[0] for pred in topNrec[user]]

        num_rec_items = len(set(rec_items))
        coverage = num_rec_items/total_items

        return coverage
    
    
    
    def getUserCoverage(self,topNPredicted, numUsers, ratingThreshold=0):
        """
        Calculate user coverage of recommended items.

        Args:
            topNPredicted: A dictionary where keys are user IDs and values are lists of tuples (item ID, predicted rating).
            numUsers: An integer indicating the total number of users in the dataset.
            ratingThreshold: A float indicating the minimum predicted rating required for an item to be considered as relevant.

        Returns:
            float indicating the proportion of users for whom at least one recommended item is relevant according to the rating threshold.
        """
        hits = 0
        for userID in topNPredicted.keys():
            hit = False
            for movieID, predictedRating in topNPredicted[userID]:
                if (predictedRating >= ratingThreshold):
                    hit = True
                    break
            if (hit):
                hits += 1

        user_coverage = hits / numUsers

        return user_coverage

    
    def getPopularity(self,trainset):
        """
        Calculate the popularity rank of movies in the training set based on the number of ratings received.

        Args:
        trainset: The training set in Surprise format.

        Returns:
        dict_popularity: A dictionary containing the popularity rank of each movie in the training set, 
                         where the key is the movie id and the value is its popularity rank.
        """
        # Convert the training set to a pandas DataFrame
        train_df = pd.DataFrame(trainset.all_ratings(), columns=['userid', 'movieid', 'rating'])
        train_df['userid'] = train_df['userid'].astype(int)
        train_df['movieid'] = train_df['movieid'].astype(int)

        # Count the number of ratings received by each movie
        interacciones = train_df['movieid'].value_counts()

        # Assign a popularity rank to each movie based on the number of ratings received
        dict_popularity = dict(zip(interacciones.index, range(1, len(interacciones) + 1)))

        return dict_popularity
    
    
    def getNovelty(self,topNPredicted, trainset):
        """
        Computes the novelty of the recommendations based on the popularity of the recommended items.

        Args:
        - topNPredicted: dictionary containing the top N predicted items for each user
        - trainset: the training set of the dataset

        Returns:
        - novelty: a float value representing the average popularity rank of the recommended items
        """
        # Define the popularity of films on the basis of the number of ratings received
        rankings = self.getPopularity(trainset)

        # Compute novelty
        n = 0
        total = 0
        for userID in topNPredicted.keys():
            for rating in topNPredicted[userID]:
                movieID = rating[0]
                rank = rankings[trainset.to_inner_iid(movieID)]
                total += rank
                n += 1

        novelty = total/n
        return novelty
    
    
    
    def addToMetricsDataframe(self,dataframe):
        """
        Appends rows from the input DataFrame to an existing metrics Excel file.
        If the file doesn't exist, creates a new metrics DataFrame with the required columns.

        Args:
            dataframe (pd.DataFrame): DataFrame containing the new metrics to be appended.

        Returns:
            None
        """
        # File path
        FILE_PATH = "metrics.xlsx"
        
        # Load existing metrics file or create a new one if it doesn't exist
        try:
            existing_metrics = pd.read_excel(FILE_PATH)
        except FileNotFoundError:
            existing_metrics = pd.DataFrame(columns=["Model", "RMSE", "MAE", "MAP", "MAR", "Mean_NDCG",
                                                     "Coverage", "User_Coverage", "Novelty"])

        # Append new rows to the existing metrics DataFrame
        updated_metrics = pd.concat([existing_metrics, dataframe], ignore_index=True)

        # Save the updated metrics DataFrame to the Excel file
        updated_metrics.to_excel(FILE_PATH, index=False)

