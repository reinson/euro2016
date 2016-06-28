import urllib.request, csv
from bs4 import BeautifulSoup
import html


def get_goals_stats():
    #goals_page = "http://www.uefa.com/statistics/uefaeuro/season=2016/statistics/round=' + round + '/players/kind=goals/_loadRemaining.html"

    #req = urllib.request.Request(
    #    goals_page,
    #    data=None,
    #    headers={
    #        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    #    }
    #)
    #f = urllib.request.urlopen(req)
    #print(f.read().decode('utf-8'))

    #page = urllib.request.urlopen(goals_page)
    #myopener = MyOpener()
    #page = myopener.open(goals_page).open()
    #print(page)
    #soup = BeautifulSoup(page, "lxml")
    #rows = soup.findAll("a", {"class": "js-data-player"})

    #print(len(rows))

    html_file = open('data/_loadRemaining_goals_2806.html', encoding='utf8')
    soup = BeautifulSoup(html.unescape(html_file.read()), 'lxml')
    rows = soup.findAll('tr')

    keys = ['matches', 'minutes', 'goals', 'assists']
    goals_stats = {}
    for row in rows:
        items = row.findAll('td')
        if len(items) != 6:
            continue
        name = items[0].findAll('span', {'class': 'html-attribute-value'})[6].contents[0]
        matches = items[1].contents[0]
        minutes = items[2].contents[0]
        goals = items[3].contents[0]
        assists = items[4].contents[0]
        d = {x: y for x, y in zip(keys, [matches, minutes, goals, assists])}
        goals_stats[name] = d

    html_file.close()
    return goals_stats


def get_passes_stats():
    html_file = open('data/_loadRemaining_distribution_2806.html', encoding='utf8')
    soup = BeautifulSoup(html.unescape(html_file.read()), 'lxml')
    rows = soup.findAll('tr')

    keys = ['pa', 'pc', 'pc_perc']
    passes_stats = {}
    for row in rows:
        items = row.findAll('td')
        if len(items) != 5:
            continue
        name = items[0].findAll('a')[0].contents[0]
        pa = items[1].contents[0]
        pc = items[2].contents[0]
        pc_perc = items[3].contents[0].strip('%')
        d = {x: y for x, y in zip(keys, [pa, pc, pc_perc])}
        passes_stats[name] = d

    html_file.close()
    return passes_stats


def get_attempts_stats():
    html_file = open('data/_loadRemaining_attempts_2806.html', encoding='utf8')
    soup = BeautifulSoup(html.unescape(html_file.read()), 'lxml')
    rows = soup.findAll('tr')

    keys = ['on_target', 'off_target', 'blocked', 'against_woodwork']
    attempts_stats = {}
    for row in rows:
        items = row.findAll('td')
        if len(items) != 7:
            continue
        name = items[0].findAll('a')[0].contents[0]
        on_target = items[2].contents[0]
        off_target = items[3].contents[0]
        blocked = items[4].contents[0]
        against_woodwork = items[5].contents[0]
        d = {x: y for x, y in zip(keys, [on_target, off_target, blocked, against_woodwork])}
        attempts_stats[name] = d

    html_file.close()
    return attempts_stats


def get_disciplinary_stats():
    html_file = open('data/_loadRemaining_disciplinary_2806.html', encoding='utf8')
    soup = BeautifulSoup(html.unescape(html_file.read()), 'lxml')
    rows = soup.findAll('tr')

    keys = ['fouls', 'suffered', 'yellow', 'red']
    disciplinary_stats = {}
    for row in rows:
        items = row.findAll('td')
        if len(items) != 7:
            continue
        name = items[0].findAll('a')[0].contents[0]#items[0].findAll('span', {'class': 'html-attribute-value'})[6].contents[0]
        fouls = items[2].contents[0]
        suffered = items[3].contents[0]
        yellow = items[4].contents[0]
        red = items[5].contents[0]
        d = {x: y for x, y in zip(keys, [fouls, suffered, yellow, red])}
        disciplinary_stats[name] = d

    html_file.close()
    return disciplinary_stats


#round = '2000448'
#get_goals_stats(round)
#get_passes_stats(round)
#get_attempts_stats(round)
#get_disciplinary_stats(round)