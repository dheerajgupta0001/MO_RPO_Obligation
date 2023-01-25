import json
from typing import List
import pandas as pd

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
    return fileMappingsDf

def getFileMappings():
    global fileMappingsDf
    return fileMappingsDf

