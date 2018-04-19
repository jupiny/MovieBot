#!/bin/bash

log_dir="log"
access_log="$log_dir/access.log"
error_log="$log_dir/error.log"
query_log="$log_dir/query.log"

for log_file in $access_log $error_log $query_log
do
  echo "" > $log_file
done
