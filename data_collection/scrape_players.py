import urllib.request, csv
from bs4 import BeautifulSoup


def extract_player(link):
    link = "http://www.uefa.com" + link
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, "lxml")

    player_data = soup.findAll("span", {"class": "profile--list--data"})
    name = player_data[0].contents[0]
    team = player_data[1].contents[0]
    position = player_data[2].contents[0].strip()
    bday, age = player_data[3].contents[0].split()
    age = age.strip('()')
    games = player_data[4].contents[0]
    club = ' '.join(player_data[8].contents[0].split()[:-1])
    club_country = player_data[8].contents[0].split()[-1].strip('()')
    height = player_data[9].contents[0].strip('cm')
    weight = player_data[10].contents[0].strip('kg')
    names = ["team", "name", "birthday", "age", "club", "club_country", "caps",
             "height", "weight", "position"]
    data = [team, name, bday, age, club, club_country, games, height, weight, position]

    d = {x: y for x, y in zip(names, data)}

    return d


def extract_team(link):
    link = "http://www.uefa.com" + link
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, "lxml")

    team_name = soup.find("h1", {"class": "team-name"}).contents[0]
    rows = soup.findAll("a", {"class": "squad--player-img"})
    links = [r.attrs["href"] for r in rows]

    result = []
    for link in links:
        try:
            player = extract_player(link)
            result.append(player)
        except Exception as e:
            print(e)
    print(team_name, " done")

    return result


def main():
    teams_page = "http://www.uefa.com/uefaeuro/season=2016/teams/index.html"

    page = urllib.request.urlopen(teams_page)
    soup = BeautifulSoup(page, "lxml")
    rows = soup.findAll("a", {"class": "team-hub_link"})

    links = [r.attrs["href"] for r in rows]

    with open("euro2016players.csv", "w", encoding='utf-8') as f:
        fieldnames = ["team", "name", "birthday", "age", "club", "club_country", "caps",
                      "height", "weight", "position"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for link in links:
            players = extract_team(link)
            for player in players:
                writer.writerow(player)



            # england = "/uefaeuro/season=2016/teams/team=39/index.html"
            # extract_team(england)
            # extract_player("/uefaeuro/season=2016/teams/player=24314/index.html")


main()