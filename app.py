
from flask import Flask, render_template,request,session,send_from_directory,send_file
from driver import initilize_driver
from selenium.webdriver.common.by import By
import pandas as pd

from flask_wtf import FlaskForm
from wtforms.fields import DateField, EmailField, TelField
from datetime import datetime
from dateutil import parser
from selenium.webdriver.support.ui import Select

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField

from gen_report import format_report

DEVELOPMENT_ENV  = True

class InfoForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = '#$%^&*'


driver = initilize_driver()


def get_selected_rows(df, start_date,end_date):
    try:
        df['temp'] = pd.to_datetime(df['Created'])
        df = df[(df['temp'] >= start_date.strftime('%m/%d/%Y')) & (df['temp'] <= end_date.strftime('%m/%d/%Y'))]
        df.pop('temp')
        return df

    except :
        
        df['temp'] = pd.to_datetime(df['Created'])
        df = df[(df['temp'] >= parser.parse(start_date).strftime('%m/%d/%Y')) & (df['temp'] <= parser.parse(end_date).strftime('%m/%d/%Y'))]
        df.pop('temp')
        return df

    
    

def get_lists(driver):
    driver.get('https://www.portfolio123.com/app/opener/LIST')

    
    x = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[3]/table/thead/tr/th[4]'))).get_attribute("class")

    print(x)
    
    select = Select(driver.find_element_by_id('resultrowspp'))
        # select by value 
    select.select_by_value('0')

    if x=="header":
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div/div[3]/table/thead/tr/th[4]/a'))).click()
    
    #table_id = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[3]/table')
    data = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[3]/table'))).get_attribute("outerHTML")
    df = pd.read_html(data)[0]
    print("++++++++")
    
    print(type(session['startdate']))
    print(session['enddate'])
    print("++++++++")

    df.pop('Unnamed: 0')
    if type(session['startdate']) =="str":
        session['startdate'] = parser.parse(session['startdate'])
    elif type(session['enddate']) =="str":
        session['enddate'] = parser.parse(session['enddate'])
    print(type(session['startdate']))
    print(type(session['enddate']))

    df = get_selected_rows(df, session['startdate'],session['enddate'])
    return df

def get_all_lists(driver):
    driver.get('https://www.portfolio123.com/app/opener/LIST')

    
    x = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[3]/table/thead/tr/th[4]'))).get_attribute("class")

    print(x)
    
    select = Select(driver.find_element_by_id('resultrowspp'))
        # select by value 
    select.select_by_value('0')

    if x=="header":
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div/div[3]/table/thead/tr/th[4]/a'))).click()
    
    #table_id = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[3]/table')
    data = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[3]/table'))).get_attribute("outerHTML")
    df = pd.read_html(data)[0]
    
    return df['Name'].values



def make_new_list(oldname , newname):
    
    driver.get('https://www.portfolio123.com/app/opener/LIST') 
    x = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[3]/table/thead/tr/th[4]'))).get_attribute("class")
    if x=="header":
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div/div[3]/table/thead/tr/th[4]/a'))).click()
    
    select = Select(driver.find_element_by_id('resultrowspp'))
    select.select_by_value('0')
    driver.find_element_by_link_text(oldname).click()

    driver.find_element_by_xpath('//*[@id="NewName"]').clear()

    Updated_name =  driver.find_element_by_xpath('//*[@id="NewName"]')

    # Send id information
    Updated_name.send_keys(newname)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ddToggleItemActions"]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SubmitSaveAs"]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="aboutDialog"]/div/div[3]/div/input[2]'))).click()
    driver.get("https://www.portfolio123.com/app/opener/LIST")
    

