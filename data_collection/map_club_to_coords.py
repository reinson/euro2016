import geocoder
import json
import requests, json

def read_country_codes():
    # http://data.okfn.org/data/core/country-codes
    d = {}
    with open('data/country-codes.json') as data_file:
        data = json.load(data_file)
        for item in data:
            d[item['FIFA']] = item['official_name']
    d['ENG'] = 'United Kingdom'
    d['WAL'] = 'Wales'
    d['SCO'] = 'Scotland'
    d['NIR'] = 'North Ireland'
    return d

country_codes = read_country_codes()


class Club:

    tags = ['longer_name', 'name', 'country_code', 'country_name', 'ac_query_name',
            'city', 'country', 'lat', 'lng']

    def __init__(self, name, country_code, ac_query_name=None):
        self.name = name
        self.country_code = country_code
        self.country_name = country_codes[self.country_code]
        self.ac_url = 'https://maps.googleapis.com/maps/api/place/queryautocomplete/json'
        self.ac_query_name = ac_query_name
        self.longer_name = None
        self.city = []
        self.country = []
        self.lat = []
        self.lng = []

    def __eq__(self, other):
        if self.name == other.name and self.country_code == other.country_code:
            return True
        return False

    def __str__(self):
        return '\t'.join([str(x) for x in [self.longer_name, self.name, self.country_code, self.country_name,
                         self.ac_query_name, self.city, self.country, self.lat, self.lng]])

    def get_longer_name(self, api_key, long_name_map):
        self.longer_name = long_name_map[self.name][-1]
        name_and_country = '+'.join(self.longer_name.split() + self.country_name.split())# + ['football'])
        params = dict(key=api_key, input=name_and_country)
        resp = requests.get(url=self.ac_url, params=params)
        data = json.loads(resp.text, encoding='utf8')
        try:
            self.ac_query_name = data['predictions'][0]['description']
        except Exception as e:
            self.ac_query_name = 'FAILED'

    def try_query(self, query_name):
        res = geocoder.google(query_name)
        if res.city is not None:
            self.city.append(res.city)
        if self.country is not None:
            self.country.append(res.country)
        if self.lat is not None:
            self.lat.append(res.lat)
        if self.lng is not None:
            self.lng.append(res.lng)
        res = geocoder.arcgis(query_name).geojson
        try:
            if res['properties']['lat'] is not None:
                self.lat.append(res['properties']['lat'])
            if res['properties']['lng'] is not None:
                self.lng.append(res['properties']['lng'])
        except KeyError:
            pass

    def query_location_with_google(self):
        query_name = self.ac_query_name
        simple_query_name = self.longer_name + ', ' + self.country_name
        very_simple_query_name = self.name + ', ' + self.country_name
        if query_name is None or query_name == 'FAILED':
            query_name = simple_query_name
        print('TEMP:', query_name, ' | ', simple_query_name, ' | ', very_simple_query_name)
        self.try_query(query_name)
        self.try_query(simple_query_name)
        self.try_query(very_simple_query_name)
        self.aggregate_queries()

    def aggregate_queries(self):
        self.city = [x for x in self.city if x is not None]
        self.city = ';'.join(list(set(self.city)))
        self.country = [x for x in self.country if x is not None]
        self.country = ';'.join(list(set(self.country)))
        lat_ok = list(set([int(x) for x in self.lat if x is not None]))
        if len(lat_ok) > 1:
            self.lat.append('DIFF')
        self.lat = ';'.join(map(str, list(set(self.lat))))
        lng_ok = list(set([int(x) for x in self.lng if x is not None]))
        if len(lng_ok) > 1:
            self.lng.append('DIFF')
        self.lng = ';'.join(map(str, list(set(self.lng))))

def main():
    country_name_map = read_country_codes()

    clubs = []
    with open('data/euro2016players.csv', encoding='utf8') as in_file:
        with open('data/euro2016players_lat_lng.csv', 'w', encoding='utf8') as out_file:
            c = 0
            try:
                header = in_file.readline().strip() + ','.join(['club_city', 'club_country_code', 'lat', 'lng'])
                out_file.write(header + '\n')
                for line in in_file:
                    if line.strip() == "":
                        continue
                    values = line.strip().split(',')
                    club = values[4]
                    club_country = country_name_map[values[5]]
                    name = club + ' (' + club_country + ')'
                    if name not in clubs:
                        clubs.append(name)
                    g = geocoder.google(club + ', ' + club_country)
                    city = g.city
                    country = g.country
                    lat = g.lat
                    lng = g.lng
                    values += [city, country, lat, lng]
                    out_file.write(','.join(map(str, values)) + '\n')
                    c += 1
            except UnicodeDecodeError as e:
                print(c)
    print('Nr of different clubs:', len(clubs))


def read_club_data():
    clubs = []
    with open('data/euro2016players_1.csv', encoding='utf8') as clubs_in:
        clubs_in.readline()
        for line in clubs_in:
            if line.strip() == '':
                continue
            values = line.strip().split(',')
            club = Club(values[4], values[5])
            if club not in clubs:
                clubs.append(club)
    return clubs


def read_uefa_mapped_names():
    clubs = {}
    with open('data/club_long_names.csv', encoding='utf8') as clubs_in:
        for line in clubs_in:
            values = line.rstrip().split('\t')
            clubs[values[0]] = values[1].split(';')
    return clubs


def write_autocomplete_file():
    api_key = 'AIzaSyAzoNQHSY1nOoG-5CRE1aViEgLSK5N_iNc'
    clubs = read_club_data()
    longer_club_names = read_uefa_mapped_names()
    with open('data/clubs_and_ac_longer_names_w_football.txt', 'w', encoding='utf8') as out_file:
        out_file.write('\t'.join(Club.tags) + '\n')
        c = 0
        for club in clubs:
            club.get_longer_name(api_key, longer_club_names)
            club.query_location_with_google()
            print(str(club))
            out_file.write(str(club) + '\n')
            c += 1


write_autocomplete_file()