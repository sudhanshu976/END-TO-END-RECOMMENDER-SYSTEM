import pandas as pd
import pickle

class ModelTester:
    def __init__(self, recipe_file='artifacts/recipes.pkl', similarity_file='artifacts/similarity.pkl'):
        self.recipe_file = recipe_file
        self.similarity_file = similarity_file
        self.recipes = None
        self.similarity = None

    def load_data(self):
        with open(self.recipe_file, 'rb') as f:
            self.recipes = pickle.load(f)
        with open(self.similarity_file, 'rb') as f:
            self.similarity = pickle.load(f)

    def recommend(self, recipe_title):
        if self.recipes is None or self.similarity is None:
            self.load_data()
        index = self.recipes[self.recipes['title'] == recipe_title].index[0]
        distances = sorted(list(enumerate(self.similarity[index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:6]:
            print(self.recipes.iloc[i[0]]['title'])

if __name__ == "__main__":
    model_tester = ModelTester()
    model_tester.recommend("Masala Karela Recipe")
