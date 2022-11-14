#!/bin/bash
date=$1
app=$2
echo "Performing query for date: $date ,and app: $app"


relative_dir="logs1"
input_files=($(ls "$relative_dir"))
median_file="user.application.$date.log"
before_files=()
after_files=()

for file in "${input_files[@]}"; do
    if [[ "$file" < "$median_file" ]]; then
        before_files+=("$file")
    else
        after_files+=("$file")
    fi
done

# find common lines with users who used that app every day before input day
app_usage="$(grep ",${app}$" "$relative_dir/${before_files[0]}")"

for file in "${before_files[@]:1}"; do
  app_usage=$(grep -f <(echo "${app_usage[@]}") "$relative_dir/${file}")
done

# filter lines to exclude users who used input app  >= input day
for file in "${after_files[@]}"; do
  app_usage=$(comm  -23 <(echo "${app_usage[@]}" | sort) <(sort "$relative_dir/${file}"))
done

# files format is userX,appY
# show only users
echo "${app_usage[@]}"| cut -d, -f1