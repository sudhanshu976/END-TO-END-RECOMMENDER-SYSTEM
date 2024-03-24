import sys
sys.path.append(r'E:\RECIPE RECOMMENDER MLOPS')
from src.logger.logger import logging
import os
import pandas as pd


class DataTransformation:
    def __init__(self, input_path='artifacts/processed_data.csv', output_path='artifacts/recipe.csv'):
        self.input_path = input_path
        self.output_path = output_path

    def load_data(self):
        try:
            self.df = pd.read_csv(self.input_path)
            logging.info(f"Data loaded successfully from {self.input_path}. Shape: {self.df.shape}")
        except Exception as e:
            logging.error(f"Error loading data from {self.input_path}: {str(e)}")
            raise e

    def split_sentences_and_clean(self, input_string):
        """
        Function to split sentences at \n, remove full stops, punctuations, and empty spaces at the end of sentences, and convert them into a list.
        """
        if isinstance(input_string, float):
            input_string = str(input_string)
        sentences = input_string.split('\n')
        cleaned_sentences = [sentence.rstrip('.!? ').rstrip() for sentence in sentences]
        return cleaned_sentences

    def transform_data(self):
        try:
            logging.info("Transforming data...")
            self.df['directions'] = self.df['directions'].apply(self.split_sentences_and_clean)
            self.df['ingredients'] = self.df['ingredients'].apply(self.split_sentences_and_clean)
            self.df["tags"] = self.df["ingredients"] + self.df["directions"]
            self.recipe = self.df[['title', 'link', 'image-url', 'tags']]
            logging.info("Data transformation completed.")
        except Exception as e:
            logging.error(f"Error transforming data: {str(e)}")
            raise e

    def save_recipe(self):
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            self.recipe.to_csv(self.output_path, index=False)
            logging.info(f"Recipe dataset saved to: {self.output_path}")
        except Exception as e:
            logging.error(f"Error saving recipe dataset to {self.output_path}: {str(e)}")
            raise e

if __name__ == "__main__":
    data_transformation = DataTransformation()
    try:
        data_transformation.load_data()
        data_transformation.transform_data()
        data_transformation.save_recipe()
    except Exception as e:
        logging.exception("An error occurred during data transformation process:")

