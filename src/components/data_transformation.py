"""
Data transformation is the process of converting raw data into a more suitable format or structure for analysis, to improve
 its quality and make it compatible with the requirements of a particular task or system.
 
 #feature engineering, model training are some of the purpose of the data transformation
"""

import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl') #path of preprocessor file path
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformer_object(self): #This function is responsible for data transformation.
        try:
            numerical_columns = ['writing score', 'reading score']
            categorical_columns = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course' ]
            
            num_pipeline = Pipeline(
                steps= [('imputer', SimpleImputer(strategy='median')),
                        ('scaler', StandardScaler())
                        
                        ]) # for handling missing values and data scaling
            cat_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehotencoder', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                         ]
                
                )
            logging.info('Categorical columns encoding completed')
            logging.info('Categorical columns encoding completed')
            
            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeling', cat_pipeline, categorical_columns)
                ])
            
            return preprocessor
        except Exception as e:  
            raise CustomException(e,sys)
            
            
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Reading train and test data is completed")
            logging.info("Obtaining the preprocessing object")
            
            
            preprocessing_obj = self.get_data_transformer_object() # Creating preprocesser as an object
            
            #creation of traget column
            target_column = "math score"
            #numerical_columns = ["writing_score", "reading_score"]

            
            input_features_train_df = train_df.drop(columns = [target_column],axis =1)
            target_feature_train_df = train_df[target_column]
            
            input_features_test_df = test_df.drop(columns = [target_column], axis =1)
            target_feature_test_df = test_df[target_column]
            
            logging.info("Apply preprocessing object on the training and test dataset")
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_features_test_df)
            
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)] #Concatenate the data according to column_wise
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            logging.info('Preprocessing Saved')
            
            #For converting preprocessor in pkl file for future prediction
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,               
                obj = preprocessing_obj
                ) 
            
            
            return(
                train_arr,
                test_arr, 
                self.data_transformation_config.preprocessor_obj_file_path
                )
        except Exception as e:
            raise CustomException(e,sys)