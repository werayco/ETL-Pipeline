import requests
import json
from http import HTTPStatus
from logger import logging
import pandas as pd
from sqlalchemy import create_engine


class ExtractTransformLoad:
    def __init__(self, api_url: str, file_name: str):
        """
        **API_URL**: this is the url to the api \n
        **File_Name**:  this is the name of your json response
        """
        self.api_url = api_url
        self.file_name = file_name


    def Extract(self):
        logging.info("Extracting data...")
        response = requests.get(self.api_url)

        if response.status_code == HTTPStatus.OK:
            logging.info("get data granted succesfully")
            data = response.json()

            with open(self.file_name, "w") as file:
                json.dump(data, file)
        return data


    def Transform(self):
        logging.info("Transforming Section")
        extrxt_data = self.Extract()

        df = pd.DataFrame(extrxt_data)
        logging.info("Dataframe created")

        df["domains"] = [",".join(map(str, i)) for i in df["domains"]]
        df["web_pages"] = [",".join(map(str, i)) for i in df["web_pages"]]

        df["id"] = range(len(df))

        logging.info("Transformation Done")
        return df

    def Load(self):
        dataframe_trans = self.Transform()
        engine = create_engine("mysql+mysqldb://root:Adeyungboi@localhost/base01")
        dataframe_trans.to_sql("etl_pracitice", engine, if_exists="replace")
        logging.info("Loading Done")


extractor = ExtractTransformLoad(
    "http://universities.hipolabs.com/search?country=United+States",
    "extracted_data.json",
)
extractor.Extract()
extractor.Transform()
extractor.Load()
