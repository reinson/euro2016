import geocoder
import json


def read_country_codes():
    # http://data.okfn.org/data/core/country-codes
    d = {}
    with open('country-codes.json') as data_file:
        data = json.load(data_file)
        for item in data:
            d[item['FIFA']] = item['official_name']
    d['ENG'] = 'United Kingdom'
    d['WAL'] = 'Wales'
    d['SCO'] = 'Scotland'
    return d


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


main()