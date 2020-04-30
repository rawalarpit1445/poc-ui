import logging
import json
import pandas as pd
import numpy as np

from flask import Flask, request, render_template, redirect, send_file

import sys
sys.path.append('/home/project/app/analytics')

from Codes.main_io import main
#from incentive_optimizer import data_filter, data_prep, f_optimizer

app = Flask(__name__)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

path_to_paths_file = '/home/project/app/analytics/paths.txt'
with open(path_to_paths_file) as json_file:
        paths = json.load(json_file)

import os
if not os.path.isdir(os.path.join(paths['Output_path'],'Honda')):
    os.makedirs(os.path.join(paths['Output_path'],'Honda'))
if not os.path.isdir(os.path.join(paths['Output_path'],'Acura')):
    os.makedirs(os.path.join(paths['Output_path'],'Acura'))
        
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/incentive-optimizer", methods = ['POST'])
def auth():
    #if 'uname' or 'psw' not in request.form:
    #    return redirect("/")
    try:
        username = request.form['uname']
        password = request.form['psw']
        if username == 'honda_user' and password == 'admin':
            return render_template('incentive-optimizer.html', make='HONDA')
        elif username == 'acura_user' and password == 'admin':
            return render_template('incentive-optimizer.html', make='ACURA')
        else:
            return redirect("/") #improve to show incorrect combination
    except Exception as e:
        print("Exception raised in login authorization check: ", str(e))
        return redirect("/")


@app.route("/generate_summary", methods=['GET', 'POST'])
def generate_summary():
    request_body= request.get_json()
    budget=float(request_body.get('budget'))
    year=int(request_body.get('year'))
    cycle=int(request_body.get('cycle'))
    make=request_body.get('make')
    print(budget, year, cycle, make)
    ret_val = main(make, budget, year, cycle)
    
    if ret_val:     # handle what to do if ter_val is false?
        if (make == 'HONDA'):
            honda_df = pd.read_csv(os.path.join(paths['Output_path'],'Honda','Honda_Executive_Summary.csv'))
            summary_html = honda_df.to_html(table_id="incentiveOptimizerSummaryTable", classes=["w3-table", "w3-striped", "w3-bordered", "w3-border", "w3-hoverable", "w3-card-4"], index=False)
            return json.dumps({"html_table": summary_html})
        elif (make == 'ACURA'):
            acura_df = pd.read_csv(os.path.join(paths['Output_path'],'Acura','Acura_Executive_Summary.csv'))
            summary_html = acura_df.to_html(table_id="incentiveOptimizerSummaryTable", classes=["w3-table", "w3-striped", "w3-bordered", "w3-border", "w3-hoverable", "w3-card-4"], index=False)
            return json.dumps({"html_table": summary_html})
        

@app.route("/download-summary/honda", methods=['GET'])
def download_summary_honda():
    csv_file_path = os.path.join(paths['Output_path'],'Honda','Honda_Executive_Summary.csv')
    excel_file_path = os.path.join(paths['Output_path'],'Honda','Honda_Executive_Summary.xlsx')
    honda_df = pd.read_csv(csv_file_path)
    honda_df.to_excel(excel_file_path, index=False)
    return send_file(excel_file_path, as_attachment=True)

@app.route("/download-summary/acura", methods=['GET'])
def download_summary_acura():	
    csv_file_path = os.path.join(paths['Output_path'],'Acura','Acura_Executive_Summary.csv')
    excel_file_path = os.path.join(paths['Output_path'],'Acura','Acura_Executive_Summary.xlsx')
    acura_df = pd.read_csv(csv_file_path)
    acura_df.to_excel(excel_file_path, index=False)
    return send_file(excel_file_path, as_attachment=True)


@app.route("/scenario-analyzer", methods=['POST'])
def scenario_default():
    make = request.form['sa_make']
    budget = float(request.form['sa_budget'])
    year = int(request.form['sa_year'])
    cycle = int(request.form['sa_cycle'])
    return render_template('scenario-analyzer.html', make=make, budget=budget, year=year, cycle=cycle)

@app.route("/initialize_analyzer", methods=['POST'])
def init_sa():
    request_body= request.get_json()
    make=request_body.get('make') 
    if (make == 'HONDA'):
        csv_file_path = os.path.join(paths['Output_path'],'Honda','Honda_Executive_Summary.csv')
        honda_df = pd.read_csv(csv_file_path)
        table_html = honda_df.to_html(table_id="saSummaryTable", classes=["w3-table"], index=False)
        return json.dumps({"html_table": table_html})
    elif (make == 'ACURA'):
        csv_file_path = os.path.join(paths['Output_path'],'Acura','Acura_Executive_Summary.csv')
        acura_df = pd.read_csv(csv_file_path)
        table_html = acura_df.to_html(table_id="saSummaryTable", classes=["w3-table"], index=False)
        return json.dumps({"html_table": table_html})
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
