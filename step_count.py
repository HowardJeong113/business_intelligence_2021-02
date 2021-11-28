import csv
from collections import defaultdict
from datetime import datetime

file_path = "com.samsung.shealth.step_daily_trend.202111072051.csv"
with open(file_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    header = None
    data_list = []
    for row in spamreader:
        if(header is None):
            header = "Ignore"
            continue

        if(header == "Ignore"):
            header = row
            continue

        data_list.append(row)

    # binning date 기준으로 count를 모음

    date_to_count = {}

    for row in data_list:
        date_str = row[1]

        date = date_str[0:10]
        weekday = datetime.fromisoformat(date).weekday()

        count = int(row[5])
        calorie = float(row[8])

        if date not in date_to_count:
            date_to_count[date] = {'count': count,
                                   'calorie': calorie, 'weekday': weekday, 'date': date}
        else:
            date_to_count[date]['count'] += count
            date_to_count[date]['calorie'] += calorie



print("row : ", header)
print(data_list[0])
print("data length :", len(data_list))

print(date_to_count)

# 요일별 평균 걸음걸이 출력

weekday_count = defaultdict(list)

for k, v in date_to_count.items():
    weekday = v['weekday']
    weekday_count[weekday].append(v['count'])


for k in sorted(weekday_count):
    v = weekday_count[k]
    print(k, sum(v) / len(v))


# 기온별 걸음걸이 

weather_path = "weather.csv"
with open(weather_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    header = None
    data_list = []
    for row in spamreader:
        if(header is None):
            header = "Ignore"
            continue

        if(header == "Ignore"):
            header = row
            continue

        data_list.append(row)

    # print(data_list)
    # binning date 기준으로 count를 모음

    date_to_weather = {}

    for row in data_list:
        if(len(row) < 1):
            continue
        date_to_weather[row[0]] = float(row[2])


weather_count = defaultdict(list)

for k, v in date_to_count.items():
    slider = 50
    date_weather = date_to_weather[str(v['date'])] + slider
    weather_grid = int(date_weather / 3) * 3 - slider
    weather_count[weather_grid].append(v['count'])

for k in sorted(weather_count.keys()):
    v = weather_count[k]
    if(len(v) > 0):
        print(k, sum(v) / len(v))

