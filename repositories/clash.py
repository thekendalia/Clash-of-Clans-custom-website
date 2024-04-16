import requests
from dotenv import load_dotenv
import os

load_dotenv()


API_TOKEN = os.getenv("CLASH_API")
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
}

# Ensure the clan tag is correctly URL encoded
clan_tag = os.getenv("clantag")  # URL encode '#' as '%23'

url = f'https://api.clashofclans.com/v1/clans/{clan_tag}/members'

response = requests.get(url, headers=headers)  # Use requests.get for clarity
member_names = []

# Check if the request was successful
if response.status_code == 200:
    clan_info = response.json()
    memname = clan_info.get('warWins', [])
    
    print("Members of the Clan:")
    for member in clan_info.get('items', []):
        member_names.append(member['name'])

        
else:
    print(f"Failed to retrieve clan information. Status Code: {response.status_code}, Error: {response.text}")
    
    
def get_member_th_level(member_name):
    """
    Returns the Town Hall level of a specified member by name.
    """
    if response.status_code == 200:
        clan_info = response.json()
        members = clan_info.get('items', [])
        
        for member in members:
            if member['name'].lower() == member_name.lower():
                return member.get('townHallLevel', 'Town Hall level not available')
        
        return "Member not found in the clan."
    else:
        return f"Failed to retrieve clan information. Status Code: {response.status_code}, Error: {response.text}"