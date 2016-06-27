import os

def read_existing_pairs():
    d = {}
    if not os.path.exists('data/club_long_names.csv'):
        return d
    with open('data/club_long_names.csv', encoding='utf8') as in_file:
        for line in in_file:
            values = line.strip().split('\t')
            d[values[0]] = values[1]
    return d


def read_uefa_clubs():
    d = {}
    with open('data/uefa_clubs.csv', encoding='utf8') as in_file:
        tags = in_file.readline().strip().split()
        for line in in_file:
            values = line.strip().split('\t')
            club_name = values[0]
            d[club_name] = values
    return d



def read_player_clubs():
    d = {}
    with open('data/euro2016players_all.csv', encoding='utf8') as in_file:
        tags = in_file.readline().strip().split()
        for line in in_file:
            values = line.strip().split('\t')
            club_name = values[4]
            if club_name not in d:
                d[club_name] = []
            d[club_name].append(values[0])
    return d


def map_club(uefa_clubs, pclub):
    matches = []
    for uclub in uefa_clubs:
        if pclub.lower() in uclub.lower() and pclub.strip() != '':
            matches.append(uclub)
    return matches


def map_clubs(uefa_clubs, player_clubs, existing_pairs):
    d = {}
    c = 0
    done = 0
    mapped = 0
    changed = 0
    nas = 0
    for pclub in player_clubs:
        c += 1
        print('-' * 20)
        print('Club', c, 'from', len(player_clubs))
        print('\nName of the club is:', pclub)
        print('Players from the club are:')
        for player in player_clubs[pclub]:
            print(player)
        if pclub in existing_pairs:
            print('Club', pclub, ' already mapped to', existing_pairs[pclub], '.')
            yn = input('Do you want to change (y/n)?')
            if yn.lower() == 'n':
                d[pclub] = existing_pairs[pclub]
                done += 1
                continue
        matches = map_club(uefa_clubs, pclub)
        print('\nMatching UEFA clubs are:')
        for i in range(len(matches)):
            print(str(i + 1) + '. ' + matches[i])
        while True:
            try:
                i = input('Write index of suitable club (or 0 if no names are suitable):')
                if i == 'Q':
                    print('Mapped: ', mapped, 'Done:', done, 'Changed:', changed, 'NAs:', nas)
                    return d
                i = int(i) - 1
                if i >= len(matches):
                    raise ValueError
                elif i < 0:
                    club_name = input('Write the name for the club:')
                    if club_name == 'NA':
                        nas += 1
                    else:
                        changed += 1
                else:
                    club_name = matches[i]
                    mapped += 1
                d[pclub] = club_name
                print('Selected club:', club_name)
                break
            except ValueError:
                print('Something is not right, answer again.')
    print('Mapped: ', mapped, 'Done:', done, 'Changed:', changed, 'NAs:', nas)
    return d


def output_results(club_names):
    with open('data/club_long_names.csv', 'w', encoding='utf8') as out_file:
        for club_name in club_names:
            if club_names[club_name] != 'NA':
                out_file.write(club_name + '\t' + club_names[club_name] + '\n')


def main():
    uefa_clubs = read_uefa_clubs()
    player_clubs = read_player_clubs()
    existing_pairs = read_existing_pairs()
    club_names = map_clubs(uefa_clubs, player_clubs, existing_pairs)
    output_results(club_names)

main()