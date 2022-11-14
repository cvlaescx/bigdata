## Problem3 definition

Given daily csv files with columns “user”,”application” available for several consecutive days,
provide a shell script that takes as argument a date and an application and prints the list of users
who were using the provided application every day up to the provided date and never used it
again starting from the the provided date. Assume the daily csv files are several GB each.


## Usage

1. Modify value for relative_dir in query3.sh to point to your test data

`relative_dir="logs1"`
2. Run script with 
`./search3.sh 2020-01-06  app53` for your date and app

## Open points

* Script has no validation about input data. This responsibility will be kept for user's shoulders
* There is no information about number of apps, of users and their distribution. Script's performance can be improved for different input data
* We don't know if files are sorted. query3.sh contains both usage of conn and grep, as examples
* Data used for testing was not sorted. We can reach much better performance when we remove `sort` from the script