def make_new_screen(oldname , newname):
    driver.get('https://www.portfolio123.com/app/opener/SCR')
    x = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table/thead/tr/th[8]'))).get_attribute("class")
    print(x)    
    select = Select(driver.find_element_by_id('resultrowspp'))
        # select by value 
    select.select_by_value('0')

    if x=="header":
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table/thead/tr/th[8]'))).click()
    
    driver.find_element_by_link_text(oldname).click()

    driver.find_element_by_xpath('//*[@id="filter_0"]/div[3]/div/textarea').clear()

    Updated_name =  driver.find_element_by_xpath('//*[@id="filter_0"]/div[3]/div/textarea')
    Updated_name.send_keys('InList("'+newname+'')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ddToggleItemActions"]'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SubmitSaveAs"]'))).click()

    driver.find_element_by_xpath('//*[@id="aboutEditNewScreenName"]').clear()
    driver.find_element_by_xpath('//*[@id="aboutEditNewScreenName"]').send_keys('All Stocks fr List Bkttst of '+newname.split('__')[-1])
    
    oldval = driver.find_element_by_xpath('//*[@id="aboutEditNewDesc"]').get_attribute('value')
    p2 = oldval.split('_names')[-1]    
    p1 = "Does a report based on all ~ 500 Long stocks retrieved by Backtest of SLE_version done by SLE fr List " + newname
    driver.find_element_by_xpath('//*[@id="aboutEditNewDesc"]').clear()
    driver.find_element_by_xpath('//*[@id="aboutEditNewDesc"]').send_keys(p1+p2)
    
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="about-edit-save"]'))).click()
    driver.get("https://www.portfolio123.com/app/opener/SCR")

def get_screens(driver):
    driver.get('https://www.portfolio123.com/app/opener/SCR')

    
    x = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table/thead/tr/th[8]'))).get_attribute("class")

    print(x)
    
    select = Select(driver.find_element_by_id('resultrowspp'))
        # select by value 
    select.select_by_value('0')

    if x=="header":
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table/thead/tr/th[8]'))).click()
    
    #table_id = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[3]/table')
    data = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table'))).get_attribute("outerHTML")
    df = pd.read_html(data)[0]

    print("++++++++")
    
    print(type(session['startdate']))
    print(session['enddate'])
    print("++++++++")

    df.pop('Unnamed: 0')
    df.pop('Unnamed: 1')
    df.pop('Unnamed: 2')
    
    if type(session['startdate']) =="str":
        session['startdate'] = parser.parse(session['startdate'])
    elif type(session['enddate']) =="str":
        session['enddate'] = parser.parse(session['enddate'])
    print(type(session['startdate']))
    print(type(session['enddate']))

    df = get_selected_rows(df, session['startdate'],session['enddate'])
    return df



def get_all_screens(driver):
    driver.get('https://www.portfolio123.com/app/opener/SCR')

    
    x = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table/thead/tr/th[8]'))).get_attribute("class")

    print(x)
    
    select = Select(driver.find_element_by_id('resultrowspp'))
        # select by value 
    select.select_by_value('0')

    if x=="header":
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table/thead/tr/th[8]'))).click()
    
    #table_id = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[3]/table')
    data = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table'))).get_attribute("outerHTML")
    df = pd.read_html(data)[0]

    

    df.pop('Unnamed: 0')
    df.pop('Unnamed: 1')
    df.pop('Unnamed: 2')
    
    return df['Name'].values


def run_selected_screens(driver, s1s):
    driver.get('https://www.portfolio123.com/app/opener/SCR')

    
    x = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table/thead/tr/th[8]'))).get_attribute("class")

    print(x)
    dfs = []
    select = Select(driver.find_element_by_id('resultrowspp'))
        # select by value 
    select.select_by_value('0')

    if x=="header":
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div/div[4]/table/thead/tr/th[8]'))).click()
    
    for s1 in sorted(s1s):
        print(s1)
        driver.find_element_by_link_text(s1).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="runScreen"]'))).click()
        select = Select(driver.find_element_by_id('resultrowspp'))
        # select by value 
        select.select_by_value('0')

        
        data = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="results-table"]/table'))).get_attribute("outerHTML")
        import pandas as pd
        df = pd.read_html(data)
        dfs.append(df[0])
        driver.get("https://www.portfolio123.com/app/opener/SCR")

    print(dfs)
    final = pd.concat(dfs)
    final.to_csv("static/files/Unformatted_file.csv",index=None)	

    

