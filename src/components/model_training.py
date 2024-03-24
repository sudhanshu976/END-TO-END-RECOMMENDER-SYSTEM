import sys
sys.path.append(r'E:\RECIPE RECOMMENDER MLOPS')
from src.logger.logger import logging
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class ModelTrainer:
    def __init__(self, input_path='artifacts/recipe.csv', output_path='artifacts/'):
        self.input_path = input_path
        self.output_path = output_path

    def preprocess_data(self):
        try:
            # Load the dataset
            recipe = pd.read_csv(self.input_path)

            # Convert list of strings to a single string and lowercase them
            recipe['tags'] = recipe['tags'].apply(lambda x: ' '.join(eval(x)).lower())

            # Stemming of words
            ps = PorterStemmer()
            recipe['tags'] = recipe['tags'].apply(lambda x: " ".join([ps.stem(word) for word in x.split()]))

            # Save preprocessed data to CSV
            recipe.to_pickle("artifacts/recipes.pkl")
            logging.info(" Recipe Pickle File saved to artifacts/recipes.pkl folder")


            return recipe['tags']

        except Exception as e:
            logging.error("Error preprocessing data: %s", str(e))
            raise e

    def train_model(self, tags):
        try:
            # Create CountVectorizer
            cv = CountVectorizer(max_features=5000, stop_words='english')

            # Fit and transform data
            vector = cv.fit_transform(tags).toarray()

            # Calculate similarity matrix
            similarity = cosine_similarity(vector)

            return vector, similarity

        except Exception as e:
            logging.error("Error training model: %s", str(e))
            raise e

    def save_artifacts(self, similarity):
        try:

            similarity_file = os.path.join(self.output_path, 'similarity.pkl')
            with open(similarity_file, 'wb') as f:
                pickle.dump(similarity, f)
            logging.info("Similarity artifacts saved to %s, Size: %.2f KB", similarity_file, os.path.getsize(similarity_file) / 1024.0)

        except Exception as e:
            logging.error("Error saving artifacts: %s", str(e))
            raise e

if __name__ == "__main__":
    # Initialize ModelTrainer
    model_trainer = ModelTrainer()

    try:
        # Preprocess data
        tags = model_trainer.preprocess_data()

        # Train model
        vector, similarity = model_trainer.train_model(tags)

        # Save artifacts
        model_trainer.save_artifacts(similarity)

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
