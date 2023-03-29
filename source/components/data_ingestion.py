import os
import sys
from source.exception import Custom_Exception
from source.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass  # use to create class variables

from source.components.data_transformation import DataTransformation
from source.components.data_transformation import DataTransformationConfig


class DataIngestionConfig:
    train_data_path: str=os.path.join('artifact', 'train.csv') ## input data given, later train.csv data will get save over here by data ingestion
    test_data_path: str=os.path.join('artifact', 'test.csv') ## so those artifacts are folders and needs to be sved to a specific path
    raw_data_path: str=os.path.join('artifact', 'data.csv')
    
#now start data ingestion
@dataclass
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()  # class variable try to config the dataset
        
    def initiate_data_ingestion(self):  # this intent to read the dataset from the databases
        logging.info("Entered the data ingestion method or component")
        
        try:
            df=pd.read_csv('notebook\data\stud.csv') ## data to be reade any source such as api and mongoDB
            logging.info('Reade the dataset as dataframe')
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)## combining directory path
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True) 
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True) 
            logging.info("Ingestion of data is completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                
                
            )
        except Exception as e:
            raise Custom_Exception(e,sys) # type: ignore
        
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()


    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)
    
    
        