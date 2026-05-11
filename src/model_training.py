import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:
    """
    First perform model training and hyperparam tuning by running:  python src/model_training.py
    Then view all the tracked items by runnning: mlflow ui --backend-store-uri sqlite:///mlflow.db
    """
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Loading training data from: {self.train_path}")

            train_df = load_data(self.train_path)

            logger.info(f"Loading testing data from: {self.test_path}")

            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns = ["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns = ["booking_status"])
            y_test = test_df["booking_status"]            

            logger.info("Data successfully split for model training")

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Error occurred while loading the data {e}")
            raise CustomException("Failed to load the data", e)
    
    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Initialising LGBMClassifier and RandomizedSearcCV configuration")

            lgbm_model = lgb.LGBMClassifier(random_state = self.random_search_params["random_state"])

            random_search = RandomizedSearchCV(
                estimator= lgbm_model,
                param_distributions= self.params_dist,
                n_iter= self.random_search_params["n_iter"],   
                cv= self.random_search_params["cv"],
                n_jobs= self.random_search_params["n_jobs"],
                verbose= self.random_search_params["verbose"],
                random_state= self.random_search_params["random_state"],
                scoring= self.random_search_params["scoring"]
            )

            logger.info(f"Starting Hyperparameter tuning: n_iter={self.random_search_params['n_iter']}, "
                        f"cv={self.random_search_params['cv']}, scoring='{self.random_search_params['scoring']}'")            
            
            random_search.fit(X_train, y_train)

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info("Hyperparamter tuning completed successfully")
            logger.info(f"Best parameters found: {best_params}")

            logger.info("Returning the best LGBM model.")

            return best_lgbm_model

        except Exception as e:
            logger.error(f"Error encountered during LGBM training: {e}")
            raise CustomException("Failed to train model", e)
        
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Starting model evaluation on test dataset.")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)            
    
            logger.info(f"Evaluation Metrics calculated as: "
                        f"Accuracy= {accuracy:.4f}, "
                        f"Precision= {precision:.4f}, "
                        f"Recall= {recall:.4f}, "
                        f"F1-Score= {f1:.4f}")
            

            return {"accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1}

        except Exception as e:
            logger.error(f"Error encountered during model evaluation: {e}")
            raise CustomException("Failed to evaluate model ", e)
    
    def save_model(self, model):
        try:
            logger.info(f"Making sure directory exists for model path: {os.path.dirname(self.model_output_path)}")
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok= True)

            logger.info(f"Seralising and saving the model to: {self.model_output_path}")
            joblib.dump(model, self.model_output_path)

            logger.info("Model saved successfully to the local directory")

        except Exception as e:
            logger.error(f"Error occurred while saving the model: {e}")
            raise CustomException("Failed to save the model ", e)
    
    def run(self):
        try:
            '''
            NEW CODE FOR MLflow  
            '''
            mlflow.set_tracking_uri("sqlite:///mlflow.db")             
            mlflow.set_experiment("Hotel_Booking_Prediction")

            with mlflow.start_run():
                logger.info("Initiating Model training pipeline & MLFlow experimentation tracking")

                logger.info("Logging training & testing datasets as artifacts to MLFlow")
                mlflow.log_artifact(self.train_path, artifact_path= "datasets")
                mlflow.log_artifact(self.test_path, artifact_path= "datasets")

                logger.info("Loading and splitting data into training & testing sets")
                X_train, y_train, X_test, y_test = self.load_and_split_data()
                
                logger.info("Starting model training and hyperparameter tuning.")
                best_lgbm_model = self.train_lgbm(X_train, y_train)

                logger.info("Executing model evaluation.")
                metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)

                logger.info("Saving the best model locally")
                self.save_model(best_lgbm_model)

                logger.info(f"Logging model artifact to MLFlow from: {self.model_output_path}")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging model hyperparameters and evaluation metrics to MLFlow")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model Training and MLFlow logging completed successfully.")
        
        except Exception as e:
            logger.error(f"Error encountered in the model training pipeline: {e}")
            raise CustomException("Failed during the training pipeline", e)

if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()


