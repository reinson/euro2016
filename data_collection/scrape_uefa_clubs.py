import urllib.request, csv
from bs4 import BeautifulSoup

def main():
    url = 'http://www.uefa.com/memberassociations/uefarankings/club/index.html'

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'lxml', from_encoding='utf8')
    rows = soup.findAll('tr')


    with open('data/uefa_clubs.csv', 'w', encoding='utf8') as out_file:
        out_file.write('\t'.join(['club_name', 'club_country_code', '11_12', '12_13', '13_14', '14_15', '15_16', 'pts']) + '\n')
        for row in rows:
            items = row.findAll('td')
            if len(items) != 8:
                continue
            club_name = items[0].findAll('img')[1]['title']
            country = items[1].contents[0]
            _11_12 = items[2].contents[0]
            _12_13 = items[3].contents[0]
            _13_14 = items[4].contents[0]
            _14_15 = items[5].contents[0]
            _15_16 = items[5].contents[0]
            pts = items[5].contents[0]

            out_file.write('\t'.join([club_name, country, _11_12, _12_13, _13_14, _14_15, _15_16, pts]) + '\n')

main()