"""
Data Ingestion: 
the foundational process of collecting, transferring, and loading structured or unstructured data from diverse sources 
(APIs, databases, IoT, files) into a centralized repository like a data lake or warehouse for model training and analysis
    
"""

import os #for file operations
import sys #Here it used for system configuration fucntion
from src.exception import CustomException  #for custom exception handling, from designed in this project
from src.logger import logging # for logging the steps, from funciton designed in this project 

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass # decorator used for defining your class variable and taking the function of this classs in your classs further
#This class perform location specific tasks
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'raw.csv')
 
#This class do actual task for data ingestion
class DataIngestion:
    def __init__(self): # a constructor for intialization
        self.ingestion = DataIngestionConfig()  #Creating an object that contain the file paths location
        
    def initiate_data_ingestion(self):
        logging.info("Entered in the data ingestion method or component")
        try:
            df = pd.read_csv("/home/Rahul/Desktop/End_to_End_ML_Projects/Notebook/Data/StudentsPerformance.csv") #reading the dataset
            logging.info("Reading the dataset as dataframe")
            
            os.makedirs(os.path.dirname(self.ingestion.train_data_path), exist_ok = True) #making dir by taking artifacts
            df.to_csv(self.ingestion.raw_data_path, index = False, header = True) #Read the raw data from the source.
            
            logging.info("Train_test_split")
            train_set, test_set = train_test_split(df, test_size = 0.2, random_state = 45)
            
            train_set.to_csv(self.ingestion.train_data_path, index =False, header = True)
            
            test_set.to_csv(self.ingestion.test_data_path, index = False, header = True)
            
            logging.info("Data Ingestion is completed")
            
            return (
                self.ingestion.train_data_path, 
                self.ingestion.test_data_path)
        except Exception as e:
            raise CustomException(e,sys)
            
            
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data, test_data)
    
    
    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))