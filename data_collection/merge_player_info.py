
from scrape_players_stats import get_goals_stats, get_passes_stats, get_attempts_stats, get_disciplinary_stats

class Player:

    keys = ['name', 'team', 'birthday', 'age', 'club_name', 'club_country_code',
            'caps', 'height', 'weight', 'position', 'matches', 'minutes',
            'goals', 'assists', 'pa', 'pc', 'pc_perc', 'on_target', 'off_target',
            'blocked', 'against_woodwork', 'fouls', 'suffered', 'yellow', 'red']

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
            players[player.name] = player
    return players


def write_players(players):
    with open('data/euro2016players_all.csv', 'w', encoding='utf8') as out_file:
        out_file.write('\t'.join(Player.keys) + '\n')
        for player in players:
            out_file.write(players[player]._str() + '\n')


def add_goal_stats(players):
    stats = get_goals_stats()
    for name in stats:
        players[name]._add_goals_stats(stats[name])


def add_passes_stats(players):
    stats = get_passes_stats()
    for name in stats:
        players[name]._add_passes_stats(stats[name])


def add_attempts_stats(players):
    stats = get_attempts_stats()
    for name in stats:
        players[name]._add_attempts_stats(stats[name])


def add_disciplinary_stats(players):
    stats = get_disciplinary_stats()
    for name in stats:
        players[name]._add_disciplinary_stats(stats[name])


def main():
    players = read_players()
    add_goal_stats(players)
    add_passes_stats(players)
    add_attempts_stats(players)
    add_disciplinary_stats(players)
    write_players(players)


main()