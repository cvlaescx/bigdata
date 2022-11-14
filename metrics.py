from csv import reader as csv_reader
from decimal import *
import os
from collections import defaultdict


class Metrics:
    def __init__(self, directory):
        self.directory = os.path.join(os.getcwd(), directory)
        self.files_indexes = dict()
        self.discover_files_indexes()

    def discover_files_indexes(self):
        # since files are stored sorted by the user column, we'll create an index.
        # for each file, get first byte of first record per existing user in file

        for file in os.scandir(self.directory):
            user_index_dict = dict()
            file_pos = Decimal(0)
            full_file_name = os.path.join(self.directory, file.name)
            print("discovering indexes for file %s" % file.name)

            with open(full_file_name, 'rb') as f:
                line = next(f)
                file_pos += len(line)
                for line in f:
                    line_list = list(map(str.strip, line.decode('utf-8').split(',')))
                    if not line_list[1] in user_index_dict:
                        user_index_dict[line_list[1]] = file_pos
                    file_pos += len(line)

            file_date = file.name[:-4]
            self.files_indexes[file_date] = user_index_dict

    def iter_user_lines(self, file_date, user):
        # iterate through lines of selected user in specified file
        # returns an iterator through csv.reader

        first_user_byte = self.files_indexes[file_date].get(user, None)
        if first_user_byte is None:
            return []

        full_file_name = os.path.join(self.directory, file_date + '.log')
        with open(full_file_name) as f:
            f.seek(first_user_byte, 0)
            reader = csv_reader(f)
            for csv_line in reader:
                if user != csv_line[1]:
                    break
                yield csv_line

    def get_user_app_data(self, from_datetime, to_datetime, user, app):
        # search in files for data corresponding to selected user and app
        # returns list of (str datetime, str user, str app, int metric1)

        user_line_keys = ["datetime", "user", "app", "metric1"]
        from_date = from_datetime[:10]
        to_date = to_datetime[:10]

        lines_lst = []
        for file_date in self.files_indexes:
            if file_date < from_date or file_date > to_date:
                continue
            for user_line_lst in self.iter_user_lines(file_date, user):
                line_dict = dict(zip(user_line_keys, user_line_lst))
                if app is not None and line_dict['app'] != app:
                    continue
                if line_dict['datetime'] < from_datetime or line_dict['datetime'] > to_datetime:
                    continue
                lines_lst.append(
                    [line_dict['user'], line_dict['app'], line_dict['datetime'], int(line_dict['metric1'])])
        return lines_lst

    def query(self, from_datetime, to_datetime, user, app, granularity, group_by):
        # main function which returns data according to query from challenge
        # returns list of (str datetime, str user, str app, int sum_metric1)

        if len(from_datetime) == 10:
            from_datetime += ' 00:00:00'

        if len(to_datetime) == 10:
            to_datetime += ' 23:59:59'

        user_data_lst = self.get_user_app_data(from_datetime=from_datetime,
                                               to_datetime=to_datetime,
                                               user=user,
                                               app=app)

        if granularity == "1day":
            d = defaultdict(int)
            for user, app, datetime, metric1 in user_data_lst:
                d[(user, app, datetime[:10])] += int(metric1)
            user_data_lst = [[user, app, "%s 00:00:00" % date, metric1] for (user, app, date), metric1 in sorted(d.items())]

        if group_by == "app":
            pass
        else:
            d = defaultdict(int)
            for user, app, datetime, metric1 in user_data_lst:
                d[(user, datetime)] += int(metric1)
            user_data_lst = [[user, datetime, metric1] for (user, datetime), metric1 in sorted(d.items())]

        return user_data_lst


if __name__ == '__main__':
    metrics = Metrics('logs2')

    result = metrics.get_user_app_data(from_datetime='XXYY-XX-01 02:00:00',
                                        to_datetime='XXYY-XX-02 02:00:00',
                                        user='user1',
                                        app='app2')

    print(result)
