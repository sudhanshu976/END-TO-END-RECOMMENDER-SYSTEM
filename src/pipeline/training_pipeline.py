import sys
sys.path.append(r'E:\RECIPE RECOMMENDER MLOPS')
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTrainer
import os

if __name__ == "__main__":
    # Check if processed_data.csv already exists in the artifacts folder
    processed_data_path = 'artifacts/processed_data.csv'
    if not os.path.isfile(processed_data_path):
        # If the file doesn't exist, perform data ingestion
        data_ingestion = DataIngestion()
        data_ingestion.read_data()
        data_ingestion.process_data()
        data_ingestion.save_artifacts()

    # Perform data transformation
    data_transformation = DataTransformation()
    data_transformation.load_data()
    data_transformation.transform_data()
    data_transformation.save_recipe()

    # Perform model training
    model_trainer = ModelTrainer()
    tags = model_trainer.preprocess_data()
    vector, similarity = model_trainer.train_model(tags)
    model_trainer.save_artifacts(similarity)