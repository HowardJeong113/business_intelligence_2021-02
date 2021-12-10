import csv
from collections import defaultdict
from datetime import datetime
from pprint import pprint
import math

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
        if(str(date) == "2019-12-28"):
            continue
        weekday = datetime.fromisoformat(date).weekday()

        count = int(row[5])
        calorie = float(row[8])

        if date not in date_to_count:
            date_to_count[date] = {'count': count,
                                   'calorie': calorie, 'weekday': weekday, 'date': date}
        else:
            date_to_count[date]['count'] += count
            date_to_count[date]['calorie'] += calorie


# print("row : ", header)
# print(data_list[0])
# print("data length :", len(data_list))

# print(date_to_count)

# 요일별 평균 걸음걸이 출력

weekday_count = defaultdict(list)

for k, v in date_to_count.items():
    weekday = v['weekday']
    weekday_count[weekday].append(v['count'])

for k in sorted(weekday_count):
    v = weekday_count[k]
    # print(k, sum(v) / len(v))


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

    date_to_weather = {}

    for row in data_list:
        if(len(row) < 1):
            continue
        date_to_weather[row[0]] = float(row[2])


weather_count = defaultdict(list)

for k, v in date_to_count.items():
    date_weather = math.floor(date_to_weather[str(v['date'])])
    weather_grid = date_weather - date_weather % 3

    weather_count[weather_grid].append(v['count'])

for k in sorted(weather_count.keys()):
    v = weather_count[k]

    # if(len(v) > 0):
    #     print(k, sum(v) / len(v))

weekday_weather_count = defaultdict(lambda: defaultdict(list))
weekday_weather_avg = defaultdict(lambda: defaultdict(int))

# 기온, 걸음걸이 합친 데이터
for k, v in date_to_count.items():
    weekday = v['weekday']

    date_weather = math.floor(date_to_weather[str(v['date'])])
    weather_grid = date_weather - date_weather % 3

    weekday_weather_count[weekday][weather_grid].append(v['count'])

for k in weekday_weather_count.keys():
    for j in weekday_weather_count[k].keys():
        v = weekday_weather_count[k][j]
        if(len(v) > 0):
            weekday_weather_avg[k][j] = sum(v) / len(v)


pprint(weekday_weather_avg)
print("초기 데이터 로드 완료")

import json
# (date_str, count, expected)
user_input_data = []

user_input_data_path = "user_data.json"


try:
    with open(user_input_data_path, "r") as st_json:
        user_input_data = json.load(st_json)
        print("기존 데이터를 불러왔습니다.")
except:
    pass

while True:
    with open(user_input_data_path, "w") as json_file:

        json.dump(user_input_data, json_file)

    # 예상 기대치 조절
    expected_mul_list = [1]
    for date_str, count, expected in user_input_data[:10]:
        expected_mul_list.append(count / expected)

    expected_mul = sum(expected_mul_list) / len (expected_mul_list)

    user_date = input("걸음수를 기록할 날짜를 입력해주세요. (YYYY-MM-DD 포맷으로 입력해주세요)")
    user_date_weekday = datetime.fromisoformat(user_date).weekday()
    if(user_date in date_to_weather):
        user_date_weather = date_to_weather[user_date]
    else:
        new_date = user_date
        while True:
            new_date = str(int(new_date[0:4]) - 1) + new_date[4:]

            if(new_date in date_to_weather):
                user_date_weather = date_to_weather[new_date]
                break
            else:
                continue

    user_date_weather = math.floor(user_date_weather)
    user_date_weather_grid = user_date_weather - user_date_weather % 3

    user_step_count = int(input("위 날짜에 걸었던 걸음 수를 입력해주세요."))

    expected = weekday_weather_avg[user_date_weekday][user_date_weather_grid] 

    real_expected = expected_mul * expected

    real_expected = max(real_expected - real_expected % 500, 1000) 

    user_input_data.append((user_date, user_step_count, expected))

    print("기대치는 ", int(real_expected), "입니다. (보정을 적용하지 않은 기대치는 ", int(expected), "입니다.) 달성률 : ", '{:.1%}'.format(user_step_count / real_expected))







