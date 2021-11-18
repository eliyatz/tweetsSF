import csv
import pandas as pd
import json
import datetime
import time
from urllib.request import urlopen
import numpy as np

print("hello")
print("create stations requests")
class station:
    def station_names(self, station1, station2, station3, station4, station5, station6, station7, station8):
        self.station1 = station1
        self.station2 = station2
        self.station3 = station3
        self.station4 = station4
        self.station5 = station5
        self.station6 = station6
        self.station7 = station7
        self.station8 = station8
        stations = np.array([station1, station2, station3, station4, station5, station6, station7, station8])
        return stations


print("changing file directory")
path = r'C:\Users\user\Desktop\sf-data\vihcle-downloads\BART\data'
dataset = pd.DataFrame(columns=['date',
                                'time',
                                'station_name',
                                'destination',
                                'abbreviation',
                                'minute',
                                'platform',
                                'direction',
                                'color',
                                'hexcolor',
                                'delay'])
x = station()
y = x.station_names('16th', '24th', 'balb', 'civc', 'embr', 'glen', 'mont', 'powl')
print("program start")
while True:
    for station in range(len(y)):
        station_name = y[station]
        url = r'http://api.bart.gov/api/etd.aspx?cmd=etd&orig={}&key=QDM5-P2T7-9URT-DWE9&json=y'.format(y[station])
        data = json.load(urlopen(url))
        date = data['root']['date']
        hour = data['root']['time']
        currenttime = datetime.datetime.now().time().strftime('%H:%M')
        SFday = datetime.datetime.strptime(date, "%m/%d/%Y")
        day = SFday.strftime('%d-%m-%Y')
        try:
            etd = data['root']['station'][00]['etd']
        except Exception:
            print(station_name + " No moovement record at " + date + "," + hour)
            dataset = dataset.append({'date': date,
                                      'time': hour,
                                      'station_name': station_name,
                                      'destination': 'NA',
                                      'abbreviation': 'NA',
                                      'minute': 'NA',
                                      'platform': 'NA',
                                      'direction': 'NA',
                                      'color': 'NA',
                                      'hexcolor': 'NA',
                                      'delay': 'NA'}, ignore_index=True)
            dataset.to_csv(path + '{}.csv'.format(day))
            pass
        else:
            print("connection to " + station_name + " success")
            for etd_id in range(len(etd)):
                estimate = data['root']['station'][0]['etd'][etd_id]['estimate']
                for i in range(len(estimate)):
                    dataset = dataset.append({'date': date,
                                              'time': hour,
                                              'station_name': station_name,
                                              'destination': etd[etd_id]['destination'],
                                              'abbreviation': etd[etd_id]['abbreviation'],
                                              'minute': estimate[i]['minutes'],
                                              'platform': estimate[i]['platform'],
                                              'direction': estimate[i]['direction'],
                                              'color': estimate[i]['color'],
                                              'hexcolor': estimate[i]['hexcolor'],
                                              'delay': estimate[i]['delay']},
                                             ignore_index=True)
                    dataset.to_csv(path + '\{}.csv'.format(day))
    if currenttime >= '13:15' and currenttime <= '13:17':
        break
    print("sleep for 25 sec' ")
    time.sleep(25)
print('finish')