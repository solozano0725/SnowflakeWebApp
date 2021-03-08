#Import packages
from flask import Flask, render_template, request
import pandas as pd
from snowflakeConnection import sf_connect

#Flask application
app = Flask("my website")

@app.route('/')
def homepage():
    cur = conn.cursor().execute("SELECT COLOR_NAME, COUNT(*) "
                                " FROM COLORS "
                                " GROUP BY COLOR_NAME " 
                                " HAVING COUNT(*) > 50 " 
                                " ORDER BY COUNT(*) DESC; ")
    rows = pd.DataFrame(cur.fetchall(), columns=['Color Name', 'Votes'])
    df_html = rows.to_html(index=False)
    return render_template('index.html', dfhtml= df_html)

@app.route('/submit')
def submitpage():
    return render_template('submit.html')

@app.route('/thanks4submit', methods=["POST"])
def thanks4submit():
    colorname = request.form.get('cname')
    username = request.form.get('uname')
    conn.cursor().execute("INSERT INTO COLORS(COLOR_UID, COLOR_NAME) " +"SELECT COLOR_UID_SEQ.nextval, '" + colorname+ "'")
    return render_template('thanks4submit.html', colorname= colorname, username=username)

@app.route('/coolcharts')
def coolcharts():
    cur = conn.cursor().execute("SELECT COLOR_NAME, COUNT(*) "
                                " FROM COLORS "
                                " GROUP BY COLOR_NAME " 
                                " ORDER BY COUNT(*) DESC; ")
    data4Charts = pd.DataFrame(cur.fetchall(), columns=['color', 'votes'])
    data4ChartsJSON = data4Charts.to_json("data4ChartsJSON.json",orient='records')
    return render_template('coolcharts.html', data4ChartsJSON=data4Charts.to_json(orient='records'))


#Snowflake
conn = sf_connect()
app.run()