@app.route('/lists', methods=['GET','POST'])
def listsindex():
    form = InfoForm()
    
    if form.validate_on_submit():
        session['startdate'] = form.startdate.data
        session['enddate'] = form.enddate.data

        df = (get_lists(driver))
        df['_'] = df['Name']
        return render_template("lists.html", form=form, link_column="_",column_names=df.columns.values, row_data=list(df.values.tolist()),zip=zip)

        

    return render_template('lists.html', form=form)


@app.route('/screens', methods=['GET','POST'])
def screensindex():
    form = InfoForm()
    
    if form.validate_on_submit():
        session['startdate'] = form.startdate.data
        session['enddate'] = form.enddate.data

        df = (get_screens(driver))
        df['_'] = df['Name']
        print(df['_'])
        return render_template("screens.html", form=form, link_column="_",column_names=df.columns.values, row_data=list(df.values.tolist()),zip=zip)

        

    return render_template('screens.html', form=form)


@app.route('/modal', methods=['GET','POST'])
def modal():
    if request.method=="POST":
        print(request.form['submit_button'])
        return render_template('modal.html', oldname = request.form['submit_button'])
    else:
        print("get")
        return render_template('modal.html')

@app.route('/screenmodal', methods=['GET','POST'])
def smodal():
    if request.method=="POST":
        print(request.form['submit_button'])
        lis = get_all_lists(driver)
        return render_template('screenmodal.html', oldname = request.form['submit_button'], row_data=list(lis))
    else:
        print("get")
        return render_template('screenmodal.html')
     

@app.route('/viewlists', methods=['GET','POST'])
def play():
    if request.method =="POST":
        print("Creating list",request.form)
        try:
            make_new_list(request.form['oldname'], request.form['newname'])
            print("Creating list done",request.form)

        except:
            print("No data provided for list")
        
        class tempform(FlaskForm):
            startdate = DateField('Start Date', default= parser.parse(session['startdate']) , format='%Y-%m-%d', validators=(validators.DataRequired(),))
            enddate = DateField('End Date',  default= parser.parse(session['enddate']) , format='%Y-%m-%d', validators=(validators.DataRequired(),))
            submit = SubmitField('Submit')
            
        form = tempform()
        #form.startdate = session['startdate']

        df = (get_lists(driver))
        df['temp'] = df['Name']
        return render_template("lists.html", form=form, link_column="temp",column_names=df.columns.values, row_data=list(df.values.tolist()),zip=zip)


@app.route('/viewscreens', methods=['GET','POST'])
def splay():
    if request.method =="POST":
        print("Creating screen",request.form)
        if request.form['submit_button'] =="create":
            make_new_screen(request.form['oldname'], request.form['selectfield'])
            print("Creating list done",request.form)

                
        class tempform(FlaskForm):
            startdate = DateField('Start Date', default= parser.parse(session['startdate']) , format='%Y-%m-%d', validators=(validators.DataRequired(),))
            enddate = DateField('End Date',  default= parser.parse(session['enddate']) , format='%Y-%m-%d', validators=(validators.DataRequired(),))
            submit = SubmitField('Submit')
            
        form = tempform()
        #form.startdate = session['startdate']

        df = (get_screens(driver))
        df['temp'] = df['Name']
        return render_template("screens.html", form=form, link_column="temp",column_names=df.columns.values, row_data=list(df.values.tolist()),zip=zip)


   


@app.route('/runscreens', methods=['GET','POST'])
def runscreens():
    if request.method == "GET":
        screens = (get_all_screens(driver))
        return render_template('runscreens.html',row_data=screens)
    
    elif request.method == "POST":
        print("Final screens",request.form)
        scs = request.form.getlist("screenselector")
        
        run_selected_screens(driver,scs)
        from datetime import datetime

        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        format_report()
        filename = 'static/files/P123_Screen_'+'_Jeff_Millennium-ProjCurrPE-sort_2000  tckrs_AAA to ZZZZ.xlsx'
        screens = (get_all_screens(driver))
        return send_file(filename, as_attachment=True)






if __name__ == '__main__':

    app.run(debug=DEVELOPMENT_ENV)