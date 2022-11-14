<!-- PROBLEM DEFINITION -->
## Problem definition

How do you handle big data?

* there is a folder "logs", with .log files
* files contain csv data with format timestamp,user,app,metric1
* files are stored sorted by the user column
* estimated file size for each file is ~25G
* estimated query time should be < 100ms
* the aggregation function for the metrics is always summation (adding the values together)

We need the most memory and IO efficient algorithm

<!-- PREREQUISITES -->

##Prerequisites
- python >= 3.10
- flask = 2.2.2

<!-- USAGE EXAMPLES -->
## Usage

1. Find some data or generate it with data_generator.py

2. Check for main section in website.py and select desired relative folder
  ```sh
  if __name__ == '__main__':
    input_logs = Metrics('logs2')
 ```    
3. Run with:

`python website.py`

4. Check results using:

`curl http://localhost:5000/query?from_datetime=XXYY-XX-01&to_datetime=XXYY-XX-05&user=user99&group_by=app&granularity=1day`

* with and without granularity
* with and without group_by
* datetime in short or long format: XXYY-XX-01 02:30:00

<!-- LIMITATIONS -->
## Limitations

As an open challenge, we have some known open points:
* records from files have timestamp at 30min interval
* sum of metrics should not exceed MAX_INT
* having no information about the number of files, users and apps, we'll assume that is low enough to create the index in memory
* there is no optimization for the initialization part. focus is on queries
* timing may vary if there is additional load on the machine

<!-- CONTACT -->
## Contact

Cristian Vlaescu  - cristian.vlaescu@gmail.com

