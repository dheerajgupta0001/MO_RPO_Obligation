import pandas as pd
import datetime
from src.fetcher.wbes_data_fetcher import SectionWbesDataFetcher
from src.config.appConfig import getJsonConfig
from src.repos.dailyDataCalculator import daywiseDataCalculator

logging = False
ans_total = {}
excelOutput = {}

def dailyDataHandler(state_name, start_date, end_date):
    currMonth = start_date.strftime("%B")
    currYear = start_date.strftime("%Y")
    # MONTH_NAME = 'May_2022.xlsx'
    MONTH_NAME = currMonth + "_" + currYear + ".xlsx"
    writer = pd.ExcelWriter(MONTH_NAME, engine='xlsxwriter')
    days = (end_date - start_date).days
    
    for curr_state in state_name:

        # cheack if "state" is present.
        if excelOutput.get(curr_state) == None:
            excelOutput[curr_state] = {}

        ans = {}
        ans_e = {}
        ans_total[curr_state] = {}

        for i in range(days + 1):

            curr_date = start_date + datetime.timedelta(days=i)
            ans[curr_date.strftime("%d-%m-%Y")] = {}
            ans_e[curr_date.strftime("%d-%m-%Y")] = {}

            wbesApiData = SectionWbesDataFetcher(
                getJsonConfig()['user'], getJsonConfig()['password'])

            currDateData = wbesApiData.makeApiCall(curr_date, curr_state)

            drawalParentAcronym = 'BuyerWBESParentStateAcronym'

            scheduleAmount = 'ScheduleAmount'

            CHECK = 'BuyerWBESParentStateAcronym'

            # Process Daywise data
            excelOutput[curr_state] = daywiseDataCalculator(
                excelOutput[curr_state], currDateData, curr_state, scheduleAmount, drawalParentAcronym)

            injectionParentAcronym = 'SellerWBESParentStateAcronym'

            excelOutput[curr_state] = daywiseDataCalculator(
                excelOutput[curr_state], currDateData, curr_state, scheduleAmount, injectionParentAcronym)
            
        transactionList = []
        # for state_name, state_data in excelOutput.items():
        for transaction_name, transaction_data in excelOutput[curr_state].items():
            new_transaction_dict = {}
            new_transaction_dict['transactionType'] = transaction_name
            for keyValue, data in transaction_data.items():
                new_transaction_dict[keyValue] = data/4000
            transactionList.append(new_transaction_dict)
            
        df = pd.DataFrame(transactionList)
        df ['solarNet'] = df['solarDrawal'] + df['solarInjection']
        df ['windNet'] = df['windDrawal'] + df['windInjection']
        df ['hydroNet'] = df['hydroDrawal'] + df['hydroInjection']
        df ['gdamNet'] = df['gdamDrawal'] + df['gdamInjection']
        df.to_excel(writer, sheet_name=curr_state)
        print("{} Processed".format(curr_state))
    writer.save()
    print("OK")
    return True, MONTH_NAME
