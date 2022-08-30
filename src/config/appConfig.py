import json
from typing import List
import pandas as pd
# from src.typeDefs.appConfig import IAppConfig


# def getConfig(configFilename='config.xlsx'):
#     """
#     Get the application config from config.xlsx file
#     Returns:
#         IAppConfig: The application configuration as a dictionary
#     """

#     df = pd.read_excel(configFilename)
    
#     return df
# fileMappings = []
fileMappingsDf = pd.DataFrame()

jsonConfig: dict = {}

def initConfigs():
    loadJsonConfig()
    loadFileMappings()

def loadJsonConfig(fName="config.json") -> dict:
    global jsonConfig
    with open(fName) as f:
        data = json.load(f)
        jsonConfig = data
        return jsonConfig

def getJsonConfig() -> dict:
    global jsonConfig
    return jsonConfig

def loadFileMappings(filePath='input_wbes.xlsx'):
    global fileMappingsDf
    fileMappingsDf = pd.read_excel(filePath)
    # Convert Nan to None
    # fileMappings = fileMappingsDf.where(pd.notnull(fileMappings),None)
    # fileMappings = fileMappingsDf.to_dict('records')
    # return fileMappings
    return fileMappingsDf

def getFileMappings():
    global fileMappingsDf
    return fileMappingsDf

