
from scrape_players_stats import get_goals_stats, get_passes_stats, get_attempts_stats, get_disciplinary_stats

class Player:

    keys = ['name', 'team', 'birthday', 'age', 'club_name', 'club_country_code',
            'caps', 'height', 'weight', 'position', 'matches', 'minutes',
            'goals', 'assists', 'pa', 'pc', 'pc_perc', 'on_target', 'off_target',
            'blocked', 'against_woodwork', 'fouls', 'suffered', 'yellow', 'red',
            'longer_club_name', 'lat', 'lng', 'uefa_club_name', 'uefa_11_12',
            'uefa_12_13', 'uefa_13_14', 'uefa_14_15', 'uefa_15_16', 'uefa_pts']

    def __init__(self, player_row):
        values = player_row.strip().split(',')
        self.team = values[0]
        self.name = values[1]
        self.birthday = values[2]
        self.age = values[3]
        self.club_name = values[4]
        self.club_country_code = values[5]
        self.caps = values[6]
        self.height = values[7]
        self.weight = values[8]
        self.position = values[9]
        self.goals = '0'
        self.minutes = '0'
        self.pc_perc = '0'
        self.fouls = '0'
        self.suffered = '0'
        self.yellow = '0'
        self.red = '0'

    def _add_club_coords(self, club_coords):
        player_club = club_coords[self.club_name]
        self.longer_club_name = player_club['longer_name']
        self.lat = player_club['lat']
        self.lng = player_club['lng']

    def _add_uefa_rankings(self, uefa_clubs, club_longer_names):
        longer_uefa_name = club_longer_names[self.club_name]
        if longer_uefa_name in uefa_clubs:
            uefa_data = uefa_clubs[longer_uefa_name]
            self.uefa_club_name = uefa_data['club_name']
            self.uefa_11_12 = uefa_data['11_12']
            self.uefa_12_13 = uefa_data['12_13']
            self.uefa_13_14 = uefa_data['13_14']
            self.uefa_14_15 = uefa_data['14_15']
            self.uefa_15_16 = uefa_data['15_16']
            self.uefa_pts = uefa_data['pts']

    def _add_goals_stats(self, stats):
        self.matches = stats['matches']
        self.minutes = stats['minutes']
        self.goals = stats['goals']
        self.assists = stats['assists']

    def _add_passes_stats(self, stats):
        self.pa = stats['pa']
        self.pc = stats['pc']
        self.pc_perc = stats['pc_perc']

    def _add_attempts_stats(self, stats):
        self.on_target = stats['on_target']
        self.off_target = stats['off_target']
        self.blocked = stats['blocked']
        self.against_woodwork = stats['against_woodwork']

    def _add_disciplinary_stats(self, stats):
        self.fouls = stats['fouls']
        self.suffered = stats['suffered']
        self.yellow = stats['yellow']
        self.red = stats['red']

    def _add_matches(self, matches):
        self.matches = matches.replace('-', '0')

    def _str(self):
        variables = []
        for key in self.keys:
            try:
                var = getattr(self, key)
            except AttributeError:
                var = None
            variables.append(var)
        return '\t'.join(map(str, variables))




def read_players():
    players = {}
    with open('data/euro2016players_1.csv', encoding='utf8') as in_file:
        in_file.readline()
        for line in in_file:
            if line.strip() == '':
                continue
            player = Player(line)
            players[player.name.strip()] = player
    return players


def write_players(players):
    with open('data/euro2016players_all.tsv', 'w', encoding='utf8') as out_file:
        out_file.write('\t'.join(Player.keys) + '\n')
        for player in players:
            out_file.write(players[player]._str() + '\n')


def add_new_matches_stats(players, goal_info):
    for player in players:
        if 'Neuer' in player:
            print(goal_info[player.strip()]['euro16_games'])
        players[player.strip()]._add_matches(goal_info[player.strip()]['euro16_games'])


def add_goal_stats(players):
    stats = get_goals_stats()
    for name in stats:
        players[name]._add_goals_stats(stats[name])


def add_passes_stats(players):
    stats = get_passes_stats()
    for name in stats:
        players[name.strip()]._add_passes_stats(stats[name])


def add_attempts_stats(players):
    stats = get_attempts_stats()
    for name in stats:
        players[name.strip()]._add_attempts_stats(stats[name])


def add_disciplinary_stats(players):
    stats = get_disciplinary_stats()
    for name in stats:
        players[name.strip()]._add_disciplinary_stats(stats[name])


def add_club_coords(players, club_coords):
    for player in players:
        players[player]._add_club_coords(club_coords)

def add_uefa_rankings(players, uefa_clubs, club_longer_names):
    for player in players:
        players[player]._add_uefa_rankings(uefa_clubs, club_longer_names)


def read_club_longer_names():
    short_to_long_name_map = {}
    with open('data/club_long_names.csv', encoding='utf8') as in_file:
        for line in in_file:
            values = line.rstrip().split('\t')
            short_to_long_name_map[values[0]] = values[1].split(';')[0]
    return short_to_long_name_map


def read_club_info():
    short_key_clubs = {}
    long_key_clubs = {}
    with open('data/club_coords_info.csv', encoding='utf8') as in_file:
        tags = in_file.readline().rstrip().split('\t')
        for line in in_file:
            values = line.rstrip().split('\t')
            name = values[1].strip()
            long_name = values[0]
            d = {x: y for x, y in zip(tags, values)}
            short_key_clubs[name] = d
            long_key_clubs[name] = d
    return short_key_clubs, long_key_clubs


def read_uefa_clubs():
    clubs = {}
    with open('data/uefa_clubs.csv', encoding='utf8') as in_file:
        tags = in_file.readline().strip().split('\t')
        for line in in_file:
            values = line.strip().split('\t')
            club_name = values[0]
            d = {x: y for x, y in zip(tags, values)}
            clubs[club_name] = d
    return clubs


def read_player_nrofgames_info_2():
    d = {}
    with open('data/euro2016players_2.csv', encoding='utf8') as in_file:
        tags = in_file.readline().rstrip().split(',')
        for line in in_file:
            if line.strip() == '':
                continue
            values = line.rstrip().split(',')
            name = values[1].split(' (')[0].strip().replace('  ', ' ')
            if 'Zinchenko' in name:
                print(name)
            d[name] = {x: y for x, y in zip(tags, values)}
    return d


def main():
    players = read_players()
    short_key_clubs, long_key_clubs = read_club_info()
    uefa_club_stats = read_uefa_clubs()
    short_to_long_name_map = read_club_longer_names()
    goal_info = read_player_nrofgames_info_2()
    add_club_coords(players, short_key_clubs)
    add_uefa_rankings(players, uefa_club_stats, short_to_long_name_map)
    add_goal_stats(players)
    add_passes_stats(players)
    add_attempts_stats(players)
    add_disciplinary_stats(players)
    add_new_matches_stats(players, goal_info)
    write_players(players)


main()