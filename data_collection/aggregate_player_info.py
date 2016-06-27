

class Club:

    tags = ['longer_name', 'name', 'country_code', 'country_name', 'ac_query_name',
            'city', 'country', 'lat', 'lng']

    str_tags = ['longer_name', 'name', 'country_code', 'country_name', 'lat', 'lng']

    def __init__(self, line):
        values = line.rstrip().split('\t')
        self.longer_name = values[0]
        self.name = values[1]
        self.country_code = values[2]
        self.country_name = values[3]
        self.ac_query_name = values[4]
        self.cities = values[5].split(';')
        self.countries = values[6].split(';')
        self.lats = [float(x) for x in values[7].split(';') if x not in ['DIFF', 'None']]
        self.lngs = [float(x) for x in values[8].split(';') if x not in ['DIFF', 'None']]
        self.lat = self.find_popular_coords('lat')[1]
        self.lng = self.find_popular_coords('lng')[1]

    def find_popular_coords(self, coord):
        if coord == 'lat':
            l = self.lats
        else:
            l = self.lngs
        sl = sorted(l)
        if len(sl) > 1:
            min_diff = 1000
            m1, m2 = None, None
            for i in range(1, len(sl)):
                diff = sl[i] - sl[i - 1]
                if diff < min_diff:
                    min_diff = diff
                    m1 = sl[i]
                    m2 = sl[i - 1]
            return min_diff, m1
        else:
            return None, self.lats[0] if coord == 'lat' else self.lngs[0]

    def dist(self, coord):
        if coord == 'lat':
            l = self.lats
        else:
            l = self.lngs
        diff = max(l) - min(l)
        return diff

    def coords_differ(self):
        if self.dist('lat') > 1 or self.dist('lng') > 1:
            return self.dist('lat'), self.dist('lng')
        return False


    def has_coords(self):
        if len(self.lats) > 0 and len(self.lngs) > 0:
            return True
        return False

    def __str__(self):
        return '\t'.join([str(x) for x in [self.longer_name, self.name, self.country_code, self.country_name,
                                           self.lat, self.lng]])


def read_club_address_data():
    clubs = {}
    with open('data/clubs_and_ac_longer_names_w_football.txt', encoding='utf8') as in_file:
        tags = in_file.readline().strip().split('\t')
        for line in in_file:
            club = Club(line)
            clubs[club.name] = club
    return clubs


def write_club_address_data(clubs):
    with open('data/club_coords_info.csv', 'w', encoding='utf8') as out_file:
        out_file.write('\t'.join(Club.str_tags) + '\n')
        for club in clubs:
            out_file.write(str(clubs[club]) + '\n')

clubs = read_club_address_data()
write_club_address_data(clubs)
