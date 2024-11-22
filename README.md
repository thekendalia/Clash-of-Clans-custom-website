# Clash of Clans Custom Clan Website


Make a custom website for your clash of clans clan
 - Members can register for CWL or clan war
 - Members can create an account and view their clash stats
 - Display clan stats, and warlog
 - Database to keep track of members when they opt-in/opt-out
 - Uses Clash of Clans API to track and display clan data like clan member count, warlog... etc

![DarkRose](https://github.com/user-attachments/assets/6b38a4e2-5bf9-4575-b5e2-c043d6809645)

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
After cloning the project create a .env in the main project folder and put these 8 things in there

```
DATABASE_URL=
CLASH_API=
clantag=%23YVOURJQG
adminpassword=
secretkey=
sitekey=
secret=
mailtrap=
```

**DATABASE_URL** - Install [DataGrip](https://www.jetbrains.com/datagrip/download/#section=windows) and [PostgreSQL](https://www.postgresql.org/download/). In DataGrip click the + in the top left corner and click "Data Source" and select PostgreSQL. In the pop-up window **set the password to what you set when installing PostgreSQL and set the user to be postgres**. 

Now the DATABASE_URL is: **postgresql://postgres:password@localhost:5432/postgres**

Next lets create a database!
```sql
CREATE DATABASE database_name;
```
Once you run "**CREATE DATABASE database_name**" delete that and then paste and run the following to make a tables
```sql
CREATE TABLE IF NOT EXISTS clash (
    id SERIAL,
    clashname VARCHAR(255) NOT NULL,
    optin BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    code int,
    clan_tag VARCHAR(255),
    PRIMARY KEY (id)
);
```

**Clash_API** - go to [Clash of Clans Dev website](https://developer.clashofclans.com/#/), create an account and make a new API key. Now copy the token and paste it in .env. Make sure you put your IP address in the allowed IP address section. You can find your public IP here: [whatismyip.com](https://www.whatismyip.com/)

**clantag** - paste your clan tag after %23 in the .env. The %23 is needed for the API

**adminpassword** - set password for the admin section

**secretkey** - This just makes a flask app secret key, so put whatever you want here as the key


**Setting Sitekey/Secret keys**:
Click [here](https://www.google.com/recaptcha/about/) to make an account to set up captcha. Register a new site, select **Challenge (v2)** then add domain. Now in the new registered domain select the settings icon then click the reCAPTCHA dropdown and copy the site and secret key into the .env

**mailtrap** - This app utilizes mailtrap API for sending emails to users to reset password. Go to [Mailtrap.com](https://mailtrap.io/sending/domains/c5a4e5ad-b8c0-4437-85d3-8b5e9df032db) make an account then click **Sending Domains**. Add your domain address, then you will have to connect the DNS records. Wherever you bought your domain from (GoDaddy, Namecheap, IONOS) go to the site and find the DNS records tab. Add a new record and copy the Missing records from mailtrap into your DNS records.

**Optional** - I have my domain connected to Cloudflare, you would set up the DNS records on Cloudflare not where you bought your domain.

To run the app type:

```python
flask run
```


To host the app you can use [Render](https://render.com/). You also can use [AWS](https://aws.amazon.com/) (this is what I use).

Here is a YouTube tut for aws: [AWS EC2](https://www.youtube.com/watch?v=uhO2JvOvTWU&t=619s)


## Issues/Questions?

Discord: 0xChamp
