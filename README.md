# Clash of Clans Custom Clan Website


Make a custom website for your clash of clans clan
 - Members can register for CWL or clan war
 - Display clan stats, and warlog
 - Database to keep track of members when they opt-in/opt-out
 - Uses Clash of Clans API to track and display clan data like clan member count, warlog... etc

![Home Page](https://media.discordapp.net/attachments/862445732534550529/1229631965246783541/github-MadewithClipchamp-ezgif.com-video-to-gif-converter.gif?ex=66325d41&is=66310bc1&hm=1c879b0ca6561ea8f5fb969636a19cb720078e271947f4767f1e8f3232bde326&=&width=1000&height=437)

## Installation

Download/Clone the project, open in vscode


create a virtual environment by running python -m venv venv in the terminal. Once that virtual environment is made type:
```python
#Windows: 
source ./venv/scripts/activate
#Mac/Linux
source ./venv/bin/activate
```

this command will activate the virtual environment. 

Now in the terminal run **pip install -r requirements.txt**

```bash
pip install -r requirements.txt
```

## .env setup
After cloning the project create a .env in the main project folder and put these 5 things in there

```
DATABASE_URL=
CLASH_API=
clantag=%23YVOURJQG
adminpassword=
secretkey=
```

**DATABASE_URL** - Install [DataGrip](https://www.jetbrains.com/datagrip/download/#section=windows) and [PostgreSQL](https://www.postgresql.org/download/). In DataGrip click the + in the top left corner and click "Data Source" and select PostgreSQL. In the pop-up window **set the password to what you set when installing PostgreSQL and set the user to be postgres**. 

Now the DATABASE_URL is: **postgresql://postgres:password@localhost:5432/postgres**

Next lets create a database!
```sql
CREATE DATABASE database_name;
```
Once you run "**CREATE DATABASE database_name**" delete that and then paste and run the following to make a table
```sql
CREATE TABLE IF NOT EXISTS clash (
    id SERIAL,
    clashname VARCHAR(255) NOT NULL,
    optin BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);
```

**Clash_API** - go to [Clash of Clans Dev website](https://developer.clashofclans.com/#/), create an account and make a new API key. Now copy the token and paste it in .env. Make sure you put your IP address in the allowed IP address section. You can find your public IP here: [whatismyip.com](https://www.whatismyip.com/)

**clantag** - paste your clan tag after %23 in the .env. The %23 is needed for the API

**adminpassword** - set password for the admin section

**secretkey** - This just makes a flask app secret key, so put whatever you want here as the key

To run the app type:

```python
flask run
```


To host the app you can use [Render](https://render.com/). You also can use [AWS](https://aws.amazon.com/) (this is what I use).

Here is a YouTube tut for aws: [AWS EC2](https://www.youtube.com/watch?v=uhO2JvOvTWU&t=619s)


## Issues/Questions?

Discord: 0xChamp
