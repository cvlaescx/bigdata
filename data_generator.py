import csv
import os
import random

directory = os.getcwd()
relative_path = "logs3"

for i in range(1,100):
    log_date = 'XXYY-XX-{:02}'.format(i)
    file_name = os.path.join(directory, relative_path, log_date+'.log')

    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['timestamp','user','app','metric1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user_index in range(1,50000):
            print(i, 'user ', user_index)
            for app_index in range(1,100):
                for data_index in range(48):
                    time_string = "{date} {hour:02}:{minute:02}:00".format(date=log_date,
                                                                           hour = data_index//2,
                                                                           minute = 0 if data_index%2 == 0 else 30)
                    writer.writerow({'timestamp': time_string,
                                     'user': 'user{}'.format(user_index),
                                    'app':'app{}'.format(app_index),
                                    'metric1':random.randint(1,100)})
