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

    def __init__(self, name, country_code, ac_query_name=None):
        self.name = name
        self.country_code = country_code
        self.country_name = country_codes[self.country_code]
        self.ac_url = 'https://maps.googleapis.com/maps/api/place/queryautocomplete/json'
        self.ac_query_name = ac_query_name

    def __eq__(self, other):
        if self.name == other.name and self.country_code == other.country_code:
            return True
        return False

    def __str__(self):
        return '\t'.join([self.name, self.country_code, self.country_name,
                         self.ac_query_name])

    def get_longer_name(self, api_key):
        name_and_country = '+'.join(self.name.split() + self.country_name.split() + ['football'])
        params = dict(key=api_key, input=name_and_country)
        resp = requests.get(url=self.ac_url, params=params)
        data = json.loads(resp.text, encoding='utf8')
        try:
            self.ac_query_name = data['predictions'][0]['description']
        except Exception as e:
            self.ac_query_name = 'FAILED'

    def query_location_with_google(self):
        query_name = self.ac_query_name
        if query_name is None or query_name == 'FAILED':
            query_name = self.name + ', ' + self.country_name
        res = geocoder.google(query_name)


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

#main
api_key = 'AIzaSyAzoNQHSY1nOoG-5CRE1aViEgLSK5N_iNc'
clubs = read_club_data()
with open('data/clubs_and_ac_names_w_football.txt', 'w', encoding='utf8') as out_file:
    for club in clubs:
        club.get_longer_name(api_key)
        out_file.write(str(club) + '\n')