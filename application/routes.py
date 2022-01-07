from application import app
from flask import render_template, url_for, request ,session, redirect ,g, Flask
import pandas as pd 
import json
import plotly
import plotly.express as px

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='abhi', password='abhi'))
users.append(User(id=2, username='pratik', password='pratik'))
users.append(User(id=3, username='rohit', password='rohit'))
app.secret_key = 'evendeadiamthehero'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method =='POST':
        session.pop('user_id', None)
        username= request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username==username][0]
        
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route("/index")
def index():
    if not g.user:
        return redirect(url_for('login'))
#graph 1 
    df = pd.read_csv('F:/canspirit/plant monitoring/PdM_machines.csv')
    fig1 = px.scatter(df, x='machineID', y='model', color='age',title='Machine Age') 
    fig1.update_traces(mode='markers+lines')
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

#graph 2
    df = pd.read_csv('F:/canspirit/plant monitoring/PdM_failures.csv')
    fig2 = px.scatter(df, x = 'machineID', y = 'failure' ,title='Failures')
    #fig2 = px.box(df, x = 'failure', y = 'machineID' )
    #fig2.update_traces(quartilemethod="inclusive")
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

#graph 3
    df = pd.read_csv('F:/canspirit/plant monitoring/PdM_telemetry.csv')
    fig3 = px.box(df, x="machineID", y="volt",title='Voltage')
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('index.html', graph1JSON = graph1JSON , graph2JSON = graph2JSON , graph3JSON = graph3JSON )