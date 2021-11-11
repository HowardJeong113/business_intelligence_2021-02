import csv

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

print("row : ", header)
print("data length :", len(data_list))