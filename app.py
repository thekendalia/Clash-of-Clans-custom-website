import time
import os
from twilio.rest import Client
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
url4 = f'https://api.clashofclans.com/v1/clans/{clan_tag}/currentwar'

member_names = []

my_dict = []
choice = []
isname = []
user = {}


sid = os.getenv("account_sid")
twilio_token = os.getenv("auth_token_twilio")

client = Client(sid, twilio_token)

message = client.messages.create(
    body="THIS IS A TEST MESSAGE",
    from_=os.getenv("phone_number"),
    to=os.getenv("my_number")
    
)
print(message.body)


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
    
    
@app.get('/currentwar')
def current_war():
    response4 = requests.get(url4, headers=headers)
    clanwar = response4.json()
    zero, one, two, three = 0, 0, 0, 0
    oppzero, oppone, opptwo, oppthree = 0, 0, 0, 0
    for member in clanwar['clan']['members']:
        if 'attacks' in member:
            for attack in member['attacks']:
                stars = attack['stars']
                if stars == 0:
                    zero += 1
                elif stars == 1:
                    one += 1
                elif stars == 2:
                    two += 1
                elif stars == 3:
                    three += 1
    for member in clanwar['opponent']['members']:
        if 'attacks' in member:
            for attack in member['attacks']:
                stars = attack['stars']
                if stars == 0:
                    oppzero += 1
                elif stars == 1:
                    oppone += 1
                elif stars == 2:
                    opptwo += 1
                elif stars == 3:
                    oppthree += 1
    members_info = []  # This will store our dictionaries

    for member in clanwar['clan']['members']:
        attacks_left = 2  # Initialize with maximum attacks
        if 'attacks' in member:
            attacks_left -= len(member['attacks'])  # Subtract the number of attacks made

        # Create a dictionary for each member with relevant information
        new_dict = {
            'name': member['name'],
            'position': member.get('mapPosition', float('inf')),  # Use float('inf') to handle missing positions
            'attacks_left': attacks_left
        }
        members_info.append(new_dict)

    # Sort members by mapPosition
    members_info = sorted(members_info, key=lambda x: x['position'])
        
    return render_template('current_war.html', clan=clanwar, three=three, two=two, one=one, zero=zero, oppzero=oppzero, oppone=oppone, opptwo=opptwo, oppthree=oppthree, clanmem=clanwar['clan'], members_info=members_info)

@app.get('/security_check')
def security_check():
    name = session['name']
    return render_template('auth.html', name=name)

@app.get('/addhome')
def addhome():
    return render_template('/addhome.html')

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