#!/bin/bash

while true; do
    cat $1 | jq .
    sleep 1.5
done