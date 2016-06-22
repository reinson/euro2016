import urllib.request, csv
from bs4 import BeautifulSoup


def extract_team(link):
    link = "http://www.uefa.com" + link[:-10] + "squad/index.html"
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, "lxml")

    team_name = soup.find("h1", {"class": "team-name"}).contents[0]

    rows = soup.findAll("tr")
    result = []
    for row in rows:
        try:
            tds = row.findAll("td")
            name = tds.pop(0)
            name = name.findAll("a")
            name = name[0].contents[0].strip()

            tags = [x.contents for x in row.findAll("td")[1:]]
            keys = ["birthday", "age", "club", "euro16_games", "euro16_goals"]

            d = {x: y[0] for x, y in zip(keys, tags)}

            d["name"] = name
            d["team"] = team_name

            result.append(d)
        except:
            pass

    return result


def main():
    teams_page = "http://www.uefa.com/uefaeuro/season=2016/teams/index.html"

    page = urllib.request.urlopen(teams_page)
    soup = BeautifulSoup(page, "lxml")
    rows = soup.findAll("a", {"class": "team-hub_link"})

    links = [r.attrs["href"] for r in rows]

    with open("data/euro2016players_2.csv", "w", encoding='utf-8') as f:
        fieldnames = ["team", "name", "birthday", "age", "club", "euro16_games", "euro16_goals"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for link in links:
            players = extract_team(link)
            for player in players:
                writer.writerow(player)



                # england = "/uefaeuro/season=2016/teams/team=39/index.html"
                # extract_team(england)


main()