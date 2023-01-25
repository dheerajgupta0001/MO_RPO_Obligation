'''
This is the web server that acts as a service that creates raw/derived data of voltage and frequency
'''
from flask import Flask, request, jsonify, render_template
import datetime as dt
# from src.config.appConfig import getConfig
from src.config.appConfig import getFileMappings
from src.config.appConfig import getJsonConfig
from src.config.appConfig import initConfigs
# from src.fetchers.significanceViolationFetcher import fetchIegcViolationData, getIegcViolationMsgsFilePath
# from src.repos.insertViolationData import IegcViolationSummaryRepo
# from src.typeDefs.iegcViolationSummary import IViolationMessageSummary
# from src.dataFetcher.iegcViolMsgsFetcher import IegcViolMsgsFetcher
from flask import Flask, request, jsonify
import os
import pandas as pd
from src.repos.dailyDataHandler import dailyDataHandler
from flask import send_from_directory

app = Flask(__name__)

# get login config
initConfigs()
# get file config
appConfig = getFileMappings()

# Set the secret key to some random bytes getJsonConfig()['flaskSecret']
app.secret_key = getJsonConfig()['flaskSecret']

# appDbConnStr = appConfig['appDbConStr']


@app.route('/')
def hello():
    return render_template('home.html.j2')


@app.route('/createRpoObligation', methods=['GET', 'POST'])
def createRpoObligation():
    # in case of post request, fetch 
    if request.method == 'POST':
        try:
            isInsSuccess = True
            startDate = request.form.get('startDate')
            startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
            endDate = request.form.get('endDate')
            endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
            reqFile = request.files.get('inpFile')
            filename = reqFile.filename
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in ['.xlsx']:
                    return render_template('rpoObligationData.html.j2', data={'message': 'Only .xlsx files are supported'})
            fileMappingsDf = pd.read_excel(reqFile)
            state_name = fileMappingsDf['State Name'].dropna()
            isInsSuccess, downloadFile = dailyDataHandler(state_name= state_name, start_date= startDate, end_date= endDate)
            # iegcViolationData = fetchIegcViolationData(reqFile)

            if isInsSuccess:
                # return jsonify({'message': 'RPO Obligation data processing successful!!!'})
                return render_template('rpoObligationData.html.j2', data= downloadFile, startDate= startDate, endDate= endDate)
        except Exception as ex:
            return jsonify({'message': 'some error occured...'}), 400
    # in case of get request just return the html template rpoObligationData.html
    return render_template('rpoObligationData.html.j2')

@app.route("/downloadExcel", methods=['GET'])
def downloadExcel():
    return send_from_directory('D:\wrldc\python projects\MO_RPO_Obligation', file.downloadFile)
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(getJsonConfig()['flaskPort']), debug=True)