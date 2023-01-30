from src.config.appConfig import getFileMappings
import pandas as pd


def daywiseDataCalculator(currStateExceOutput, currDateData, currState, scheduleAmount, parentAcronymType):
    # get file config
    appConfig = getFileMappings()
    solar = appConfig['Solar'].dropna()
    
    hydroBefore = appConfig['Hydro Name Before 08_03_2019'].dropna()
    hydroAfter = appConfig['Hydro After 08_03_2019'].dropna()
    
    windBefore = appConfig['Wind Perc Before 31_03_2022'].dropna()
    windAfter = appConfig['Wind After 31_03_2022'].dropna()
    inputWbesDf = pd.read_excel('input_wbes.xlsx', sheet_name= 'New_input')

    for temp in currDateData:
        if temp[parentAcronymType] == currState:
            seller = temp['SellerAcr']
            scheduleType = temp['ScheduleTypeName']
            subScheduleType = temp['SubScheduleTypeName']
            ScheduleData = temp[scheduleAmount].split(',')
            ScheduleDataList = pd.Series(ScheduleData)
            scheduleDataSum = ScheduleDataList.astype('float').sum()
            # if scheduleType in ['ISGS', 'LTA', 'MTOA', 'REMC', 'IEX', 'PXI', 'STOA', 'GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX', 'RTM_IEX', 'RTM_PXI', 'RTM_HPX']:
            if scheduleType in ['ISGS', 'LTA', 'MTOA', 'REMC', 'STOA', 'GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX']:
                # if scheduleType == 'REMC' and subScheduleType in ['LTA', 'MTOA', 'IEX', 'PXI', 'STOA', 'GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX', 'RTM_IEX', 'RTM_PXI', 'RTM_HPX']:
                if scheduleType == 'REMC' and subScheduleType in ['LTA', 'MTOA', 'STOA', 'GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX']:
                    # cheack if "TRANSACTION TYPE" is present.
                    if currStateExceOutput.get(subScheduleType) == None:
                        # if subScheduleType not in currStateExceOutput[subScheduleType]:
                        currStateExceOutput[subScheduleType] = {
                            'solarDrawal': 0, 'solarInjection': 0, 'solarNet': 0,
                            'windDrawal before 31_03_2022': 0, 'windInjection before 31_03_2022': 0, 'windNet before 31_03_2022': 0,
                            'windDrawal after 31_03_2022': 0, 'windInjection after 31_03_2022': 0, 'windNet after 31_03_2022': 0,
                            'hydroDrawal  before 08_03_2019': 0, 'hydroInjection  before 08_03_2019': 0, 'hydroNet  before 08_03_2019': 0,
                            'hydroDrawal  after 08_03_2019': 0, 'hydroInjection  after 08_03_2019': 0, 'hydroNet  after 08_03_2019': 0,
                            'gdamDrawal': 0, 'gdamInjection': 0, 'gdamNet': 0
                        }
                    # BUYER WBESParentStateAcronym
                    if parentAcronymType == 'BuyerWBESParentStateAcronym':
                        if subScheduleType in ['GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX']:
                            currStateExceOutput[subScheduleType]['gdamDrawal'] += scheduleDataSum
                            
                        elif seller in set(solar):
                            currStateExceOutput[subScheduleType]['solarDrawal'] += scheduleDataSum

                        # wind part
                        elif seller in set(windBefore):
                            percValue = inputWbesDf.loc[inputWbesDf['Wind Before 31_03_2022'] == seller, 'Wind Perc Before 31_03_2022'].iloc[0]
                            currStateExceOutput[subScheduleType]['windDrawal before 31_03_2022'] += scheduleDataSum*percValue/100
                            
                        elif seller in set(windAfter):
                            percValue = inputWbesDf.loc[inputWbesDf['Wind After 31_03_2022'] == seller, 'Wind Perc After 31_03_2022'].iloc[0]
                            currStateExceOutput[subScheduleType]['windDrawal after 31_03_2022'] += scheduleDataSum*percValue/100

                        # hydro part
                        elif seller in set(hydroBefore):
                            percValue = inputWbesDf.loc[inputWbesDf['Hydro Name Before 08_03_2019'] == seller, 'Hydro Perc Before  08_03_2019'].iloc[0]
                            currStateExceOutput[subScheduleType]['hydroDrawal  before 08_03_2019'] += scheduleDataSum*percValue/100
                            
                        elif seller in set(hydroAfter):
                            percValue = inputWbesDf.loc[inputWbesDf['Hydro After 08_03_2019'] == seller, 'Hydro Perc After  08_03_2019'].iloc[0]
                            currStateExceOutput[subScheduleType]['hydroDrawal  after 08_03_2019'] += scheduleDataSum*percValue/100

                    # SELLER WBESParentStateAcronym
                    if parentAcronymType == 'SellerWBESParentStateAcronym':
                        if subScheduleType in ['GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX']:
                            currStateExceOutput[subScheduleType]['gdamInjection'] += -(scheduleDataSum)
                            
                        elif seller in set(solar):
                            currStateExceOutput[subScheduleType]['solarInjection'] += -(scheduleDataSum)
                            
                        # wind part
                        elif seller in set(windBefore):
                            percValue = inputWbesDf.loc[inputWbesDf['Wind Before 31_03_2022'] == seller, 'Wind Perc Before 31_03_2022'].iloc[0]
                            currStateExceOutput[subScheduleType]['windInjection before 31_03_2022'] += scheduleDataSum*percValue/100
                            
                        elif seller in set(windAfter):
                            percValue = inputWbesDf.loc[inputWbesDf['Wind After 31_03_2022'] == seller, 'Wind Perc After 31_03_2022'].iloc[0]
                            currStateExceOutput[subScheduleType]['windInjection after 31_03_2022'] += scheduleDataSum*percValue/100

                        # hydro part
                        elif seller in set(hydroBefore):
                            percValue = inputWbesDf.loc[inputWbesDf['Hydro Name Before 08_03_2019'] == seller, 'Hydro Perc Before  08_03_2019'].iloc[0]
                            currStateExceOutput[subScheduleType]['hydroInjection  before 08_03_2019'] += scheduleDataSum*percValue/100
                            
                        elif seller in set(hydroAfter):
                            percValue = inputWbesDf.loc[inputWbesDf['Hydro After 08_03_2019'] == seller, 'Hydro Perc After  08_03_2019'].iloc[0]
                            currStateExceOutput[subScheduleType]['hydroInjection  after 08_03_2019'] += scheduleDataSum*percValue/100
                            
                # except REMC schedules, this part handles
                else:
                    # cheack if "TRANSACTION TYPE" is present.
                    if currStateExceOutput.get(scheduleType) == None:
                        # if scheduleType not in currStateExceOutput[scheduleType]:
                        currStateExceOutput[scheduleType] = {
                            'solarDrawal': 0, 'solarInjection': 0, 'solarNet': 0,
                            'windDrawal before 31_03_2022': 0, 'windInjection before 31_03_2022': 0, 'windNet Before_31_03_2022': 0,
                            'windDrawal after 31_03_2022': 0, 'windInjection after 31_03_2022': 0, 'windNet After_31_03_2022': 0,
                            'hydroDrawal  before 08_03_2019': 0, 'hydroInjection  before 08_03_2019': 0, 'hydroNet Before 08_03_2019': 0,
                            'hydroDrawal  after 08_03_2019': 0, 'hydroInjection  after 08_03_2019': 0, 'hydroNet After_08_03_2019': 0,
                            'gdamDrawal': 0, 'gdamInjection': 0, 'gdamNet': 0
                        }
                    if parentAcronymType == 'BuyerWBESParentStateAcronym':
                        if scheduleType in ['GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX']:
                            currStateExceOutput[scheduleType]['gdamDrawal'] += scheduleDataSum
                            
                        elif seller in set(solar):
                            # currStateExceOutput[scheduleType]['solarData']['drawal'] += scheduleDataSum
                            currStateExceOutput[scheduleType]['solarDrawal'] += scheduleDataSum

                        # wind part
                        elif seller in set(windBefore):
                            percValue = inputWbesDf.loc[inputWbesDf['Wind Before 31_03_2022'] == seller, 'Wind Perc Before 31_03_2022'].iloc[0]
                            currStateExceOutput[scheduleType]['windDrawal before 31_03_2022'] += scheduleDataSum*percValue/100
                            
                        elif seller in set(windAfter):
                            percValue = inputWbesDf.loc[inputWbesDf['Wind After 31_03_2022'] == seller, 'Wind Perc After 31_03_2022'].iloc[0]
                            currStateExceOutput[scheduleType]['windDrawal after 31_03_2022'] += scheduleDataSum*percValue/100

                        # hydro part
                        elif seller in set(hydroBefore):
                            percValue = inputWbesDf.loc[inputWbesDf['Hydro Name Before 08_03_2019'] == seller, 'Hydro Perc Before  08_03_2019'].iloc[0]
                            currStateExceOutput[scheduleType]['hydroDrawal  before 08_03_2019'] += scheduleDataSum*percValue/100
                        
                        elif seller in set(hydroAfter):
                            percValue = inputWbesDf.loc[inputWbesDf['Hydro After 08_03_2019'] == seller, 'Hydro Perc After  08_03_2019'].iloc[0]
                            currStateExceOutput[scheduleType]['hydroDrawal  after 08_03_2019'] += scheduleDataSum*percValue/100

                    if parentAcronymType == 'SellerWBESParentStateAcronym':
                        if scheduleType in ['GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX']:
                            currStateExceOutput[scheduleType]['gdamInjection'] += -(scheduleDataSum)
                            
                        elif seller in set(solar):
                            # currStateExceOutput[scheduleType]['solarData']['injection'] += scheduleDataSum
                            currStateExceOutput[scheduleType]['solarInjection'] += -(scheduleDataSum)

                        elif seller in set(windBefore):
                            percValue = inputWbesDf.loc[inputWbesDf['Wind Before 31_03_2022'] == seller, 'Wind Perc Before 31_03_2022'].iloc[0]
                            currStateExceOutput[scheduleType]['windInjection before 31_03_2022'] += -(scheduleDataSum*percValue/100)
                            
                        elif seller in set(windAfter):
                            percValue = inputWbesDf.loc[inputWbesDf['Wind After 31_03_2022'] == seller, 'Wind Perc After 31_03_2022'].iloc[0]
                            currStateExceOutput[scheduleType]['windInjection after 31_03_2022'] += -(scheduleDataSum*percValue/100)
                        
                        # hydro part
                        elif seller in set(hydroBefore):
                            percValue = inputWbesDf.loc[inputWbesDf['Hydro Name Before 08_03_2019'] == seller, 'Hydro Perc Before  08_03_2019'].iloc[0]
                            currStateExceOutput[scheduleType]['hydroInjection  before 08_03_2019'] += -(scheduleDataSum*percValue/100)
                            
                        elif seller in set(hydroAfter):
                            percValue = inputWbesDf.loc[inputWbesDf['Hydro After 08_03_2019'] == seller, 'Hydro Perc After  08_03_2019'].iloc[0]
                            currStateExceOutput[scheduleType]['hydroInjection  after 08_03_2019'] += -(scheduleDataSum*percValue/100)
            else:
                pass

    return currStateExceOutput
