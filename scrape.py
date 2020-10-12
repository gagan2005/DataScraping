import requests
from bs4 import BeautifulSoup

baseurl = 'https://fbref.com/'

def connection(url):
    try:
        site = requests.get(url) 
        soup = BeautifulSoup(site.content,'html.parser')
        return soup
    except Exception as e:
        print(e)
        exit()
    

def geturl(s,soup):
    comps_tables = soup.find_all('table')
    for a in comps_tables:
        for b in a.find_all('a'):
            if b.text==s:
                return b['href']


### League and season 
soup = connection(baseurl+'/en/comps')
league = geturl('La Liga',soup)
soup = connection(baseurl+league)
season = geturl('2020-2021',soup)
#print(league,season)

### All teams 
soup = connection(baseurl+season)
td = soup.find_all('table')[0].find_all('td', attrs={"data-stat" : "squad"})
teams =[ i.find_all('a')[0]['href'] for i in td ] ## links of teams
#print(teams) 
 
### All players
players=[]  ### will contain all players links
for team in teams:
    soup = connection(baseurl+team)
    th = soup.find_all('table')[0].find_all('th', attrs={"data-stat" : "player","scope":"row"})
    for i in th:
        a = i.find_all('a')
        if a!=[]:
            print(a[0]['href'])
            players.append(a[0]['href']) 
