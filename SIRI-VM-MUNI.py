import csv
import pandas as pd
import json
import datetime
import time
from urllib.request import urlopen
token = 'b0be483e-49e7-4c77-82d8-ff88b23e9a6e'
url = r'http://api.511.org/transit/VehicleMonitoring?api_key={}&agency=SF&format=JSON'.format(token)
path = r'G:\My Drive\sf-data\vihcle-downloads\MUNI\data\MUNIDATA'
data = json.load(urlopen(url))
VehicleActivity = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery']['VehicleActivity']
print('Creating Dataset')
dataset = pd.DataFrame(columns=['RecordedAtTime',
                                      'LineRef',
                                      'DatedVehicleJourneyRef',
                                      'Lon',
                                      'Lat',
                                      'StopPointRef',
                                      'AimedArrivalTime',
                                      'ExpectedArrivalTime'])
while True:
    try:
        data = json.load(urlopen(url))
    except Exception:
        pass
    else:
        VehicleActivity = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery']['VehicleActivity']
        for i in range(len(VehicleActivity)):
            try:
                dataset = dataset.append({'RecordedAtTime': VehicleActivity[i]['RecordedAtTime'],
                                          'LineRef' : VehicleActivity[i]['MonitoredVehicleJourney']['LineRef'],
                                          'DatedVehicleJourneyRef' : VehicleActivity[i]['MonitoredVehicleJourney']['FramedVehicleJourneyRef']['DatedVehicleJourneyRef'],
                                          'Lon': VehicleActivity[i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude'],
                                          'Lat': VehicleActivity[i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude'],
                                          'StopPointRef': VehicleActivity[i]['MonitoredVehicleJourney']['MonitoredCall']['StopPointRef'],
                                          'AimedArrivalTime' : VehicleActivity[i]['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime'],
                                          'ExpectedArrivalTime' : VehicleActivity[i]['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime']},
                                         ignore_index=True)
            except Exception:
                print(Exception)
        #SFday = datetime.datetime.strptime(date, "%m/%d/%Y")
        day = datetime.datetime.now().date().strftime('%d-%m-%Y')
        dataset.to_csv(path + '\{}.csv'.format(day))
        currenttime = datetime.datetime.now().time().strftime('%H:%M')
        if '13:15' <= currenttime <= '13:17':
            print('finish')
            break
        print("sleep for 60 sec' ")
        time.sleep(50)
