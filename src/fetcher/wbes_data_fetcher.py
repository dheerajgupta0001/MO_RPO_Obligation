from typing import List
import requests
import datetime as dt

class SectionWbesDataFetcher():
    def __init__(self,user:str, password:str) -> None:
        """constructor   
        """
        self.user = user
        self.password = password
    
    # def makeApiCall(self, dateKey:dt.datetime, acronymName:str, parameterName):
    #     dateStr = dt.datetime.strftime(dateKey, '%d-%m-%Y')
    #     url = f'https://wbes.wrldc.in/WebAccess/GetFilteredSchdData?USER={self.user}&PASS={self.password}&DATE={dateStr}&ACR={acronymName}'
    #     resp = requests.get(url)
    #     if not resp.status_code == 200:
    #         print(resp.status_code)
    #         print("unable to get data from wbes api")
    #         return []
    #     respJson = resp.json()
    #     paramsData = respJson["groupWiseDataList"][0]["fullschdList"][parameterName].split(',')
    #     if len(paramsData) == 0:
    #         return []
    #     return paramsData
    def makeApiCall(self, dateKey:dt.datetime, acronymName:str):
        dateStr = dt.datetime.strftime(dateKey, '%d-%m-%Y')
        url = f'https://wbes.wrldc.in/WebAccess/GetFilteredSchdData?USER={self.user}&PASS={self.password}&DATE={dateStr}&ACR={acronymName}'
        resp = requests.get(url)
        if not resp.status_code == 200:
            print(resp.status_code)
            print("unable to get data from wbes api")
            return []
        respJson = resp.json()
        paramsData = respJson["groupWiseDataList"][0]["fullschdList"]
        if len(paramsData) == 0:
            return []
        return paramsData
    
    # def generateTimestampDay(self, dateKey:dt.datetime): 
    #     startTime = dateKey.replace(hour=0,minute=0, second=0)
    #     endTime = startTime+ dt.timedelta(hours=23, minutes=45)
    #     timestampList = []

    #     currTime = startTime
    #     while currTime<=endTime:
    #         timestampList.append(str(currTime))
    #         currTime = currTime + dt.timedelta(minutes=15)
    #     return timestampList

    # def zipTwoList(self, list1:List, list2:List ):
    #     return list(zip(list1, list2))

    # def fetchDataWbesApi(self, startDate:dt.datetime, endDate:dt.datetime):
    #     currDate = startDate
    #     rrasScedData =[]
    #     while currDate<=endDate:
    #         currStateData = self.makeApiCall(currDate, 'MP_State', 'SCED')
    #         rrasData = self.makeApiCall(currDate, 'VAE_WR', 'RRAS')
    #         timestampList = self.generateTimestampDay(currDate)
    #         scedListTuple= self.zipTwoList(timestampList, currStateData)
    #         rrasListTuple= self.zipTwoList(timestampList, rrasData)
    #         rrasScedData.append({'rras':rrasListTuple, 'sced':scedListTuple, 'dateKey':str(currDate.date())})
    #         currDate = currDate+dt.timedelta(days=1)

    #     return rrasScedData
    