#!/bin/bash

running_processes=$(lsof -i:8090 |
                  sed -r -e "s/[^ ]+ +([^ ]+).+/\1/" |
                  tail -n +2)
for process in $running_processes
do
  kill -9 $process
  echo "kill ${process} process"
done
