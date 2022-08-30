from src.config.appConfig import getFileMappings
import pandas as pd


def daywiseDataCalculator(currStateExceOutput, currDateData, currState, scheduleAmount, parentAcronymType):
    # get file config
    appConfig = getFileMappings()
    hydro = appConfig['Hydro Name'].dropna()
    solar = appConfig['Solar'].dropna()
    wind = appConfig['Wind'].dropna()

    for temp in currDateData:
        if temp[parentAcronymType] == currState:
            seller = temp['SellerAcr']
            scheduleType = temp['ScheduleTypeName']
            subScheduleType = temp['SubScheduleTypeName']
            ScheduleData = temp[scheduleAmount].split(',')
            ScheduleDataList = pd.Series(ScheduleData)
            scheduleDataSum = ScheduleDataList.astype('float').sum()
            if scheduleType in ['ISGS', 'LTA', 'MTOA', 'REMC', 'IEX', 'PXI', 'STOA', 'GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX', 'RTM_IEX', 'RTM_PXI', 'RTM_HPX']:
                if scheduleType == 'REMC' and subScheduleType in ['LTA', 'MTOA', 'IEX', 'PXI', 'STOA', 'GDAM_IEX', 'GDAM_PXI', 'GDAM_HPX', 'RTM_IEX', 'RTM_PXI', 'RTM_HPX']:
                    # cheack if "TRANSACTION TYPE" is present.
                    if currStateExceOutput.get(subScheduleType) == None:
                        # if subScheduleType not in currStateExceOutput[subScheduleType]:
                        currStateExceOutput[subScheduleType] = {
                            # 'solarData': {'drawal': 0, 'injection': 0, 'net': 0},
                            # 'windData': {'drawal': 0, 'injection': 0, 'net': 0},
                            # 'hydroData': {'drawal': 0, 'injection': 0, 'net': 0}
                            'solarDrawal': 0, 'solarInjection': 0, 'solarNet': 0,
                            'windDrawal': 0, 'windInjection': 0, 'windNet': 0,
                            'hydroDrawal': 0, 'hydroInjection': 0, 'hydroNet': 0
                        }
                    if parentAcronymType == 'BuyerWBESParentStateAcronym':
                        if seller in set(solar):
                            # currStateExceOutput[subScheduleType]['solarData']['drawal'] += scheduleDataSum
                            currStateExceOutput[subScheduleType]['solarDrawal'] += scheduleDataSum

                        elif seller in set(wind):
                            currStateExceOutput[subScheduleType]['windDrawal'] += scheduleDataSum

                        elif seller in set(hydro):
                            currStateExceOutput[subScheduleType]['hydroDrawal'] += scheduleDataSum

                    if parentAcronymType == 'SellerWBESParentStateAcronym':
                        if seller in set(solar):
                            # currStateExceOutput[subScheduleType]['solarData']['injection'] += scheduleDataSum
                            currStateExceOutput[subScheduleType]['solarInjection'] += scheduleDataSum

                        elif seller in set(wind):
                            currStateExceOutput[subScheduleType]['windInjection'] += scheduleDataSum

                        elif seller in set(hydro):
                            currStateExceOutput[subScheduleType]['hydroInjection'] += scheduleDataSum
                else:
                    # cheack if "TRANSACTION TYPE" is present.
                    if currStateExceOutput.get(scheduleType) == None:
                        # if scheduleType not in currStateExceOutput[scheduleType]:
                        currStateExceOutput[scheduleType] = {
                            # 'solarData': {'drawal': 0, 'injection': 0, 'net': 0},
                            # 'windData': {'drawal': 0, 'injection': 0, 'net': 0},
                            # 'hydroData': {'drawal': 0, 'injection': 0, 'net': 0}
                            'solarDrawal': 0, 'solarInjection': 0, 'solarNet': 0,
                            'windDrawal': 0, 'windInjection': 0, 'windNet': 0,
                            'hydroDrawal': 0, 'hydroInjection': 0, 'hydroNet': 0
                        }
                    if parentAcronymType == 'BuyerWBESParentStateAcronym':
                        if seller in set(solar):
                            # currStateExceOutput[scheduleType]['solarData']['drawal'] += scheduleDataSum
                            currStateExceOutput[scheduleType]['solarDrawal'] += scheduleDataSum

                        elif seller in set(wind):
                            currStateExceOutput[scheduleType]['windDrawal'] += scheduleDataSum

                        elif seller in set(hydro):
                            currStateExceOutput[scheduleType]['hydroDrawal'] += scheduleDataSum

                    if parentAcronymType == 'SellerWBESParentStateAcronym':
                        if seller in set(solar):
                            # currStateExceOutput[scheduleType]['solarData']['injection'] += scheduleDataSum
                            currStateExceOutput[scheduleType]['solarInjection'] += -(scheduleDataSum)

                        elif seller in set(wind):
                            currStateExceOutput[scheduleType]['windInjection'] += -(scheduleDataSum)

                        elif seller in set(hydro):
                            currStateExceOutput[scheduleType]['hydroInjection'] += -(scheduleDataSum)
            else:
                pass

    return currStateExceOutput
