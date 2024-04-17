import time
import os
from dotenv import load_dotenv
import requests
from flask import render_template, Flask, request, flash, url_for, redirect, jsonify, session

from repositories import clashuser
from repositories.clashuser import delete_clash_users
from repositories.clash import get_member_th_level

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secretkey")

API_TOKEN = os.getenv("CLASH_API")
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
}

clan_tag = os.getenv("clantag")

url1 = f'https://api.clashofclans.com/v1/clans/{clan_tag}/members'
url2 = f'https://api.clashofclans.com/v1/clans/{clan_tag}/warlog'
url3 = f'https://api.clashofclans.com/v1/clans/{clan_tag}'

member_names = []

my_dict = []
choice = []
isname = []
user = {}


@app.get('/')
def index():
    member_names.clear()
    sum = 0
    response = requests.get(url1, headers=headers)  # Use requests.get for clarity
    if response.status_code == 200:
        clan_info = response.json()
        for member in clan_info.get('items', []):
            member_names.append(member['name'])
            sum = sum + 1
    message = request.args.get('message', '')
    # Loads the Home Page.
    if my_dict != None:
        my_dict.clear()
    roseusers = clashuser.get_clash_users()
    print(roseusers)
    first = choice[0] if choice else None
    popname = isname[0] if isname else None
    if choice != None:
        choice.clear()
    if isname != None:
        isname.clear()
    return render_template('index.html', member_names=member_names, response=first, nummems=sum, names=popname, message=message)

@app.get('/clanstats')
def clanstats():
    response2 = requests.get(url2, headers=headers)
    response3 = requests.get(url3, headers=headers)
    warlog = response2.json()
    clan = response3.json()
    wars = warlog.get('items', [])
    drose = "Dark Rose"
    return render_template('clan_stats.html', drose=drose, wars=wars, clandata=clan)

@app.route('/api/member-names')
def get_member_names():
    return jsonify(member_names)

@app.get('/admin')
def admin():
    if len(my_dict) == 0:
        return redirect(url_for('index'))
    else:
        roseusers = clashuser.get_clash_users()
        
        return render_template('admin.html', rose=roseusers, no_search_bar=True, homeie=True)
    
@app.get('/auth')
def auth():
    name = session['name']
    opt_choice = session['opt_choice']
    lvl = get_member_th_level(name)
    response = int(request.args.get('thlvl'))
    if response == lvl:
        if clashuser.check_user_exists(name.lower()):
            return redirect(url_for('index', submitted=True, message="Status Updated"))
        elif opt_choice == '1':
            isin = True
            choice.append("in")
            isname.append(name)
            clashuser.insert_clash_users(name.lower(), isin)
            return redirect(url_for('index', submitted=True, message=f"{name} has opted in!"))
        elif opt_choice == '2':
            isin = False
            choice.append("out")
            isname.append(name)
            clashuser.insert_clash_users(name.lower(), isin)
            return redirect(url_for('index', submitted=True, message=f"{name} has opted out!"))
    if response != lvl: 
        return redirect(url_for('index', submitted=True, message="Security Failed: incorrect TH"))
    
    

@app.get('/security_check')
def security_check():
    name = session['name']
    return render_template('auth.html', name=name)

@app.post('/adduser')
def adduser():
    session['name'] = request.form['name']
    session['opt_choice'] = request.form['opt_choice']
    return redirect(url_for('security_check'))
            
        
@app.post('/adminlogin')
def admin_pass():
    adpass = request.form.get('adminpass')
    setpass = os.getenv("adminpassword")
    if adpass == setpass:
        my_dict.append(1)
        return redirect(url_for('admin'))
    else:
        flash("Wrong Password Homie")
    
    return redirect(url_for('index'))

@app.post('/delete')
def delete_user():
    entry_id = request.form['entry_id']
    delete_clash_users(entry_id)
    return redirect(url_for('admin'))